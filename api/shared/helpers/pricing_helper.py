

def calc_movement(increase: float, price: float) -> float:
    if increase is None or price is None or price == 0:
        return 0
    return (increase / price) * 100


def calc_total_change(holding: float, change: float) -> float:
    if holding is None or change is None:
        return 0
    return (holding * change)


def calc_total(holding: float, price: float) -> float:
    if holding is None or price is None:
        return 0
    return (holding * price)


def calc_change(price: float, open: float) -> float:
    if price is None or open is None:
        return 0
    return (price - open)
