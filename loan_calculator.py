import math


print("""What do you want to calculate?
    Type 'n' - for number of monthly payments
    Type 'p' - for the loan principal
    Type 'a' for the annuity monthly payment amount""")
cmd = str(input())

if cmd == "n":
    print("Enter the loan principal:")
    loan_principal = int(input())
    print("Enter the monthly payment:")
    payment = int(input())
    print("Enter the annual interest rate:")
    api = float(input())
    monthly_rate = float(api / (12 * 100))
    period = math.ceil(math.log((payment / (payment - monthly_rate * loan_principal)), 1 + monthly_rate))
    years = int(period / 12)
    months = period - years * 12
    if period == 1:
        print(f'It will take {int(period)} month to repay the loan')
    if period == 12:
        print(f'It will take {years} year to repay the loan')
    elif period % 12 == 0:
        print(f'It will take {years} years to repay the loan')
    elif period > 12 and months == 1:
        print(f'It will take {years} years and {months} month to repay the loan')
    elif period > 12 and months != 1:
        print(f'It will take {years} years and {months} months to repay the loan')
    elif period == 12 and months == 1:
        print(f'It will take {years} year and {months} month to repay the loan')
    elif period == 12 and months != 1:
        print(f'It will take {years} year and {months} month to repay the loan')

if cmd == "a":
    print("Enter the loan principal:")
    loan_principal = int(input())
    print("Enter the number of periods:")
    periods = int(input())
    print("Enter the annual interest:")
    api = float(input())
    monthly_rate = float(api / (12 * 100))
    payment = math.ceil(loan_principal * (monthly_rate * (pow(1 + monthly_rate, periods)
                                                          / (pow(1 + monthly_rate, periods) - 1))))
    print(f'Your monthly payment = {int(payment)}!')

if cmd == "p":
    print("Enter the annuity payment:")
    payment = float(input())
    print("Enter the number of periods:")
    periods = int(input())
    print("Enter the annual interest:")
    api = float(input())
    monthly_rate = float(api / (12 * 100))
    loan_principal = payment / ((monthly_rate * pow(1 + monthly_rate, periods)) / (pow(1 + monthly_rate, periods) - 1))
    print(f'Your loan principal = {loan_principal:0.2f}')
