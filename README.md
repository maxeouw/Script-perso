# Stock Management Tool

Ce programme en ligne de commande permet de gérer les stocks d'une entreprise en consolidant plusieurs fichiers CSV, en permettant la recherche de produits et en générant des rapports récapitulatifs. Il est conçu pour faciliter la gestion des stocks et la génération de résumés par catégorie.

## Fonctionnalités principales

- **Consolidation des fichiers CSV** : Importez plusieurs fichiers CSV situés dans un répertoire donné. Les données seront combinées en un seul tableau de bord centralisé.
- **Recherche de données** : Recherchez des informations par produit, catégorie ou prix.
- **Génération de rapports** : Générez des rapports récapitulatifs montrant la quantité totale et le prix moyen des produits par catégorie.

## Installation

1. Assurez-vous d'avoir **Python 3.x** installé sur votre système.
2. Clonez ou téléchargez ce dépôt.
3. Installez les dépendances requises (notamment `pandas`) via pip :

   ```bash
   pip install pandas

## Utilisation

1. Lancez le programme:

   ```bash
   python main.py

2. Choisissez une option en entrant le numéro correspondant :

- 1 : Consolider les fichiers CSV.
- 2 : Rechercher des données (par produit, catégorie, etc.).
- 3 : Générer un rapport récapitulatif.
- 4 : Quitter le programme.

3. Entrées requises :

- Lors de la consolidation des fichiers CSV, fournissez le chemin du répertoire contenant les fichiers CSV.
- Lors de la recherche, entrez le nom de la colonne et la valeur à rechercher.
- Lors de la génération du rapport, vous pouvez choisir un fichier de sortie ou accepter le nom par défaut.

## Exemple de fonctionnement
  ```plaintext
    Welcome to the Stock Management Tool
    1. Consolidate CSV Files
    2. Search Data
    3. Generate Summary Report
    4. Exit
    
    Enter your choice: 1
    Enter the directory containing CSV files: /path/to/csv/files
    CSV files consolidated successfully.
    
    Enter your choice: 3
    Enter the output file name for the summary report (or press Enter for default): report.csv
    Summary report saved to report.csv
    
    Enter your choice: 4
    Exiting the program. Goodbye!
  ```

## Aide

En cas de problème avec le programme, vérifiez que :

- Le répertoire contient des fichiers CSV valides.
- Les fichiers CSV incluent les colonnes suivantes : name, quantity, price, et category.
  
Si le problème persiste, consultez les messages d'erreur affichés dans le terminal pour plus de détails.  
