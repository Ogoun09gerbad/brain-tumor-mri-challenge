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
    """
    Compare une soumission avec la vérité terrain en utilisant les noms de classes.
    """
    print(f"[INFO] Évaluation du fichier : {submission_file}")

    if not os.path.exists(TRUTH_FILE):
        print(f"[ERREUR] Vérité terrain introuvable : {TRUTH_FILE}")
        return None

    try:
        # Lecture des fichiers
        df_truth = pd.read_csv(TRUTH_FILE)
        df_pred = pd.read_csv(submission_file)

        # 1. Normalisation des en-têtes
        df_truth.columns = [c.strip().lower() for c in df_truth.columns]
        df_pred.columns = [c.strip().lower() for c in df_pred.columns]

        # 2. Vérification colonnes
        if 'filename' not in df_pred.columns:
            print("[ERREUR] La colonne 'filename' est manquante.")
            return None

        target_col = next((c for c in ['prediction', 'label'] if c in df_pred.columns), None)
        if not target_col:
            print("[ERREUR] Colonne de prédiction ('prediction' ou 'label') manquante.")
            return None

        # 3. Nettoyage des données (IMPORTANT pour les noms de classes)
        # On passe tout en minuscule et on enlève les espaces pour la comparaison
        for df in [df_truth, df_pred]:
            df['filename'] = df['filename'].astype(str).str.strip()
            # On applique la normalisation sur la colonne de label/prédiction
            col = 'label' if 'label' in df.columns else target_col
            df[col] = df[col].astype(str).str.strip().str.lower()

        # 4. Alignement (Merge)
        df_merged = pd.merge(df_truth, df_pred, on="filename", suffixes=("_true", "_pred"))

        print(f"[DEBUG] Match : {len(df_merged)} images trouvées sur {len(df_truth)} attendues.")

        if len(df_merged) == 0:
            print("[ERREUR] Aucun nom de fichier ne correspond.")
            return None

        # 5. Extraction des vecteurs
        y_true = df_merged["label_true"]
        y_pred = df_merged[f"{target_col}_pred"]

        # 6. Calcul des métriques
        acc = accuracy_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred, average="weighted")
        
        # Rapport détaillé
        report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)

        print(f"--- RÉSULTATS ---")
        print(f"Accuracy : {acc:.4f} | F1-Score : {f1:.4f}")
        
        return {
            "accuracy": acc,
            "f1_score": f1,
            "details": report
        }

    except Exception as e:
        print(f"[ERREUR SYSTEME] : {e}")
        return None

def save_results(team_name, metrics):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    output_path = os.path.join(RESULTS_DIR, f"{team_name}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)
    print(f"[OK] Résultats sauvegardés : {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Évaluation MRI Challenge")
    parser.add_argument("--submission", type=str, required=True, help="Chemin vers le CSV de l'élève")
    args = parser.parse_args()

    if os.path.exists(args.submission):
        team_name = os.path.basename(args.submission).lower().replace(".csv", "").replace(" ", "_")
        results = evaluate_submission(args.submission)
        if results:
            save_results(team_name, results)
    else:
        print(f"[!] Fichier introuvable : {args.submission}")