# Docker Quick Start Guide

Quick reference for running ULTIMAI with Docker.

## Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose (usually included with Docker Desktop)

## Quick Commands

### Build
```bash
docker build -t ultimai:latest .
```

### Run Tests
```bash
docker run --rm ultimai:latest
```

### Generate Everything (using Docker Compose)
```bash
# Run tests
docker compose run --rm ultimai

# Generate graph
docker compose run --rm generate-graph

# Generate report
docker compose run --rm generate-report
```

### One-Liner: Full Pipeline
```bash
docker compose run --rm ultimai && \
docker compose run --rm generate-graph && \
docker compose run --rm generate-report
```

## Interactive Development

### Open a Shell in Container
```bash
docker run --rm -it ultimai:latest /bin/bash
```

### Run with Live Code
```bash
docker run --rm -it \
  -v $(pwd)/ultimai:/app/ultimai \
  -v $(pwd)/tests:/app/tests \
  ultimai:latest \
  /bin/bash
```

## View Results

Generated files will be in:
- `build/graph/graph.json` - Reasoning graph
- `build/graph/graph.png.txt` - Graph visualization (text)
- `build/report/report.md` - Audit report

## Cleanup

### Remove Containers
```bash
docker compose down
```

### Clean Up Images
```bash
docker rmi ultimai:latest
```

### Full Cleanup (use with caution)
```bash
docker system prune -a
```

## Troubleshooting

### Permission Errors
```bash
mkdir -p build/graph build/report public/graph public/report
chmod -R 777 build public
```

### See Logs
```bash
docker logs <container_name>
```

### Check Running Containers
```bash
docker ps -a
```

## More Information

See [docs/docker.md](docs/docker.md) for comprehensive documentation.
