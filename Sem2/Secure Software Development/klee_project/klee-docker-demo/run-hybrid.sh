#!/usr/bin/env bash
set -euo pipefail

echo "=== Hybrid analysis over multiple inputs ==="

echo "=== 0) CLEANUP old artifacts ==="
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
  CWE121_Stack_Based_Buffer_Overflow__CWE193_char_alloca_loop_04

# ensure output directories exist
mkdir -p results static-report bitcode-files

# loop over all Juliet testcases + sample
for SRC in juliet/testcases/*.c; do
  BASE=$(basename "$SRC" .c)
  BC="bitcode-files/${BASE}.bc"
  OUTDIR="klee-out-${BASE}"

  echo -e "\n\n===== Processing: ${BASE} ============================"

  # --- cleanup per-file ---
  echo "=== 0) CLEANUP for ${BASE} ==="
  rm -rf \
    "${OUTDIR}" \
    results/${BASE}.overflow.txt \
    static-report/${BASE}.html \
    bitcode-files/${BASE}.bc \
    "${BASE}" \
    klee-last

  # --- static analysis ---
  echo "=== 1) Static analysis: locating strcpy in ${BASE} ==="
  LINE=$(clang-13 --analyze \
           -Xclang -analyzer-checker=security.insecureAPI.strcpy \
           -Xclang -analyzer-output=text \
           "${SRC}" 2>&1 \
         | sed -n 's/.*:\([0-9]\+\):.*strcpy.*/\1/p' \
         | head -n1)
  if [[ -z "$LINE" ]]; then
    echo "⚠️  No strcpy found in ${BASE}; continuing with KLEE anyway."
  else
    echo " -> strcpy at ${SRC}:${LINE}"
  fi

  # --- compile to bitcode ---
  echo -e "\n=== 2) Compile to LLVM bitcode ==="
  clang-13 -emit-llvm -c "${SRC}" -o "${BC}"

  # --- run KLEE with randomized search ---
  echo -e "\n=== 3) Run KLEE with randomized search ==="
  RNG_SEED=$(od -An -N4 -tu4 /dev/urandom | tr -d ' ')
  klee --libc=uclibc --posix-runtime --readable-posix-inputs \
       --search=random-path \
       -rng-initial-seed="${RNG_SEED}" \
       --output-dir="${OUTDIR}" \
       "${BC}" --sym-arg 20

  echo " -> KLEE output in ${OUTDIR}"
  ln -sfn "${OUTDIR}" klee-last
  KLEE_OUT="${OUTDIR}"

  # --- find & extract overflow only if KLEE reported an error ---
  if compgen -G "${KLEE_OUT}/*.ptr.err" > /dev/null; then
    echo -e "\n=== 4) Find the overflow test ==="
    ERR_FILE=$(ls "${KLEE_OUT}"/*.ptr.err | head -n1)
    TEST_BASE=$(basename "${ERR_FILE}" .ptr.err)
    KT_FILE="${KLEE_OUT}/${TEST_BASE}.ktest"

    echo -e "\n=== 5) Extract overflow string ==="
    ktest-tool "${KT_FILE}" \
      | sed -n 's/^ *object 0: text: //p' \
      > results/${BASE}.overflow.txt
    echo " -> results/${BASE}.overflow.txt:"
    cat results/${BASE}.overflow.txt

    echo -e "\n=== 6) Replay ==="
    echo "-> Native run:"
    clang-13 -o "${BASE}" "${SRC}"
    ./"${BASE}" "$(cat results/${BASE}.overflow.txt)" || true

    echo "-> KLEE replay:"
    klee-replay "${BASE}" "${KT_FILE}" || true
  else
    echo "⚠️  No overflow detected for ${BASE}; skipping extract & replay."
    # create an empty marker if desired:
    > results/${BASE}.overflow.txt
  fi

  # --- HTML static-analysis report ---
  echo -e "\n=== 7) HTML static-analysis report ==="
  clang-13 --analyze \
    -Xclang -analyzer-checker=security.insecureAPI.strcpy \
    -Xclang -analyzer-output=html \
    "${SRC}" -o static-report/${BASE}.html
  echo " -> static-report/${BASE}.html"
done

echo -e "\n✅ All files processed. Please inspect:\n" \
        "   • results/*.overflow.txt\n" \
        "   • static-report/*.html\n" \
        "   • bitcode-files/*.bc"
