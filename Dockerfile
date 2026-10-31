FROM python:3.11-slim

WORKDIR /app

# Copy package files
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install package and dependencies
RUN pip install --no-cache-dir .

# Entrypoint runs the MCP server on stdio
ENTRYPOINT ["instagram-mcp"]
