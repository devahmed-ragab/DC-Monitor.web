def calc_price_categ(consumption):
    bill = 0.0
    if consumption < 51:
        return 1
    elif 51 <= consumption <= 100:  # 49kwh
        return 2
    elif 100 < consumption <= 200:
        return 3
    elif 201 <= consumption <= 350:  # 150kwh
        return 4
    elif 351 <= consumption <= 650:  # 301kwh
        return 5
    elif 651 <= consumption <= 1000:  # 351kwh
        return 6
    return 7


def Binary_calc_price_categ(c):
    if c > 350:
        if c <= 550:
            return 5
        else:
            return 7
    if c < 201:
        if c > 100:
            return 3
        if c > 50:
            return 2
        elif c < 51:
            return 1
    return 3
