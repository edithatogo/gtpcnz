
## Covering note schedule policy

Each scheduled Substack post in this series must have a matching scheduled covering Note. The Note must contain the canonical Rare Insights post URL, must be no more than three sentences, and must be scheduled for the same local release time as the post. The schedule must be auditable in `catalogue/primary-care-covering-notes-schedule.json` and mirrored into `catalogue/covering-notes.json`.

## Settings, tagging and SEO policy

Each post in this series, including already published posts, must have Substack settings metadata reviewed and applied. Required settings include a concise description/dek, SEO title, SEO description, social title/social description where supported, stable slug preservation after publication, reusable primary-care series tags, and relevant post-specific tags. The settings pass must be auditable in `catalogue/primary-care-v172-settings-seo-audit.json`, with live apply runs recorded under `catalogue/run-log/`.
