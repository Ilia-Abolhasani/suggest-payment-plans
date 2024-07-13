def get_discount(raas_day, config):
    if raas_day < 5:
        return 20
    if raas_day < 10:
        return 19.5
    if raas_day < 15:
        return 19
    if raas_day < 20:
        return 18.25
    if raas_day < 25:
        return 17.5
    if raas_day < 30:
        return 16.25
    if raas_day < 35:
        return 15
    if raas_day < 40:
        return 13.5
    if raas_day < 45:
        return 12
    if raas_day < 50:
        return 10
    if raas_day < 55:
        return 8
    if raas_day < 60:
        return 5.5
    if raas_day < 65:
        return 3
    if raas_day < 70:
        return 0
    return get_discount(65 - (raas_day - 65))
