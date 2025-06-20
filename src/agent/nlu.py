def detect_intent(user_input: str) -> str:
    if "stock" in user_input.lower():
        return "stocks"
    elif "etf" in user_input.lower():
        return "ETFs"
    elif "customer" in user_input.lower():
        return "customers"
    elif "account" in user_input.lower():
        return "accounts"
    elif "transaction" in user_input.lower():
        return "transactions"
    return "stocks"
