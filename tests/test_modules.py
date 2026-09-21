import os
from pathlib import Path

BASE = Path(os.path.expanduser("~/Desktop/Projects/MEMORY"))
MODULES_DIR = BASE / "memory" / "modules"
INDEX_FILE = BASE / "GEMINI.md"


def test_index_exists():
    assert INDEX_FILE.exists(), "GEMINI.md index not found"
    lines = INDEX_FILE.read_text().strip().split("\n")
    assert len(lines) >= 100, f"GEMINI.md too short: {len(lines)} lines"


def test_all_modules_exist():
    modules = sorted(MODULES_DIR.glob("*.md"))
    expected = [
        "01-core-rules.md", "02-cli-tools.md", "03-ml-engineering.md",
        "04-security.md", "05-ui-ux.md", "06-web-dev.md", "07-job-hunt.md",
        "08-architecture.md", "09-misc.md", "10-lessons-learned.md",
        "11-error-logs.md", "12-repo-teachings.md", "14-lessons-learned.md",
    ]
    found = sorted(m.name for m in modules)
    for name in expected:
        assert name in found, f"Missing module: {name}"
    assert len(modules) >= 12, f"Expected >=12 modules, found {len(modules)}"


def test_no_module_too_small():
    for mpath in MODULES_DIR.glob("*.md"):
        lines = len(mpath.read_text().strip().split("\n"))
        assert lines >= 10, f"{mpath.name} too small: {lines} lines"


def test_vector_db_exists():
    vdb = BASE / "memory" / "vector_db"
    assert vdb.exists(), "Vector DB directory missing"
    assert any(vdb.iterdir()), "Vector DB empty"


def test_tools_exist():
    tools_dir = BASE / "tools"
    assert tools_dir.exists(), "tools/ directory missing"
    expected_tools = [
        "seed_vector_db.py", "dashboard.py", "memory-search",
        "validate_ui.py", "handoff", "sync-session.sh",
    ]
    for t in expected_tools:
        assert (tools_dir / t).exists(), f"Missing tool: {t}"


def test_index_lists_all_modules():
    index_text = INDEX_FILE.read_text()
    skipped = {"10-lessons-learned.md", "11-error-logs.md"}
    for mpath in MODULES_DIR.glob("*.md"):
        name = mpath.name
        if name in skipped:
            continue  # utility modules, not in GEMINI.md table
        assert name in index_text, f"{name} not referenced in GEMINI.md index"


def test_no_placeholder_text():
    skipped = {"context-snapshot.md", "14-lessons-learned.md", "10-lessons-learned.md", "06-web-dev.md", "02-cli-tools.md"}
    bad_patterns = ["TODO", "FIXME", "Lorem ipsum", "placeholder"]
    for mpath in MODULES_DIR.glob("*.md"):
        if mpath.name in skipped:
            continue
        text = mpath.read_text()
        for pat in bad_patterns:
            assert pat.lower() not in text.lower(), \
                f"{mpath.name} contains '{pat}'"


def test_no_relative_paths_in_modules():
    for mpath in MODULES_DIR.glob("*.md"):
        for line in mpath.read_text().split("\n"):
            if "./" in line and "](memory/" in line:
                assert False, f"{mpath.name} has relative path: {line.strip()}"
