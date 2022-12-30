def deposit(balance):
    amount = float(input("How much would you like to deposit?: $"))
    return(balance + amount)

def withdraw(balance):
    while True:
        amount = float(input("How much would you like to withdraw? $"))
        if amount > balance:
            print("Your withdraw amount is larger than your balance.")
            print("Please enter another amount!")
        else:
            return(balance - amount)

