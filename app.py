import sys
from banking_pkg.account import deposit, withdraw
from banking_pkg.user import login, register, transfer
import pandas as pd



authorized_user = ""

def main():
    while True:
        option = input("Press '1' to log in"
                        "\nPress '2' to register"
                        "\nPress 'E' to exit\n").upper()
        if option == "1":
            authorized_user, balance = login()
            
            menu(authorized_user, balance)
        elif option == "2":
            register()
        elif option == "E":
            print("Good bye!")
            sys.exit()
        else:
            print("Please enter a valid input\n")

def menu(authorized_user, balance):
    print("\n-----Menu-----")
    while True:
        option = input("\nPress 'D' to deposit\n"
                "Press 'W' to withdraw\n"
                "Press 'B' to check balance\n"
                "Press 'T' to transfer\n"
                "Press'E' to exit\n").upper()
        if option == "D":
            print("\n-----Deposit-----")
            balance = deposit(balance)
            print(f"Your balance is ${balance}")
            update_balance(authorized_user, balance)  
            
        elif option == "W":
            print("\n-----Withdraw-----")
            balance = withdraw(balance)
            print(f"Your balance is ${balance}")
            update_balance(authorized_user, balance)            

        elif option == "B":
            print("\n-----Balance-----")
            print(f"Your balance is ${balance}")       
        elif option == "T":
            print("\n-----Transfer-----")
            t = transfer(authorized_user, balance)
            t_amount = t[0]
            receiver = t[1]
            receiver_balance = float(t[2])
            update_balance(authorized_user, balance-t_amount)
            update_balance(receiver, receiver_balance + t_amount)
            print(f"You just made a transfer of ${t_amount} to {receiver}\n")
        elif option == "E":
            sys.exit("Good bye!")
        else:
            print("Please enter a correct letter!")

def update_balance(authorized_user, balance):
    # reading the csv file
    data = pd.read_csv("database.csv", on_bad_lines="skip")

    # updating the column value/data
    data.loc[data["email"]==authorized_user, "balance"] = balance
    # writing into the file
    data.to_csv("database.csv", index=False)
    return data



if __name__ == "__main__":
    main()