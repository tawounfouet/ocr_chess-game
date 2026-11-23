from colorama import Fore, Style

class ViewPlayer:

    def display_player_menu(self):
        """Display the player menu and return user choice."""
        
        while True:
            print("\n")
            print(Fore.BLUE + "Player Menu".center(80, "-") + Style.RESET_ALL)
            print("1. " + Fore.GREEN + "Create new player" + Style.RESET_ALL)
            print("2. " + Fore.GREEN + "Modify player" + Style.RESET_ALL)
            print("3. " + Fore.GREEN + "List players by name" + Style.RESET_ALL)
            print("4. " + Fore.GREEN + "List players by rank" + Style.RESET_ALL)
            print("5. " + Fore.RED + "Back to main menu" + Style.RESET_ALL)
            print("\n") 
            choice = input("Enter your choice: ")
            print("\n")
            
            if choice in ["1", "2", "3", "4", "5"]:
                return choice
            else:
                print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)
                print()
                continue


    
