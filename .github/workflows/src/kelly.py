def stake(prob, odds, frac=0.25):
    k = (prob * odds - 1) / (odds - 1) if odds != 1 else 0
    return 0.0 if k < 0.01 else k * frac
