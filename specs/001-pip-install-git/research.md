# Research: Python Git Installation Configuration

## Decision

Use the `setuptools` build backend in `pyproject.toml` to support installation directly from Git using pip.

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

## Rationale

- **PEP 517/518 Compliance**: Standardizes how modern python packages are built.
- **Auto-Discovery**: Setuptools automatically discovers the `reaper` directory as the package since it is a standard src-less layout (package folder at root).
- **Zero Configuration overhead**: We do not need additional metadata tables since `pyproject.toml`'s `[project]` table is already fully defined (name, version, dependencies, requires-python).

## Alternatives Considered

- **Hatchling / Flit**: Modern lightweight build backends.
  - *Why rejected*: Setuptools is the most standard build backend, already installed in almost all virtual environments, reducing potential bootstrap dependency issues.
- **setup.py (Legacy)**: Adding a setup.py file.
  - *Why rejected*: Deprecated approach. Declarative `pyproject.toml` with `build-system` is the standard since PEP 518/621.
