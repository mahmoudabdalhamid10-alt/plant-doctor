import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from plant_doctor.classes import CLASSES, BY_KEY, PLANTDOC_TO_PV

def test_38_classes_unique_indices():
    assert len(CLASSES) == 38
    assert sorted(c.idx for c in CLASSES) == list(range(38))
    assert len(BY_KEY) == 38

def test_every_class_has_arabic_and_advice():
    for c in CLASSES:
        assert c.ar and c.advice_ar and c.en and c.advice_en

def test_healthy_flags():
    healthy = [c.key for c in CLASSES if c.healthy]
    assert len(healthy) == 15
    assert "tomato_healthy" in healthy and "apple_healthy" in healthy

def test_plantdoc_mapping_targets_exist():
    for cat, idx in PLANTDOC_TO_PV.items():
        assert 0 <= idx < 38
