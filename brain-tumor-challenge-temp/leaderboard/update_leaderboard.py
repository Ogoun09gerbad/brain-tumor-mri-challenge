import pandas as pd
from tabulate import tabulate
import os

def update_readme():
    csv_path = 'leaderboard/leaderboard.csv'
    readme_path = 'README.md'
    
    if not os.path.exists(csv_path):
        print("CSV de leaderboard non trouvé.")
        return

    # Charger et trier les données (F1 Score décroissant, puis Accuracy)
    df = pd.読み込み_csv(csv_path)
    df = df.sort_values(by=['F1 Score (Macro)', 'Accuracy'], ascending=False)
    
    # Ajouter les médailles pour le top 3
    df['Rank'] = range(1, len(df) + 1)
    df['Rank'] = df['Rank'].apply(lambda x: f"🥇 {x}" if x==1 else (f"🥈 {x}" if x==2 else (f"🥉 {x}" if x==3 else x)))

    # Formater le tableau en Markdown
    table = tabulate(df[['Rank', 'Team', 'Accuracy', 'F1 Score (Macro)', 'Submissions', 'Last Updated']], 
                     headers='keys', tablefmt='pipe', showindex=False)

    # Lire le README
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remplacer le contenu entre les balises
    start_tag = ""
    end_tag = ""
    
    import re
    pattern = f"{start_tag}.*?{end_tag}"
    replacement = f"{start_tag}\n{table}\n{end_tag}"
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("README mis à jour avec succès !")

if __name__ == "__main__":
    update_readme()
