# Stock Management Tool

Ce programme en ligne de commande permet de gérer les stocks d'une entreprise en consolidant plusieurs fichiers CSV, en permettant la recherche de produits et en générant des rapports récapitulatifs. Il est conçu pour faciliter la gestion des stocks et la génération de résumés par catégorie.

## Fonctionnalités principales

- **Consolidation des fichiers CSV** : Importez plusieurs fichiers CSV situés dans un répertoire donné. Les données seront combinées en un seul tableau de bord centralisé.
- **Recherche de données** : Recherchez des informations par produit, catégorie ou prix.
- **Génération de rapports** : Générez des rapports récapitulatifs montrant la quantité totale et le prix moyen des produits par catégorie.
- **Mode interactif** :
  Accédez à un menu interactif pour naviguer facilement dans les options sans utiliser directement des arguments en ligne de    commande.

## Installation

1. Assurez-vous d'avoir **Python 3.x** installé sur votre système.
2. Clonez ou téléchargez ce dépôt.
3. Installez les dépendances requises (notamment `pandas`) via pip :

   ```bash
   pip install pandas

## Utilisation
# Mode ligne de commande
Utilisez argparse pour exécuter les actions directement depuis le terminal.

### Commandes disponibles :
- #### Consolidation des fichiers CSV :

   ```bash
   python main.py consolidate --directory <chemin_du_répertoire>

- #### Recherche de données :

   ```bash
   python main.py search --directory <chemin_du_répertoire> --column <nom_de_la_colonne> --value <valeur>

- #### Génération de rapports :

   ```bash
   python main.py summary --directory <chemin_du_répertoire> --output <nom_du_fichier>

- #### Mode interactif :

   ```bash
   python main.py interactive

## Mode interactif
Si vous préférez un mode guidé, lancez simplement :

   ```bash
   python main.py interactive
   ```

Un menu s'affiche, et vous pouvez naviguer entre les options :

   ```plaintext
   Welcome to the Stock Management Tool
   1. Consolidate CSV Files
   2. Search Data
   3. Generate Summary Report
   4. Exit

   Enter your choice:
   ```

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

## Aide et dépannage
Pour afficher l’aide sur les commandes disponibles, utilisez :

   ```bash
   python main.py --help
   ```
En cas de problème :

- Assurez-vous que le répertoire spécifié contient des fichiers CSV valides.
- Vérifiez que les colonnes ```name```, ```quantity```, ```price```, et ```category``` sont bien présentes dans les fichiers CSV.
- Consultez les messages d’erreur dans le terminal pour plus de détails. 

## Licence
Ce programme est distribué sous licence MIT

### Points mis à jour :
- Inclusion des nouvelles options `argparse`.
- Explication du mode interactif et de l'accès via `argparse`.
- Clarification des commandes pour chaque fonctionnalité.
- Conservation des instructions claires pour le dépannage et les exemples d'utilisation.
