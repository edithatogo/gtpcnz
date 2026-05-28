# Public Mirror Maintenance

The `public/gtpcnz/` directory mirrors deployment-critical root files so reviewers
and deployment platforms can find the right entrypoints.

## Regenerate

```powershell
python scripts/sync_public_mirror.py
```

## Check for Drift

```powershell
python scripts/sync_public_mirror.py --check
```

## When to Sync

- Before every public release
- After changing `streamlit_app.py` or `app.py`
- After adding/modifying contracts or validation modules

The sync script only copies source files; generated artifacts and cache directories
are intentionally excluded from the mirror.
