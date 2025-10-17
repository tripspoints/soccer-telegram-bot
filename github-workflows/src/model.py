import numpy as np
from scipy.optimize import minimize

def _tau(x, y, rho):
    if (x, y) == (0, 0): return 1 - rho
    if (x, y) in ((1, 0), (0, 1)): return 1 + rho
    if (x, y) == (1, 1): return 1 - rho
    return 1.0

def fit(df, rho=0.0):
    teams = sorted(set(df.home_team) | set(df.away_team))
    n, t2i = len(teams), {t: i for i, t in enumerate(teams)}
    home = df.home_team.map(t2i).values
    away = df.away_team.map(t2i).values
    gh, ga = df.gh.values, df.ga.values

    def ll(par):
        atk, deff, ha = par[:n], par[n:2*n], par[2*n]
        ll = 0.0
        for h, a, x, y in zip(home, away, gh, ga):
            lam = np.exp(ha + atk[h] - deff[a])
            mu  = np.exp(atk[a] - deff[h])
            t   = _tau(x, y, rho)
            ll += np.log(t) + (x*np.log(lam) - lam - np.math.factorial(x)) + \
                              (y*np.log(mu)  - mu  - np.math.factorial(y))
        return -ll

    res = minimize(ll, np.zeros(2*n + 1), method="L-BFGS-B")
    atk, deff, ha = res.x[:n], res.x[n:2*n], res.x[2*n]
    return {"teams": teams, "atk": dict(zip(teams, atk)),
            "def": dict(zip(teams, deff)), "home_adv": ha, "rho": rho}

def grid(params, home, away, max_goals=15):
    atk, deff, ha, rho = params["atk"], params["def"], params["home_adv"], params["rho"]
    lam = np.exp(ha + atk[home] - deff[away])
    mu  = np.exp(atk[away] - deff[home])
    g = np.zeros((max_goals+1, max_goals+1))
    for i in range(max_goals+1):
        for j in range(max_goals+1):
            g[i, j] = _tau(i, j, rho) * (lam**i * np.exp(-lam) / np.math.factorial(i)) * \
                                        (mu**j * np.exp(-mu) / np.math.factorial(j))
    g /= g.sum()
    home_win = g.tril(-1).sum()
    draw     = g.diagonal().sum()
    away_win = g.triu(1).sum()
    class Out:
        home_win, draw, away_win = home_win, draw, away_win
        btts_yes = 1 - (g[0, 0] + g[1:, 0].sum() + g[0, 1:].sum())
        over_25  = 1 - g[:3, :3].sum()
    return Out()
