import random
from collections import Counter
import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

backGroundColor = "#d8ffd8"


class AIPoweredRPS:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Powered Rock Paper Scissors")
        self.root.geometry("750x700")
        self.root.resizable(True, True)
        self.root.configure(bg=backGroundColor)

        self.moves = ["rock", "paper", "scissors"]
        self.player_history = []

        self.player_score = 0
        self.ai_score = 0
        self.rounds = 0

        self.player_wins = 0
        self.ai_wins = 0
        self.draws = 0

        self.chart_visible = False

        self.create_widgets()

    def create_widgets(self):

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Game.TButton",
            font=("Arial", 12, "bold"),
            padding=10
        )

        self.main_frame = tk.Frame(
            self.root,
            bg=backGroundColor
        )
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # ================= TITLE =================
        self.title_label = tk.Label(
            self.main_frame,
            text="🎮 AI-Powered Rock Paper Scissors",
            bg=backGroundColor,
            fg="#1d3557",
            font=("Arial", 22, "bold")
        )
        self.title_label.pack(pady=10)

        # ================= RESULT BOX =================
        self.result_frame = tk.Frame(
            self.main_frame,
            bg="white",
            bd=3,
            relief="ridge"
        )
        self.result_frame.pack(fill="x", pady=10)

        self.result_label = tk.Label(
            self.result_frame,
            text="Choose your move!",
            bg="white",
            fg="#e63946",
            font=("Arial", 16, "bold"),
            pady=10
        )
        self.result_label.pack()

        # ================= MOVES =================
        self.moves_frame = tk.Frame(
            self.main_frame,
            bg=backGroundColor
        )
        self.moves_frame.pack(pady=10)

        self.player_move_label = tk.Label(
            self.moves_frame,
            text="👤 Your Move: None",
            bg=backGroundColor,
            font=("Arial", 13, "bold")
        )
        self.player_move_label.grid(row=0, column=0, padx=20)

        self.ai_move_label = tk.Label(
            self.moves_frame,
            text="🤖 AI Move: None",
            bg=backGroundColor,
            font=("Arial", 13, "bold")
        )
        self.ai_move_label.grid(row=0, column=1, padx=20)

        # ================= BUTTONS =================
        self.button_frame = tk.Frame(
            self.main_frame,
            bg=backGroundColor
        )
        self.button_frame.pack(pady=20)

        self.rock_button = ttk.Button(
            self.button_frame,
            text="🪨 Rock",
            style="Game.TButton",
            command=lambda: self.play_round("rock")
        )
        self.rock_button.grid(row=0, column=0, padx=10)

        self.paper_button = ttk.Button(
            self.button_frame,
            text="📄 Paper",
            style="Game.TButton",
            command=lambda: self.play_round("paper")
        )
        self.paper_button.grid(row=0, column=1, padx=10)

        self.scissors_button = ttk.Button(
            self.button_frame,
            text="✂️ Scissors",
            style="Game.TButton",
            command=lambda: self.play_round("scissors")
        )
        self.scissors_button.grid(row=0, column=2, padx=10)

        # ================= SCORE CARD =================
        self.stats_frame = tk.Frame(
            self.main_frame,
            bg="white",
            bd=3,
            relief="ridge"
        )
        self.stats_frame.pack(fill="x", pady=10)

        self.stats_title = tk.Label(
            self.stats_frame,
            text="📊 Game Statistics",
            bg="white",
            fg="#1d3557",
            font=("Arial", 15, "bold")
        )
        self.stats_title.pack(pady=5)

        self.stats_label = tk.Label(
            self.stats_frame,
            text=self.get_stats_text(),
            bg="white",
            justify="left",
            font=("Consolas", 12)
        )
        self.stats_label.pack(pady=5)

        # ================= CONTROL BUTTONS =================
        self.control_frame = tk.Frame(
            self.main_frame,
            bg=backGroundColor
        )
        self.control_frame.pack(pady=10)

        self.toggle_chart_button = ttk.Button(
            self.control_frame,
            text="📊 Show Chart",
            style="Game.TButton",
            command=self.toggle_chart
        )
        self.toggle_chart_button.grid(row=0, column=0, padx=10)

        self.reset_button = ttk.Button(
            self.control_frame,
            text="🔄 Reset Game",
            style="Game.TButton",
            command=self.reset_game
        )
        self.reset_button.grid(row=0, column=1, padx=10)

        # ================= CHART FRAME =================
        self.chart_frame = tk.Frame(
            self.main_frame,
            bg=backGroundColor
        )

    def predict_player_move(self):
        if not self.player_history:
            return random.choice(self.moves)

        return Counter(self.player_history).most_common(1)[0][0]

    def get_ai_move(self):
        predicted = self.predict_player_move()

        counters = {
            "rock": "paper",
            "paper": "scissors",
            "scissors": "rock"
        }

        return counters[predicted]

    def determine_winner(self, player_move, ai_move):

        if player_move == ai_move:
            return "draw"

        win = {
            "rock": "scissors",
            "paper": "rock",
            "scissors": "paper"
        }

        return "player" if win[player_move] == ai_move else "ai"

    def play_round(self, player_move):

        ai_move = self.get_ai_move()
        result = self.determine_winner(player_move, ai_move)

        self.player_move_label.config(
            text=f"👤 Your Move: {player_move.capitalize()}"
        )

        self.ai_move_label.config(
            text=f"🤖 AI Move: {ai_move.capitalize()}"
        )

        if result == "player":
            self.player_score += 1
            self.player_wins += 1

            self.result_label.config(
                text="🎉 You Win!",
                fg="green"
            )

        elif result == "ai":
            self.ai_score += 1
            self.ai_wins += 1

            self.result_label.config(
                text="🤖 AI Wins!",
                fg="red"
            )

        else:
            self.draws += 1

            self.result_label.config(
                text="🤝 Draw!",
                fg="#ff9800"
            )

        self.player_history.append(player_move)
        self.rounds += 1

        self.stats_label.config(
            text=self.get_stats_text()
        )

        self.update_chart()

    def get_stats_text(self):

        return (
            f"Rounds Played : {self.rounds}\n"
            f"Player Score  : {self.player_score}\n"
            f"AI Score      : {self.ai_score}\n"
            f"Draws         : {self.draws}"
        )

    def update_chart(self):

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        labels = ["Player", "AI", "Draw"]
        values = [
            self.player_wins,
            self.ai_wins,
            self.draws
        ]

        fig = plt.Figure(figsize=(5, 3.5), dpi=100)

        ax = fig.add_subplot(111)

        ax.bar(labels, values)

        ax.set_title("Performance Chart")
        ax.set_ylabel("Wins")

        canvas = FigureCanvasTkAgg(
            fig,
            master=self.chart_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack()

    def toggle_chart(self):

        if self.chart_visible:

            self.chart_frame.pack_forget()

            self.toggle_chart_button.config(
                text="📊 Show Chart"
            )

            self.chart_visible = False

        else:

            self.chart_frame.pack(pady=10)

            self.update_chart()

            self.toggle_chart_button.config(
                text="❌ Hide Chart"
            )

            self.chart_visible = True

    def reset_game(self):

        self.player_history.clear()

        self.player_score = 0
        self.ai_score = 0
        self.rounds = 0

        self.player_wins = 0
        self.ai_wins = 0
        self.draws = 0

        self.result_label.config(
            text="Choose your move!",
            fg="#e63946"
        )

        self.player_move_label.config(
            text="👤 Your Move: None"
        )

        self.ai_move_label.config(
            text="🤖 AI Move: None"
        )

        self.stats_label.config(
            text=self.get_stats_text()
        )

        if self.chart_visible:
            self.update_chart()

        messagebox.showinfo(
            "Game Reset",
            "The game has been reset!"
        )


if __name__ == "__main__":

    root = tk.Tk()

    game = AIPoweredRPS(root)

    root.mainloop()