class UnknownDevice:
    def __init__(self, wattage=0, hours=0, days=1):
        self.wattage = wattage
        self.days = days
        self.hours = hours
        self.units = self.wattage_consumption()
        self.category = self.binary_calc_price_categ(self.units)

        self.S1 = 0
        self.S2 = 0
        self.S3 = 0
        self.S4 = 0
        self.S5 = 0
        self.S6 = 0
        self.S7 = 0

    def binary_calc_price_categ(self, unit):
        if unit > 350:
            if unit <= 550:
                return 5
            else:
                return 7
        if unit < 201:
            if unit > 100:
                return 3
            if unit > 50:
                return 2
            elif unit < 51:
                return 1
        return 3

    def wattage_consumption(self):
        """
        take time in mints, wattage in watt and convert time  to hours, watt to kilowatt
        to return unit.
        unit => total Wattage * Time / 10000
        :param days:
        :param hours:
        :param time_in_min:
        :param wattage: running Total wattage
        :return: unit => KWH
        """
        time_in_hours = self.hours * self.days
        try:
            unit = (self.wattage * time_in_hours) / 1000
        except ZeroDivisionError:
            unit = 0
        print(f'wattage_consumption : unit = {unit}')
        return unit

    def price_dictionary(self):
        """
        assign prices and return dictionary for the device consumption prices in all the 7 categories
        :return: dictionary
        """
        self.S1 = self.units * 0.30
        self.S2 = self.units * 0.40
        self.S3 = self.units * 0.50
        self.S4 = self.units * 0.82
        self.S5 = self.units * 1.0
        self.S6 = self.units * 1.40
        self.S7 = self.units * 1.45
        dic = {1: round(self.S1, 1), 2: round(self.S2, 1), 3: round(self.S3, 1), 4: round(self.S4, 1), 5: round(self.S5, 1), 6: round(self.S6, 1), 7: round(self.S7,1)}
        return dic


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
