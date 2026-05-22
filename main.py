import random
from collections import Counter
import tkinter as tk
from tkinter import messagebox

backGroundColor = "lightgreen"
class AIPoweredRPS:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Powered Rock Paper Scissors")
        self.root.geometry("500x500")
        self.root.resizable(True, True)   
        self.root.configure(bg=backGroundColor)
        self.moves = ["rock", "paper", "scissors"]
        self.player_history = []
        self.player_score = 0
        self.ai_score = 0
        self.rounds = 0

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(
            self.root,
            text="AI-Powered Rock Paper Scissors",
            bg= backGroundColor,
            font=("Arial", 20, "bold")
        )
        self.title_label.pack(pady=20)
        self.result_label = tk.Label(
            self.root,
            text="Choose your move!",
            bg=backGroundColor,
            font=("Arial", 14)
        )
        self.result_label.pack(pady=10)

        self.player_move_label = tk.Label(
            self.root,
            text="Your Move: None",
            bg=backGroundColor,
            font=("Arial", 12)
        )
        self.player_move_label.pack()

        self.ai_move_label = tk.Label(
            self.root,
            text="AI Move: None",
            bg=backGroundColor,
            font=("Arial", 12)
        )
        self.ai_move_label.pack(pady=5)

        self.button_frame = tk.Frame(self.root, bg=backGroundColor)
        self.button_frame.pack(pady=20)

        self.rock_button = tk.Button(
            self.button_frame,
            text="Rock",
            width=12,
            height=2,
            command=lambda: self.play_round("rock")
        )
        self.rock_button.grid(row=0, column=0, padx=10)

        self.paper_button = tk.Button(
            self.button_frame,
            text="Paper",
            width=12,
            height=2,
            command=lambda: self.play_round("paper")
        )
        self.paper_button.grid(row=0, column=1, padx=10)

        self.scissors_button = tk.Button(
            self.button_frame,
            text="Scissors",
            width=12,
            height=2,
            command=lambda: self.play_round("scissors")
        )
        self.scissors_button.grid(row=0, column=2, padx=10)

        self.stats_label = tk.Label(
            self.root,
            text=self.get_stats_text(),
            font=("Arial", 12),
            justify="left"
        )
        self.stats_label.pack(pady=20)

        self.reset_button = tk.Button(
            self.root,
            text="Reset Game",
            width=15,
            command=self.reset_game
        )
        self.reset_button.pack(pady=10)

    def predict_player_move(self):
        if not self.player_history:
            return random.choice(self.moves)

        move_counter = Counter(self.player_history)
        predicted_move = move_counter.most_common(1)[0][0]

        return predicted_move

    def get_ai_move(self):
        predicted_move = self.predict_player_move()

        counters = {
            "rock": "paper",
            "paper": "scissors",
            "scissors": "rock"
        }

        return counters[predicted_move]

    def determine_winner(self, player_move, ai_move):
        if player_move == ai_move:
            return "draw"

        winning_cases = {
            "rock": "scissors",
            "paper": "rock",
            "scissors": "paper"
        }

        if winning_cases[player_move] == ai_move:
            return "player"

        return "ai"

    def play_round(self, player_move):
        ai_move = self.get_ai_move()

        self.player_move_label.config(
            text=f"Your Move: {player_move.capitalize()}"
        )

        self.ai_move_label.config(
            text=f"AI Move: {ai_move.capitalize()}"
        )

        result = self.determine_winner(player_move, ai_move)

        if result == "player":
            self.result_label.config(text="You Win This Round!")
            self.player_score += 1

        elif result == "ai":
            self.result_label.config(text="AI Wins This Round!")
            self.ai_score += 1

        else:
            self.result_label.config(text="It's a Draw!")

        self.player_history.append(player_move)
        self.rounds += 1

        self.stats_label.config(text=self.get_stats_text())

    def get_stats_text(self):
        stats = (
            f"Rounds Played: {self.rounds}\n"
            f"Player Score: {self.player_score}\n"
            f"AI Score: {self.ai_score}\n"
        )

        if self.player_history:
            move_counter = Counter(self.player_history)
            stats += "\nMove Frequency:\n"

            for move, count in move_counter.items():
                stats += f"{move.capitalize()}: {count}\n"

        return stats

    def reset_game(self):
        self.player_history.clear()
        self.player_score = 0
        self.ai_score = 0
        self.rounds = 0

        self.result_label.config(text="Choose your move!")
        self.player_move_label.config(text="Your Move: None")
        self.ai_move_label.config(text="AI Move: None")
        self.stats_label.config(text=self.get_stats_text())

        messagebox.showinfo(
            "Game Reset",
            "The game has been reset."
        )


if __name__ == "__main__":
    root = tk.Tk()
    game = AIPoweredRPS(root)
    root.mainloop()