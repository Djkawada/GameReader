# GameReader 🎮🗣️

Un lecteur d'écran automatique pour Linux (Hyprland/Wayland) conçu pour les jeux vidéo.
Il capture automatiquement la moitié inférieure de l'écran, détecte le texte (dialogues, sous-titres) et le lit à voix haute.

## Prérequis

Ce logiciel est conçu pour fonctionner sous **Linux** avec l'environnement graphique **Hyprland** (Wayland).

Il nécessite les paquets systèmes suivants :
*   `python`
*   `tesseract` (et les données de langue, ex: `tesseract-data-fra`)
*   `grim` (capture d'écran Wayland)
*   `espeak-ng` (synthèse vocale)

Sous Arch Linux / Omarchy :
```bash
sudo pacman -S tesseract tesseract-data-fra espeak-ng grim python
```

## Installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/VOTRE_NOM_UTILISATEUR/GameReader.git
   cd GameReader
   ```

2. Créez un environnement virtuel et installez les dépendances :
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Utilisation

Lancez simplement le script :

```bash
source venv/bin/activate
python game_reader.py
```

Le logiciel va :
1. Détecter votre écran actif.
2. Capturer la moitié inférieure toutes les 2 secondes.
3. Lire tout nouveau texte détecté.

Appuyez sur `Ctrl+C` dans le terminal pour arrêter.

## Configuration

Vous pouvez modifier les variables au début du fichier `game_reader.py` pour ajuster :
*   `CHECK_INTERVAL` : La fréquence de lecture.
*   `LANG` : La langue à détecter (par défaut 'fra').
