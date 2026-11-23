"""CLI: python -m plant_doctor.predict leaf.jpg -> top-3 diagnosis + Arabic advice."""
import sys
from pathlib import Path
from PIL import Image
import numpy as np
import joblib
from .classes import CLASSES
from .features import extract

def predict(image_path, top=3):
    model_path = Path(__file__).resolve().parents[2] / "models" / "head.joblib"
    clf = joblib.load(model_path)
    img = Image.open(image_path).convert("RGB")
    x = extract([img])
    if hasattr(clf, "predict_proba"):
        probs = clf.predict_proba(x)[0]
    else:
        m = clf.decision_function(x)[0]
        e = np.exp(m - m.max()); probs = e / e.sum()
    order = probs.argsort()[::-1][:top]
    return [(CLASSES[int(i)], float(probs[i])) for i in order]

def main():
    if len(sys.argv) < 2:
        print("usage: python -m plant_doctor.predict <leaf.jpg>"); sys.exit(1)
    for cls, p in predict(sys.argv[1]):
        print(f"{p*100:5.1f}%  {cls.ar}  ({cls.en})")
    best, p = predict(sys.argv[1])[0]
    print("\n" + best.advice_ar)
    if p < 0.5:
        print("\n⚠️ الثقة منخفضة؛ صور الحقول أصعب على النموذج. جرّب ورقة واحدة قريبة بخلفية بسيطة.")

if __name__ == "__main__":
    main()
