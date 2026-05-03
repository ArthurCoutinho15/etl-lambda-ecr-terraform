import os
import requests

import pandas as pd
from dotenv import load_dotenv


class ApiFootballHandler:
    load_dotenv()

    def __init__(self):
        self.token: str = os.getenv("API_TOKEN")
        self.url = "https://v3.football.api-sports.io/fixtures?team=121&season=2024"

    def _build_headers(self) -> dict:
        if not self.token:
            raise ValueError("API_TOKEN não configurado")

        return {
            "x-apisports-key": self.token,
        }

    def _make_request(self) -> dict:
        try:
            response = requests.request("GET", self.url, headers=self._build_headers())
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Error making request: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def extract_data(self, data: dict) -> pd.DataFrame:
        clean_data = []

        for match in data["response"]:
            ternary_winner = (
                match["teams"]["home"]["name"]
                if match["teams"]["home"]["winner"] == "True"
                else match["teams"]["away"]["name"]
            )
            row = {
                "date": match["fixture"]["date"],
                "referee": match["fixture"]["referee"],
                "venue": f"{match['fixture']['venue']['name']}, {match['fixture']['venue']['city']}",
                "home_team": match["teams"]["home"]["name"],
                "away_team": match["teams"]["away"]["name"],
                "home_goals": match["goals"]["home"],
                "away_goals": match["goals"]["away"],
                "league": match["league"]["name"],
                "winner": ternary_winner,
                "status": match["fixture"]["status"]["short"],
            }
            clean_data.append(row)

        return pd.DataFrame(clean_data)

    def run(self) -> pd.DataFrame:
        raw_data = self._make_request()
        clean_data = self.extract_data(raw_data)

        return clean_data
