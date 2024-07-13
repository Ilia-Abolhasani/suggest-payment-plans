import numpy as np


def get_plans(dates, start_date, number_of_checks, number_of_months, config):
    plans = []
    max_depth = len(dates)

    def get_selected_dates(ans, index=0, in_month_check=0, total_checkd=0):
        if total_checkd == number_of_checks:
            plans.append(ans)

        elif index >= max_depth:
            return

        elif in_month_check == 0:
            # for selection
            temp_ans = ans.copy()
            temp_ans[index] = 1
            if index + 2 < max_depth and dates[index].month == dates[index + 2].month:
                in_month_check = 1
            get_selected_dates(temp_ans, index + 2, in_month_check, total_checkd + 1)
            # for not selection
            temp_ans = ans.copy()
            get_selected_dates(temp_ans, index + 1, 0, total_checkd)

        elif in_month_check == 1:
            # for selection
            temp_ans = ans.copy()
            temp_ans[index] = 1
            counter = 0
            for i in range(index + 1, max_depth):
                if dates[index].month != dates[i].month:
                    break
                counter += 1
            counter = max(counter, 2)
            get_selected_dates(temp_ans, index + counter, 0, total_checkd + 1)
            # for not selection
            temp_ans = ans.copy()
            if index + 1 < max_depth and dates[index].month != dates[index + 1].month:
                in_month_check = 0
            get_selected_dates(temp_ans, index + 1, in_month_check, total_checkd)

    ans = np.zeros(max_depth, int)
    get_selected_dates(ans.copy())
    return plans
