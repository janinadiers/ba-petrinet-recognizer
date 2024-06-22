def use(X, candidate)-> dict:
    
    if (X[0] <= 50) and (X[1] < 0.24) and (X[2] < 0.24):
        return {'valid': {'rectangle': candidate}}
    elif (X[0] > 50) and (X[1] >= 0.24) and (X[2] >= 0.24):
        return {'valid': {'circle': candidate}}
    else:
        return {'invalid': candidate}
         