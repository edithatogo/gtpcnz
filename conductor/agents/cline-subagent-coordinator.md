# Cline Subagent Coordinator

Role: allocate work packages across tracks 050-062 while preventing file collisions and claim-boundary drift.

Responsibilities:

- enforce `depends_on`, `blocks`, and `can_run_parallel_with`;
- keep each subagent inside its allowed file globs;
- require handoff notes for cross-track edits;
- reject any public claim upgrade unless calibration and release gates pass;
- run `scripts/check_conductor_parallel_tracks.py` after track metadata changes.
