import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_head_json_shape():
    head = json.load(open(ROOT / "models" / "head.json"))
    assert len(head["classes"]) == 38
    assert len(head["coef"]) == 38 and len(head["coef"][0]) == 576
    assert len(head["intercept"]) == 38

def test_classes_json_complete():
    classes = json.load(open(ROOT / "docs" / "model" / "classes.json"))
    assert len(classes) == 38
    assert all(c["ar"] and c["advice_ar"] for c in classes)

def test_demo_page_links_assets():
    html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "model/backbone.onnx" in html and "model/head.json" in html and "ort.InferenceSession" in html
