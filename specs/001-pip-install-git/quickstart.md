# Quickstart & Verification Guide: Install Reaper from Git

This guide details the validation steps to verify that the `reaper` library is successfully installable via pip directly from the git repository.

## Prerequisites

- Python >= 3.14
- Virtualenv/venv capability

## Verification Scenarios

### Scenario 1: Clean Installation & Import

Run the following commands to create a clean virtual environment, install the local repository as if it were a Git repository (using pip's local folder path or direct URL), and verify import.

1. **Create and activate a clean environment**:
   ```bash
   python -m venv test_env
   # On Windows:
   .\test_env\Scripts\activate
   # On Unix/macOS:
   source test_env/bin/activate
   ```

2. **Install the package locally**:
   Since the code is not yet pushed to GitHub, we can verify the pip build system is working by running pip install on the current directory:
   ```bash
   pip install .
   ```

3. **Verify import and version**:
   ```bash
   python -c "import reaper; print(reaper.__file__)"
   ```

4. **Clean up**:
   Deactivate and delete the environment.
   ```bash
   deactivate
   # On Windows:
   rm -r test_env
   # On Unix/macOS:
   rm -rf test_env
   ```

### Scenario 2: Dependency Verification

After running `pip install .` in Scenario 1:

1. **Verify dependencies**:
   ```bash
   pip show reaper
   ```
   Ensure the output shows `Requires: httpx, narwhals, pydantic` (or matches requirements in `pyproject.toml`).
