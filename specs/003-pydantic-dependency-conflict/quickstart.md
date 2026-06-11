# Quickstart & Verification Guide: Resolve Pydantic Dependency Conflict

This guide details the validation steps to verify that `reaper` is successfully installable alongside `gradio==5.50.0`.

## Prerequisites

- Python >= 3.12
- `uv` package manager

## Verification Scenarios

### Scenario 1: Install alongside Gradio

Verify that `reaper` installs successfully in an environment that has `gradio==5.50.0` installed.

1. **Create and run a test environment**:
   ```bash
   uv run --with "gradio==5.50.0" --with . python -c "import reaper, gradio; print('Reaper and Gradio imported successfully')"
   ```
   Ensure this completes without dependency resolution errors or import errors.

### Scenario 2: Test Suite Execution with Pydantic 2.12.3

Ensure `reaper` is fully functional under `pydantic==2.12.3`:

```bash
uv run --with "pydantic==2.12.3" pytest -o pythonpath=.
```
Ensure all tests pass successfully.
