import os
import csv
import torch
from torch.utils.data import DataLoader
from torchvision import datasets

from baseline.model import build_model, get_transforms, DEVICE

TEST_DIR   = "data/test"
MODEL_SAVE = "baseline/best_model.pth"
PRED_CSV   = "submissions/baseline_predictions.csv"
BATCH_SIZE = 32

def predict():
    print("[INFO] Generating predictions...")

    test_ds = datasets.ImageFolder(TEST_DIR, transform=get_transforms(train=False))
    test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=4)

    img_paths = [os.path.basename(p) for p, _ in test_ds.imgs]

    model = build_model()
    model.load_state_dict(torch.load(MODEL_SAVE, map_location=DEVICE))
    model.eval()

    all_preds = []
    with torch.no_grad():
        for imgs, _ in test_loader:
            imgs = imgs.to(DEVICE)
            out  = model(imgs)
            preds = out.argmax(1).cpu().tolist()
            all_preds.extend(preds)

    os.makedirs("submissions", exist_ok=True)
    with open(PRED_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "prediction"])
        for fname, pred in zip(img_paths, all_preds):
            writer.writerow([fname, pred])

    print(f"[OK] Saved {len(all_preds)} predictions to {PRED_CSV}")
    print("\nLabel mapping: 0=glioma, 1=meningioma, 2=no_tumor, 3=pituitary")

if __name__ == "__main__":
    predict()
