#!/bin/bash

# ==============================================================================
# Script d'évaluation locale pour le Brain Tumor MRI Challenge
# Usage: ./run_local_eval.sh [chemin_du_fichier_csv]
# ==============================================================================

# 1. Vérification de l'argument
if [ -z "$1" ]; then
    echo "❌ Erreur : Veuillez fournir le chemin vers un fichier de soumission."
    echo "Usage : ./run_local_eval.sh submissions/equipe_test.csv"
    exit 1
fi

SUB_FILE=$1

# 2. Vérification de l'existence du fichier
if [ ! -f "$SUB_FILE" ]; then
    echo "❌ Erreur : Le fichier '$SUB_FILE' est introuvable."
    exit 1
fi

echo "🚀 Démarrage de l'évaluation locale..."
echo "--------------------------------------"

# 3. Préparation (Simulation du job 'Run Evaluation')
echo "[1/2] Évaluation du modèle..."
mkdir -p submissions
mkdir -p evaluation/results

# On copie le fichier dans le dossier attendu par le script si nécessaire
# (ou on l'utilise directement)
cp "$SUB_FILE" "submissions/$(basename "$SUB_FILE")"

# Exécution du script d'évaluation
python evaluation/evaluate.py --submission "submissions/$(basename "$SUB_FILE")"

# Vérification du succès de l'évaluation
if [ $? -eq 0 ]; then
    echo "✅ Évaluation réussie."
else
    echo "❌ L'évaluation a échoué. Vérifiez les logs ci-dessus."
    exit 1
fi

echo "--------------------------------------"

# 4. Mise à jour du classement (Simulation du job 'Update Leaderboard')
echo "[2/2] Mise à jour du leaderboard..."
python leaderboard/update_leaderboard.py

if [ $? -eq 0 ]; then
    echo "✅ Leaderboard mis à jour avec succès (leaderboard/leaderboard.csv)."
else
    echo "❌ Échec de la mise à jour du leaderboard."
    exit 1
fi

echo "--------------------------------------"
echo "🎉 Terminé ! Vous pouvez maintenant voir le classement et pusher les changements."