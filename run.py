```python
import typer, pandas as pd, datetime as dt
from src.db import init, insert, fetch
from src.scraper import pull
from src.model import fit, grid
from src.kelly import stake
from src.telegram import send_lines
import asyncio

app = typer.Typer()

@app.command()
def update_db(league: str = "EPL", season: str = "2024-2025"):
    """Pull yesterday results + tomorrow fixtures."""
    init()
    df = pull(league, season)
    insert(df.assign(league=league, season=season))
    print(f"Stored {len(df)} matches")

@app.command()
def fit_model(league: str = "EPL", season: str = "2024-2025"):
    """Fit Dixon-Coles and cache params (pickle)."""
    df = fetch(league, season)
    params = fit(df)
    pd.to_pickle(params, f"{league}_params.pkl")
    print("Model fitted")

@app.command()
def notify_today(league: str = "EPL"):
    """Send today’s fixtures + Kelly to Telegram."""
    params = pd.read_pickle(f"{league}_params.pkl")
    today = dt.date.today()
    df    = fetch(league, "")          # all seasons
    fixtures = df[df.date == today]
    lines = []
    for _, r in fixtures.iterrows():
        g = grid(params, r.home_team, r.away_team)
        odds_home = 1 / g.home_win
        kelly = stake(g.home_win, odds_home)
        lines.append(
            f"{r.home_team} vs {r.away_team}\n"
            f"1X2: {g.home_win:.1%}  {g.draw:.1%}  {g.away_win:.1%}\n"
            f"Kelly: {abs(kelly):.2f}u on {'home' if kelly>0 else 'away'}"
        )
    asyncio.run(send_lines(lines))

if __name__ == "__main__":
    app()
