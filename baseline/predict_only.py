import os
import csv
import torch
from torch.utils.data import DataLoader
from torchvision import datasets

from model import build_model, get_transforms

# Config
TEST_DIR   = "data/Testing"               # dossier test de la compétition
MODEL_SAVE = "baseline/best_model.pth"    # ton modèle sauvegardé
PRED_CSV   = "submissions/predictions.csv"
BATCH_SIZE = 32
DEVICE     = "cuda" if torch.cuda.is_available() else "cpu"

def predict():
    print("[INFO] Loading model from:", MODEL_SAVE)

    # Dataset test
    test_ds = datasets.ImageFolder(TEST_DIR, transform=get_transforms(train=False))
    test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=2)

    # Récupérer les noms de fichiers
    img_paths = [os.path.basename(p) for p, _ in test_ds.imgs]

    # Charger le modèle
    model = build_model()
    model.load_state_dict(torch.load(MODEL_SAVE, map_location=DEVICE))
    model.eval()

    # Prédictions
    all_preds = []
    with torch.no_grad():
        for imgs, _ in test_loader:
            imgs = imgs.to(DEVICE)
            out  = model(imgs)
            preds = out.argmax(1).cpu().tolist()
            all_preds.extend(preds)

    # Sauvegarde CSV
    os.makedirs("submissions", exist_ok=True)
    with open(PRED_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "prediction"])
        for fname, pred in zip(img_paths, all_preds):
            writer.writerow([fname, pred])

    print(f"[OK] Saved {len(all_preds)} predictions to {PRED_CSV}")

if __name__ == "__main__":
    predict()
