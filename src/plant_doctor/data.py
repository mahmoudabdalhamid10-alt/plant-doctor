"""Data loading: PlantVillage parquet shards + PlantDoc field images."""
import io
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq
from PIL import Image

RAW = Path(__file__).resolve().parents[2] / "data" / "raw"

def iter_plantvillage(raw_dir=RAW, max_shards=13):
    """Yield (label_idx, PIL.Image) from PlantVillage parquet shards."""
    for i in range(max_shards):
        path = Path(raw_dir) / f"pv-{i:05d}.parquet"
        if not path.exists():
            continue
        pf = pq.ParquetFile(path)
        for rg in range(pf.num_row_groups):
            t = pf.read_row_group(rg)
            for row in t.to_pylist():
                img = Image.open(io.BytesIO(row["image"]["bytes"])).convert("RGB")
                yield row["label"], img

def stratified_sample(labels, cap, seed=42):
    """Indices of a per-class-capped random subset."""
    rng = np.random.default_rng(seed)
    labels = np.asarray(labels)
    keep = []
    for cls in np.unique(labels):
        idx = np.flatnonzero(labels == cls)
        rng.shuffle(idx)
        keep.extend(idx[:cap].tolist())
    return np.array(sorted(keep))

def plantdoc_rows(raw_dir=RAW):
    """Yield (image_id, category, PIL.Image) from PlantDoc parquet files."""
    from .classes import PLANTDOC_TO_PV
    for name in ["plantdoc-train-0.parquet", "plantdoc-train-1.parquet", "plantdoc-test.parquet"]:
        path = Path(raw_dir) / name
        if not path.exists():
            continue
        t = pq.read_table(path)
        for row in t.to_pylist():
            cats = list(dict.fromkeys(row["objects"]["category"]))
            if len(cats) != 1 or cats[0] not in PLANTDOC_TO_PV:
                continue  # ambiguous or unmappable image
            img = Image.open(io.BytesIO(row["image"]["bytes"])).convert("RGB")
            yield row["image_id"], PLANTDOC_TO_PV[cats[0]], img
