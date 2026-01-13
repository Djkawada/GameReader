# GameVox 🎮🗣️

**GameVox** (anciennement GameReader) est un lecteur d'écran intelligent pour Linux (**Hyprland/Wayland**) conçu pour les jeux vidéo.
Il capture le texte à l'écran (dialogues, sous-titres), le nettoie et le lit instantanément avec une voix naturelle.

## ✨ Fonctionnalités

*   **Voix Naturelle Locale** : Utilise l'IA **Piper** pour une synthèse vocale neuronale fluide sans aucun délai et sans connexion internet.
*   **Sélection de Zone (Slurp)** : Définissez précisément la zone de l'écran à lire (ex: la boîte de dialogue) pour éviter les lectures inutiles.
*   **Système de Profils** : Sauvegardez et chargez des zones spécifiques pour chaque jeu.
*   **Nettoyage Intelligent** : Filtre les caractères spéciaux de l'OCR tout en conservant les lettres et les chiffres.
*   **Contrôle à la Manette** : Activez/Désactivez la lecture à tout moment via un bouton de votre manette.

## 📋 Prérequis

Système : **Wayland** (testé sur Hyprland).

Paquets nécessaires :
```bash
sudo pacman -S tesseract tesseract-data-fra grim slurp paplay python
```
*   `tesseract` : Moteur OCR.
*   `grim` & `slurp` : Capture de zone.
*   `paplay` : Lecture audio (standard PulseAudio/PipeWire).

## 🚀 Installation

1.  **Cloner le dépôt** :
    ```bash
    git clone https://github.com/Djkawada/GameReader.git
    cd GameReader
    ```
    *(Note: Le nom du dépôt GitHub sera mis à jour prochainement)*

2.  **Environnement Python** :
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Installer Piper (TTS)** :
    Le moteur vocal n'est pas inclus (trop lourd). Pour l'installer automatiquement :
    ```bash
    mkdir -p piper_tts && cd piper_tts
    wget https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz
    tar -xvf piper_linux_x86_64.tar.gz
    wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fr/fr_FR/upmc/medium/fr_FR-upmc-medium.onnx
    wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fr/fr_FR/upmc/medium/fr_FR-upmc-medium.onnx.json
    cd ..
    ```

## 🎮 Configuration de la manette

1.  Identifiez votre bouton :
    ```bash
    sudo ./venv/bin/python find_button.py
    ```
2.  Notez le chemin `/dev/input/eventXX` et le code du bouton.
3.  Modifiez les constantes au début de `gamevox.py`.

## 🛠️ Utilisation

Lancez le script :
```bash
# Sudo est requis uniquement pour l'écoute de la manette
sudo ./venv/bin/python gamevox.py
```

### Menu de démarrage :
*   **Mode Auto** : Scanne la moitié inférieure de l'écran actif.
*   **Sélectionner un Profil** : Charge une zone déjà enregistrée.
*   **Créer un nouveau profil** : Demande un nom, puis vous permet de dessiner un rectangle à l'écran avec la souris.
*   **Supprimer un profil** : Efface un profil existant.

## ⌨️ Raccourcis
*   **Bouton Manette** : Play / Pause (vocalise l'état).
*   **Ctrl + C** : Quitter proprement.