def use(X, candidate)-> dict:
    
    if X[0] < 0.53:
        return {'valid': candidate}
    else:
        return {'invalid': candidate}