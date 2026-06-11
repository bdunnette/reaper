# Research: Python 3.12 vs 3.14 Compatibility

## Decision

Change python version requirement to `requires-python = ">=3.12"` in `pyproject.toml`.

## Rationale

- **Google Colab / Enterprise environments**: Mainstream cloud notebook services like Google Colab run Python 3.12 or 3.13 by default. Lowering the minimum version requirement ensures the library is accessible without requiring manual runtime updates.
- **Codebase Compatibility**: The Reaper client uses `httpx`, `pydantic` (v2), and `narwhals`. These dependencies support Python >= 3.12. The codebase itself does not employ any Python 3.13 or 3.14 specific syntax features (such as `typing.TypeVar` syntax updates that aren't backward-compatible, new async loop features, or exclusive standard library changes).

## Alternatives Considered

- **Keep Python >= 3.14 requirement**:
  - *Why rejected*: Severely limits adoption. Google Colab and standard platforms do not run Python 3.14 as their default target runtime yet.
- **Support Python 3.10 / 3.11**:
  - *Why rejected*: Out of scope for this request, and keeping minimum at 3.12 allows us to use modern syntax (e.g. PEP 695 generic classes/functions) while maintaining broad hosted runtime support.
