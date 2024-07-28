import sys
import json
import math
import random
import jdatetime

# from typing import Union, List

from src.suggest import suggest_payment_plans


class DotDict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def run(
    start_date_year: int,
    start_date_month: int,
    start_date_day: int,
    total: float,
    cash_amount: float,
    number_of_month: int,
    check_number: int,
    # config params
    max_discount_percentage: float,
    max_raas_days: int,
    max_price_change: int = 3,
    number_of_generated_pricess: int = 100,
):
    # Type and range checks
    assert 1 <= start_date_day <= 31, "start_date_day must be between 1 and 31"
    assert 1 <= start_date_month <= 12, "start_date_month must be between 1 and 12"
    assert start_date_year >= 1403, "start_date_year must be 1403 or later"
    assert isinstance(total, float), "total must be a float"
    assert isinstance(cash_amount, float), "cash_amount must be a float"
    assert cash_amount < total, "cash_amount must be less than total"
    assert 1 <= number_of_month <= 7, "number_of_month must be between 1 and 7"
    assert (
        1 <= check_number <= number_of_month * 2
    ), "check_number must be between 1 and number_of_month * 2"
    assert (
        0 < max_discount_percentage < 0.3
    ), "max_discount_percentage must be a float between 0 and 0.3"

    assert max_raas_days >= 30, "max_raas_days must be greater than 30"

    # config file
    config = DotDict(
        {
            "max_discount_percentage": max_discount_percentage,
            "max_raas_days": max_raas_days,
            "max_price_change": max_price_change,
            "number_of_generated_pricess": number_of_generated_pricess,
            "start_shift_days": 20,
            "acceptable_days": [5, 10, 15, 20, 25, 30],
        }
    )
    # Call function
    start_date = jdatetime.date(start_date_year, start_date_month, start_date_day)

    suggested_plan = suggest_payment_plans(
        start_date, total, cash_amount, check_number, number_of_month, config
    )
    return suggested_plan


def disp(plan):
    print("raas_days", plan["raas_days"])
    print("discount", str(plan["discount"] * 100) + "%")
    for check in plan["checks"]:
        formatted_date = check[0].strftime("%Y,%m,%d")
        print((formatted_date, check[1]))


if __name__ == "__main__":
    input_json = sys.stdin.read()
    input_data = json.loads(input_json)
    output_data = run(**input_data)
    print(json.dumps(output_data, default=str))
    """
    suggested_plan = run(
        start_date_year=1403,
        start_date_month=8,
        start_date_day=20,
        total=100.0,
        cash_amount=20.0,
        number_of_month=3,
        check_number=3,
        max_discount_percentage=0.2,
        max_raas_days=65,
        max_price_change=3,
        number_of_generated_pricess=100,
    )
    print("total answer:", len(suggested_plan))
    print()
    print("===============================================")
    print()

    for plan in suggested_plan[:100]:
        disp(plan)
        print()
        print("===============================================")
        print()
    """
