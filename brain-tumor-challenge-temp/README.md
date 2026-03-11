# 🧠 Brain Tumor MRI Classification Challenge

<div align="center">

[![Evaluation System](https://github.com/Ogoun09gerbad/brain-tumor-mri-challenge/actions/workflows/evaluate.yml/badge.svg)](https://github.com/Ogoun09gerbad/brain-tumor-mri-challenge/actions/workflows/evaluate.yml)
![Classes](https://img.shields.io/badge/Classes-4-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

**Can your model detect brain tumors from MRI scans?**

[📊 Leaderboard](#-leaderboard) • [📁 Dataset](#-dataset) • [🚀 Quick Start](#-quick-start) • [📤 How to Submit](#-submission-process)

</div>

---

## 🏆 Leaderboard

| Rank | Team | Accuracy | F1 Score (Macro) | Submissions | Last Updated |
|------|------|----------|-------------------|-------------|--------------|
| 🥇 | — | — | — | — | — |
| 🥈 | — | — | — | — | — |
| 🥉 | — | — | — | — | — |
> 📣 Le classement est mis à jour automatiquement après chaque soumission valide.
> Historique complet : [`leaderboard/leaderboard.csv`](leaderboard/leaderboard.csv)

---

## 📋 Overview
### Task
Classify brain MRI images into **4 categories**: 0=glioma, 1=meningioma, 2=no_tumor, 3=pituitary.

## 📤 Submission Process

### Step 1 — Encrypt Your Submission
```bash
python encryption/encrypt.py submissions/nom_equipe.csv encryption/public_key.pem submissions/nom_equipe.enc
