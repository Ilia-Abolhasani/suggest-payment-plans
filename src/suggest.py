import jdatetime
import numpy as np
from src.discount import get_discount
from src.feature_dates import get_date
from src.plan import get_plans
from src.price_variations import generate_price_variations


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
    # duration_score
    duration_score = non_zero[:, -1] / (config.number_of_months * 30)
    duration_score *= config.w_duration
    # balance_score
    diffs = np.diff(non_zero, axis=1)
    variances = np.var(diffs, axis=1)
    balance_score = 1 / (1 + variances)
    balance_score *= config.w_balance

    indices = np.where(
        (raas_days < config.max_raas_days) & (raas_days > config.min_raas_days)
    )
    indices_list = list(zip(indices[0], indices[1]))
    valid_plans = []
    for i, j in indices_list:
        rass = raas_days[i, j]
        raas_score = rass / config.max_raas_days
        raas_score *= config.w_raas_days
        score = balance_score[i] + duration_score[i] + raas_score
        plan = {
            "i": i,
            "j": j,
            "score": score,
            "raas_days": rass,
            "combination": non_zero[i, :],
        }
        valid_plans.append(plan)
    sorted_plans = sorted(valid_plans, key=lambda x: x["score"], reverse=True)
    sorted_plans = sorted_plans[: config.max_answer]
    for plan in sorted_plans:
        rass = plan["raas_days"]
        i = plan["i"]
        j = plan["j"]
        discount = get_discount(rass, config) / 100
        total_after_discount = total * (1 - discount)
        suggestion_price = pricess[j, :]  # todo* (1 - discount)
        check_dates = []
        for u in range(check_number):
            days_to_add = int(non_zero[i, u])
            date = start_date + jdatetime.timedelta(days=days_to_add)
            check_dates.append((date, suggestion_price[u]))
        plan["discount"] = discount
        plan["checks"] = check_dates
        del plan["i"], plan["j"], plan["score"], plan["combination"]
    return sorted_plans
