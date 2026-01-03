import time
import subprocess
import json
import sys
from PIL import Image
import pytesseract
import io

# Configuration
CHECK_INTERVAL = 2  # Temps en secondes entre chaque lecture
MIN_TEXT_LENGTH = 5 # Ignorer les textes trop courts
LANG = 'fra'        # Langue pour l'OCR

def get_active_monitor_geometry():
    """Récupère la géométrie de l'écran actif via hyprctl."""
    try:
        # Récupérer les infos des moniteurs au format JSON
        result = subprocess.run(['hyprctl', 'monitors', '-j'], capture_output=True, text=True)
        monitors = json.loads(result.stdout)
        
        # Trouver le moniteur focalisé
        for monitor in monitors:
            if monitor['focused']:
                return {
                    'x': monitor['x'],
                    'y': monitor['y'],
                    'width': monitor['width'],
                    'height': monitor['height'],
                    'scale': monitor['scale']
                }
        # Fallback si aucun focus trouvé (prendre le premier)
        if monitors:
             return {
                    'x': monitors[0]['x'],
                    'y': monitors[0]['y'],
                    'width': monitors[0]['width'],
                    'height': monitors[0]['height'],
                    'scale': monitors[0]['scale']
                }
    except Exception as e:
        print(f"Erreur lors de la récupération de la géométrie écran: {e}")
        return None

def capture_bottom_half(geometry):
    """Capture la moitié inférieure de l'écran."""
    # Calcul de la zone (Moitié inférieure)
    # X, Y, Width, Height
    # On commence à Y + Height/2
    
    x = geometry['x']
    y = geometry['y'] + (geometry['height'] // 2)
    w = geometry['width']
    h = geometry['height'] // 2
    
    region = f"{x},{y} {w}x{h}"
    
    try:
        # Utilisation de grim pour capturer une région spécifique
        # grim -g "x,y wxH" -
        cmd = ['grim', '-g', region, '-t', 'png', '-']
        result = subprocess.run(cmd, capture_output=True)
        
        if result.returncode != 0:
            print("Erreur grim:", result.stderr)
            return None
            
        return Image.open(io.BytesIO(result.stdout))
    except Exception as e:
        print(f"Erreur capture: {e}")
        return None

def speak(text):
    """Prononce le texte via espeak."""
    try:
        # On utilise espeak-ng. 
        # -v fr: voix française
        # -s 150: vitesse un peu plus rapide (défaut ~175, 150 est plus calme)
        subprocess.Popen(['espeak-ng', '-v', 'fr', '-s', '150', text])
    except Exception as e:
        print(f"Erreur audio: {e}")

def clean_text(text):
    """Nettoie le texte (enlève les sauts de ligne inutiles)."""
    # Remplace les retours à la ligne par des espaces et nettoie les espaces multiples
    return " ".join(text.split())

def main():
    print("=== GameReader Démarré ===")
    print("Lecture de la moitié inférieure de l'écran...")
    print("Appuyez sur Ctrl+C pour arrêter.")
    
    last_text = ""
    
    try:
        while True:
            geo = get_active_monitor_geometry()
            if not geo:
                print("Impossible de détecter l'écran. Nouvelle tentative...")
                time.sleep(2)
                continue
                
            image = capture_bottom_half(geo)
            
            if image:
                # Pré-traitement optionnel (conversion niveau de gris pour meilleur OCR)
                image = image.convert('L') 
                
                # OCR
                text = pytesseract.image_to_string(image, lang=LANG)
                cleaned = clean_text(text)
                
                if len(cleaned) > MIN_TEXT_LENGTH:
                    # On compare avec le dernier texte lu pour éviter la répétition
                    # On utilise un ratio de similarité simple ou juste l'égalité exacte
                    if cleaned != last_text:
                        print(f"Lu : {cleaned}")
                        speak(cleaned)
                        last_text = cleaned
            
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        print("\nArrêt du programme.")

if __name__ == "__main__":
    main()
