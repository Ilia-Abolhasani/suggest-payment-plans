import jdatetime
import numpy as np
from src.discount import get_discount
from src.feature_dates import get_date
from src.plan import get_plans
from src.price_variations import generate_price_variations


def score(raas_days, combination):
    w_balance = 0.5
    w_raas_days = 0.5
    # balance score
    if len(combination) < 2:
        return 0
    diffs = combination.copy()
    for i in range(len(diffs) - 1, 0, -1):
        diffs[i] -= diffs[i - 1]
    variance = np.var(diffs)
    balance_score = 1 / (1 + variance)
    return w_balance * balance_score + w_raas_days * raas_days


def suggest_payment_plans(
    start_date, total, cash_amount, check_number, number_of_months, config
):
    remain = total - cash_amount
    check_amount = remain // check_number
    dates = get_date(start_date, number_of_months, config)
    plans = get_plans(dates, start_date, check_number, number_of_months, config)
    print(len(plans))
    pricess = generate_price_variations(
        [check_amount for i in range(check_number)], config
    )
    # apply the reamin money for first check
    remain = remain - (check_amount * check_number)

    # calc duration between them
    duration = np.zeros(len(dates), int)
    for i in range(len(duration)):
        duration[i] = (dates[i] - start_date).days

    plans = plans * duration
    n = len(plans)
    non_zero = np.zeros((n, check_number), int)
    for i in range(0, n):
        p = plans[i]
        non_zero[i, :] = p[p != 0]

    pricess = np.array(pricess)
    raas_days = (np.dot(non_zero, pricess.T) / total).round()
    valid_plans = []
    for i in range(raas_days.shape[0]):
        check_date = None
        for j in range(raas_days.shape[1]):
            rass = raas_days[i, j]
            if rass <= config.max_raas_days:  # and rass >= 65:
                discount = get_discount(rass, config) / 100
                total_after_discount = total * (1 - discount)
                suggestion_price = pricess[j, :]  # todo* (1 - discount)
                if not check_date:
                    check_dates = []
                    for u in range(check_number):
                        days_to_add = int(non_zero[i, u])
                        date = start_date + jdatetime.timedelta(days=days_to_add)
                        check_dates.append((date, suggestion_price[u]))
                plan = {
                    "discount": discount,
                    "checks": check_dates,
                    "raas_days": rass,
                    "checks_days": non_zero[i, :],
                }
                valid_plans.append(plan)
    sorted_plans = sorted(
        valid_plans,
        key=lambda x: score(x["raas_days"] / config.max_raas_days, x["checks_days"]),
        reverse=True,
    )
    return sorted_plans
