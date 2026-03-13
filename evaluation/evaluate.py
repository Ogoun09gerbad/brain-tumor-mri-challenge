import pandas as pd
import os
from sklearn.metrics import accuracy_score, classification_report, f1_score
import json

# ─── CONFIGURATION ────────────────────────────────────────────────────────
TRUTH_FILE = "evaluation/true_labels.csv"
SUBMISSION_DIR = "submissions"
RESULTS_DIR = "evaluation/results"
# ──────────────────────────────────────────────────────────────────────────

def evaluate_submission(submission_file):
    """
    Compare une soumission avec la vérité terrain et calcule les scores.
    """
    print(f"[INFO] Évaluation du fichier : {submission_file}")

    # 1. Chargement des données
    if not os.path.exists(TRUTH_FILE):
        print(f"[ERREUR] Fichier de vérité terrain introuvable à {TRUTH_FILE}")
        return None

    df_truth = pd.read_csv(TRUTH_FILE)
    df_pred = pd.read_csv(submission_file)

    # 2. Alignement des données
    # On s'assure que les deux fichiers ont les mêmes images dans le même ordre
    df_merged = pd.merge(df_truth, df_pred, on="filename", suffixes=("_true", "_pred"))

    if len(df_merged) != len(df_truth):
        print(f"[ATTENTION] Nombre de prédictions incorrect ({len(df_merged)}/{len(df_truth)})")
        # On peut décider de continuer ou d'arrêter ici

    y_true = df_merged["label"]
    y_pred = df_merged["prediction"]

    # 3. Calcul des métriques
    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average="weighted")
    report = classification_report(y_true, y_pred, target_names=["glioma", "meningioma", "notumor", "pituitary"], output_dict=True)

    print(f"--- RÉSULTATS ---")
    print(f"Accuracy : {acc:.4f}")
    print(f"F1-Score : {f1:.4f}")
    
    return {
        "accuracy": acc,
        "f1_score": f1,
        "details": report
    }

def save_results(team_name, metrics):
    """Sauvegarde les scores dans un fichier JSON pour le leaderboard."""
    os.makedirs(RESULTS_DIR, exist_ok=True)
    output_path = os.path.join(RESULTS_DIR, f"{team_name}.json")
    
    with open(output_path, "w") as f:
        json.dump(metrics, f, indent=4)
    print(f"[OK] Résultats sauvegardés pour {team_name}")

if __name__ == "__main__":
    # Exemple d'usage manuel :
    # Ici, on teste avec la baseline générée par predict.py
    baseline_path = "submissions/baseline_predictions.csv"
    
    if os.path.exists(baseline_path):
        metrics = evaluate_submission(baseline_path)
        if metrics:
            save_results("baseline_team", metrics)
    else:
        print("[!] Aucun fichier de soumission trouvé pour le test.")