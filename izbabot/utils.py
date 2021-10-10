def get_beer_word(amount):
    if amount == 1:
        return 'piwo'
    elif amount in [2, 3, 4]:
        return 'piwa'
    else:
        return 'piw'