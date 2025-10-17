import pandas as pd
import requests, io
from datetime import date

BASE = "https://www.football-data.co.uk/mmz4281/{}/{}.csv"
CODES = {                     # season 2024-25 codes
    "EPL": ("2425", "E0"),    # England
    "E1":  ("2425", "E1"),
    "E2":  ("2425", "E2"),
    "WSL": ("2324", "W1"),    # Women’s Super League
    "D1":  ("2324", "D1"),    # Bundesliga
    "I1":  ("2324", "I1"),    # Serie A
    "SP1": ("2324", "SP1"),   # La Liga
    "F1":  ("2324", "F1"),    # Ligue 1
    "WCQ": ("2226", "WQ"),    # World Cup qualifiers
}

def pull(league: str, season: str) -> pd.DataFrame:
    code, div = CODES[league]
    url = BASE.format(code, div)
    df = pd.read_csv(io.StringIO(requests.get(url).text), encoding="ISO-8859-1")
    df = df.rename(columns={
        "Date": "date", "HomeTeam": "home_team", "AwayTeam": "away_team",
        "FTHG": "gh", "FTAG": "ga"
    })
    df["date"] = pd.to_datetime(df.date, dayfirst=True).dt.date
    df = df[["date", "home_team", "away_team", "gh", "ga"]].dropna()
    year = int(season[:4])
    df = df[(df.date >= date(year, 7, 1)) & (df.date < date(year+1, 7, 1))]
    return df.reset_index(drop=True)
