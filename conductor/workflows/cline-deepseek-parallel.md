# Cline DeepSeek Parallel Workflow

1. Coordinator runs the startup command set in `conductor/cline-parallel-execution.md`.
2. Coordinator opens `conductor/parallel-execution-matrix.json` and assigns Wave 1 work packages.
3. Track leads assign one work package per subagent. Do not assign overlapping allowed file globs concurrently.
4. Subagents implement only their package, run package gates, and return the handoff format from `work-packages.md`.
5. Track lead updates `implementation-log.md`.
6. Coordinator advances the next wave only after dependency gates pass.
7. Coordinator runs the closeout command set before release-wave work is called complete.
