# Quickstart & Verification Guide: Support Python 3.12 and Later

This guide details the validation steps to verify that the `reaper` library is successfully installable and testable on Python 3.12.

## Prerequisites

- Python 3.12 or 3.13 installed
- `uv` package manager

## Verification Scenarios

### Scenario 1: Isolated Python 3.12 Build and Import

Run the following commands using `uv` to download/run a Python 3.12 environment, install the local package, and run verification.

1. **Verify import and metadata using Python 3.12**:
   ```bash
   uv run --python 3.12 python -c "import reaper; print(reaper.__file__)"
   ```

2. **Verify metadata version requirement**:
   ```bash
   uv run --python 3.12 python -c "import importlib.metadata; dist = importlib.metadata.distribution('reaper'); print(dist.requires)"
   ```

### Scenario 2: Test Suite Execution on Python 3.12

Run the entire unit test suite within a Python 3.12 environment:

```bash
uv run --python 3.12 pytest -o pythonpath=.
```
Ensure all tests pass.
