from colorama import Fore, Style

class ViewApp:

    def display_main_menu(self):
        """Display the main menu and return the user's choice."""
        
        while True:
            print(Fore.GREEN + "\nWelcome to the Chess Tournament Manager\n".center(120, "-"))
            print(Fore.YELLOW + "\n1. Tournament menu")
            print("2. Player menu")
            print("4. Quit")
            print(Style.RESET_ALL)

            choice = input(Fore.CYAN + "Enter your choice: " + Style.RESET_ALL)

            if choice in ["1", "2", "4"]:
                if choice == "4":
                    print(Fore.GREEN + "Goodbye!" + Style.RESET_ALL)
                return choice
            else:
                print(Fore.RED + "Invalid choice. Please try again.")
                print(Style.RESET_ALL)
                print()
                continue
