# Hybrid Vulnerability Detection using KLEE & Clang Static Analyzer

Hybrid‑Vulnerability‑Detection is a proof‑of‑concept pipeline that **combines static analysis with dynamic symbolic execution** to triage memory‑safety bugs in C programs.  
Static warnings from the *Clang Static Analyzer* act as beacons that guide *KLEE* toward the most suspicious code paths, drastically reducing search explosion and false positives.

---

## ✨ Key Features
* **One‑shot batch script (`run‑hybrid.sh`)** – cleans artefacts, runs the static checker, compiles to LLVM bitcode, executes KLEE with a reproducible RNG seed, and produces HTML & CSV reports :contentReference[oaicite:0]{index=0}  
* **Docker‑first workflow** – the `Dockerfile` installs LLVM 13, Z3, klee‑uclibc and KLEE v3.1 on top of Ubuntu 22.04 so the tool‑chain works identically on any host :contentReference[oaicite:1]{index=1}  
* **Automatic crash confirmation** – failing `.ktest` cases are replayed against the native binary to prove the bug is real, not a false alarm :contentReference[oaicite:2]{index=2}  
* **CSV summary** – each analysed source file is summarised with static line number, KLEE error flag, native replay status and the printable overflow string (if any) :contentReference[oaicite:3]{index=3}  

---

## 🔍 How It Works

1. **Static pass** – `clang‑13 --analyze` with the *security.insecureAPI.strcpy* checker pin‑points a risky line number in every Juliet test case :contentReference[oaicite:4]{index=4}.  
2. **Bitcode generation** – sources are re‑compiled with the same compiler flags (default `-DOMITGOOD`) to `.bc` files :contentReference[oaicite:5]{index=5}.  
3. **Guided symbolic execution** – KLEE is invoked with POSIX runtime, klee‑uclibc and the captured line hint; search strategy defaults to `random‑path` :contentReference[oaicite:6]{index=6}.  
4. **Error extraction & replay** – the first `.ptr.err` is converted into a printable input, then re‑run natively and via `klee‑replay` to verify the crash :contentReference[oaicite:7]{index=7}.  
5. **Reporting** – An HTML diagnostic report per file plus a project‑wide `results/summary.csv` give at‑a‑glance status :contentReference[oaicite:8]{index=8}.  

The approach follows KLEE’s official recommendations for *docker‑based* deployments :contentReference[oaicite:9]{index=9} and mirrors their build instructions :contentReference[oaicite:10]{index=10}.

---

## 🛠️ Prerequisites

| Host requirement | Why |
|------------------|-----|
| **Docker >= 24** | Eliminates solver/compiler version drift |
| 4 CPU cores & 8 GB RAM | Building klee‑uclibc + KLEE inside the image |
| Optional: WSL 2 | Tested under Windows 10/11 as per `commands.txt` :contentReference[oaicite:11]{index=11} |

---

## 🚀 Quick‑start

```bash
# 1. Clone the repo
git clone https://github.com/viseshb/Hybrid-Vulnerability-Detection.git
cd Hybrid-Vulnerability-Detection

# 2. Build the analysis image (≈15 min the first time)
docker build -t klee-env .

# 3. Launch an ephemeral container mounted to the repo
docker run --rm -it -v "$(pwd)":/work klee-env bash

# 4. Inside the container, kick off the batch analysis
cd /work/klee-docker-demo
./run-hybrid.sh            # accepts ENV overrides, see below
