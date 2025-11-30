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

# Create a non-root user (required by HF Spaces for some setups)
RUN useradd -m -u 1000 user

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set up working directory
WORKDIR /app

# Copy files and set ownership
COPY --chown=user . .

# Switch to non-root user
USER user

# Install dependencies
RUN uv sync

# Expose port for Hugging Face Spaces
EXPOSE 7860

ENTRYPOINT ["uv", "run", "src/server.py"]
