FROM ubuntu:24.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    clang \
    llvm \
    rustc \
    golang \
    binutils \
    linux-tools-common \
    linux-tools-generic \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
COPY . .

# Install dependencies
RUN uv sync

ENTRYPOINT ["uv", "run", "src/server.py"]
