.PHONY: data features train test
data: ; python scripts/download_data.py
features: ; python scripts/extract_features.py 0 13 && python scripts/extract_features.py plantdoc && python scripts/extract_features.py plantdoc_crops
train: ; python scripts/train_evaluate.py
test: ; python -m pytest tests/ -q
