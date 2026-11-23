"""Extract MobileNetV3 features, streaming in small chunks to stay under RAM limits."""
import sys, time, io
from pathlib import Path
import numpy as np
import pyarrow.parquet as pq
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from plant_doctor.features import extract
from plant_doctor.classes import PLANTDOC_TO_PV

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"; PROC.mkdir(parents=True, exist_ok=True)
CHUNK = 64

def run_chunks(records, out_path, tag):
    """records: iterable of (label, PIL img). Stream -> features -> npz."""
    Xs, ys = [], []
    buf_l, buf_i = [], []
    n = 0
    for label, img in records:
        buf_l.append(label); buf_i.append(img)
        if len(buf_i) == CHUNK:
            Xs.append(extract(buf_i)); ys.extend(buf_l); n += len(buf_i)
            print(f"{tag}: {n}", flush=True)
            buf_l, buf_i = [], []
    if buf_i:
        Xs.append(extract(buf_i)); ys.extend(buf_l)
    X = np.concatenate(Xs)
    np.savez_compressed(out_path, X=X, y=np.array(ys, dtype=np.int64))
    print(f"{tag} DONE: {X.shape}", flush=True)

def pv_records(shard_idx):
    pf = pq.ParquetFile(PROC.parent / "raw" / f"pv-{shard_idx:05d}.parquet")
    for rg in range(pf.num_row_groups):
        t = pf.read_row_group(rg)
        for row in t.to_pylist():
            yield row["label"], Image.open(io.BytesIO(row["image"]["bytes"])).convert("RGB")
        del t

def plantdoc_records():
    for name in ["plantdoc-train-0.parquet", "plantdoc-train-1.parquet", "plantdoc-test.parquet"]:
        p = PROC.parent / "raw" / name
        if not p.exists(): continue
        pf = pq.ParquetFile(p)
        for rg in range(pf.num_row_groups):
            t = pf.read_row_group(rg)
            for row in t.to_pylist():
                cats = list(dict.fromkeys(row["objects"]["category"]))
                if len(cats) == 1 and cats[0] in PLANTDOC_TO_PV:
                    yield PLANTDOC_TO_PV[cats[0]], Image.open(io.BytesIO(row["image"]["bytes"])).convert("RGB")
            del t

if __name__ == "__main__" and sys.argv[1] != "plantdoc_crops":
    if sys.argv[1] == "plantdoc":
        out = PROC / "plantdoc_feats.npz"
        if not out.exists(): run_chunks(plantdoc_records(), out, "plantdoc")
        else: print("plantdoc cached")
    else:
        for i in range(int(sys.argv[1]), int(sys.argv[2])):
            out = PROC / f"pv_feats_{i:02d}.npz"
            if out.exists():
                print(f"shard {i} cached", flush=True); continue
            t0 = time.time()
            run_chunks(pv_records(i), out, f"pv{i}")
            print(f"shard {i} in {time.time()-t0:.0f}s", flush=True)

def plantdoc_crop_records(min_area=4000):
    for name in ["plantdoc-train-0.parquet", "plantdoc-train-1.parquet", "plantdoc-test.parquet"]:
        p = PROC.parent / "raw" / name
        if not p.exists(): continue
        pf = pq.ParquetFile(p)
        for rg in range(pf.num_row_groups):
            t = pf.read_row_group(rg)
            for row in t.to_pylist():
                cats = list(dict.fromkeys(row["objects"]["category"]))
                if len(cats) != 1 or cats[0] not in PLANTDOC_TO_PV:
                    continue
                img = Image.open(io.BytesIO(row["image"]["bytes"])).convert("RGB")
                W, H = img.size
                for (x, y0, w, h) in row["objects"]["bbox"]:
                    if w * h < min_area: continue
                    x1, y1 = min(max(0, x), W), min(max(0, y0), H)
                    x2, y2 = min(W, x + w), min(H, y0 + h)
                    if x2 - x1 < 10 or y2 - y1 < 10: continue
                    yield PLANTDOC_TO_PV[cats[0]], img.crop((x1, y1, x2, y2))
            del t

if len(sys.argv) > 1 and sys.argv[1] == "plantdoc_crops":
    out = PROC / "plantdoc_crop_feats.npz"
    if not out.exists(): run_chunks(plantdoc_crop_records(), out, "pdcrops")
    else: print("cached")
