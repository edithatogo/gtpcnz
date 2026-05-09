from pathlib import Path
import re, csv, shutil, textwrap, zipfile, os
ROOT = Path('/mnt/data/repo_v151')
BASE = ROOT/'docs/substack-ready'
SRC = BASE/'posts-v1.5.0'
PUB = BASE/'posts-v1.5.1-public'
APP = BASE/'appendices-v1.5.1'
BACKUP = BASE/'long-drafts-v1.5.1-backup'
FIGS = BASE/'figures'
for d in [PUB, APP, BACKUP]:
    if d.exists(): shutil.rmtree(d)
    d.mkdir(parents=True, exist_ok=True)

def words(text):
    return re.findall(r"\b\w+(?:[-']\w+)?\b", text)

def external_links(text):
    return re.findall(r'https?://[^)\s]+', text)

def markdown_links(text):
    return re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text)

def extract_sources(text, n=8):
    m = re.search(r'## Sources and further reading\n(.+)$', text, flags=re.S)
    if not m:
        return []
    lines=[]
    for line in m.group(1).splitlines():
        if line.strip().startswith('- ['):
            lines.append(line.strip())
    return lines[:n]

def extract_read_alongside(text):
    m = re.search(r'## Read this alongside\n(.+?)(?=\n## Sources and further reading\n|\Z)', text, flags=re.S)
    if not m:
        return ''
    # keep as one paragraph if not huge
    s = m.group(1).strip()
    return s

post_rows=[]
complete_parts=[]
appendix_parts=[]
for f in sorted(SRC.glob('post-*.md')):
    text = f.read_text()
    num = re.search(r'post-(\d+)', f.name).group(1)
    title = text.splitlines()[0].lstrip('# ').strip()
    shutil.copy2(f, BACKUP/f.name)
    split = re.split(r'\n## The plain-English version\n', text, maxsplit=1)
    main = split[0].rstrip()
    deep = ''
    if len(split)>1:
        deep = '## The plain-English version\n' + split[1].strip()
    else:
        # fallback: split near 1000 words by paragraph
        paras = text.split('\n\n')
        running=[]; wc=0; rest=[]; hit=False
        for para in paras:
            if not hit and wc + len(words(para)) < 950:
                running.append(para); wc += len(words(para))
            else:
                hit=True; rest.append(para)
        main='\n\n'.join(running).rstrip(); deep='\n\n'.join(rest).strip()
    # create appendix file
    app_name = f"appendix-{num}-{f.name[8:].replace('-v1.5.0','-v1.5.1')}"
    app_text = f"# Deep dive appendix for Post {num}: {title}\n\n"
    app_text += "This appendix preserves the longer explanatory material, model notes, game tables and source lists that sit behind the shorter public Substack post. It is intended as optional background, not the main public post.\n\n"
    app_text += deep
    (APP/app_name).write_text(app_text)
    # compact links
    source_lines=extract_sources(text, n=8)
    read_alongside=extract_read_alongside(text)
    appendix_rel=f"../appendices-v1.5.1/{app_name}"
    short_name=f.name.replace('-v1.5.0','-v1.5.1')
    public = main + "\n\n---\n\n"
    public += f"**Deep dive:** the longer notes, game table, model implications and full source list are in the [appendix for this post]({appendix_rel}).\n\n"
    if source_lines:
        public += "## Useful links\n\n"
        public += "These are the main source links for readers who want to check the background without opening the full appendix.\n\n"
        public += '\n'.join(source_lines) + "\n"
    elif read_alongside:
        public += "## Useful links\n\n" + read_alongside + "\n"
    (PUB/short_name).write_text(public)
    complete_parts.append(public)
    appendix_parts.append(app_text)
    post_rows.append({
        'post':num,
        'title':title,
        'public_file':str(PUB.relative_to(ROOT)/short_name),
        'appendix_file':str(APP.relative_to(ROOT)/app_name),
        'public_words':len(words(public)),
        'long_draft_words':len(words(text)),
        'appendix_words':len(words(app_text)),
        'external_links_public':len(external_links(public)),
        'external_links_appendix':len(external_links(app_text)),
        'figure_links_public':len([l for _,l in markdown_links(public) if l.lower().endswith(('.png','.jpg','.jpeg','.webp','.svg'))]),
        'target_status':'pass' if 750 <= len(words(public)) <= 1150 else 'check',
    })

complete = "# Complete short-form Substack series v1.5.1\n\n" + "\n\n---\n\n".join(complete_parts)
(BASE/'complete-substack-series-v1.5.1.md').write_text(complete)
appendix_comp = "# Complete deep-dive appendix compendium v1.5.1\n\n" + "\n\n---\n\n".join(appendix_parts)
(BASE/'complete-substack-appendices-v1.5.1.md').write_text(appendix_comp)

# QA checklist
qa_path = BASE/'substack-post-qa-checklist-v1.5.1.csv'
with qa_path.open('w', newline='') as fh:
    fieldnames=list(post_rows[0].keys())
    w=csv.DictWriter(fh, fieldnames=fieldnames)
    w.writeheader(); w.writerows(post_rows)

# publication guidance
cal = (BASE/'publication-calendar-twice-weekly-v1.5.0.md').read_text() if (BASE/'publication-calendar-twice-weekly-v1.5.0.md').exists() else ''
strategy = f"""# Short-form Substack publication strategy v1.5.1

## Recommendation

Use the **short public posts** in `posts-v1.5.1-public/` as the main Substack copy. Keep the long v1.5.0 drafts as backup material and use the `appendices-v1.5.1/` files as optional deep dives.

The short posts are designed for readers who want the core argument in one sitting. The appendices preserve the fuller game tables, model notes, source lists and explanatory material for readers who want to go further.

## Why this structure is better

The v1.5.0 posts were comprehensive, but at roughly 1,850-2,050 words they risked feeling like mini-papers. The v1.5.1 public posts are mostly 850-1,050 words, which is better for a twice-weekly series. They still include figures, key source links and a clear deep-dive path.

## Suggested cadence

Keep the twice-weekly cadence: Tuesday for the core concept, Friday for the application or game/policy implication. The existing v1.5.0 calendar remains suitable.

{cal}

## Posting workflow

1. Publish the short public post.
2. Include one figure near the top or middle of the post.
3. Keep the "Useful links" section in the public post.
4. Place the appendix either as a linked Google Doc, a separate Substack note, or a downloadable Markdown/PDF if you want the longer evidence available.
5. Use the long v1.5.0 draft as your personal backup if comments or stakeholder questions need fuller detail.

## Editorial rule

The post should make one main point. The appendix can carry the complexity.
"""
(BASE/'short-form-publication-strategy-v1.5.1.md').write_text(strategy)

# local link audit for public and appendices
link_rows=[]
for f in list(PUB.glob('*.md'))+list(APP.glob('*.md'))+[BASE/'complete-substack-series-v1.5.1.md', BASE/'complete-substack-appendices-v1.5.1.md']:
    txt=f.read_text()
    for label,link in markdown_links(txt):
        if link.startswith('http') or link.startswith('mailto:') or link.startswith('#'):
            status='external_or_anchor'
            target=''
        else:
            target=(f.parent/link).resolve()
            status='exists' if target.exists() else 'missing'
        link_rows.append({'file':str(f.relative_to(ROOT)), 'label':label, 'link':link, 'status':status, 'target':str(target) if target else ''})
link_audit=BASE/'local-link-audit-v1.5.1.csv'
with link_audit.open('w', newline='') as fh:
    w=csv.DictWriter(fh, fieldnames=['file','label','link','status','target'])
    w.writeheader(); w.writerows(link_rows)

# source note
readme = f"""# Substack publication pack v1.5.1

This pack contains:

- `posts-v1.5.1-public/`: shorter 800-1,100 word public posts.
- `appendices-v1.5.1/`: optional deep-dive appendices.
- `long-drafts-v1.5.1-backup/`: the original long v1.5.0 drafts retained as backup.
- `complete-substack-series-v1.5.1.md`: all short posts in one file.
- `complete-substack-appendices-v1.5.1.md`: all appendices in one file.
- `short-form-publication-strategy-v1.5.1.md`: posting strategy and cadence.
- `substack-post-qa-checklist-v1.5.1.csv`: word-count and link-count QA.

The intended publication model is: **short post first, appendix available for readers who want the evidence and modelling detail.**
"""
(BASE/'README-v1.5.1.md').write_text(readme)

# update root readme and changelog lightly
root_readme=ROOT/'README.md'
r= root_readme.read_text(errors='ignore') if root_readme.exists() else ''
insert="""

## v1.5.1 short-form Substack update

The Substack series now has a short-form public version plus optional appendices. Public posts are generally 850-1,050 words, retain figures and key source links, and preserve the longer v1.5.0 material as deep-dive appendices and backup drafts.

Key files:

- `docs/substack-ready/posts-v1.5.1-public/`
- `docs/substack-ready/appendices-v1.5.1/`
- `docs/substack-ready/complete-substack-series-v1.5.1.md`
- `docs/substack-ready/complete-substack-appendices-v1.5.1.md`
- `docs/substack-ready/short-form-publication-strategy-v1.5.1.md`

"""
if '## v1.5.1 short-form Substack update' not in r:
    root_readme.write_text(r+insert)
changelog=ROOT/'CHANGELOG.md'
c=changelog.read_text(errors='ignore') if changelog.exists() else ''
entry="""

## v1.5.1 - Short-form Substack public series

- Split the v1.5.0 long Substack drafts into shorter public posts and optional deep-dive appendices.
- Preserved all long drafts as backup material.
- Added a short-form publication strategy for twice-weekly rollout.
- Added QA checklist and local link audit for the short posts and appendices.
"""
if '## v1.5.1 - Short-form Substack public series' not in c:
    changelog.write_text(c+entry)

# Copy key files to outputs
OUT=ROOT/'outputs'
OUT.mkdir(exist_ok=True)
for file in [BASE/'complete-substack-series-v1.5.1.md', BASE/'complete-substack-appendices-v1.5.1.md', BASE/'short-form-publication-strategy-v1.5.1.md', BASE/'substack-post-qa-checklist-v1.5.1.csv', BASE/'local-link-audit-v1.5.1.csv']:
    shutil.copy2(file, OUT/file.name)

# Create substack pack zip
pack_path=Path('/mnt/data/substack-publication-pack-v1.5.1.zip')
if pack_path.exists(): pack_path.unlink()
with zipfile.ZipFile(pack_path,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for rel in ['README-v1.5.1.md','complete-substack-series-v1.5.1.md','complete-substack-appendices-v1.5.1.md','short-form-publication-strategy-v1.5.1.md','substack-post-qa-checklist-v1.5.1.csv','local-link-audit-v1.5.1.csv','source-bank-v1.5.0.md','publication-calendar-twice-weekly-v1.5.0.md']:
        p=BASE/rel
        if p.exists(): z.write(p, arcname=p.relative_to(BASE))
    for folder in [PUB,APP,BACKUP,FIGS]:
        for p in folder.rglob('*'):
            if p.is_file(): z.write(p, arcname=p.relative_to(BASE))
print('created', pack_path)
print('posts', len(post_rows))
print('word counts', [r['public_words'] for r in post_rows])
print('missing links', sum(1 for r in link_rows if r['status']=='missing'))
