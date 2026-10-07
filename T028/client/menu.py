
from core.constants import MENU_TEXT, MENU_OPTIONS


def show_menu():
    print(MENU_TEXT)


def get_selection():

    choice = input("Select: ").strip()

    if choice not in MENU_OPTIONS:
        print("Invalid selection. Please choose a number from 1 to 8.\n")
        return None, None

    command, needs_host = MENU_OPTIONS[choice]

    params = ""
    if needs_host:
        params = input(f"Enter target host/IP for {command}: ").strip()
        if not params:
            print("A host/IP is required for this command.\n")
            return None, None

    return command, params
