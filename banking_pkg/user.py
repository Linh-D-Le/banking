import sys, csv
from validator_collection import validators
import pwinput
import bcrypt



# balance = 0.0
def database():
    user_names = []
    with open("database.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_names.append(row)
    return user_names

def login():
    while True:
        print("\n-----Log in-----")
        username = input("Enter username: ").lower()
        user_names = database()
        data_name = [u["name"] for u in user_names if username == u["email"]]

        if data_name != []:
            data_password = [u["password"] for u in user_names if username == u["email"]]
            data_balance = [u["balance"] for u in user_names if username == u["email"]]
            record_balance = float(data_balance[0])

            tries = 0
            while True:
                if tries == 3:
                    sys.exit()
                password = pwinput.pwinput(prompt="Enter password: ", mask="*")
                
                # data_password[0] return a string
                # Need to remove b and '' out of the data_password[0] before encoding it from str to byte
                hashed_data_password = data_password[0][2:-1].encode("utf-8")
                hashed_password = bcrypt.hashpw(password.encode("utf-8"), hashed_data_password)

                if hashed_password == hashed_data_password:
                    print(f"Signed in as {data_name[0]}. Welcome back!")
                    return username, record_balance
                else:
                    print("Wrong password!")
                    tries += 1
        else:
            print("Username has not been registered yet. Please register first!")
            register()


def register():
    balance = 0.0
    print("\n-----Register-----\n")
    email = check_email()
    name, password = pass_rule()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    with open("database.csv", "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["email", "name", "password", "balance"])
        writer.writerow({"email":email, "name":name, "password":hashed_password, "balance":balance})
    

def check_email():
    tries = 0
    while True:
        if tries == 3:
            sys.exit()
        email = input("Enter an email to register: ").lower()
        try:
            if validators.email(email):
                users = database()
                e_list = []
                for e in users:
                    e_list.append(e["email"])
                if email in e_list:
                    print("This email has been taken. Please enter another email")
                    tries += 1
                else:
                    return email
        except:
            print("It is not an email")
            tries += 1
            continue

def pass_rule():
    f_name = input("Enter your first name: ").strip()
    l_name = input("Enter your last name: ").strip()
    name = f_name.title() + " " + l_name.title()
    tries = 0
    while True:
        if tries == 10:
            sys.exit()
        pw = pwinput.pwinput(prompt="Enter password: ", mask="*")
        
        if len(pw)<8 or len(pw)>20:
            print("Password must have a minimum 8 characters and a maximum of 20 characters")
            tries += 1
        elif " " in pw:
            print("Must not include any spaces")
            tries += 1
        elif f_name in pw or l_name in pw:
            print("Password must be different than your Name") 
            tries += 1 
        elif pw.isalnum() and pw.isalpha() or pw.isnumeric():
            print("Must have a minimum of one alpha character and minimum of one numeric character")
            tries += 1
        else:
            cf_pw = pwinput.pwinput(prompt="Confirm password: ", mask="*")
            if cf_pw != pw:
                print("Password is not mathching. Try again")
                tries +=1
            else:
                print("Account has been created\n")
                return name, pw

def transfer(authorized_user, balance):
    while True:
        receiver = input("\nEnter the receiver's username: ")
        user = database()
        receiver_balance = [u["balance"] for u in user if u["email"] == receiver]
        receiver_list = []
        for u in user:
            receiver_list.append(u["email"])
        if receiver in receiver_list and receiver != authorized_user:
            t_amount = float(input("\nHow much would you like to transfer?: $"))
            if t_amount > balance:
                print("Sorry, you can not make a transfer with amount larger than your balance")
            else:            
                return [t_amount, receiver, receiver_balance[0]]
        elif receiver == authorized_user:
            print("Unable to transfer money within an account")
        else:
            print(f"The account {receiver} is not available")
        while True:
            option = input("Would you like to try again? Y/N\n").upper()
            if option == "Y":
                break
            elif option == "N":
                quit
            else:
                print("Please try again!")
