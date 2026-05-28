# Comprehensive Report: Game Theory and Game Mechanics

This investigation reviews the game-theoretic structures, payoff logic, and dynamic simulations in the primary care funding model codebase. 

---

## 1. Overview of Games & Mechanics
The system implements three distinct educational/demonstrative games/simulations within the Streamlit runtime dashboard:
1. **Claims Audit Game:** Models the strategic tension between honest claiming and claim inflation/gaming as audit strength is varied.
2. **Coordination Game:** Models a two-clinic assurance/Stag Hunt dilemma, showing how place accountability can shift incentives toward whole-population care over selective cherry-picking.
3. **Gaming-Risk Frontier:** Represents a policymaker's multi-objective optimization problem, mapping the Pareto trade-off between maximizing access gains and minimizing gaming risk as control strength and monitoring overhead change.

---

## 2. Core Mathematical Utilities & Strategic Response Functions
All strategic response calculations rely on mathematical primitives located in [models/primarycare_model/runtime_lab.py](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/runtime_lab.py#L29-L40):

*   **Clamping Function (`clamp`):** Bounds values to $[L, U]$ (defaults to $[0, 100]$):
    $$\text{clamp}(x, L, U) = \max(L, \min(U, x))$$
    Reference: `runtime_lab.py:L29-30`.
*   **Diminishing Returns (`diminishing_return`):** Exponential saturation curve mapping $[0, 1]$ to $[0, 1]$:
    $$g(x, \alpha) = \frac{1 - e^{-\alpha x}}{1 - e^{-\alpha}}$$
    Reference: `runtime_lab.py:L33-35`.
*   **Strategic Response Function (`strategic_response`):** A sigmoidal logistic function capturing threshold-based behavioral flips:
    $$h(x, \theta, k) = \frac{1}{1 + e^{-k(x - \theta)}}$$
    Where $\theta$ is the midpoint threshold and $k$ is the steepness parameter.
    Reference: `runtime_lab.py:L38-39`.

---

## 3. Detailed Payoff Logic & Formulation

### 3.1 Claims Audit Game
Located in [models/primarycare_model/app.py](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/app.py#L643-L740).
This game models a clinic choosing between **Honest Claiming** ($S_H$) and **Claim Inflation** ($S_G$) given audit strength $a \in [0, 1]$.
*   **Inputs:**
    *   $g \in [0, 1]$: Marginal gain from extra claims (`game_marginal_gain`)
    *   $p \in [0, 1]$: Penalty strength / penalty cost (`game_audit_cost`)
    *   $q \in [0, 1]$: Claim rule clarity (`game_claim_quality`)
    *   $y \in [0, 1]$: Place accountability (`game_place_accountability`)
*   **Signals:**
    *   $\text{honest\_bonus} = h(0.42 q + 0.34 y + 0.24 a, 0.48, 7.0)$
    *   $\text{detection\_risk} = h(0.55 a + 0.25 p + 0.20 y, 0.46, 7.0)$
    *   $\text{gaming\_attraction} = h(0.62 g + 0.22 (1 - q) + 0.16 (1 - y), 0.42, 7.0)$
*   **Payoffs:**
    *   **Honest Payoff ($U_H$):**
        $$U_H(a) = 48 + 34 \cdot \text{honest\_bonus} + 14 \cdot g(g, 2.4) - 8 a$$
    *   **Gaming Payoff ($U_G$):**
        $$U_G(a) = 48 + 42 \cdot \text{gaming\_attraction} - 36 \cdot \text{detection\_risk} - 8 a^{1.2}$$

### 3.2 Coordination Game
Located in [models/primarycare_model/app.py](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/app.py#L741-L842).
This game models the strategic interaction between clinics choosing to **Cooperate** ($S_C$) or **Cherry-pick** ($S_P$).
*   **Inputs:**
    *   $c_{gain} \in [0, 1]$: Cooperation gain
    *   $p_{gain} \in [0, 1]$: Cherry-pick gain
    *   $e \in [0, 1]$: Equity protection
    *   $f \in [0, 1]$: Scope flexibility
    *   $y \in [0, 1]$: Place accountability (variable on X-axis)
*   **Signals:**
    *   $s_C = 0.38 c_{gain} + 0.25 e + 0.20 f + 0.24 y$
    *   $s_P = 0.56 p_{gain} + 0.12 (1 - e) + 0.10 (1 - f) - 0.34 y$
*   **Payoffs:**
    *   **Cooperate Payoff ($U_C$):**
        $$U_C(y) = 46 + 48 \cdot h(s_C, 0.48, 7.0)$$
    *   **Cherry-pick Payoff ($U_P$):**
        $$U_P(y) = 46 + 48 \cdot h(s_P, 0.32, 7.0)$$

### 3.3 Gaming-Risk Frontier
Located in [models/primarycare_model/app.py](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/app.py#L843-L953).
Models system-level tradeoffs under varying control strength $c \in [0, 1]$.
*   **Inputs:**
    *   $a_{gain} \in [0, 1]$: Access gain target
    *   $m \in [0, 1]$: Monitoring cost/administrative overhead
    *   $y \in [0, 1]$: Place accountability
*   **Signals:**
    *   $s_R = 0.54 a_{gain} - 0.42 c - 0.16 y + 0.14 m$
    *   $s_A = 0.48 a_{gain} + 0.18 \cdot g(c, 2.4) + 0.16 y - 0.10 m^{1.2}$
*   **Outputs:**
    *   **Gaming Risk ($R$):**
        $$R(c) = 100 \cdot h(s_R, 0.10, 7.0)$$
    *   **Access Gain ($A$):**
        $$A(c) = 100 \cdot h(s_A, 0.35, 6.5)$$

---

## 4. Analytical Assessment

### 4.1 Underlying Assumptions
*   **Logistic Flip Midpoints:** Sigmoid curves capture abrupt threshold flips. The midpoints ($\theta = 0.48$, $0.32$, etc.) represent hard-coded behavioral tipping points.
*   **Enforcement Friction:** Non-linear terms like $-8 a^{1.2}$ (audit cost) and $-0.10 m^{1.2}$ (monitoring friction) assume administrative overhead scales super-linearly.
*   **Best Response:** In the games, agents are assumed to play the strategy with the higher static payoff at the selected setting (best response).

### 4.2 Mathematical & Code Correctness
*   **Correct Scaling:** Inputs from sliders (0–100) are correctly normalized by dividing by 100.0 before evaluating.
*   **Lack of Separation of Concerns:** Payoff arrays are calculated directly inside the Streamlit UI presentation loop in `app.py`. The calculation is not modularized inside `runtime_lab.py`, which prevents external invocation and programmatic validation.
*   **Heuristic Nature:** The "Flip Threshold" is calculated by checking where one static curve crosses the other. This is an illustrative heuristic, not a true dynamic Nash Equilibrium solver.

### 4.3 Missing Validation & Gaps
*   **No Unit Tests:** While `models/tests/test_runtime_lab.py` checks indices, there are zero tests covering the game theory formulas, payoff thresholds, or frontier behavior.
*   **No Boundary Tests:** There is no programmatic verification that payoffs remain mathematically bounded or do not divide by zero if inputs are perturbed.

---

## 5. Completeness & Path to Bleeding Edge
*   **Current State:** The games are **completed educational layers** for visual demonstration in Streamlit.
*   **What is Missing:**
    *   No dynamic multi-period interactions.
    *   No agent-based update rules (e.g. learning, selection).
    *   No game-theoretic solver module.
*   **What Would Make it Bleeding Edge:**
    1.  **Stochastic Replicator Dynamics:** Model a population of clinics sharing and updating strategies via the replicator equation:
        $$\frac{dx_i}{dt} = x_i \left( U_i(\mathbf{x}) - \bar{U}(\mathbf{x}) \right) + \sigma dW_i$$
    2.  **Phase Portrait Vector Fields:** Visualize the trajectories towards stable Nash equilibria or limit cycles interactively.
    3.  **Explicit Game Solvers:** Implement support enumeration or Lemke-Howson algorithms in a dedicated `game_theory_engine.py` module to solve for mixed and pure strategy Nash Equilibria dynamically.
