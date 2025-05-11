import tkinter as tk
from tkinter import ttk
import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class GameDataViewer(tk.Tk):
    def __init__(self, csv_file="game_data.csv"):
        super().__init__()
        self.title("Game Data Viewer")
        self.geometry("600x400")
        self.csv_file = csv_file

        self.columns = ("name", "round", "success_defeat", "health_remain", "win_in", "score")
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center", width=100)

        self.tree.pack(fill="both", expand=True)

        self.load_csv()

        # Buttons
        tk.Button(self, text="Boxplot (Time to Win)", command=self.show_boxplot).pack(pady=2)
        tk.Button(self, text="Histogram (Health)", command=self.show_histogram).pack(pady=2)
        tk.Button(self, text="Scatter (Score by Player)", command=self.show_scatter).pack(pady=2)
        tk.Button(self, text="Boss Defeat Mode", command=self.show_mode).pack(pady=2)
        tk.Button(self, text="Quit", command=self.destroy).pack(pady=5)

    def load_csv(self):
        try:
            with open(self.csv_file, newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    values = tuple(row.get(col, "") for col in self.columns)
                    self.tree.insert("", "end", values=values)
        except FileNotFoundError:
            print(f"CSV file '{self.csv_file}' not found.")

    def load_dataframe(self):
        df = pd.read_csv(self.csv_file)
        # Clean and convert
        for col in ["success_defeat", "health_remain", "win_in", "score"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        return df

    def show_boxplot(self):
        df = self.load_dataframe()
        df["win_in"] = df["win_in"] / 1000  # Convert ms to seconds
        sns.boxplot(y=df["win_in"].dropna())
        plt.title("Time to Win (seconds)")
        plt.ylabel("Seconds")
        plt.show()

    def show_histogram(self):
        df = self.load_dataframe()
        df["health_remain"].dropna().hist(bins=10)
        plt.title("Health Remaining Histogram")
        plt.xlabel("Health")
        plt.ylabel("Frequency")
        plt.show()

    def show_scatter(self):
        df = self.load_dataframe()
        df = df.dropna(subset=["score"])
        df["attempt"] = df.groupby("name").cumcount() + 1
        sns.scatterplot(data=df, x="attempt", y="score", hue="name")
        plt.title("Player Scores Over Time")
        plt.xlabel("Attempt Number")
        plt.ylabel("Score")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()

    def show_mode(self):
        df = self.load_dataframe()
        mode_val = df["success_defeat"].mode().iloc[0]
        count = (df["success_defeat"] == mode_val).sum()

        df["success_defeat"].value_counts().plot(kind="bar")
        plt.title("Number of Bosses Defeated")
        plt.xlabel("Bosses Defeated")
        plt.ylabel("Frequency")
        plt.show()


