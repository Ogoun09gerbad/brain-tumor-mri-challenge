import pandas as pd
import os
import argparse
from sklearn.metrics import accuracy_score, classification_report, f1_score
import json

# ─── CONFIGURATION ────────────────────────────────────────────────────────
TRUTH_FILE = "evaluation/true_labels.csv"
RESULTS_DIR = "evaluation/results"
# ──────────────────────────────────────────────────────────────────────────

def evaluate_submission(submission_file):
    """Compare une soumission avec la vérité terrain et calcule les scores."""
    print(f"[INFO] Évaluation du fichier : {submission_file}")

    if not os.path.exists(TRUTH_FILE):
        print(f"[ERREUR] Vérité terrain introuvable : {TRUTH_FILE}")
        return None

    try:
        df_truth = pd.read_csv(TRUTH_FILE)
        df_pred = pd.read_csv(submission_file)

        # On force les noms de colonnes en minuscules pour éviter les erreurs de frappe
        df_truth.columns = [c.lower() for c in df_truth.columns]
        df_pred.columns = [c.lower() for c in df_pred.columns]

        # Alignement des données sur 'filename'
        df_merged = pd.merge(df_truth, df_pred, on="filename", suffixes=("_true", "_pred"))

        if len(df_merged) == 0:
            print("[ERREUR] Aucune correspondance trouvée entre les fichiers (vérifiez la colonne 'filename')")
            return None

        # On récupère les colonnes de labels
        # Note : assure-toi que ton true_labels.csv a une colonne 'label'
        y_true = df_merged["label"]
        y_pred = df_merged["prediction"]

        acc = accuracy_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred, average="weighted")
        report = classification_report(y_true, y_pred, output_dict=True)

        print(f"--- RÉSULTATS ---")
        print(f"Accuracy : {acc:.4f} | F1-Score : {f1:.4f}")
        
        return {
            "accuracy": acc,
            "f1_score": f1,
            "details": report
        }
    except Exception as e:
        print(f"[ERREUR] Échec de l'évaluation : {e}")
        return None

def save_results(team_name, metrics):
    """Sauvegarde les scores dans un fichier JSON pour le leaderboard."""
    os.makedirs(RESULTS_DIR, exist_ok=True)
    output_path = os.path.join(RESULTS_DIR, f"{team_name}.json")
    with open(output_path, "w") as f:
        json.dump(metrics, f, indent=4)
    print(f"[OK] Résultats sauvegardés pour : {team_name}")

if __name__ == "__main__":
    # 1. Gestion des arguments
    parser = argparse.ArgumentParser(description="Évaluation de soumission MRI")
    parser.add_argument("--submission", type=str, help="Chemin vers le fichier CSV du participant")
    args = parser.parse_args()

    # 2. Choix du fichier à évaluer
    target_file = args.submission

    if target_file and os.path.exists(target_file):
        # Extraire le nom de l'équipe du nom du fichier
        team_name = os.path.basename(target_file).replace(".csv", "")
        
        metrics = evaluate_submission(target_file)
        if metrics:
            save_results(team_name, metrics)
    else:
        print("[!] Erreur : Veuillez spécifier un fichier valide avec --submission <chemin>")