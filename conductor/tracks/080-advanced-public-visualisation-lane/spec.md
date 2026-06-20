# Track 080 - Advanced public visualisation lane

Add high-value public visualisations that explain model structure, uncertainty, evidence priorities, and policy dynamics without overstating validation.

## Scope

Add or upgrade the following Dash/GitHub Pages visual surfaces:

- scenario morph animation from F0 current reform to selected hybrid scenarios;
- equity by complexity heatmap and small multiples;
- VOI evidence-priority chart;
- structural ensemble uncertainty chart;
- policy shock sequence view;
- causal architecture graph linking levers, mechanisms, outputs, caveats, and evidence gaps;
- 19-games/Nash game navigator;
- Bass diffusion adoption and budget surface;
- 3D payoff surface where it is performant and public-safe;
- animated regime sweep where it adds insight and does not harm Hugging Face CPU performance.

## Non-Goals

- Do not add decorative visuals without analytic value.
- Do not add 3D or animation if browser tests show slow, blank, or unreadable rendering.
- Do not make any visual imply a calibrated patient-level or causal forecast.
- Do not require paid hosting, paid hardware, persistent storage, Redis, or GPU.

## Required Checks

```powershell
python -m pytest -q models/tests/test_dashboard_service.py models/tests/test_dash_app.py models/tests/test_public_site_visual_contract.py
python scripts/run_accessibility_audit.py --check-only
python scripts/check_public_only_boundary.py
python scripts/check_concern_boundaries.py
```

Browser smoke checks should cover desktop and mobile widths for any animation, 3D, or dense heatmap.
