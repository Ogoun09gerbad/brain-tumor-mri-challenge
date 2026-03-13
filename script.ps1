# Chercher le premier fichier CSV dans submissions
$subFile = Get-ChildItem "submissions\*.csv" | Select-Object -First 1

# Vérifier qu'un fichier existe
if ($null -eq $subFile) {
    Write-Host "Aucun fichier CSV trouve dans le dossier submissions"
    exit 1
}

Write-Host "Evaluation de : $($subFile.FullName)"

# Lancer l'évaluation
python evaluation\evaluate.py --submission $subFile.FullName