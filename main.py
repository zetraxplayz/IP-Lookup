import tkinter as tk
from tkinter import messagebox
import requests
import os
import time

try:
    from colorama import Fore, Style, init #Colorama bruges til at farve tekst i CMD
    init(autoreset=True)
except ImportError:
    Fore = Style = type('', (), {'RESET_ALL': '', 'CYAN': '', 'YELLOW': '', 'GREEN': '', 'MAGENTA': ''})() # Fore er brugt til at farve teksten i CMD, men gør det ikke hvis Colorama ikke er ikke-eksisterede

def clear():
    os.system("cls" if os.name == "nt" else "clear") #os.systeem Rydder CMD'EN for output

def startup_screen():
    clear()
    banner = f"""
{Fore.CYAN}
███████╗███████╗████████╗██████╗  █████╗ ██╗  ██╗
██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██║ ██╔╝
███████╗█████╗     ██║   ██████╔╝███████║█████╔╝ 
╚════██║██╔══╝     ██║   ██║   ██╔═══╝ ██╔══██║██╔═██╗ 
███████║███████╗   ██║   ██║     ██║  ██║██║  ██╗
╚══════╝╚══════╝   ╚═╝   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝
{Style.RESET_ALL}
            {Fore.YELLOW}v1.0 af mit program{Style.RESET_ALL}
    {Fore.GREEN}Kodet af din lokale bot{Style.RESET_ALL}
    """
    for line in banner.splitlines():
        print(line)
        time.sleep(0.02)
    print(f"""
{Fore.MAGENTA}Åbner program...{Style.RESET_ALL}
""")

# API Delen
def lookup_ip(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    try:
        response = requests.get(url, timeout=5) # Timeout på 5 sekunder for at undgå lange ventetider
        if response.status_code == 200: #
            data = response.json()
            if data.get("status") == "success":
                # Oversætter til Dansk
                danish_data = {
                    "IP-adresse": data.get("query"),
                    "Land": data.get("country"),
                    "Region": data.get("regionName"),
                    "By": data.get("city"),
                    "Postnummer": data.get("zip"),
                    "Latitude": data.get("lat"),
                    "Longitude": data.get("lon"),
                    "Tidszone": data.get("timezone"),
                    "Udbydere": data.get("isp"),
                    "Firma": data.get("org"),
                    "AS": data.get("as")
                }
                info = "\n".join([f"{key}: {value}" for key, value in danish_data.items()]) # Formaterer resultatet til en læsbar streng
                messagebox.showinfo("IP Information", info) # Viser en beskedboks med IP informationen
                return danish_data # Returnerer den danske data
            else:
                raise ValueError(data.get("message", "Ukendt fejl")) # Hvis der er fejl i API'en, så vises en fejlbesked
        else:
            raise Exception("Kunne ikke hente data fra API.") # Fejl beskeden, hvis der er fejl med API'en
    except Exception as e:
        raise e # Rais e betyder at fejlen bliver sendt videre til den der kalder funktionen, så den kan håndteres der

def on_lookup():
    ip = ip_entry.get() # Henter IP-adressen fra inputfeltet
    try:
        result = lookup_ip(ip) # Kalder funktionen lookup_ip med den indtastede IP-adresse
        info = "\n".join([f"{key}: {value}" for key, value in result.items()]) # Formaterer resultatet til en læsbar streng
        result_label.config(text=info)
    except Exception as e:
        messagebox.showerror("Fejl", f"Der opstod en fejl:\n{e}") #Sender en besked med en fejl

# UI DELEN

root = tk.Tk()
root.title("IP-opslag")
root.geometry('600x400')

ip_entry = tk.Entry(root)
ip_entry.pack(pady=10)

lookup_button = tk.Button(root, text="Slå IP-adresse op", command=on_lookup) # Knapper, Knapper og flere Knapper
lookup_button.pack(pady=5) # Knappens størrelse

result_label = tk.Label(root, text="", justify="left", anchor="w") # Label til at vise resultatet
result_label.pack(pady=10, fill="both", expand=True) # Labelens størrelse

# Startup screen
if __name__ == "__main__":
    startup_screen()
    root.mainloop()
