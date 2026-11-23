from rich.table import Table

# import colorama
from colorama import Fore, Back, Style

from tabulate import tabulate

class BaseView:
    """Base view class"""

    def __init__(self):
        pass

    def display_list(self, data, title, pause):
        """Display a list of data"""
        if title:
            print(f"{Fore.GREEN}" + f"{title} ".center(72, "=") + f"{Style.RESET_ALL}")

        grid = f"{Fore.LIGHTCYAN_EX}"
        grid += tabulate(data, headers="keys", tablefmt="fancy_grid")
        print(grid)
        if pause:
            input("\n{Fore.MAGENTA}Press Enter to go back to the main menu...")



    def table_settings(self, headers, title, items):
        """Setings the visual of a dynamic table with data (from Player of Tournament objects) with Rich library"""

        print("\n")

        table = Table(
            title=title,
            padding=(0, 1),
            show_header=True,
            show_lines=True,
            header_style="bold magenta",
            title_style="bold green",
            title_justify="center",
            width=120,
            )
        
        try:
            headers = items[0].keys()

        except IndexError:
            print("No data to display")
            return
        
        for header in headers:
            table.add_column(header)



    def ask_confirmation(self, message):
        """Ask a confirmation to the user and return True or False"""
        answer = input(f"{Fore.RED }{message}")
        if answer.lower() in ["yes", "y", "oui", "o"]:
            return True
        else:
            return False


