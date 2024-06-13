def use(X, candidate)-> dict:
    if X[0] < 800:
        return {'valid': candidate}
    else:
        return {'invalid': candidate}