import os
import csv

# CONFIGURATION
TEST_DIR = "data/test"  # Chemin vers vos images de test
OUTPUT_FILE = "evaluation/true_labels.csv"

# Récupère le nom des dossiers (classes)
CLASS_NAMES = sorted([d for d in os.listdir(TEST_DIR) if os.path.isdir(os.path.join(TEST_DIR, d))])

def generate_truth_file():
    print(f"[INFO] Classes détectées : {CLASS_NAMES}")
    
    truth_data = []
    
    # Parcourir chaque dossier de classe
    for class_name in CLASS_NAMES:
        class_path = os.path.join(TEST_DIR, class_name)
        
        # Lister toutes les images dans ce dossier
        for img_name in os.listdir(class_path):
            # On stocke maintenant le nom de la classe (ex: "glioma") au lieu de l'index
            truth_data.append([img_name, class_name])

    # Tri par nom de fichier pour garantir une cohérence avec les soumissions
    truth_data.sort(key=lambda x: x[0])

    # Écriture du fichier CSV
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "label"])
        writer.writerows(truth_data)

    print(f"[OK] Fichier de vérité terrain généré : {OUTPUT_FILE}")
    print(f"Total images : {len(truth_data)}")

if __name__ == "__main__":
    generate_truth_file()