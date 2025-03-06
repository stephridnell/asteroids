import json
import os
from typing import List, Tuple


class Score:
    def __init__(self):
        self.current_score = 0
        self.high_scores: List[Tuple[str, int]] = []
        self.score_file = "highscores.json"
        self.load_high_scores()

    def add_points(self, points: int) -> None:
        self.current_score += points

    def get_current_score(self) -> int:
        return self.current_score

    def reset_score(self) -> None:
        self.current_score = 0

    def load_high_scores(self) -> None:
        try:
            if os.path.exists(self.score_file):
                with open(self.score_file, 'r') as f:
                    self.high_scores = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading high scores: {e}")
            self.high_scores = []

    def save_high_scores(self) -> None:
        try:
            with open(self.score_file, 'w') as f:
                json.dump(self.high_scores, f)
        except IOError as e:
            print(f"Error saving high scores: {e}")

    def update_high_scores(self, player_name: str) -> None:
        # Add new score
        self.high_scores.append((player_name, self.current_score))
        # Sort by score (highest first)
        self.high_scores.sort(key=lambda x: x[1], reverse=True)
        # Keep only top 10
        self.high_scores = self.high_scores[:10]
        # Save to file
        self.save_high_scores()

    def get_high_scores(self) -> List[Tuple[str, int]]:
        return self.high_scores
