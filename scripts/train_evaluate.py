"""Train classifier heads on cached features; honest evaluation incl. PlantDoc field test."""
import json, sys, time
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from plant_doctor.classes import CLASSES

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
OUT = ROOT / "reports"; (OUT / "figures").mkdir(parents=True, exist_ok=True)
MODELS = ROOT / "models"; MODELS.mkdir(exist_ok=True)

# ---- load features
Xs, ys = [], []
for f in sorted(PROC.glob("pv_feats_*.npz")):
    d = np.load(f); Xs.append(d["X"]); ys.append(d["y"])
X = np.concatenate(Xs); y = np.concatenate(ys)
print("PV:", X.shape, flush=True)
d = np.load(PROC / "plantdoc_feats.npz")
Xf, yf = d["X"], d["y"]
print("PlantDoc:", Xf.shape, flush=True)

# ---- stratified 70/15/15 split
from sklearn.model_selection import train_test_split
X_tr, X_tmp, y_tr, y_tmp = train_test_split(X, y, test_size=0.30, stratify=y, random_state=42)
X_va, X_te, y_va, y_te = train_test_split(X_tmp, y_tmp, test_size=0.50, stratify=y_tmp, random_state=42)
print("split:", X_tr.shape[0], X_va.shape[0], X_te.shape[0], flush=True)

from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, f1_score

candidates = {
    "dummy_most_frequent": DummyClassifier(strategy="most_frequent"),
    "logreg_balanced": LogisticRegression(C=10, class_weight="balanced", max_iter=3000),
    "linsvc_balanced": LinearSVC(C=1.0, class_weight="balanced"),
    "knn5": KNeighborsClassifier(n_neighbors=5, n_jobs=1),
}
results = {}
for name, clf in candidates.items():
    t0 = time.time()
    clf.fit(X_tr, y_tr)
    va = clf.predict(X_va)
    results[name] = {"val_acc": float(accuracy_score(y_va, va)),
                     "val_macro_f1": float(f1_score(y_va, va, average="macro")),
                     "fit_s": round(time.time() - t0, 1)}
    print(name, results[name], flush=True)

best = max((k for k in candidates if k != "dummy_most_frequent"), key=lambda k: results[k]["val_macro_f1"])
print("BEST:", best, flush=True)
clf = candidates[best]

# ---- in-domain test
from sklearn.metrics import classification_report, confusion_matrix
te = clf.predict(X_te)
rep = classification_report(y_te, te, output_dict=True, zero_division=0)
# ---- field test (PlantDoc)
fd = clf.predict(Xf)
rep_f = classification_report(yf, fd, output_dict=True, zero_division=0)

summary = {
    "best_model": best,
    "candidates": results,
    "pv_test": {"n": int(len(y_te)), "acc": rep["accuracy"], "macro_f1": rep["macro avg"]["f1-score"], "weighted_f1": rep["weighted avg"]["f1-score"]},
    "plantdoc_field": {"n": int(len(yf)), "acc": rep_f["accuracy"], "macro_f1": rep_f["macro avg"]["f1-score"], "weighted_f1": rep_f["weighted avg"]["f1-score"]},
}
json.dump(summary, open(OUT / "metrics_summary.json", "w"), indent=2)
json.dump({"pv_test": rep, "plantdoc": rep_f}, open(OUT / "per_class_report.json", "w"))
print(json.dumps(summary, indent=2)[:900], flush=True)

# ---- confusion matrices
np.save(OUT / "cm_pv_test.npy", confusion_matrix(y_te, te, labels=list(range(38))))
np.save(OUT / "cm_plantdoc.npy", confusion_matrix(yf, fd, labels=list(range(38))))

# ---- persist model
import joblib
joblib.dump(clf, MODELS / "head.joblib")
if best == "logreg_balanced":
    head = {"classes": [c.key for c in CLASSES],
            "coef": clf.coef_.astype(float).round(6).tolist(),
            "intercept": clf.intercept_.astype(float).round(6).tolist()}
    json.dump(head, open(MODELS / "head.json", "w"))
    print("head.json exported", flush=True)
