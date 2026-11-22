import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_index_html_and_assets_exist():
    index = ROOT / "index.html"
    assert index.exists()
    content = index.read_text(encoding="utf-8")
    assert "<html" in content.lower()
    assert "src/" in content


def test_all_js_files_have_valid_syntax():
    node = shutil.which("node")
    if not node:
        return
    js_files = list((ROOT / "src").rglob("*.js"))
    assert js_files, "No JS files found under src/"
    for js_file in js_files:
        proc = subprocess.run([node, "--check", str(js_file)], capture_output=True, text=True)
        assert proc.returncode == 0, f"JS syntax error in {js_file.name}: {proc.stderr}"


def test_all_dataset_json_files_valid():
    dataset_dir = ROOT / "Dataset"
    assert dataset_dir.exists()
    json_files = list(dataset_dir.rglob("*.json"))
    assert json_files, "No JSON datasets found"
    for jf in json_files:
        data = json.loads(jf.read_text(encoding="utf-8"))
        assert data is not None
