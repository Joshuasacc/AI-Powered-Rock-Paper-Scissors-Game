import random
from collections import Counter
import tkinter as tk
from tkinter import messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

backGroundColor = "lightgreen"


class AIPoweredRPS:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Powered Rock Paper Scissors")
        self.root.geometry("600x650")
        self.root.resizable(True, True)
        self.root.configure(bg=backGroundColor)

        self.moves = ["rock", "paper", "scissors"]
        self.player_history = []

        self.player_score = 0
        self.ai_score = 0
        self.rounds = 0

        # chart stats
        self.player_wins = 0
        self.ai_wins = 0
        self.draws = 0

        # toggle
        self.chart_visible = False

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(
            self.root,
            text="AI-Powered Rock Paper Scissors",
            bg=backGroundColor,
            font=("Arial", 20, "bold")
        )
        self.title_label.pack(pady=10)

        self.result_label = tk.Label(
            self.root,
            text="Choose your move!",
            bg=backGroundColor,
            font=("Arial", 14)
        )
        self.result_label.pack(pady=5)

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
        self.button_frame.pack(pady=10)

        self.rock_button = tk.Button(self.button_frame, text="Rock", width=10, height=2,
                                     command=lambda: self.play_round("rock"))
        self.rock_button.grid(row=0, column=0, padx=5)

        self.paper_button = tk.Button(self.button_frame, text="Paper", width=10, height=2,
                                      command=lambda: self.play_round("paper"))
        self.paper_button.grid(row=0, column=1, padx=5)

        self.scissors_button = tk.Button(self.button_frame, text="Scissors", width=10, height=2,
                                         command=lambda: self.play_round("scissors"))
        self.scissors_button.grid(row=0, column=2, padx=5)

        self.stats_label = tk.Label(
            self.root,
            text=self.get_stats_text(),
            bg=backGroundColor,
            font=("Arial", 11),
            justify="left"
        )
        self.stats_label.pack(pady=10)

        # chart frame hidden
        self.chart_frame = tk.Frame(self.root, bg=backGroundColor)

        self.toggle_chart_button = tk.Button(
            self.root,
            text="Show Chart 📊",
            width=15,
            command=self.toggle_chart
        )
        self.toggle_chart_button.pack(pady=5)

        self.reset_button = tk.Button(
            self.root,
            text="Reset Game",
            width=15,
            command=self.reset_game
        )
        self.reset_button.pack(pady=5)

    def predict_player_move(self):
        if not self.player_history:
            return random.choice(self.moves)
        return Counter(self.player_history).most_common(1)[0][0]

    def get_ai_move(self):
        predicted = self.predict_player_move()
        counters = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
        return counters[predicted]

    def determine_winner(self, player_move, ai_move):
        if player_move == ai_move:
            return "draw"
        win = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
        return "player" if win[player_move] == ai_move else "ai"

    def play_round(self, player_move):
        ai_move = self.get_ai_move()
        result = self.determine_winner(player_move, ai_move)

        self.player_move_label.config(text=f"Your Move: {player_move.capitalize()}")
        self.ai_move_label.config(text=f"AI Move: {ai_move.capitalize()}")

        if result == "player":
            self.player_score += 1
            self.player_wins += 1
            self.result_label.config(text="You Win! 🎉")
        elif result == "ai":
            self.ai_wins += 1
            self.ai_score += 1
            self.result_label.config(text="AI Wins 🤖")
        else:
            self.draws += 1
            self.result_label.config(text="Draw 🤝")

        self.player_history.append(player_move)
        self.rounds += 1

        self.stats_label.config(text=self.get_stats_text())
        self.update_chart()

    def get_stats_text(self):
        return f"Rounds: {self.rounds}\nPlayer Score: {self.player_score}\nAI Score: {self.ai_score}"

    def update_chart(self):
        for w in self.chart_frame.winfo_children():
            w.destroy()

        labels = ["Player", "AI", "Draw"]
        values = [self.player_wins, self.ai_wins, self.draws]

        fig = plt.Figure(figsize=(4.5, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(labels, values)
        ax.set_title("Performance Chart")

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def toggle_chart(self):
        if self.chart_visible:
            self.chart_frame.pack_forget()
            self.toggle_chart_button.config(text="Show Chart 📊")
            self.chart_visible = False
        else:
            self.chart_frame.pack()
            self.update_chart()
            self.toggle_chart_button.config(text="Hide Chart 📊")
            self.chart_visible = True

    def reset_game(self):
        self.player_history.clear()
        self.player_score = 0
        self.ai_score = 0
        self.rounds = 0
        self.player_wins = 0
        self.ai_wins = 0
        self.draws = 0

        self.result_label.config(text="Choose your move!")
        self.player_move_label.config(text="Your Move: None")
        self.ai_move_label.config(text="AI Move: None")
        self.stats_label.config(text=self.get_stats_text())

        if self.chart_visible:
            self.update_chart()

        messagebox.showinfo("Game Reset", "The game has been reset!")


if __name__ == "__main__":
    root = tk.Tk()
    game = AIPoweredRPS(root)
    root.mainloop()