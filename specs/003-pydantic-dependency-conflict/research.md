# Research: Pydantic Version Compatibility and Gradio Conflict

## Decision

Relax the `pydantic` requirement in `pyproject.toml` from `pydantic>=2.13.4` to `pydantic>=2.0`.

## Rationale

- **Gradio Compatibility**: Gradio 5.50.0 requires `pydantic<=2.12.3,>=2.0`. Setting `pydantic>=2.0` in `pyproject.toml` permits pip to select a mutually compatible version (like `2.12.3`) when installing both packages together in environments like Google Colab.
- **Minimal Codebase Impact**: Reaper utilizes core Pydantic v2 features (`BaseModel`, `Field`, `model_validator`). These interfaces are present and stable since Pydantic 2.0.0. Testing the codebase on older Pydantic versions (like `2.12.3` or `2.0.0` series) ensures no runtime incompatibilities.

## Alternatives Considered

- **Pin `pydantic>=2.0,<=2.12.3`**:
  - *Why rejected*: Overly restrictive. Users who do not run Gradio should be allowed to use newer versions of Pydantic (e.g. 2.13+). Declaring `pydantic>=2.0` allows maximum flexibility for both sets of users.
