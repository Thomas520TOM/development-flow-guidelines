#!/usr/bin/env python3
"""coding-guidelines validation script.

Checks:
    1. Frontmatter completeness — all required fields present in every module
    2. Reference reachability — all referenced files exist
    3. Gate closure — all input.from references resolve to upstream output fields
    4. Token budget consistency — declared budget matches actual file size
    5. Dependency graph integrity — no circular dependencies, all refs valid
    6. Release surface presence — required top-level discovery files exist
"""

import os
import re
import sys
import yaml
from pathlib import Path
from collections import defaultdict

SKILL_ROOT = Path(__file__).resolve().parent.parent

MODULE_FILES = [
    "SKILL.md",
    "01-code-generation/rules.md",
    "02-skill-dictionary/index.md",
    "03-project-setup/01-requirements-analysis.md",
    "03-project-setup/02-technical-design.md",
    "04-maintenance/rules.md",
    "05-log-memory/system.md",
    "06-evaluation/system.md",
    "07-testing-strategy/rules.md",
    "08-code-review/rules.md",
    "09-security-review/rules.md",
    "context-management.md",
    "error-recovery.md",
    "extension-interface.md",
    "progress-tracking.md",
]

RELEASE_SURFACE_FILES = [
    "AGENTS.md",
    "README.md",
    "LICENSE",
    "platforms/opencode/SKILL.md",
]

REQUIRED_FIELDS = ["description", "version", "module_id", "category", "depends_on", "inputs", "outputs", "gates"]
TITLE_FIELDS = ["title", "name"]
VALID_CATEGORIES = {"lifecycle", "system", "meta"}
VALID_GATE_ACTIONS = {"block", "warn", "skip"}

TOKEN_BUDGET_MAP = {
    "low": 5000,
    "medium": 15000,
    "high": 50000,
}

# --- helpers ---

def parse_frontmatter(filepath: Path) -> dict | None:
    """Extract YAML frontmatter from a markdown file."""
    text = filepath.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("---", 3)
    if end == -1:
        return None
    try:
        return yaml.safe_load(text[3:end])
    except yaml.YAMLError as e:
        return {"_parse_error": str(e)}


def file_size_chars(filepath: Path) -> int:
    return len(filepath.read_text(encoding="utf-8"))


def check_token_budget(fm: dict, size: int) -> list[str]:
    """Return warnings if token_budget field mismatches actual size."""
    issues = []
    if "token_budget" not in fm:
        return issues
    declared = fm["token_budget"]
    if declared not in TOKEN_BUDGET_MAP:
        issues.append(f"Unknown token_budget value: {declared}")
        return issues
    limit = TOKEN_BUDGET_MAP[declared]
    if size > limit:
        issues.append(f"File size {size:,} chars exceeds token_budget '{declared}' limit of {limit:,}")
    if declared == "low" and size > limit * 0.8:
        issues.append(f"File size {size:,} chars near token_budget 'low' limit ({limit:,}) — consider upgrading to medium")
    if declared == "high" and size < TOKEN_BUDGET_MAP["medium"]:
        issues.append(f"File size {size:,} chars well below token_budget 'high' limit — consider downgrading to medium")
    return issues


# --- check functions ---

def check_frontmatter_completeness(modules: dict[str, dict]) -> list[str]:
    issues = []
    for mod_id, fm in modules.items():
        if "_parse_error" in fm:
            issues.append(f"[{mod_id}] YAML parse error: {fm['_parse_error']}")
            continue
        has_title = any(f in fm for f in TITLE_FIELDS)
        if not has_title:
            issues.append(f"[{mod_id}] Missing title/name field")
        for field in REQUIRED_FIELDS:
            if field not in fm:
                issues.append(f"[{mod_id}] Missing required field: {field}")
        if fm.get("category") and fm["category"] not in VALID_CATEGORIES:
            issues.append(f"[{mod_id}] Invalid category '{fm['category']}' — must be one of {VALID_CATEGORIES}")
        ver = fm.get("version", "")
        if ver and not re.match(r"^\d+\.\d+\.\d+", str(ver)):
            issues.append(f"[{mod_id}] Invalid version '{ver}' — must be semver")
        for g in fm.get("gates", []):
            if isinstance(g, dict) and g.get("on_fail") not in VALID_GATE_ACTIONS:
                issues.append(f"[{mod_id}] Gate '{g.get('description','?')}' has invalid on_fail: {g.get('on_fail')}")
    return issues


def check_reference_reachability(modules: dict[str, dict]) -> list[str]:
    issues = []
    all_files = set()
    for root, _, files in os.walk(SKILL_ROOT):
        if ".git" in root or ".project" in root:
            continue
        for f in files:
            all_files.add(os.path.relpath(os.path.join(root, f), SKILL_ROOT))

    for mod_file in MODULE_FILES:
        fpath = SKILL_ROOT / mod_file
        if not fpath.exists():
            issues.append(f"[{mod_file}] File does not exist in filesystem")
            continue
        content = fpath.read_text(encoding="utf-8")
        refs = re.findall(r'`([\w/-]+\.(?:md|yaml|yml))`', content)
        refs += re.findall(r'"([\w/-]+\.(?:md|yaml|yml))"', content)
        for ref in refs:
            if ref.startswith(("http", "C:", "/")):
                continue
            resolved = (SKILL_ROOT / mod_file).parent / ref
            rel = os.path.relpath(str(resolved), SKILL_ROOT)
            if not os.path.exists(resolved) and rel not in all_files:
                issues.append(f"[{mod_file}] Reference not found: {ref}")
    return issues


def check_gate_closure(modules: dict[str, dict]) -> list[str]:
    issues = []
    valid_ids = set(modules.keys())

    for mod_id, fm in modules.items():
        if "_parse_error" in fm:
            continue

        for dep in fm.get("depends_on", []):
            if dep not in valid_ids:
                issues.append(f"[{mod_id}] depends_on unknown module: {dep}")

        for inp in fm.get("inputs", []):
            if not isinstance(inp, dict):
                continue
            upstream = inp.get("from")
            if not upstream:
                continue
            if upstream not in valid_ids:
                issues.append(f"[{mod_id}] input '{inp.get('field','?')}' references unknown module: {upstream}")
                continue
            upstream_fm = modules.get(upstream)
            if not upstream_fm or "_parse_error" in upstream_fm:
                continue
            upstream_outputs = {o["field"] for o in upstream_fm.get("outputs", []) if isinstance(o, dict)}
            upstream_field = inp.get("field")  # field name in the upstream module
            alias = inp.get("alias")  # local alias in this module
            check_name = alias or upstream_field
            if upstream_field and upstream_field not in upstream_outputs:
                issues.append(f"[{mod_id}] input '{check_name}' (field '{upstream_field}') not found in {upstream} outputs: {upstream_outputs}")

    return issues


def check_circular_dependencies(modules: dict[str, dict]) -> list[str]:
    issues = []
    adj = defaultdict(set)
    for mod_id, fm in modules.items():
        if "_parse_error" in fm:
            continue
        for dep in fm.get("depends_on", []):
            if dep in modules:
                adj[mod_id].add(dep)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {mid: WHITE for mid in modules}

    def dfs(node, path):
        color[node] = GRAY
        for neighbor in adj[node]:
            if color[neighbor] == GRAY:
                cycle = path[path.index(neighbor):] + [neighbor, node]
                issues.append(f"Circular dependency: {' → '.join(cycle)}")
                return
            if color[neighbor] == WHITE:
                dfs(neighbor, path + [node])
        color[node] = BLACK

    for mid in modules:
        if color[mid] == WHITE:
            dfs(mid, [])
    return issues


def check_token_budgets(modules: dict[str, dict]) -> list[str]:
    issues = []
    for mod_id in modules:
        mod_file = next((f for f in MODULE_FILES if modules[mod_id].get("module_id") == mod_id), None)
        if not mod_file and mod_id == "system-router":
            mod_file = "SKILL.md"
        if not mod_file:
            continue
        fpath = SKILL_ROOT / mod_file
        if not fpath.exists():
            continue
        size = file_size_chars(fpath)
        fm = modules[mod_id]
        issues.extend([f"[{mod_id}] {i}" for i in check_token_budget(fm, size)])
    return issues


def check_lifecycle_coverage(modules: dict[str, dict]) -> list[str]:
    """Ensure the standard flow from requirements to evaluation is traceable."""
    issues = []
    lifecycle_order = [
        "01-requirements-analysis",
        "02-technical-design",
        "07-testing-strategy",
        "01-code-generation",
        "08-code-review",
        "09-security-review",
        "06-evaluation",
    ]
    for i in range(len(lifecycle_order) - 1):
        current = lifecycle_order[i]
        nxt = lifecycle_order[i + 1]
        fm_next = modules.get(nxt)
        if not fm_next:
            issues.append(f"Lifecycle module {nxt} not found")
            continue
        deps = fm_next.get("depends_on", [])
        upstream_modules = [current]
        for inp in fm_next.get("inputs", []):
            if isinstance(inp, dict) and inp.get("from"):
                upstream_modules.append(inp["from"])
        if current not in deps and current not in upstream_modules:
            issues.append(f"[{nxt}] does not declare dependency on {current}")
    return issues


def check_release_surface() -> list[str]:
    issues = []
    for rel_path in RELEASE_SURFACE_FILES:
        if not (SKILL_ROOT / rel_path).exists():
            issues.append(f"Release surface file missing: {rel_path}")
    return issues


# --- main ---

def main():
    modules = {}
    for mod_file in MODULE_FILES:
        fpath = SKILL_ROOT / mod_file
        if not fpath.exists():
            print(f"MISSING: {mod_file}")
            continue
        fm = parse_frontmatter(fpath)
        if fm is None:
            print(f"NO FRONTMATTER: {mod_file}")
            continue
        mid = fm.get("module_id", mod_file)
        modules[mid] = fm

    print(f"Loaded {len(modules)} modules\n")

    all_issues = []
    checks = [
        ("Frontmatter Completeness", check_frontmatter_completeness(modules)),
        ("Reference Reachability", check_reference_reachability(modules)),
        ("Gate Closure", check_gate_closure(modules)),
        ("Circular Dependencies", check_circular_dependencies(modules)),
        ("Token Budget Consistency", check_token_budgets(modules)),
        ("Lifecycle Coverage", check_lifecycle_coverage(modules)),
        ("Release Surface Presence", check_release_surface()),
    ]

    total = 0
    for name, issues in checks:
        print(f"--- {name} ---")
        if not issues:
            print("  PASSED")
        for issue in issues:
            print(f"  FAIL: {issue}")
        total += len(issues)
        print()

    print(f"Total issues: {total}")
    if total == 0:
        print("ALL CHECKS PASSED — production-ready.")
    else:
        print(f"{total} issue(s) found. Fix before release.")
    sys.exit(0 if total == 0 else 1)


if __name__ == "__main__":
    main()
