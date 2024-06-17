def use(X, candidate)-> dict:
    print('in rejector')
    print('X', X)
    if X[0] < 800:
        return {'valid': candidate}
    else:
        return {'invalid': candidate}