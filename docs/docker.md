# Docker Guide for ULTIMAI

This guide provides detailed information on using Docker with the ULTIMAI reasoning infrastructure.

## Overview

Docker support has been added to ULTIMAI to provide:
- **Isolated environment**: Run ULTIMAI in a clean, reproducible environment
- **Easy deployment**: Deploy ULTIMAI without worrying about system dependencies
- **Portability**: Run ULTIMAI on any platform that supports Docker
- **Consistency**: Ensure all team members use the same environment

## Files

- **Dockerfile**: Defines the Docker image for ULTIMAI
- **docker-compose.yml**: Orchestrates multiple Docker services for different tasks
- **.dockerignore**: Specifies files to exclude from the Docker build context

## Docker Image

The ULTIMAI Docker image is based on `python:3.11-slim` and includes:
- Python 3.11 runtime
- ULTIMAI package and all its modules
- Test suite
- Scripts for graph generation and reporting
- Pre-created directories for build artifacts

## Basic Usage

### Building the Image

```bash
docker build -t ultimai:latest .
```

### Running Tests

```bash
docker run --rm ultimai:latest
```

### Generating Graph

To generate a graph from seed data, mount the data and build directories:

```bash
docker run --rm \
  -v $(pwd)/build:/app/build \
  -v $(pwd)/data:/app/data \
  ultimai:latest \
  python scripts/generate_graph.py --input data/seeds.json --output build/graph/graph.json
```

### Generating Report

To generate an audit report:

```bash
docker run --rm \
  -v $(pwd)/build:/app/build \
  ultimai:latest \
  python scripts/dump_report.py --graph build/graph/graph.json --output build/report/report.md
```

## Docker Compose

Docker Compose simplifies multi-container workflows. The `docker-compose.yml` file defines three services:

1. **ultimai**: Runs the test suite
2. **generate-graph**: Generates a reasoning graph from seed data
3. **generate-report**: Generates an audit report from the graph

### Using Docker Compose

**Run tests:**
```bash
docker compose run --rm ultimai
```

**Generate graph:**
```bash
docker compose run --rm generate-graph
```

**Generate report (depends on graph generation):**
```bash
docker compose run --rm generate-report
```

**Build all services:**
```bash
docker compose build
```

## Volume Mounts

The Docker setup uses volume mounts to:
- Persist build artifacts outside the container
- Allow easy access to generated graphs and reports
- Enable updates to seed data without rebuilding the image

Key directories that are mounted:
- `./build:/app/build` - Build artifacts (graphs, reports)
- `./data:/app/data` - Input data (seeds.json, config.yaml)
- `./public:/app/public` - Public artifacts for GitHub Pages

## Environment Variables

The Docker containers use the following environment variables:
- `PYTHONPATH=/app` - Ensures the ULTIMAI package is discoverable
- `PYTHONUNBUFFERED=1` - Ensures Python output is not buffered
- `PYTHONDONTWRITEBYTECODE=1` - Prevents creation of .pyc files

## Advanced Usage

### Interactive Shell

To run an interactive shell in the container:

```bash
docker run --rm -it ultimai:latest /bin/bash
```

### Custom Commands

Run any Python script or command:

```bash
docker run --rm \
  -v $(pwd)/build:/app/build \
  ultimai:latest \
  python -c "from ultimai import ReasoningGraph; print('Hello from ULTIMAI')"
```

### Development Mode

For active development, mount the source code:

```bash
docker run --rm -it \
  -v $(pwd)/ultimai:/app/ultimai \
  -v $(pwd)/tests:/app/tests \
  ultimai:latest \
  /bin/bash
```

## Troubleshooting

### Permission Issues

If you encounter permission issues with mounted volumes, ensure the build directories exist:

```bash
mkdir -p build/graph build/report public/graph public/report
```

### Build Context Too Large

The `.dockerignore` file excludes unnecessary files from the build context. If you still have issues, check for large files in the repository.

### Container Fails to Start

Check container logs:
```bash
docker logs <container_id>
```

Run in interactive mode to debug:
```bash
docker run --rm -it ultimai:latest /bin/bash
```

## Best Practices

1. **Use specific tags**: Instead of `latest`, use version tags for production deployments
2. **Clean up regularly**: Remove unused images and containers with `docker system prune`
3. **Layer caching**: Order Dockerfile commands from least to most frequently changing
4. **Security**: Regularly update the base image for security patches
5. **Multi-stage builds**: Consider multi-stage builds for smaller production images

## CI/CD Integration

Docker can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Docker image
        run: docker build -t ultimai:test .
      - name: Run tests
        run: docker run --rm ultimai:test
```

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
