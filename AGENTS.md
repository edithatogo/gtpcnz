# Working on GTPCNZ

Read [README.md](README.md), [CONTRIBUTING.md](CONTRIBUTING.md), the owning
[Conductor plan](conductor/tracks.md) and the
[solver posture decision](docs/decisions/solver-posture-v1.8.5.md) before editing.
Preserve the public-data and claim boundaries of the educational benchmark.

## Game capability ownership

UOGTO is the authoritative game ontology; Paignia owns reusable game
representations and solvers. For every newly identified, added or materially
changed game, follow
the [contributor intake rule](CONTRIBUTING.md#game-capability-intake) and record
both semantic coverage and reusable implementation needs using:

- [UOGTO downstream game intake](https://github.com/edithatogo/UOGTO/blob/main/docs/contracts/downstream-game-intake.md).
- [Paignia downstream game intake](https://github.com/edithatogo/paignia/blob/main/docs/integrations/downstream-game-intake.md).

Record UOGTO's `reuse_existing`, `extension_required`, `unsupported` or
`mapping_review_pending` disposition separately from Paignia's `reuse_existing`,
`extension_required`, `unsupported`, `domain_only` or `assessment_pending`.
Funding scenarios, data, payoff construction and calibration remain
here; generic changes and synthetic conformance fixtures belong upstream.

The existing pedagogical best-response model may remain while migration is
assessed. Keep its heuristic status visible and do not present its stopping
criterion as proof of equilibrium. No automatic solver rewrite is authorised
by this policy. Any later migration needs accepted immutable provider revisions
and the focused conformance checks actually run.
