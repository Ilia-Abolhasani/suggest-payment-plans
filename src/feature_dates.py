import jdatetime


def get_date(start_date, number_of_months, config):
    dates = []
    current_date = start_date
    first_check_date = start_date + jdatetime.timedelta(days=config.start_shift_days)

    for _ in range(number_of_months):
        year = current_date.year
        month = current_date.month

        for day in config.acceptable_days:
            try:
                temp = jdatetime.date(year, month, day)
                if temp < first_check_date:
                    continue
                dates.append(temp)
            except ValueError:
                continue

        # Move to the next month
        if month == 12:
            current_date = jdatetime.date(year + 1, 1, 1)
        else:
            current_date = jdatetime.date(year, month + 1, 1)

    return dates
