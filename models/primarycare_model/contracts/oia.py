"""OIA/data-gap to model component mapping contracts.

Each entry in the OIA component map links a specific OIA request (or data-gap
topic) to the model component, chart, or calculation it would support — so
that the dashboard can display what each missing dataset would unlock.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from models.primarycare_model.contracts.parameters import StrictContract

ComponentType = Literal[
    "input",
    "parameter",
    "scenario",
    "engine",
    "result",
    "ui",
    "audit",
]


class OIAComponentEntry(StrictContract):
    """Typed mapping from one OIA request / data-gap to model components.

    This is the contract-side counterpart of a row in the
    ``oia_component_map.v1.yaml`` registry.  Every entry records:

    * the OIA request identifier (e.g. ``OIA-001``) or data-gap topic code;
    * a human-readable topic label;
    * the kind of model component this request would inform;
    * the exact file path (Python module or registry) of that component;
    * the specific chart or table name in the Streamlit dashboard;
    * a plain-English description of the impact this data would have.
    """

    oia_id: str = Field(
        min_length=1,
        description="OIA request ID (e.g. OIA-001) or data-gap topic code",
    )
    topic: str = Field(
        min_length=1,
        description="Short human-readable topic label",
    )
    component_type: ComponentType = Field(
        description=(
            "Kind of model component this mapping targets: "
            "``input`` (a slider or data input), "
            "``parameter`` (a model parameter definition), "
            "``scenario`` (a scenario definition), "
            "``engine`` (a calculation engine), "
            "``result`` (a precomputed result column), "
            "``ui`` (a dashboard chart, table or expander), "
            "``audit`` (a validation or audit overlay)."
        ),
    )
    component_path: str = Field(
        min_length=1,
        description=(
            "Python module path relative to ``models/primarycare_model/`` "
            "or a registry YAML path, e.g. ``runtime_lab.py`` or "
            "``registries/scenarios.v1.yaml``"
        ),
    )
    chart_or_table: str = Field(
        min_length=1,
        description=(
            "Name of the specific chart, table, metric tile or expander "
            "in the Streamlit dashboard that this component supports"
        ),
    )
    impact_description: str = Field(
        min_length=1,
        description=(
            "Plain-English description of what having this data would "
            "unlock or improve in the model"
        ),
    )

