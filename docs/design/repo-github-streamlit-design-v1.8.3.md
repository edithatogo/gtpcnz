# Repo, GitHub Pages and Streamlit Design v1.8.3

This design records the current strict-validation architecture without changing the empirical claim boundary.

## Public Surface

```mermaid
flowchart LR
    Repo["Root repo"]
    Pages["GitHub Pages"]
    Streamlit["Streamlit app"]
    Public["Public reader"]
    Repo --> Pages
    Repo --> Streamlit
    Pages --> Public
    Streamlit --> Public
```

## Concern Boundaries

```mermaid
flowchart LR
    Registries["YAML registries"]
    Contracts["Pydantic contracts"]
    Validation["Validation helpers"]
    Runtime["Runtime calculations"]
    UI["Streamlit UI"]
    Registries --> Contracts --> Validation --> Runtime --> UI
```

## Runtime Calculation Path

```mermaid
flowchart TD
    Scenario["RuntimeScenario registry row"]
    Adapter["RuntimeScenario dataclass adapter"]
    Formula["calculate_indices"]
    Results["DataFrame result"]
    Check["validation checks"]
    Scenario --> Adapter --> Formula --> Results --> Check
```

## Test And Release Gates

```mermaid
flowchart TD
    Tests["pytest model tests"]
    Boundary["check_concern_boundaries.py"]
    Health["check_repo_health.py"]
    Deploy["Pages/Streamlit deployment"]
    Tests --> Boundary --> Health --> Deploy
```
