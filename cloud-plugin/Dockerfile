FROM python:3.12-slim

# System dependencies: ffmpeg for video assembly, git for optional repo cloning
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the whole repository so the plugin can import scripts/
COPY . /app

# Install Python dependencies for the plugin
RUN pip install --no-cache-dir -r cloud-plugin/requirements.txt

# Default output directory (override with volume or env)
ENV K2E_OUTPUT_DIR=/data/generated
RUN mkdir -p /data/generated

# Expose port for HTTP/SSE transport
EXPOSE 8000

# Default: run MCP server over HTTP/SSE for cloud use
# Override command for stdio if needed
CMD ["fastmcp", "run", "cloud-plugin/server.py", "--transport", "sse", "--port", "8000"]
