import random


def generate_price_variations(prices, config):
    m = config.max_price_change

    def adjust_prices(prices):
        new_prices = prices.copy()
        for i in range(len(new_prices)):
            change = random.randint(-m, m)
            new_prices[i] += change
            new_prices[i] = max(new_prices[i], 0)
        # Adjust to make sure the sum remains the same
        total_change = sum(new_prices) - sum(prices)
        if total_change != 0:
            adjust_index = random.randint(0, len(new_prices) - 1)
            new_prices[adjust_index] -= total_change
            # Ensure price doesn't go below 0
            new_prices[adjust_index] = max(new_prices[adjust_index], 0)
        return new_prices

    variations = {}
    for _ in range(config.number_of_generated_pricess):
        v = adjust_prices(prices)
        if 0 in v:
            continue
        variations[str(v)] = v
    return list(variations.values())
