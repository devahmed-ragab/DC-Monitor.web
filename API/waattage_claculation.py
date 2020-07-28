
def bill_calc(units):
    """
    this function takes the KWH usage on return it's price (EGP)
    based on it's sugment.
    :param units: double
    :return bill: double
    """
    bill = 0.0

    if units < 51:
        bill = units * 0.30
    elif 51 <= units <= 100:  # 49kwh
        bill = (50 * 0.30) + ((units - 50) * 0.40)
    elif 100 < units <= 200:
        # break point
        bill = units * 0.50
    elif 201 <= units <= 350:  # 150kwh
        bill = (200 * 0.50) + ((units - 200) * 0.82)
    elif 351 <= units <= 650:  # 301kwh
        bill = (200 * 0.50) + (150 * 0.82) + ((units - 350) * 1)
    elif 651 <= units <= 1000:  # 351kwh
        bill = (200 * 0.50) + (150 * 0.82) + 300 + ((units - 650) * 1.40)
    elif units > 1000:  # 1000kwh
        # break point
        bill = units * 1.45

    return bill