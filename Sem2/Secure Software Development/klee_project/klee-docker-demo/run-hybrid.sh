
#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# run-hybrid.sh
#
# Batch hybrid analysis (Static + KLEE) over Juliet C testcases.
#
# Features:
#   • Cleans old artifacts
#   • Static analysis (strcpy checker) → line capture
#   • Compile to LLVM bitcode w/ flags (default: -DOMITGOOD)
#   • KLEE run (printable inputs, random-path search, symbolic argv)
#   • Extract first error test (.ptr.err → .ktest)
#   • Derive printable overflow string
#   • Native replay (detect crash)
#   • KLEE replay
#   • Per-test HTML static-analysis report
#   • CSV summary of results
#
# Customize:
#   Set COMPILE_FLAGS env var before running to override (-DOMITGOOD by default).
#   Example: COMPILE_FLAGS="-DOMITBAD" ./run-hybrid.sh
###############################################################################

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
COMPILE_FLAGS="${COMPILE_FLAGS:--DOMITGOOD}"     # default to bad flows only
SYM_ARG_LEN="${SYM_ARG_LEN:-20}"                 # symbolic arg length
SEARCH_STRAT="${SEARCH_STRAT:-random-path}"      # KLEE searcher
TEST_GLOB="${TEST_GLOB:-juliet/testcases/*.c}"   # which sources to process

echo "=== Hybrid analysis over multiple inputs ==="
echo "Config:"
echo "  COMPILE_FLAGS = ${COMPILE_FLAGS}"
echo "  SYM_ARG_LEN   = ${SYM_ARG_LEN}"
echo "  SEARCH_STRAT  = ${SEARCH_STRAT}"
echo "  TEST_GLOB     = ${TEST_GLOB}"

# ---------------------------------------------------------------------------
# Global cleanup
# ---------------------------------------------------------------------------
echo -e "\n=== 0) CLEANUP old artifacts ==="
rm -rf \
  klee-out-* \
  results \
  static-report \
  bitcode-files \
  *.o \
  sample \
  klee-last \
  CWE121_Stack_Based_Buffer_Overflow__CWE193_char_alloca_loop_01 \
  CWE121_Stack_Based_Buffer_Overflow__CWE193_char_alloca_loop_02 \
  CWE121_Stack_Based_Buffer_Overflow__CWE193_char_alloca_loop_03 \
  CWE121_Stack_Based_Buffer_Overflow__CWE193_char_alloca_loop_04 || true

# ensure output directories exist
mkdir -p results static-report bitcode-files

# init summary CSV
SUMMARY="results/summary.csv"
echo "Testcase,StaticLine,KLEEError?,ErrorTest,NativeStatus,KLEEOutDir,RNGSeed,OverflowString" > "$SUMMARY"

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
for SRC in $TEST_GLOB; do
  [[ -f "$SRC" ]] || continue  # skip globs that don't match

  BASE=$(basename "$SRC" .c)
  BC="bitcode-files/${BASE}.bc"
  OUTDIR="klee-out-${BASE}"

  echo -e "\n\n===== Processing: ${BASE} ============================"

  # --- cleanup per-file ---
  echo "=== 0) CLEANUP for ${BASE} ==="
  rm -rf \
    "${OUTDIR}" \
    "results/${BASE}.overflow.txt" \
    "static-report/${BASE}.html" \
    "${BC}" \
    "${BASE}" \
    klee-last || true

  # --- static analysis ---
  echo "=== 1) Static analysis: locating strcpy in ${BASE} ==="
  LINE=$(clang-13 --analyze \
           -Xclang -analyzer-checker=security.insecureAPI.strcpy \
           -Xclang -analyzer-output=text \
           ${COMPILE_FLAGS} \
           "${SRC}" 2>&1 \
         | sed -n 's/.*:\([0-9]\+\):[0-9]\+:.*strcpy.*/\1/p' \
         | head -n1 || true)
  if [[ -z "$LINE" ]]; then
    echo "⚠️  No strcpy found in ${BASE}; continuing with KLEE anyway."
  else
    echo " -> strcpy at ${SRC}:${LINE}"
  fi

  # --- compile to bitcode ---
  echo -e "\n=== 2) Compile to LLVM bitcode ==="
  clang-13 ${COMPILE_FLAGS} -emit-llvm -c "${SRC}" -o "${BC}"

  # --- run KLEE ---
  echo -e "\n=== 3) Run KLEE with ${SEARCH_STRAT} search ==="
  RNG_SEED=$(od -An -N4 -tu4 /dev/urandom | tr -d ' ')
  klee \
    --libc=uclibc \
    --posix-runtime \
    --readable-posix-inputs \
    --search="${SEARCH_STRAT}" \
    -rng-initial-seed="${RNG_SEED}" \
    --output-dir="${OUTDIR}" \
    "${BC}" --sym-arg "${SYM_ARG_LEN}"

  echo " -> KLEE output in ${OUTDIR}"
  ln -sfn "${OUTDIR}" klee-last
  KLEE_OUT="${OUTDIR}"

  KLEE_ERR="no"
  TEST_BASE=""
  OVERFLOW=""
  NATIVE_STATUS="NA"

  # --- find & extract overflow only if KLEE reported an error ---
  if compgen -G "${KLEE_OUT}/*.ptr.err" > /dev/null; then
    KLEE_ERR="yes"
    echo -e "\n=== 4) Find the overflow test ==="
    ERR_FILE=$(ls "${KLEE_OUT}"/*.ptr.err | head -n1)
    TEST_BASE=$(basename "${ERR_FILE}" .ptr.err)
    KT_FILE="${KLEE_OUT}/${TEST_BASE}.ktest"

    echo -e "\n=== 5) Extract overflow string ==="
    ktest-tool "${KT_FILE}" \
      | sed -n 's/^ *object 0: text: //p' \
      > "results/${BASE}.overflow.txt"
    echo " -> results/${BASE}.overflow.txt:"
    cat "results/${BASE}.overflow.txt" || true
    OVERFLOW=$(tr -d '\n' < "results/${BASE}.overflow.txt")

    # --- native replay ---
    echo -e "\n=== 6) Replay ==="
    echo "-> Native run:"
    if clang-13 ${COMPILE_FLAGS} -o "${BASE}" "${SRC}"; then
      set +e
      ./"${BASE}" "${OVERFLOW}" >/dev/null 2>&1
      RC=$?
      set -e
      if [[ $RC -ne 0 ]]; then
        NATIVE_STATUS="CRASH"
      else
        NATIVE_STATUS="OK"
      fi
    else
      echo " (build failed; skipping native replay)"
      NATIVE_STATUS="BUILD_FAIL"
    fi

    echo "-> KLEE replay:"
    klee-replay "${BASE}" "${KT_FILE}" >/dev/null 2>&1 || true
  else
    echo "⚠️  No overflow detected for ${BASE}; skipping extract & replay."
    > "results/${BASE}.overflow.txt"
    NATIVE_STATUS="NO_ERR"
  fi

  # --- HTML static-analysis report ---
  echo -e "\n=== 7) HTML static-analysis report ==="
  clang-13 --analyze \
    -Xclang -analyzer-checker=security.insecureAPI.strcpy \
    -Xclang -analyzer-output=html \
    ${COMPILE_FLAGS} \
    "${SRC}" -o "static-report/${BASE}.html" || true
  echo " -> static-report/${BASE}.html"

  # --- record summary ---
 # --- 8) Append to summary CSV (clean, quoted) ---
   QUOTED_OVERFLOW=$(printf '%s' "$OVERFLOW" | sed 's/"/""/g')
   printf '%s,%s,%s,%s,%s,%s,%s,"%s"\n' \
  "$BASE" \
  "$LINE" \
  "$KLEE_ERR" \
  "$TEST_BASE" \
  "$NATIVE_STATUS" \
  "$OUTDIR" \
  "$RNG_SEED" \
  "$QUOTED_OVERFLOW" >> "$SUMMARY"


done

echo -e "\n✅ All files processed."
echo "Summary CSV: $SUMMARY"
echo "Artifacts:"
echo "   • results/*.overflow.txt"
echo "   • static-report/*.html"
echo "   • bitcode-files/*.bc"
echo "   • klee-out-* (raw runs)"
