#  Wird aufgerufen, bevor der rejector gestartet wird, um den besten Schwellwert für die Closed-Shape-Filterung zu bestimmen.
# Es werden Werte zwischen 0 und 1 getestet und die Anzahl der richtig abgelehnten Shapes wird gezählt.
threshold = 0

def next_threshold():
    global threshold
    threshold += 0.1
    return threshold

def get_threshold():
    global threshold
    return threshold