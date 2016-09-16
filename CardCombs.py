import itertools

def CardCombs(deck):
    deck_comb = list(itertools.combinations(deck,6))
    
    return deck_comb