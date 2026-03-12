import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torch.optim import Adam
from torch.optim.lr_scheduler import CosineAnnealingLR

from model import build_model, get_transforms, DEVICE

DATA_DIR   = "data"
TRAIN_DIR  = os.path.join(DATA_DIR, "train")
TEST_DIR   = os.path.join(DATA_DIR, "test")
MODEL_SAVE = "baseline/best_model.pth"
BATCH_SIZE = 32
EPOCHS     = 20
LR         = 1e-4

def train():
    print(f"[INFO] Training on: {DEVICE}")

    train_ds = datasets.ImageFolder(TRAIN_DIR, transform=get_transforms(train=True))
    val_ds   = datasets.ImageFolder(TEST_DIR,  transform=get_transforms(train=False))

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,  num_workers=4)
    val_loader   = DataLoader(val_ds,  batch_size=BATCH_SIZE, shuffle=False, num_workers=4)

    model     = build_model()
    criterion = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=LR, weight_decay=1e-4)
    scheduler = CosineAnnealingLR(optimizer, T_max=EPOCHS)

    best_acc = 0.0
    os.makedirs("baseline", exist_ok=True)

    for epoch in range(1, EPOCHS + 1):
        # --- Train ---
        model.train()
        total_loss, correct = 0, 0
        for imgs, labels in train_loader:
            imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
            optimizer.zero_grad()
            out  = model(imgs)
            loss = criterion(out, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * imgs.size(0)
            correct    += (out.argmax(1) == labels).sum().item()
        scheduler.step()
        train_acc = correct / len(train_ds)

        # --- Validate ---
        model.eval()
        val_correct = 0
        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
                out = model(imgs)
                val_correct += (out.argmax(1) == labels).sum().item()
        val_acc = val_correct / len(val_ds)

        print(f"Epoch {epoch:02d}/{EPOCHS} | Loss: {total_loss/len(train_ds):.4f} | "
              f"Train Acc: {train_acc:.4f} | Val Acc: {val_acc:.4f}")

        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), MODEL_SAVE)
            print(f"  ✓ Best model saved (acc={best_acc:.4f})")

    print(f"\n[DONE] Best Val Accuracy: {best_acc:.4f}")
    return best_acc

if __name__ == "__main__":
    train()
