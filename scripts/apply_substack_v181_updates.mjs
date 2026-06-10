import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const manifestPath = path.join(root, "docs/substack-ready/posts-v1.8.1-updates/manifest-v1.8.1.csv");
const outDir = path.join(root, "docs/substack-ready/posts-v1.8.1-applied");
const schedulePath = path.join(root, "launch-schedule-v1.7.2.json");
const seriesPrefix = "rareinsights/primary-care-funding-architecture-v1.7.2/";

const publicSubtitles = new Map([
  ["08", "How capped payment can suppress marginal supply, and how access pressure moves through the system."],
  ["09", "What PHOs can usefully do, where payment friction matters, and why place accountability changes incentives."],
  ["10", "Why ACC, ambulance, urgent care and ED pressure need to be treated as one upstream system."],
  ["11", "Why safe supply expansion depends on scope, governance and claim rules, not just workforce counts."],
  ["12", "Why telehealth can extend local care but cannot replace local clinical supply."],
  ["13", "Why co-payments can signal demand and still create equity failure when access is constrained."],
  ["14", "A map of the linked games behind primary-care access, funding and hospital pressure."],
  ["15", "Why the answer is an architecture rather than a single payment lever."],
  ["16", "What the model now supports, what it still does not support, and why those boundaries matter."],
  ["17", "How MCDA can make policy disagreement explicit, testable and useful."],
  ["18", "A staged policy architecture for growing primary care before hospitals have to absorb the failure."]
]);

function readText(filePath) {
  return fs.readFileSync(filePath, "utf8").replace(/^\uFEFF/, "");
}

function parseCsvLine(line) {
  const cells = [];
  let current = "";
  let quoted = false;
  for (let i = 0; i < line.length; i += 1) {
    const char = line[i];
    if (char === '"' && line[i + 1] === '"') {
      current += '"';
      i += 1;
    } else if (char === '"') {
      quoted = !quoted;
    } else if (char === "," && !quoted) {
      cells.push(current);
      current = "";
    } else {
      current += char;
    }
  }
  cells.push(current);
  return cells;
}

function csvEscape(value) {
  const text = String(value);
  return /[",\r\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}

function parseManifest(csvText) {
  const [headerLine, ...lines] = csvText.trim().split(/\r?\n/);
  const headers = parseCsvLine(headerLine);
  return lines.filter(Boolean).map((line) => {
    const cells = parseCsvLine(line);
    return Object.fromEntries(headers.map((header, index) => [header, cells[index] ?? ""]));
  });
}

function postNumberFromUpdateId(updateId) {
  const match = updateId.match(/post-(\d{2})-/);
  if (!match) {
    throw new Error(`Cannot infer post number from ${updateId}`);
  }
  return match[1];
}

function launchBaseFor(originalPath, postNumber) {
  const originalAbs = path.join(root, originalPath);
  const originalName = path.basename(originalPath);
  if (Number(postNumber) <= 6) {
    const launchName = originalName.replace("-v1.6.0.md", "-v1.7.2.md");
    const launchPath = path.join(root, "docs/substack-ready/posts-v1.7.2-launch", launchName);
    if (fs.existsSync(launchPath)) {
      return path.relative(root, launchPath).replace(/\\/g, "/");
    }
  }
  if (!fs.existsSync(originalAbs)) {
    throw new Error(`Missing base post: ${originalPath}`);
  }
  return originalPath;
}

function extractSection(markdown, heading) {
  const lines = markdown.split(/\r?\n/);
  const start = lines.findIndex((line) => line.trim() === `## ${heading}`);
  if (start < 0) return "";
  const body = [];
  for (const line of lines.slice(start + 1)) {
    if (line.startsWith("## ")) break;
    body.push(line);
  }
  return body.join("\n").trim();
}

function buildAppliedMarkdown(baseMarkdown, updateMarkdown) {
  const changed = extractSection(updateMarkdown, "What changed since v1.6.0");
  const boundary = extractSection(updateMarkdown, "Claim boundary");
  const trimmedBase = baseMarkdown.trimEnd();
  return `${trimmedBase}

---

## v1.8.1 model update

The current Streamlit model release is v1.8.1. Its public aggregate validation lane is \`public_aggregate_validated\`, and its claim level is \`empirically_supported_if_gated\` for registered gates only.

${changed}

**Claim boundary:** ${boundary}
`;
}

fs.mkdirSync(outDir, { recursive: true });

const rows = parseManifest(readText(manifestPath));
const appliedRows = [];
const appliedByPost = new Map();

for (const row of rows) {
  const postNumber = postNumberFromUpdateId(row.update_id);
  const baseRel = launchBaseFor(row.original_path, postNumber);
  const updateRel = row.update_path;
  const baseText = readText(path.join(root, baseRel));
  const updateText = readText(path.join(root, updateRel));
  const baseName = path.basename(baseRel).replace(/-v1\.(6\.0|7\.2)\.md$/, "-v1.8.1-applied.md");
  const appliedRel = `docs/substack-ready/posts-v1.8.1-applied/${baseName}`;
  fs.writeFileSync(path.join(root, appliedRel), buildAppliedMarkdown(baseText, updateText), "utf8");
  appliedRows.push({
    update_id: row.update_id,
    post_number: postNumber,
    base_path: baseRel,
    update_path: updateRel,
    applied_path: appliedRel,
    update_type: row.update_type,
    claim_status: row.claim_status
  });
  appliedByPost.set(postNumber, appliedRel);
}

const appliedManifest = [
  "update_id,post_number,base_path,update_path,applied_path,update_type,claim_status",
  ...appliedRows.map((row) => [
    row.update_id,
    row.post_number,
    row.base_path,
    row.update_path,
    row.applied_path,
    row.update_type,
    row.claim_status
  ].map(csvEscape).join(","))
].join("\n");
fs.writeFileSync(path.join(outDir, "manifest-v1.8.1-applied.csv"), `${appliedManifest}\n`, "utf8");

const readme = `# Applied v1.8.1 Substack posts

Generated by \`node scripts/apply_substack_v181_updates.mjs\`.

These files combine the current public post text with the v1.8.1 update notes. They preserve the bounded claim status:

- calibration status: \`public_aggregate_validated\`
- claim level: \`empirically_supported_if_gated\`
- scope: registered public aggregate validation gates only

Do not convert these applied posts into claims of precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, patient-level forecasts, or causal effects.
`;
fs.writeFileSync(path.join(outDir, "README.md"), readme, "utf8");

const schedule = JSON.parse(readText(schedulePath));
for (const item of schedule) {
  if (!item.postNumber || item.postNumber === "00") {
    continue;
  }
  const appliedRel = appliedByPost.get(item.postNumber);
  if (!appliedRel) {
    throw new Error(`No applied v1.8.1 post for schedule post ${item.postNumber}`);
  }
  item.postPath = `${seriesPrefix}${appliedRel}`;
  if (publicSubtitles.has(item.postNumber)) {
    item.subtitle = publicSubtitles.get(item.postNumber);
  }
}
fs.writeFileSync(schedulePath, `${JSON.stringify(schedule, null, 2)}\n`, "utf8");

console.log(`Wrote ${appliedRows.length} applied v1.8.1 posts and updated ${schedulePath}`);
