def get_trade_signal(symbol):
    # This is a simple mockup for now
    from random import choice

    directions = ["by", "sell", None]
    direction = choice(directions)

    if direction:
        return {
            "signal": direction,
            "entry_price": 2345.0,
            "sl": 2340.0,
            "tp": 2355.0,
            "confluences": "SMC + OB"
        }
    else:
        return None