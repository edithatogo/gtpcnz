from pathlib import Path
import csv
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path('/mnt/data/work/project/primary-care-funding-architecture')
VER='v1.1.0'
FIG=ROOT/'docs/figures'; OUT=ROOT/'outputs'
FIG.mkdir(parents=True, exist_ok=True); OUT.mkdir(parents=True, exist_ok=True)

# Load priority checks
with (ROOT/f'docs/validation/priority-empirical-checks-{VER}.csv').open(encoding='utf-8') as f:
    checks=list(csv.DictReader(f))
labels=[r['parameter'] for r in checks]
short_labels=['Marginal supply','Unmet need -> hospital','ACC stabilisation','PHO intermediation','Scope-enabled supply']
criticality=[int(r['policy_criticality_1_5']) for r in checks]
feasibility=[int(r['initial_feasibility_1_5']) for r in checks]
gap=[int(r['evidence_gap_1_5']) for r in checks]

# Figure 1: priority empirical checks matrix
fig, ax = plt.subplots(figsize=(10,6))
x=np.arange(len(short_labels))
width=0.25
ax.bar(x-width, criticality, width, label='Policy criticality')
ax.bar(x, feasibility, width, label='Initial feasibility')
ax.bar(x+width, gap, width, label='Evidence gap')
ax.set_xticks(x)
ax.set_xticklabels(short_labels, rotation=25, ha='right')
ax.set_ylim(0,5.5)
ax.set_ylabel('Score (1-5)')
ax.set_title('Priority empirical checks before any full predictive calibration')
ax.legend(loc='upper right')
ax.grid(axis='y', linestyle=':', alpha=0.4)
fig.tight_layout()
for path in [FIG/f'priority-empirical-checks-{VER}.png', OUT/f'priority-empirical-checks-{VER}.png']:
    fig.savefig(path, dpi=200, bbox_inches='tight')
plt.close(fig)

# Figure 2: validation roadmap
fig, ax = plt.subplots(figsize=(11,3.8))
steps=['Policy synthesis','Stakeholder MCDA','OIA/data requests','Rapid review','Targeted checks','Pilot design']
weeks=[1,2,3,4,6,8]
ax.plot(weeks, np.ones(len(weeks)), marker='o')
for i,(w,s) in enumerate(zip(weeks,steps)):
    ax.text(w, 1.05 if i%2==0 else 0.88, s, ha='center', va='bottom' if i%2==0 else 'top', fontsize=10)
ax.set_yticks([])
ax.set_xlabel('Approximate start week')
ax.set_title('Pragmatic validation pathway: no full calibration yet')
ax.set_xlim(0,10)
ax.set_ylim(0.75,1.25)
ax.grid(axis='x', linestyle=':', alpha=0.4)
fig.tight_layout()
for path in [FIG/f'validation-roadmap-{VER}.png', OUT/f'validation-roadmap-{VER}.png']:
    fig.savefig(path, dpi=200, bbox_inches='tight')
plt.close(fig)

# Figure 3: evidence threshold by output, categorical status
with (ROOT/f'docs/validation/evidence-threshold-matrix-{VER}.csv').open(encoding='utf-8') as f:
    rows=list(csv.DictReader(f))
status_score={'Ready':3,'Ready with caveats':2,'Not ready':1}
y=[status_score.get(r['current_status'],0) for r in rows]
outs=[r['output'] for r in rows]
fig, ax = plt.subplots(figsize=(10,5.5))
ax.barh(np.arange(len(outs)), y)
ax.set_yticks(np.arange(len(outs)))
ax.set_yticklabels(outs)
ax.set_xlim(0,3.2)
ax.set_xticks([1,2,3])
ax.set_xticklabels(['Not ready','Ready with caveats','Ready'])
ax.set_title('Evidence threshold by intended output')
ax.invert_yaxis()
ax.grid(axis='x', linestyle=':', alpha=0.4)
fig.tight_layout()
for path in [FIG/f'evidence-thresholds-{VER}.png', OUT/f'evidence-thresholds-{VER}.png']:
    fig.savefig(path, dpi=200, bbox_inches='tight')
plt.close(fig)

print('plots saved')
