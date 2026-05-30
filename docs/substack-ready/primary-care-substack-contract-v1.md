# Primary care Substack contract v1

This contract applies to the active v1.7.2 primary-care funding series drafts on Rare Insights.

## Scope

- Landing page and Post 01 may already have bespoke live edits and should not be bulk-rewritten without a post-specific pass.
- Posts 02-06 are launch essays with matching deep-dive appendices. Their appendices should be included in the same Substack draft, not linked as local Markdown files.
- Posts 07-18 are appendix-style posts. They should stand alone and should not append another copy of themselves.

## Content Contract

- Every scheduled post must have a subtitle, cover image, and scheduled release.
- Scheduled release time should be 7:00am Australia/Sydney unless the user explicitly asks for another time.
- Every scheduled post must also have a scheduled covering Note at the same local release time as the post.
- The covering Note must contain the canonical Rare Insights post URL and must be no more than three sentences.
- No local Markdown links may remain in live drafts, such as `../appendices/...` or `posts-v1.7.2-launch/...`.
- Hyperlink anchors must be six words or fewer.
- Factual links should point to current, relevant, high-quality sources: official agencies, primary policy documents, reputable evidence reviews, or clearly identified contextual reporting.
- Use italics for emphasis. Do not use bold purely for emphasis.
- First substantive use of recurring technical terms should be italicised where it helps orient the reader.
- Do not leave editorial/process markers such as `TODO`, `FIXME`, `red-team`, `Source-confidence`, or `RACMA`.

## Appendix Contract

- Launch essays with appendices must include their appendix at the bottom of the draft.
- The deep-dive line should refer to the appendix below, not to a local file path.
- Appended appendices should not duplicate the main post's introductory explanation, diagram explanation, or plain-English recap unless the content adds new detail.
- Appendix game tables should be editor-safe. Substack currently rejects `tableHeader`, `tableCell`, and `tableRow` nodes in this editor surface, so use a compact structured list unless a compatible Substack table representation is confirmed.

## Visual Contract

- Each post should have a thumbnail-safe Mermaid-rendered cover image.
- Where a concept is easier to understand visually, include one clear diagram or visual guide in the body.
- Images need meaningful alt text and captions.
- Do not add decorative visuals that merely repeat the prose.

## Verification Contract

- Saved draft JSON must not contain unsupported table nodes.
- Saved draft JSON must not contain non-HTTP links, except where a Substack-supported internal link has been manually verified.
- Saved draft JSON must not contain relative Markdown links.
- The editor must load body text after the save.
- Any live mutation should be auditable under `catalogue/` or `catalogue/run-log/`.
- Covering-note scheduling must be auditable in `catalogue/primary-care-covering-notes-schedule.json` and reflected in `catalogue/covering-notes.json`.

## Settings, tagging and SEO Contract

- Every post in the series, including already published posts, must have Substack settings metadata reviewed, not only body content.
- Each post must have a concise Substack description/dek aligned with its subtitle or core reader promise.
- Each post must have an SEO title and SEO description where Substack exposes those fields.
- Social title and social description should be populated where Substack exposes those fields, using the post title and a short plain-English description.
- Slugs should remain stable after publication unless the user explicitly approves a URL change.
- Tags must include the reusable primary-care series tags plus relevant post-specific topic tags.
- Tags should be topical, durable and reusable. Avoid one-off tags that only mirror a full post title.
- The settings/tagging/SEO pass must be auditable in `catalogue/primary-care-v172-settings-seo-audit.json` and any live apply run must also write a timestamped `catalogue/run-log/` entry.

## Contract v2 additions

- Literal separator paragraphs such as `---` must be stored as Substack horizontal-rule nodes, not visible text.
- Quote formatting must use real blockquote nodes where the post is using a quote block; raw `>` markers must not appear as visible body text.
- Each scheduled draft should include a short plain-English bridge near the top so a non-specialist reader can understand the practical stakes before the technical detail.
- Body images must have meaningful alt text and native Substack captions. In the Substack draft JSON, this means using the caption-capable image node with inline caption content, not a normal paragraph before or after the image.
- Each post must be checked for whether a microeconomic, game-theory, plot, or diagrammatic explanation would help. If a visual is used, prefer a clean Mermaid-rendered diagram or plot-style visual over a dense decorative image.
- Link rendering must be checked in the Substack document JSON: links should be HTTP(S), inline, relevant, high-quality, and no more than six linked words at a time.
- Humanising checks should remove chatbot residue, mechanical bold emphasis, formulaic AI phrasing, and over-structured tables/lists where prose or compact lists read better.
