"""Feature extraction with a frozen pretrained MobileNetV3-Small backbone."""
import numpy as np

IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)
IMG_SIZE = 224
FEAT_DIM = 576

_backbone = None

def get_backbone():
    """Load MobileNetV3-Small (ImageNet-1K weights) with the classifier removed."""
    global _backbone
    if _backbone is None:
        import torch
        from torchvision.models import mobilenet_v3_small, MobileNet_V3_Small_Weights
        torch.set_num_threads(1)
        m = mobilenet_v3_small(weights=MobileNet_V3_Small_Weights.IMAGENET1K_V1)
        m.classifier = torch.nn.Identity()
        m.eval()
        _backbone = m
    return _backbone

def preprocess(img):
    """PIL image -> normalized float32 CHW array (224x224, ImageNet stats)."""
    x = np.asarray(img.resize((IMG_SIZE, IMG_SIZE)), dtype=np.float32) / 255.0
    x = (x - IMAGENET_MEAN) / IMAGENET_STD
    return x.transpose(2, 0, 1)

def extract(images, batch_size=32):
    """images: list of PIL images -> (N, 576) float32 features."""
    import torch
    model = get_backbone()
    feats = []
    with torch.no_grad():
        for i in range(0, len(images), batch_size):
            batch = np.stack([preprocess(im) for im in images[i:i + batch_size]])
            out = model(torch.from_numpy(batch))
            feats.append(out.numpy().astype(np.float32))
    return np.concatenate(feats, axis=0)
