from colorama import Fore, init
init(convert=True)
commandBox = f"""
╔══════════════════════════════════════╗
║                                      ║
║         [{Fore.BLUE}1{Fore.WHITE}] Copy Group               ║
║         [{Fore.BLUE}2{Fore.WHITE}] Copy Shirts              ║
║         [{Fore.BLUE}3{Fore.WHITE}] Copy Pants               ║
║         [{Fore.BLUE}4{Fore.WHITE}] Copy a Clothing          ║
║                                      ║
║         [{Fore.BLUE}5{Fore.WHITE}] Display Robux            ║
║         [{Fore.BLUE}6{Fore.WHITE}] Display Uploaded         ║
║         [{Fore.BLUE}7{Fore.WHITE}] Project Clothing         ║
║                                      ║
║         [{Fore.BLUE}8{Fore.WHITE}] Refresh                  ║
║         [{Fore.BLUE}9{Fore.WHITE}] Credits                  ║
║                                      ║
╚══════════════════════════════════════╝
"""

clothingSortBox = f"""
╔════════════════════════════════════════════╗
║                                            ║
║         [{Fore.BLUE}1{Fore.WHITE}] Relevance                      ║
║                                            ║
║         [{Fore.BLUE}2{Fore.WHITE}] Favourited All Time            ║
║         [{Fore.BLUE}3{Fore.WHITE}] Favourited Past Week           ║
║         [{Fore.BLUE}4{Fore.WHITE}] Favourited Past Day            ║
║                                            ║
║         [{Fore.BLUE}5{Fore.WHITE}] Best-Selling All Time          ║
║         [{Fore.BLUE}6{Fore.WHITE}] Best-Selling Past Week         ║
║         [{Fore.BLUE}7{Fore.WHITE}] Best-Selling Past Day          ║
║                                            ║
║         [{Fore.BLUE}8{Fore.WHITE}] Recently Updated               ║
║                                            ║
╚════════════════════════════════════════════╝
"""

credits = f"""
╔════════════════════════════════╗
║     {Fore.BLUE}cereb#0001/Dreamer#5114{Fore.WHITE}    ║
║     {Fore.BLUE}Adaaks (GitHub){Fore.WHITE}            ║
╚════════════════════════════════╝
"""

def cl(txt, color, symbol=">", txtcolor=True):
    if txtcolor:
        if str(color).lower() == "blue":
            print(f"[{Fore.BLUE}{symbol}{Fore.WHITE}] {Fore.BLUE}{txt}{Fore.WHITE}")
        elif str(color).lower() == "green":
            print(f"[{Fore.GREEN}{symbol}{Fore.WHITE}] {Fore.GREEN}{txt}{Fore.WHITE}")
        elif str(color).lower() == "yellow":
            print(f"[{Fore.YELLOW}{symbol}{Fore.WHITE}] {Fore.YELLOW}{txt}{Fore.WHITE}")
        elif str(color).lower() == "red":
            print(f"[{Fore.RED}{symbol}{Fore.WHITE}] {Fore.RED}{txt}{Fore.WHITE}")
    else:
        if str(color).lower() == "blue":
            print(f"[{Fore.BLUE}{symbol}{Fore.WHITE}] {txt}{Fore.WHITE}")
        elif str(color).lower() == "green":
            print(f"[{Fore.GREEN}{symbol}{Fore.WHITE}] {txt}{Fore.WHITE}")
        elif str(color).lower() == "yellow":
            print(f"[{Fore.YELLOW}{symbol}{Fore.WHITE}] {txt}{Fore.WHITE}")
        elif str(color).lower() == "red":
            print(f"[{Fore.RED}{symbol}{Fore.WHITE}] {txt}{Fore.WHITE}")

def ci(txt, color, symbol="?", txtcolor=True):
    if txtcolor:
        if str(color).lower() == "blue":
            return input(f"[{Fore.BLUE}{symbol}{Fore.WHITE}] {Fore.BLUE}{txt}{Fore.WHITE}")
        elif str(color).lower() == "green":
            return input(f"[{Fore.GREEN}{symbol}{Fore.WHITE}] {Fore.GREEN}{txt}{Fore.WHITE}")
        elif str(color).lower() == "yellow":
            return input(f"[{Fore.YELLOW}{symbol}{Fore.WHITE}] {Fore.YELLOW}{txt}{Fore.WHITE}")
        elif str(color).lower() == "red":
            return input(f"[{Fore.RED}{symbol}{Fore.WHITE}] {Fore.RED}{txt}{Fore.WHITE}")
    else:
        if str(color).lower() == "blue":
            return input(f"[{Fore.BLUE}{symbol}{Fore.WHITE}] {txt}{Fore.WHITE}")
        elif str(color).lower() == "green":
            return input(f"[{Fore.GREEN}{symbol}{Fore.WHITE}] {txt}{Fore.WHITE}")
        elif str(color).lower() == "yellow":
            return input(f"[{Fore.YELLOW}{symbol}{Fore.WHITE}] {txt}{Fore.WHITE}")
        elif str(color).lower() == "red":
            return input(f"[{Fore.RED}{symbol}{Fore.WHITE}] {txt}{Fore.WHITE}")

def ce(txt, color, symbol="!", txtcolor=True):
    if txtcolor:
        if str(color).lower() == "blue":
            print(f"[{Fore.BLUE}{symbol}{Fore.WHITE}] {Fore.BLUE}{txt}{Fore.WHITE}")
        elif str(color).lower() == "green":
            print(f"[{Fore.GREEN}{symbol}{Fore.WHITE}] {Fore.GREEN}{txt}{Fore.WHITE}")
        elif str(color).lower() == "yellow":
            print(f"[{Fore.YELLOW}{symbol}{Fore.WHITE}] {Fore.YELLOW}{txt}{Fore.WHITE}")
        elif str(color).lower() == "red":
            print(f"[{Fore.RED}{symbol}{Fore.WHITE}] {Fore.RED}{txt}{Fore.WHITE}")
    else:
        if str(color).lower() == "blue":
            print(f"[{Fore.BLUE}{symbol}{Fore.WHITE}] {txt}{Fore.WHITE}")
        elif str(color).lower() == "green":
            print(f"[{Fore.GREEN}{symbol}{Fore.WHITE}] {txt}{Fore.WHITE}")
        elif str(color).lower() == "yellow":
            print(f"[{Fore.YELLOW}{symbol}{Fore.WHITE}] {txt}{Fore.WHITE}")
        elif str(color).lower() == "red":
            print(f"[{Fore.RED}{symbol}{Fore.WHITE}] {txt}{Fore.WHITE}")