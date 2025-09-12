# ==== IMPORTS ====
import json
import requests
import time
import os
import csv
from datetime import datetime
import threading
import shutil
import sys

# ==== COLORES ====
RESET = "\033[0m"
GREEN = "\033[32m"
RED = "\033[31m"
WHITE = "\033[97m"
BOLD = "\033[1m"
BLUE = "\033[34m"
CYAN = "\033[36m"
PURPLE = "\033[35m"
YELLOW = "\033[33m"
LIGHTGREEN = "\033[92m"
GOLD = "\033[93m"

# ==== BANNER ====
BANNER = f"""
{WHITE}
{GREEN} █████          ███████    █████   ████    ███████    ██████   ██████    ███████    ███████████ █████ █████   █████{RESET}
{GREEN}░░███         ███░░░░░███ ░░███   ███░   ███░░░░░███ ░░██████ ██████   ███░░░░░███ ░█░░░███░░░█░░███ ░░███   ░░███ {RESET}
{WHITE} ░███        ███     ░░███ ░███  ███    ███     ░░███ ░███░█████░███  ███     ░░███░   ░███  ░  ░███  ░███    ░███ {RESET}
{WHITE} ░███       ░███      ░███ ░███████    ░███      ░███ ░███░░███ ░███ ░███      ░███    ░███     ░███  ░███    ░███ {RESET}
{WHITE} ░███       ░███      ░███ ░███░░███   ░███      ░███ ░███ ░░░  ░███ ░███      ░███    ░███     ░███  ░░███   ███  {RESET}
{RED} ░███      █░░███     ███  ░███ ░░███  ░░███     ███  ░███      ░███ ░░███     ███     ░███     ░███   ░░░█████░   {RESET}
{RED} ███████████ ░░░███████░   █████ ░░████ ░░░███████░   █████     █████ ░░░███████░      █████    █████    ░░███     {RESET}
{RED}░░░░░░░░░░░    ░░░░░░░    ░░░░░   ░░░░    ░░░░░░░    ░░░░░     ░░░░░    ░░░░░░░       ░░░░░    ░░░░░      ░░░ {WHITE}By:{GOLD}SrWyatt{RESET}
"""

# ==== TAGLINE ====
TAGLINE = f"{RESET}{BOLD}- Snapshot {GREEN}1.4.1{RESET}{WHITE} ({GOLD}LÉTOV{RESET})-\n" + f"+" + " "f"{WHITE}-"*60 + f"{LIGHTGREEN}{RESET}{BOLD}+ \n\n\n"

# ==== CARGA DE ARCHIVO SOCIAL ====
with open("social.json","r") as f:
    social_sites = json.load(f)

# ==== CLEAR SCREEN ====
def clear_screen():
    os.system('clear' if os.name=='posix' else 'cls')

# ==== LOADER ====
class Loader:
    def __init__(self):
        self.running = False
        self.thread = None
        self.train = [
            "  _____   _____   _____   _____   _____  ",
            "-|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|-",
            " `-0-0-\"'`-0-0-\"'`-0-0-\"'`-0-0-\"'`-0-0-' "
        ]
        self.pos = 10          
        self.min_pos = 0      
        self.max_pos = 80      
        self.width = shutil.get_terminal_size((70, 20)).columns
        self.progress = 0
        self.elapsed = 0

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.animate)
        self.thread.daemon = True
        self.thread.start()

    def update_progress(self, progress, elapsed):
        self.progress = progress
        self.elapsed = elapsed

    def animate(self):
        while self.running:
            clear_screen()
            print(BANNER)
            print(TAGLINE)
            for line in self.train:
                display_line = " " * self.pos + line
                print(display_line[:self.width])
            print(f"\n{GOLD}Cargando sitios ({self.progress}%) - ({round(self.elapsed,1)}s){RESET}")
            self.pos += 2
            if self.pos > self.max_pos:
                self.pos = self.min_pos
            time.sleep(0.1)

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        clear_screen()
        print(BANNER)
        print(TAGLINE)

# ==== CHECK PROFILE ====
def check_profile(url, config=None):
    start = time.time()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        r = requests.get(url, timeout=5, allow_redirects=True, headers=headers)
        elapsed = round(time.time() - start, 2)

        # Si hay configuración específica del sitio, usarla para detección precisa
        if config and "errorType" in config:
            error_type = config["errorType"]

            if error_type == "status_code":
                error_codes = config.get("errorCode", [404])
                if isinstance(error_codes, int):
                    error_codes = [error_codes]
                if r.status_code in error_codes:
                    return 5, elapsed  # Baja probabilidad: no existe
                else:
                    return 95, elapsed  # Alta probabilidad: existe

            elif error_type == "message":
                error_msgs = config.get("errorMsg", [])
                if isinstance(error_msgs, str):
                    error_msgs = [error_msgs]
                if any(msg in r.text for msg in error_msgs):
                    return 5, elapsed  # No existe
                else:
                    return 95, elapsed  # Existe

            elif error_type == "response_url":
                error_url = config.get("errorUrl", "")
                if r.url == error_url.replace("{user}", url.split('/')[-1]):  # Reemplaza {user} si aplica
                    return 5, elapsed  # No existe
                else:
                    return 95, elapsed  # Existe

        # Lógica fallback (vieja) si no hay config o errorType no manejado
        if r.status_code == 200:
            return 95, elapsed
        elif r.status_code == 404:
            return 5, elapsed
        elif r.history:
            return 50, elapsed
        else:
            return 0, elapsed
    except requests.exceptions.RequestException:
        return 0, round(time.time() - start, 2)

# ==== DISPLAY RESULTS (MODIFICADO PARA TU ESTÉTICA) ====
def display_results(results):
    clear_screen()
    print(BANNER)
    print(TAGLINE)
    print("─"*60)
    print(f"{RESET}{BOLD}[ {GREEN}+{RESET} ] {BOLD} = Alta probabilidad | {RESET}{BOLD}[ {RED}-{RESET} ] {BOLD} = Baja probabilidad")
    print("─"*60)
    print(f"{RESET}{BOLD}Probabilidad ({GREEN}E{RESET}) | {BOLD}Tiempo ({GOLD}T{RESET}) | {BOLD}Progreso ({CYAN}P{RESET})")
    print("─"*60)
    posibles = 0
    baja = 0
    total_time = 0
    for site, data in sorted(results.items(), key=lambda x: x[1]["prob"], reverse=True):
        prob = data["prob"]
        t = data["time"]
        url = data["url"]
        total_time += t
        if prob >= 90:
            color = GREEN
            sign = "+"
            posibles += 1
        else:
            color = RED
            sign = "-"
            baja += 1
        # Progreso (P) se calcula como el porcentaje de probabilidad para la estética
        p = prob
        print(f"[{color}{sign}{RESET}] {BOLD}{site}{RESET}: ({GREEN}E{RESET}){BOLD}{prob}%{RESET} - ({GOLD}T{RESET}){BOLD}{t}s{RESET} - ({CYAN}P{RESET}){BOLD}{p}%{RESET} → {url}")
    promedio = round(total_time/len(results),2) if results else 0
    print("─"*60)
    print(f"{BOLD}{GREEN}Sitios posibles:{RESET}{posibles}")
    print(f"{BOLD}{RED}Sitios baja probabilidad: {RESET}{baja}")
    print(f"{BOLD}{WHITE}Tiempo promedio carga: {RESET}{promedio}s")
    print("─"*60+"\n")
    choice = input("Guardar en CSV? (s/n): ").lower()
    if choice == 's':
        save_to_csv(results)
    input("Presiona ENTER para volver...")

# ==== SAVE TO CSV ====
def save_to_csv(results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results_{timestamp}.csv"
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Sitio", "Probabilidad", "Tiempo", "URL"])
        for site, data in results.items():
            writer.writerow([site, data["prob"], data["time"], data["url"]])
    print(f"Guardado en {filename}")

# ==== BÚSQUEDA BÁSICA ====
def basic_search():
    while True:
        clear_screen()
        print(BANNER)
        print(TAGLINE)
        username = input("Usuario (00 para cancelar, 666 para salir): ")
        if username == '00':
            break
        if username == '666':
            sys.exit(0)
        results = {}
        loader = Loader()
        loader.start()
        all_sites = []
        for cat, sites in social_sites.items():
            for site, config in sites.items():
                all_sites.append((site, config))
        total = len(all_sites)
        start_time = time.time()
        for idx, (site, config) in enumerate(all_sites, start=1):
            url = config["url"].replace("{user}", username)
            prob, t = check_profile(url, config)
            results[site] = {"prob": prob, "time": t, "url": url}
            progress = int((idx / total) * 100)
            elapsed = time.time() - start_time
            loader.update_progress(progress, elapsed)
        loader.stop()
        display_results(results)

# ==== BÚSQUEDA AVANZADA ====
def advanced_search():
    while True:
        clear_screen()
        print(BANNER)
        print(TAGLINE)
        print("+-----------------------+")
        print(f"{BOLD}{GOLD}BÚSQUEDA AVANZADA{RESET}")
        print("+-----------------------+")
        print(f"{BOLD}{WHITE}1. Ver categorías")
        print(f"{BOLD}{WHITE}2. Buscar en categoría")
        print("+-----------------------+")
        print(f"{BOLD}{LIGHTGREEN}00. Volver al menú principal{RESET}")
        print(f"{BOLD}{RED}666. Salir de la interfaz{RESET}")
        print("+-----------------------+")
        choice = input("[/]> : ")
        if choice == '00':
            break
        elif choice == '666':
            sys.exit(0)
        elif choice == '1':
            clear_screen()
            print(BANNER)
            print(TAGLINE)
            for cat, sites in social_sites.items():
                print(f"{BOLD}{GOLD}{cat}{RESET}:")
                for site in sites:
                    print(f" - {site}")
            input("\nPresiona ENTER para volver...")
        elif choice == '2':
            clear_screen()
            print(BANNER)
            print(TAGLINE)
            categories = list(social_sites.keys())
            for idx, cat in enumerate(categories, start=1):
                print(f"{idx}. {cat}")
            cat_choice = input("Número de categoría (00=volver, 666=salir): ")
            if cat_choice == '00':
                continue
            elif cat_choice == '666':
                sys.exit(0)
            try:
                cat_choice = int(cat_choice) - 1
                cat = categories[cat_choice]
                username = input("Usuario (00 para cancelar, 666 para salir): ")
                if username == '00':
                    continue
                if username == '666':
                    sys.exit(0)
                results = {}
                loader = Loader()
                loader.start()
                sites_dict = social_sites[cat]
                total = len(sites_dict)
                start_time = time.time()
                for idx, (site, config) in enumerate(sites_dict.items(), start=1):
                    url = config["url"].replace("{user}", username)
                    prob, t = check_profile(url, config)
                    results[site] = {"prob": prob, "time": t, "url": url}
                    progress = int((idx / total) * 100)
                    elapsed = time.time() - start_time
                    loader.update_progress(progress, elapsed)
                loader.stop()
                display_results(results)
            except:
                print("Selección inválida.")
        else:
            print("Opción inválida.")

# ==== BÚSQUEDA PERSONALIZADA ====
def custom_search():
    clear_screen()
    print(BANNER)
    print(TAGLINE)
    try:
        with open("custom.json", "r") as f:
            custom_sites = json.load(f)
    except:
        print("No se pudo cargar custom.json")
        return
    username = input("Usuario (00 para cancelar, 666 para salir): ")
    if username == '00':
        return
    if username == '666':
        sys.exit(0)
    results = {}
    loader = Loader()
    loader.start()
    all_custom = []
    for cat, sites in custom_sites.items():
        for site, config in sites.items():
            all_custom.append((site, config))
    total = len(all_custom)
    start_time = time.time()
    for idx, (site, config) in enumerate(all_custom, start=1):
        url = config["url"].replace("{user}", username)
        prob, t = check_profile(url, config)
        results[site] = {"prob": prob, "time": t, "url": url}
        progress = int((idx / total) * 100)
        elapsed = time.time() - start_time
        loader.update_progress(progress, elapsed)
    loader.stop()
    display_results(results)

# ==== MAIN MENU ====
def main_menu():
    while True:
        clear_screen()
        print(BANNER)
        print(TAGLINE)
        print("+-----------------------+")
        print(f"{BOLD}{GOLD}MENÚ PRINCIPAL{RESET}")
        print("+-----------------------+")
        print(f"{BOLD}{WHITE}1. Búsqueda Básica")
        print(f"{BOLD}{WHITE}2. Búsqueda Avanzada")
        print(f"{BOLD}{WHITE}3. Búsqueda Personalizada")
        print("+-----------------------+")
        print(f"{BOLD}{RED}666. Salir de la interfaz{RESET}")
        print("+-----------------------+")
        choice = input("[/]> : ")
        if choice == '1':
            basic_search()
        elif choice == '2':
            advanced_search()
        elif choice == '3':
            custom_search()
        elif choice == '666':
            sys.exit(0)
        else:
            print("Opción inválida.")

# ==== EJECUCIÓN ====
if __name__ == "__main__":
    main_menu()
