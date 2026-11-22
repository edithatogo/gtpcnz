# Contributing

GTPCNZ is currently maintained as a public research and translation repository.

## Ground Rules

- Keep claims source-bounded.
- Preserve the distinction between parameterised scaffold and calibrated forecast.
- Do not add precise fiscal, workforce, or hospital-demand claims without real data and validation notes.
- Keep equity, rurality, disability, and Te Tiriti implications visible when proposing policy interpretation changes.

## Development Workflow

1. Create a branch.
2. Run `pytest -q`.
3. Run `quarto render --to html`.
4. If changing the dashboard, run `streamlit run streamlit_app.py` and check the app locally.
5. Open a pull request.

## Pull Request Checklist

- Tests pass.
- Quarto website renders.
- Public claims are caveated.
- New dependencies are added to `requirements.txt`.
- Streamlit changes include `AppTest` coverage where practical.

## Game capability intake

UOGTO owns game-theoretic semantics and Paignia owns reusable game
representations and solvers. Every newly identified, added or materially changed
game must have linked records under both upstream contracts:

- [UOGTO semantic coverage and extension intake](https://github.com/edithatogo/UOGTO/blob/main/docs/contracts/downstream-game-intake.md).
- [Paignia generic capability and fixture intake](https://github.com/edithatogo/paignia/blob/main/docs/integrations/downstream-game-intake.md).

Use the same intake key in both records and link them from the local plan or
pull request. Identify the originating source path and immutable revision,
players, actions, information, timing, payoff meaning and requested solution.
Record the semantic and implementation dispositions separately:

| Upstream | Allowed dispositions |
| --- | --- |
| UOGTO | `reuse_existing`, `extension_required`, `unsupported`, `mapping_review_pending` |
| Paignia | `reuse_existing`, `extension_required`, `unsupported`, `domain_only`, `assessment_pending` |

For `reuse_existing`, add or refine the UOGTO mapping/example with full term
IRIs and link the supported Paignia API/profile, its limits and fixture evidence.
For `extension_required`, link the upstream proposal, a minimal synthetic example
and independently expected results. `unsupported` records the missing requirement
and its effect on claims or execution. Paignia's `domain_only` records why the
change needs no generic implementation. Pending assessments need a reason,
owner and next action; they do not establish semantic or executable support.

Inspect existing upstream work before proposing another term, solver or fixture.
An unchanged game with new parameters can reuse its intake key and add an
application example. Data, assumptions, payoff construction and calibration
remain here; Paignia receives only reusable representations, algorithms and
conformance fixtures. Preserve source revision, licence and attribution for
any transferred example or implementation.

On adoption, record the exact UOGTO revision/profile and full IRIs, Paignia
revision or artifact hash, fixture identity, and focused semantic/native/consumer
checks actually run, including independent expected results and invalid or
unsupported cases. Ontology conformance and numerical verification are separate.
A record or dependency pin alone does not complete a migration.

Existing local or pedagogical implementations may remain while migration is
assessed, with their scope and limitations labelled. New game changes still
require intake. This policy does not replace algorithms, change model assumptions
or promote heuristic outputs to verified equilibria.
