"""Download the two real-photo datasets (public Hugging Face mirrors)."""
from pathlib import Path
import urllib.request

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)
FILES = {
    **{f"pv-{i:05d}.parquet": f"https://huggingface.co/datasets/dpdl-benchmark/plant_village/resolve/main/data/train-{i:05d}-of-00013.parquet" for i in range(13)},
    "plantdoc-train-0.parquet": "https://huggingface.co/datasets/agyaatcoder/PlantDoc/resolve/main/data/train-00000-of-00002.parquet",
    "plantdoc-train-1.parquet": "https://huggingface.co/datasets/agyaatcoder/PlantDoc/resolve/main/data/train-00001-of-00002.parquet",
    "plantdoc-test.parquet": "https://huggingface.co/datasets/agyaatcoder/PlantDoc/resolve/main/data/test-00000-of-00001.parquet",
}
for name, url in FILES.items():
    p = RAW / name
    if p.exists():
        print("cached", name); continue
    print("downloading", name, flush=True)
    urllib.request.urlretrieve(url, p)
print("done")
