from sqlalchemy import create_engine, text
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).parent.parent / "data.db"
engine  = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)

def init():
    with engine.begin() as con:
        con.execute(text("""
            CREATE TABLE IF NOT EXISTS matches(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE, league TEXT, season TEXT,
                home_team TEXT, away_team TEXT, gh INTEGER, ga INTEGER);
            CREATE UNIQUE INDEX IF NOT EXISTS ux_match
                ON matches(date, league, home_team, away_team);
        """))

def insert(df: pd.DataFrame):
    df.to_sql("matches", engine, if_exists="append", index=False, method="multi")

def fetch(league: str, season: str) -> pd.DataFrame:
    return pd.read_sql(
        "SELECT * FROM matches WHERE league=? AND season=?",
        engine, params=(league, season)
    )
