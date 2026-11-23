from tinydb import TinyDB, Query
import uuid


from models.player import Player
from models.round import Round
from models.match import Match
from models.tournament import Tournament

from views.base import BaseView
from views.tournament import TournamentView

from datetime import datetime
import random


class TournamentController:
    def __init__(self):
        self.view = TournamentView()
        self.base_view = BaseView()
        self.tournament = None
        self.players = Player.get_all_players()
        self.tournaments = Tournament.get_all_tournaments()
        self.rounds = []

        self.timer = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def handle_tournament_menu(self):
        """Handle tournament menu"""
        exit_requested = False

        while not exit_requested:
            choice = self.view.display_tournament_menu()

            if choice == "1":
                self.create_tournament()
            elif choice == "2":
                self.view.display_tournaments(self.tournaments)
            elif choice == "3":
                # display tournament info using tournament ID
                tournament_id = self.view.input_message("Enter tournament ID to view details: ")
                self.view.display_tournament_info(tournament_id)

            elif choice == "4":
                # Consult the rounds using the same public UUID displayed in the list.
                tournament_id = self.view.input_message("Enter tournament ID to view rounds: ")
                self.view.display_rounds_list(tournament_id)
            elif choice == "6":
                exit_requested = True
            else:
                self.view.display_message("Invalid choice. Please try again.")

    def create_tournament(self):
        tournament_data = self.view.get_tournament_data()
        self.tournament = Tournament(**tournament_data)
        
        
        # Display the list of players
        self.view.display_players(self.players)
 

        # Ask the user for the exact number of players to add
        #num_players_to_add = int(input("Enter the number of players to add: "))

        # Add players to the tournament
        player_ids = self.view.get_player_ids_to_add()
        players_to_add = [Player.get_player_by_id(id_db)  for id_db in player_ids]
        # players_to_add = [player_id for player_id in player_ids]
        self.tournament.players = players_to_add

        #self.view.display_message(f"Players added to the tournament: {players_to_add}")
        self.view.display_message("\n") 
        
        #print(f"Players: {self.tournament.players}")
        #self.tournament.save_to_db()
        
        #self.tournament.id_db = 
        #self.tournament.tournament_id = str(uuid.uuid4())
       
    
        # Generate rounds
        # num_rounds = self.tournament.nb_rounds # the defauly value is set to 4
        # rounds = self.generate_rounds(players_to_add, num_rounds=num_rounds)
        # self.tournament.rounds = rounds
        # self.tournament.save_to_db()

        # craete the first round
        round_1 = self.create_round(players_to_add, 1)
        self.tournament.rounds.append(round_1)
        self.tournament.save_to_db()

        # Display the list of matches for the first round
        self.get_matches_list(round_1)

        # Ask the user if they want to start the first round
        choice_start_round = self.base_view.ask_confirmation("Do you want to start the first round? (y/n): ")

        if choice_start_round:
            self.add_scores_to_tournament(round_1)
            self.manage_rounds(self.tournament)
        else:
            self.view.display_message("The first round has not been started.")


        # save results to the database
        self.tournament.save_to_db()

        # nex
            

        





     

      

        # Display tournament results
        self.view.display_message(f"Tournament {self.tournament.name} created successfully.")


    # def generate_rounds(self, players, num_rounds=4):
    #     """Generate rounds with matches for the tournament."""
    #     rounds = []

    #     for round_num in range(1, num_rounds + 1):
    #         round_name = f"Round {round_num}"
    #         start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #         end_date = None  # Set end date accordingly, to be updated when the round is completed
    #         matches = self.generate_matches(players, rounds)
    #         status = ""  # Set status accordingly, to be updated during the tournament
    #         round = Round(
    #             name=round_name,
    #             start_date=start_date,
    #             end_date=end_date,
    #             matches=matches,
    #             status=status,
    #         )
    #         rounds.append(round)

    #     return rounds
        
    def get_matches_list(self, round):
        """Display the list of matches for a round."""
        self.view.display_message(f"Matches for {round.name}:")
        
        matches = []

        # Enumerate :  attrbibuer un index
        for index, match in enumerate(round.matches):
            
            match_data = {
                "N. Match": str(index + 1),
                "Player 1": match.player_1.full_name if match.player_1 else "Bye",
                "Player 2": match.player_2.full_name if match.player_2 else "Bye"
            }
            
            matches.append(match_data)
        
        # display the list of matches
        headers = ["N. Match", "Player 1", "Player 2"]
        title = f"Matches for {round.name}"
        self.base_view.table_settings(headers, title, matches)

    def add_scores_to_tournament(self, round):
        """Returns player's scores of each match  and ends the round (status + end_date) or None user enters 'n'"""

        choice = self.base_view.ask_confirmation("Do you want to add scores to the matches? (y/n): ")

        if choice.lower() == "n":
            return "n"
        
        for match in round.matches:
            self.view.get_current_match(round, match)

            choice = self.view.get_choices_match_result(round)

            if choice == "1":
                match.p1_score = 1
            
            elif choice == "2":
                match.p2_score = 1

            elif choice == "3":
                match.p1_score = 0.5
                match.p2_score = 0.5

        # Update the round status and end date
        round.status = "Completed"
        round.end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.view.display_message(f"Round {round.name} completed successfully.")



        
    def create_round(self, players, current_round):
        """Create a round for the tournament."""
        round_name = f"Round {current_round}"
        start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Round Creation
        matches = []

        while len(players) > 0:
            player_1 = players.pop(0)
            player_2 = players.pop(0) if len(players) > 0 else None
            match = Match(player_1=player_1, player_2=player_2)
            matches.append(match)

        round = Round(
            name=round_name,
            start_date=start_date,
            matches=matches,
        )

        return round
    

    def manage_rounds(self, tournament):
        """Manage rounds for a tournament."""
        
        continue_rounds = True

        while continue_rounds:
            choice_next_round = self.base_view.ask_confirmation("Do you want to start the next round? (y/n): ")

            if choice_next_round.lower() == "n":
                continue_rounds = False
                break

            round = None

            try:
                round = tournament.rounds[tournament.current_round]
            except IndexError:
                print("No more rounds to start.")
                pass

            if round is not None:
                self.view.display_message(f"Starting Round {round.name}...")
                # make copies of the players list to avoid modifying the original list
                players = tournament.players.copy()
                # firt round is created with the list of players (randomly shuffled)
                if tournament.current_round == 0:
                    shuffle_players = random.shuffle(players)
                # next rounds are created with the list of players sorted by score
                else:
                    players.sort(key=lambda player: player.score, reverse=True)

                # round creation with the list of players
                round = self.create_round(players, tournament.current_round + 1)

                # display the list of matches for the round
                self.get_matches_list(round)
                


    def resume_tournament(self):
        """display list of tournaments "In progress" and resume the selected one or None if user enters exit or quit"""
        tournaments = Tournament.get_all_tournaments()
        in_progress_tournaments = [tournament for tournament in tournaments if tournament["status"] == "In progress"]
        if not in_progress_tournaments:
            self.view.display_message("No tournament in progress.")
            return None
        self.view.display_tournaments(in_progress_tournaments)
        tournament_id = self.view.input_message("Enter the tournament ID to resume: ")
        if tournament_id.lower() in ["exit", "quit"]:
            return None
        return Tournament.get_tournament_by_id(tournament_id)



    # def get_matches_list(self, round):
    #     """Display the list of matches for a round."""
    #     self.view.display_message(f"Matches for {round.name}:")
    #     for match in round.matches:
    #         if match.player_2:
    #             self.view.display_message(f"{match.player_1.full_name} vs {match.player_2.full_name}")
    #         else:
    #             self.view.display_message(f"{match.player_1.full_name} (Bye)")
    




    
    # def generate_matches(self, players, rounds):
    #     """Generate matches for a round."""
    #     matches = []
    #     num_players = len(players)

    #     # Shuffle players for random pairing
    #     random.shuffle(players)

    #     # Create a dictionary to track which players have already played against each other
    #     played_matches = {}

    #     # Iterate through pairs of players
    #     for i in range(0, num_players, 2):
    #         player_1 = players[i]["id_db"]
    #         player_2 = players[i + 1]["id_db"] if i + 1 < num_players else None

    #         # Check if the players have already played against each other in previous rounds
    #         while player_2 in played_matches.get(player_1, []):
    #             i += 2  # Move to the next pair of players
    #             player_1 = players[i]["id_db"]
    #             player_2 = players[i + 1]["id_db"] if i + 1 < num_players else None

    #         # Add the match to the list of played matches for both players
    #         played_matches.setdefault(player_1, []).append(player_2)
    #         played_matches.setdefault(player_2, []).append(player_1)

    #         match = Match(player_1=player_1, player_2=player_2)
    #         matches.append(match)

    #     return matches




    # def start_round(self, tournament):
    #     round_1 = tournament.rounds[0]
    #     self.view.display_message("Players for Round 1:")
    #     for match in round_1.matches:
    #         #print(f"{match.player_1.full_name} vs {match.player_2.full_name}")
    #         print(f"{match.player_1} vs {match.player_2}")

    #     save_scores = input("Do you want to save the scores? (y/n): ")
    #     if save_scores.lower() == "y":
    #         self.save_scores_to_tournament(tournament)

        

    # def display_round_players(self, round):
    #     """Display the players for a specific round."""
    #     print(f"Players for {round.name}:")
    #     for match in round.matches:
    #         if match.player_2:
    #             print(f"{match.player_1.full_name} vs {match.player_2.full_name}")
    #         else:
    #             print(f"{match.player_1.full_name} (Bye)")

    # def display_tournament_results(self):
    #     """Display tournament results"""
    #     self.view.display_tournament_results(self.model)




    # def save_scores_to_tournament(self, tournament):
    #     """Run a round and prompt for scores."""
    #     for round in tournament.rounds:
    #         for match in round.matches:
    #             #choice = input(f"Enter result for {match.player_1.full_name} vs {match.player_2.full_name}: "
    #             choice = input( f"Enter result for {match.player_1} vs {match.player_2}: "
    #                 "1 for Player 1, 2 for Player 2, 3 for Draw: "
    #             )
    #             if choice == "1":
    #                 match.p1_score = 1
    #                 # Mettre à jour le score du joueur 1 avec un score de match gagnant
    #                 #Player.update_score(match.player_1, 1)
    #                 self.update_player_score(match.player_1, 1)

    #             elif choice == "2":
    #                 match.p2_score = 1
    #                 # Mettre à jour le score du joueur 2 avec un score de match gagnant
    #                 # Player.update_score(match.player_2, 1)
    #                 self.update_player_score(match.player_2, 1)
    #             elif choice == "3":
    #                 match.p1_score = 0.5
    #                 match.p2_score = 0.5
    #                 # Mettre à jour le score des deux joueurs avec un score de match nul
    #                 self.update_player_score(match.player_1, 0.5)
    #                 self.update_player_score(match.player_2, 0.5)

    #             # Update database records with new scores
    #             self.update_match_record_in_database(
    #                 tournament_id=tournament.tournament_id,
    #                 round_name=round.name,
    #                 player_1_id=match.player_1,
    #                 player_2_id=match.player_2,
    #                 p1_score=match.p1_score,
    #                 p2_score=match.p2_score,
    #             )


    # def update_player_score(self, id_db, score_change):
    #     """Update player's score."""
    #     player_data = Player.get_player_by_id(id_db)
    #     if player_data:
    #         # Instancier un objet Player à partir des données du joueur
    #         player = Player(**player_data)
    #         player.score += score_change
    #         player.save_to_db()  # Sauvegarde du joueur dans la base de données
    #         print(f"Le score du joueur {id_db} a été mis à jour avec succès.")
    #     else:
    #         print("Joueur non trouvé dans la base de données.")


    # def update_match_record_in_database(
    #     self, tournament_id, round_name, player_1_id, player_2_id, p1_score, p2_score
    # ):
    #     """Update match record in the database."""
    #     db_tournaments = TinyDB("data/tournaments.json", indent=4)
    #     tournaments_table = db_tournaments.table("tournaments")

    #     # Create a Query object to locate the tournament by its tournament_id
    #     query = Query()
    #     tournament_record = tournaments_table.get(query.tournament_id == tournament_id)

    #     # Find the round within the tournament's rounds list
    #     for round_record in tournament_record["rounds"]:
    #         if round_record["name"] == round_name:
    #             # Find the match within the round's matches list
    #             for match in round_record["matches"]:
    #                 if (
    #                     match["player_1"] == player_1_id
    #                     and match["player_2"] == player_2_id
    #                 ):
    #                     # Update the scores for the match
    #                     match["p1_score"] = p1_score
    #                     match["p2_score"] = p2_score
    #                     # Update the tournament record in the database
    #                     tournaments_table.update(
    #                         tournament_record, doc_ids=[tournament_record.doc_id]
    #                     )
    #                     return

    # def load_tournament(self, tournament_id):
    #     """Load a tournament from the database by its ID."""
    #     tournament = Tournament.get_tournament_by_id(tournament_id)
    #     if tournament:
    #         return tournament
    #     else:
    #         print("Tournament not found.")
    #         return None

    # def display_rounds(self, tournament):
    #     """Display the list of rounds in a tournament."""
    #     rounds = tournament.rounds_results
    #     if not rounds:
    #         print("No rounds found.")
    #         return
    #     print("List of Rounds:")
    #     for round in rounds:
    #         print(f"- {round.name}")

    # def display_matches(self, tournament):
    #     """Display the list of matches in a tournament."""
    #     rounds = tournament.rounds_results
    #     if not rounds:
    #         print("No matches found.")
    #         return
    #     print("List of Matches:")
    #     for round in rounds:
    #         print(f"Round: {round.name}")
    #         for match in round.matches:
    #             # print(f"  {match.player_1.full_name} vs {match.player_2.full_name}")
    #             print(f"  {match.player_1} vs {match.player_2}")


  


if __name__ == "__main__":
    """Test TournamentController class"""
    tc = TournamentController()
    tc.handle_tournament_menu()
