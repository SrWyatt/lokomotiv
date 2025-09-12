
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
def check_profile(url):
    start = time.time()
    try:
        r = requests.get(url, timeout=5, allow_redirects=True)
        elapsed = round(time.time()-start,2)
        if r.status_code==200: prob=95
        elif r.status_code==404: prob=5
        else: prob=50
    except:
        elapsed = round(time.time()-start,2)
        prob=0
    return prob,elapsed

# ==== DISPLAY RESULTS ====
def display_results(results):
    print("─"*60)
    print(f"{RESET}{BOLD}[ {GREEN}+{RESET} ] {BOLD} = Alta probabilidad | {RESET}{BOLD}[ {RED}-{RESET} ] {BOLD} = Baja probabilidad")
    print("─"*60)
    print(f"{RESET}{BOLD}Probabilidad ({GREEN}E{RESET}) | {BOLD}Tiempo ({GOLD}T{RESET}) | {BOLD}Progreso ({CYAN}P{RESET})")
    print("─"*60)

    posibles,baja,total_time = 0,0,0
    sitios_probables = []

    for idx,(site,data) in enumerate(results.items(),start=1):
        prob,t,url = data['prob'],data['time'],data['url']
        p = round((idx/len(results))*100)
        total_time+=t
        sign = '+' if prob>50 else '-'
        color = GREEN if prob>50 else RED
        if prob>50:
            posibles+=1
            sitios_probables.append((site, url))
        else:
            baja+=1
        print(f"[{color}{sign}{RESET}] {BOLD}{site}{RESET}: ({GREEN}E{RESET}){BOLD}{prob}%{RESET} - ({GOLD}T{RESET}){BOLD}{t}s{RESET} - ({CYAN}P{RESET}){BOLD}{p}%{RESET} → {url}")

    promedio = round(total_time/len(results),2) if results else 0
    print("─"*60)
    print(f"{BOLD}{GREEN}Sitios posibles:{RESET}{posibles}")
    print(f"{BOLD}{RED}Sitios baja probabilidad: {RESET}{baja}")
    print(f"{BOLD}{WHITE}Tiempo promedio carga: {RESET}{promedio}s")
    print("─"*60+"\n")

    if sitios_probables:
        print(f"{BOLD}Sitios con alta probabilidad (>50%):{RESET}")
        for s,u in sitios_probables:
            print(f" - {s}: {u}")
        print("─"*60+"\n")

    save_csv = input("¿Guardar resultados en CSV? (s/n): ").lower()
    if save_csv=='s':
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.csv")
        with open(filename,'w',newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Sitio","Probabilidad","Tiempo(s)","URL"])
            for site,data in results.items():
                writer.writerow([site,data['prob'],data['time'],data['url']])
        print(f"{BOLD}Resultados guardados como: {GREEN}{filename}{RESET}\n")
        input("Presiona ENTER para continuar...")

# ==== BÚSQUEDA BÁSICA ====
def basic_search():
    clear_screen()
    print(BANNER)
    print(TAGLINE)

    username = input("Usuario (00 para cancelar, 666 para salir): ")
    if username=='00': return
    if username=='666': sys.exit(0)

    basic_sites = {k:v for k,v in social_sites.get("ENTRETENIMIENTO",{}).items() if k in ["Facebook","Instagram","Twitter","YouTube","GitHub"]}
    results={}

    loader = Loader()
    loader.start()

    total = len(basic_sites)
    start_time = time.time()
    for idx,(site,template) in enumerate(basic_sites.items(),start=1):
        url = template.replace("{user}",username)
        prob,t = check_profile(url)
        results[site] = {"prob":prob,"time":t,"url":url}
        progress = int((idx/total)*100)
        elapsed = time.time()-start_time
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
        print(f"{BOLD}{GOLD}MENÚ DE BÚSQUEDA{RESET}")
        print("+-----------------------+") 
        print(f"{WHITE}{BOLD}1. Búsqueda en bruto (100 sitios a la vez)")
        print(f"{WHITE}{BOLD}2. Buscar por categoría")
        print(f"{WHITE}{BOLD}3. Ver categorías")
        print("+-----------------------+")
        print(f"{LIGHTGREEN}{LIGHTGREEN}00. Volver")
        print(f"{BOLD}{RED}666. Salir de la interfaz{RESET}")
        print("+-----------------------+")
        choice=input("[/]> : ")
        if choice=='00': return
        elif choice=='666': sys.exit(0)
        elif choice=='1':
            username=input("Usuario (00 para cancelar, 666 para salir): ")
            if username=='00': continue
            if username=='666': sys.exit(0)
            results={}
            loader = Loader()
            loader.start()
            all_sites = [(cat,site,template) for cat,sites in social_sites.items() for site,template in sites.items()]
            total = len(all_sites)
            start_time = time.time()
            for idx,(cat,site,template) in enumerate(all_sites,start=1):
                url=template.replace("{user}",username)
                prob,t=check_profile(url)
                results[site]={"prob":prob,"time":t,"url":url}
                progress=int((idx/total)*100)
                elapsed=time.time()-start_time
                loader.update_progress(progress, elapsed)
            loader.stop()
            display_results(results)
        elif choice=='2':
            clear_screen()
            print(BANNER)
            print(TAGLINE)
            categories=list(social_sites.keys())
            for idx,cat in enumerate(categories,start=1): print(f"{idx}. {cat}")
            cat_choice=input("Número de categoría (00=volver, 666=salir): ")
            if cat_choice=='00': continue
            elif cat_choice=='666': sys.exit(0)
            try:
                cat_choice=int(cat_choice)-1
                cat=categories[cat_choice]
                username=input("Usuario (00 para cancelar, 666 para salir): ")
                if username=='00': continue
                if username=='666': sys.exit(0)
                results={}
                loader = Loader()
                loader.start()
                sites_list = list(social_sites[cat].items())
                total = len(sites_list)
                start_time = time.time()
                for idx,(site,template) in enumerate(sites_list,start=1):
                    url=template.replace("{user}",username)
                    prob,t=check_profile(url)
                    results[site]={"prob":prob,"time":t,"url":url}
                    progress=int((idx/total)*100)
                    elapsed=time.time()-start_time
                    loader.update_progress(progress, elapsed)
                loader.stop()
                display_results(results)
            except: 
                print("Selección inválida.")
        elif choice=='3':
            clear_screen()
            print(BANNER)
            print(TAGLINE)
            for cat,sites in social_sites.items():
                print(f"{BOLD}{GOLD}{cat}{RESET}:")
                for site in sites: print(f" - {site}")
            input("\nPresiona ENTER para volver...")
        else: print("Opción inválida.")

# ==== BÚSQUEDA PERSONALIZADA ====
def custom_search():
    clear_screen()
    print(BANNER)
    print(TAGLINE)
    try:
        with open("custom.json","r") as f: custom_sites=json.load(f)
    except: 
        print("No se pudo cargar custom.json"); return
    username=input("Usuario (00 para cancelar, 666 para salir): ")
    if username=='00': return
    if username=='666': sys.exit(0)
    results={}
    loader = Loader()
    loader.start()
    total = len(custom_sites)
    start_time = time.time()
    for idx,(site,template) in enumerate(custom_sites.items(),start=1):
        url=template.replace("{user}",username)
        prob,t=check_profile(url)
        results[site]={"prob":prob,"time":t,"url":url}
        progress=int((idx/total)*100)
        elapsed=time.time()-start_time
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
        choice=input("[/]> : ")
        if choice=='1': basic_search()
        elif choice=='2': advanced_search()
        elif choice=='3': custom_search()
        elif choice=='666': sys.exit(0)
        else: print("Opción inválida.")

# ==== EJECUCIÓN ====
if __name__=="__main__":
    main_menu()
