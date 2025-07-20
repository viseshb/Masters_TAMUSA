# Use Ubuntu 22.04 base image
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

# Install basic build tools and libraries (as per KLEE docs):contentReference[oaicite:3]{index=3}
RUN apt-get update && apt-get install -y \
    build-essential cmake curl file git unzip bash \
    g++-multilib gcc-multilib libcap-dev libgoogle-perftools-dev \
    libncurses5-dev libsqlite3-dev libtcmalloc-minimal4 python3-pip \
    graphviz doxygen wget gnupg2

# Install lit, wllvm, tabulate via pip (LLVM testing and bitcode utilities):contentReference[oaicite:4]{index=4}
RUN pip3 install lit wllvm tabulate

# Add LLVM 13 repository and key, then install Clang/LLVM 13 and tools:contentReference[oaicite:5]{index=5}
RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add - && \
    apt-get update && apt-get install -y \
    clang-13 llvm-13 llvm-13-dev llvm-13-tools clang-tools-13

# Install Z3 SMT solver (version ≥4.8 is available on Ubuntu 22.04)
RUN apt-get install -y z3 libz3-dev

# Set Clang/LLVM 13 as default via update-alternatives
RUN update-alternatives --install /usr/bin/clang clang /usr/bin/clang-13 100 \
 && update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-13 100 \
 && update-alternatives --install /usr/bin/llvm-config llvm-config /usr/bin/llvm-config-13 100

# Clone and build klee-uclibc (POSIX C library for KLEE):contentReference[oaicite:6]{index=6}
RUN git clone https://github.com/klee/klee-uclibc.git /opt/klee-uclibc && \
    cd /opt/klee-uclibc && \
    ./configure --make-llvm-lib && make -j$(nproc)

# Clone and build KLEE v3.1 with POSIX support and Z3 solver:contentReference[oaicite:7]{index=7}:contentReference[oaicite:8]{index=8}
RUN git clone --branch v3.1 https://github.com/klee/klee.git /opt/klee && \
    cd /opt/klee && mkdir build && cd build && \
    cmake -DENABLE_SOLVER_STP=OFF -DENABLE_SOLVER_Z3=ON \
          -DENABLE_POSIX_RUNTIME=ON -DKLEE_UCLIBC_PATH=/opt/klee-uclibc \
          -DLLVM_CONFIG=llvm-config .. && \
    make -j$(nproc) && make install

# Ensure the KLEE libraries are found at runtime
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
