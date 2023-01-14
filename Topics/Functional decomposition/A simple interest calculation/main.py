def calculate(amount, interest_rate, time):
    # your code here
    interest = (amount * interest_rate * time) / 100
    total_amount = amount + interest
    return interest, total_amount


def print_result(interest, total_amount):
    # your code here
    print(f"The interest is: {interest}")
    print(f"The total amount is: {total_amount}")
