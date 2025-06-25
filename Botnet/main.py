#!/usr/bin/env python3
"""
Network Testing Tool - Main Program
Super misto interface: ASCII rosu, text gri, meniu ultra aliniat si modern
"""

import argparse
import sys
import os
from colorama import init, Fore, Style, Back
import json
import time
import getpass
from pathlib import Path
from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
import random

# Initialize colorama for cross-platform colored output
init(autoreset=True)
console = Console()

# Import our modules
from layer7.layer7_tester import Layer7Tester
from layer4.layer4_tester import Layer4Tester
from cloudflare.cloudflare_bypass import CloudflareBypass
from fivem.fivem_tester import FiveMTester
from minecraft.minecraft_tester import MinecraftTester
try:
    from waf.waf_bypass import WafBypass
except ImportError:
    WafBypass = None

# Load JSON configs for layers and animations
CONFIG_PATH = Path(__file__).parent / 'ui_config.json'
if CONFIG_PATH.exists():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        UI_CONFIG = json.load(f)
else:
    UI_CONFIG = {}

DDOS_FRAMES = UI_CONFIG.get("ddos_animation_frames", [])

modules = [
    ("Cloudflare Bypass", "cloudflare"),
    ("FiveM Tester", "fivem"),
    ("Layer4 Tester", "layer4"),
    ("Layer7 Tester", "layer7"),
    ("Minecraft Tester", "minecraft"),
    ("WAF Bypass", "waf"),
    ("Exit", None)
]

# --- THEME COLORS ---
RED = Fore.RED + Style.BRIGHT
GRAY = Fore.LIGHTBLACK_EX + Style.BRIGHT

def animated_print(text, delay=0.01, color=GRAY):
    for char in text:
        print(color + char, end='', flush=True)
        time.sleep(delay)
    print(Style.RESET_ALL)

def login():
    banner = UI_CONFIG.get('login_banner', 'LOGIN')
    for char in banner:
        print(RED + char, end='', flush=True)
        time.sleep(0.002)
    print(Style.RESET_ALL)
    for _ in range(3):
        username = input(GRAY + 'Username: ' + Style.RESET_ALL)
        password = getpass.getpass(GRAY + 'Password: ' + Style.RESET_ALL)
        if username == 'root' and password == 'root':
            animated_print("Login successful!", 0.01, color=Fore.GREEN + Style.BRIGHT)
            return True
        else:
            error_text = "Invalid credentials. Try again."
            for char in error_text:
                print(RED + char, end='', flush=True)
                time.sleep(0.005)
            print(Style.RESET_ALL)
    exit_text = "Too many failed attempts. Exiting."
    for char in exit_text:
        print(RED + char, end='', flush=True)
        time.sleep(0.005)
    print(Style.RESET_ALL)
    sys.exit(1)

def print_banner(layer=None):
    banner = ""
    if layer and UI_CONFIG.get('layers', {}).get(layer):
        banner = UI_CONFIG['layers'][layer].get('banner', '')
    else:
        banner = UI_CONFIG.get('main_banner', '')
    if not banner:
        banner = "Network Testing Tool"
    for char in banner:
        print(RED + char, end='', flush=True)
        time.sleep(0.001)
    print(Style.RESET_ALL)

main_ascii_art = r'''
                       ::!~!!!!!:.
                  .xUHWH!! !!?M88WHX:.
                .X*#M@$!!  !X!M$$$$$$WWx:.
               :!!!!!!?H! :!$!$$$$$$$$$$8X:
              !!~  ~:~!! :~!$!#$$$$$$$$$$8X:
             :!~::!H!<   ~.U$X!?R$$$$$$$$MM!
             ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!
               !:~~~ .:!M"T#$$$$WX??#MRRMMM!
               ~?WuxiW*`   `"#$$$$8!!!!??!!!
             :X- M$$$$       `"T#$T~!8$WUXU~
            :%`  ~#$$$m:        ~!~ ?$$$$$$
          :!`.-   ~T$$$$8xx.  .xWW- ~""##*"
.....   -~~:<` !    ~?T#$$@@W@*?$$      /`
W$@@M!!! .!~~ !!     .:XUW$W!~ `"~:    :
#"~~`.:x%`!!  !H:   !WM$$$$Ti.: .!WUn+!`
:::~:!!`:X~ .: ?H.!u "$$$B$$$!W:U!T$$M~
.~~   :X@!.-~   ?@WTWo("*$$$W$TH$! `
Wi.~!X$?!-~    : ?$$$B$Wu("**$RM!
$R@i.~~ !     :   ~$$$$$B$$en:``
?MXT@Wx.~    :     ~"##*$$$$M~
'''

def animated_banner(text, delay=0.001):
    for char in text:
        print(RED + char, end='', flush=True)
        time.sleep(delay)
    print(Style.RESET_ALL)

def ddos_animation(cycles=2, delay=0.12):
    if not DDOS_FRAMES:
        return
    for _ in range(cycles):
        for frame in DDOS_FRAMES:
            os.system('cls' if os.name == 'nt' else 'clear')
            animated_banner(main_ascii_art, delay=0.0002)
            print()
            console.print(Text("BOTNET C2 MAIN MENU", style="bold red"), justify="center")
            print(RED + frame + Style.RESET_ALL)
            time.sleep(delay)

def build_realistic_menu():
    # Realistic, hacker-style menu using ASCII and rich, compact, no childish separators
    table = Table(
        show_header=False,
        box=None,
        expand=True,
        padding=(0, 2),
        style="white on black"
    )
    menu_rows = [
        ("[bold red]1[/]. [white]Cloudflare Bypass",),
        ("[bold red]2[/]. [white]FiveM Tester",),
        ("[bold red]3[/]. [white]Layer4 Tester",),
        ("[bold red]4[/]. [white]Layer7 Tester",),
        ("[bold red]5[/]. [white]Minecraft Tester",),
        ("[bold red]6[/]. [white]WAF Bypass",),
        ("[bold red]7[/]. [white]Exit",),
    ]
    for row in menu_rows:
        table.add_row(row[0])
    return table

def show_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    animated_banner(main_ascii_art, delay=0.0002)
    print()
    border = "=" * 46
    title = "[bold white] Server C2 Panel [/bold white]"
    console.print(f"[bold red]{border}[/bold red]", justify="center")
    console.print(title, justify="center")
    console.print(f"[bold red]{border}[/bold red]", justify="center")
    menu_panel = Panel(
        Align.center(build_realistic_menu(), vertical="middle"),
        border_style="white",
        padding=(1, 4),
        width=60
    )
    console.print(menu_panel, justify="center")
    # Status/info bar for realism
    import getpass, platform
    user = getpass.getuser()
    sysinfo = f"User: {user} | OS: {platform.system()} {platform.release()} | Python: {platform.python_version()}"
    console.print(f"[bold bright_black]{sysinfo}[/bold bright_black]", justify="center")
    print()

def get_test_params():
    # Super-aligned input prompts
    def prompt(label, default=None, validator=None, error_msg=None):
        while True:
            prompt_str = f"{GRAY}{label}{f' [{default}]' if default else ''}: {Style.RESET_ALL}"
            value = input(prompt_str).strip()
            if value == "" and default is not None:
                return default
            if validator is None or validator(value):
                return value
            print(RED + (error_msg or "Invalid input!") + Style.RESET_ALL)

    target = prompt(
        "Target (IP sau domeniu)",
        validator=lambda v: bool(v),
        error_msg="Target nu poate fi gol!"
    )
    port = int(prompt(
        "Port",
        validator=lambda v: v.isdigit() and 0 < int(v) < 65536,
        error_msg="Port invalid! (1-65535)"
    ))
    threads = int(prompt(
        "Threads", default="10",
        validator=lambda v: v.isdigit() and int(v) > 0,
        error_msg="Threads trebuie să fie un număr pozitiv!"
    ))
    duration = int(prompt(
        "Durata (secunde)", default="60",
        validator=lambda v: v.isdigit() and int(v) > 0,
        error_msg="Durata trebuie să fie un număr pozitiv!"
    ))
    verbose = prompt(
        "Verbose? (y/n)", default="n",
        validator=lambda v: v.lower() in ("y", "n"),
        error_msg="Raspunde cu y sau n!"
    ).lower() == "y"
    return target, port, threads, duration, verbose

def type_effect(text, delay=0.002, color=GRAY):
    for char in text:
        print(color + char, end='', flush=True)
        time.sleep(delay)
    print(Style.RESET_ALL)

def main():
    while True:
        show_menu()
        try:
            choice = int(input(GRAY + "\n[>] Select option: " + Style.RESET_ALL))
        except ValueError:
            print(RED + "Invalid input! Enter a number." + Style.RESET_ALL)
            time.sleep(1)
            continue
        if 1 <= choice <= len(modules):
            name, module = modules[choice-1]
            if module is None:
                type_effect("Exiting... Stay anonymous!", 0.01, GRAY)
                break
            else:
                type_effect(f"Launching {name}...", 0.01, color=GRAY)
                time.sleep(1)
                if module == "layer7":
                    print_banner("layer7")
                    try:
                        target, port, threads, duration, verbose = get_test_params()
                        Layer7Tester(target, port, threads, duration, verbose).run_tests()
                    except Exception as e:
                        type_effect(f"[!] Layer7 Tester error: {e}", 0.01, RED)
                        time.sleep(1.5)
                elif module == "layer4":
                    print_banner("layer4")
                    try:
                        target, port, threads, duration, verbose = get_test_params()
                        Layer4Tester(target, port, threads, duration, verbose).run_tests()
                    except Exception as e:
                        type_effect(f"[!] Layer4 Tester error: {e}", 0.01, RED)
                        time.sleep(1.5)
                elif module == "cloudflare":
                    print_banner("cloudflare")
                    try:
                        target, port, threads, duration, verbose = get_test_params()
                        CloudflareBypass(target, port, threads, duration, verbose).run_tests()
                    except Exception as e:
                        type_effect(f"[!] Cloudflare Bypass error: {e}", 0.01, RED)
                        time.sleep(1.5)
                elif module == "fivem":
                    print_banner("fivem")
                    try:
                        target, port, threads, duration, verbose = get_test_params()
                        FiveMTester(target, port, threads, duration, verbose).run_tests()
                    except Exception as e:
                        type_effect(f"[!] FiveM Tester error: {e}", 0.01, RED)
                        time.sleep(1.5)
                elif module == "minecraft":
                    print_banner("minecraft")
                    try:
                        target, port, threads, duration, verbose = get_test_params()
                        MinecraftTester(target, port, threads, duration, verbose).run_tests()
                    except Exception as e:
                        type_effect(f"[!] Minecraft Tester error: {e}", 0.01, RED)
                        time.sleep(1.5)
                elif module == "waf":
                    print_banner("waf")
                    if WafBypass:
                        try:
                            target, port, threads, duration, verbose = get_test_params()
                            WafBypass(target, port, threads, duration, verbose).run_tests()
                        except Exception as e:
                            type_effect(f"[!] WAF Bypass error: {e}", 0.01, RED)
                            time.sleep(1.5)
                    else:
                        type_effect(f"[!] WAF Bypass module not yet implemented!", 0.01, RED)
                        time.sleep(1.5)
                else:
                    type_effect(f"[!] {name} module not yet implemented!", 0.01, RED)
                    time.sleep(1.5)
        else:
            print(RED + "Invalid option!" + Style.RESET_ALL)
            time.sleep(1)

if __name__ == "__main__":
    if login():
        main() 