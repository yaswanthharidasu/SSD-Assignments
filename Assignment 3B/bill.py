from flask import json
import requests
from requests.sessions import Session
import random
import datetime

launch_option = 0
username = "###"
password = "###"

# Stores menu items
items = dict()

# Stores data related orders
ordered_items_count = 0
ordered_items_full = dict()
ordered_items_half = dict()
tip_percentage = 0
items_amount = 0
tip_amount = 0
total_amount = 0
draw_amount = 0
no_of_persons = 0
contribution_per_person = 0

# Data related lucky draw
interested = 0
draw_result = 0

session = requests.Session()

# ====================================== Authentication ===========================================


def signup():
    username = input("Enter username:")
    password = input("Enter password:")
    user = {
        "username": username,
        "password": password
    }
    jsonObj = json.dumps(user)
    response = session.post(
        'http://localhost:8080/signup', json=jsonObj).content
    response = response.decode()
    response = json.loads(response)
    print("========================================")
    print(response["message"])
    print("========================================")
    print()
    print()


def signin():
    global username, password
    username = input("Enter username:")
    password = input("Enter password:")
    user = {
        "username": username,
        "password": password
    }
    jsonObj = json.dumps(user)
    response = session.post(
        'http://localhost:8080/signin', json=jsonObj).content
    response = response.decode()
    response = json.loads(response)
    print("========================================")
    print(response["message"])
    print("========================================")
    print()
    print()
    return response["type"]


def signout():
    global username, password
    response = session.get(
        'http://localhost:8080/signout').content
    # print(response)
    response = response.decode()
    response = json.loads(response)
    print(response["message"])
    username = "###"
    password = "###"
    print()
    print()
    return response["status"]

# ======================================== Common methods =========================================


def retrieve_menu():
    response = session.get(
        'http://localhost:8080/retrieveMenu').content
    response = response.decode()
    response = json.loads(response)
    for item in response:
        items[int(item)] = [response[item]["half"], response[item]["full"]]


def print_menu():
    """ Displays the menu in the format:
        <id>, <half_amount>, <full_amount>
    """
    if(len(items) == 0):
        print("========================================")
        print('No items in the menu. Sorry :(')
        print("========================================")
    else:
        print("===============================================================")
        print("ID\t\tHalf\t\tFull:")
        print("----------------------------------------")
        for i in items:
            print(i, "%.2f" % items[i][0], "%.2f" % items[i][1], sep="\t\t")
        print("===============================================================")
    print()


def take_order():
    """ Takes the order and tip percentage as input from the user
        Enter number of items to order and then details of each order
    """
    global ordered_items_count, tip_percentage
    print("Order Details:")
    print("-------------------------------------------------------")
    print("Enter no.of items to order:", end=" ")
    ordered_items_count = int(input())
    for i in range(ordered_items_count):
        print("-------------------------------------------------------")
        print("Enter Item", i + 1, "details:")
        print("Item Id:", end=" ")
        a = int(input())
        print("Half(1)/Full(2):", end=" ")
        b = int(input())
        while b != 1 and b != 2:
            print("Enter 1 for half and 2 for full:", end=" ")
            b = int(input())
        print("Quantity:", end=" ")
        c = int(input())
        if b == 1:
            if a in ordered_items_half:
                ordered_items_half[a] += c
            else:
                ordered_items_half[a] = c
        elif b == 2:
            if a in ordered_items_full:
                ordered_items_full[a] += c
            else:
                ordered_items_full[a] = c

    print("-------------------------------------------------------")
    print("Enter the tip percentage(0/10/20) in numbers:", end=" ")
    tip_percentage = int(input())
    print()
    print()


def generate_bill():
    ''' Generates the total amount after including the tip '''
    global items_amount, tip_amount, ordered_items, total_amount
    print("Bill Contribution:")
    print("-------------------------------------------------------")

    for i in ordered_items_full:
        item = items[i]
        items_amount += item[1] * ordered_items_full[i]

    for i in ordered_items_half:
        item = items[i]
        items_amount += item[0] * ordered_items_half[i]

    tip_amount = (tip_percentage / 100) * items_amount
    total_amount = items_amount + tip_amount
    print("Total amount to be paid:", "%.2f" % total_amount)


def split_bill():
    """ Splits the total amount based on the number of persons and
        displays the amount each person has to contribute
    """
    global no_of_persons, contribution_per_person
    print("Enter no.of persons:", end=" ")
    no_of_persons = int(input())
    contribution_per_person = total_amount / no_of_persons
    print("Each person has to contribute:", "%.2f" % contribution_per_person)
    print()


def test_luck():
    """ Takes input from the user whether they are interested
        in the lucky draw or not
    """
    print()
    print("Lucky Draw")
    print("-------------------------------------------------------")
    print('The restaurant has started a limited time event called',
          '"Test your luck".')
    print("Do you want to participate in this event?")
    print("If YES enter 1, otherwise enter 0: ", end="")
    global interested, draw_result, popluation, chances
    interested = int(input())
    print()


def lucky_draw_result():
    """ Displays the discount/increase value obtained in the lucky draw and
        prints the pattern based on the result
    """
    global draw_result, draw_amount
    print()
    print("Lucky Draw Result:")
    print("-------------------------------------------------------")
    rand = random.randint(1, 101)
    if rand <= 5:
        draw_result = -50
        print("Hurrah!!, You get a 50% discount off the bill")
    elif rand > 5 and rand <= 15:
        draw_result = -25
        print("Hurrah!!, You get a 25% discount off the bill")
    elif rand > 15 and rand <= 30:
        draw_result = -10
        print("Hurrah!!, You get a 10% discount off the bill")
    elif rand > 30 and rand <= 50:
        draw_result = 0
        print("You got nothing")
    else:
        draw_result = 20
        print("Oops!!, You need to pay extra 20% off the bill")

    draw_amount = (draw_result / 100) * total_amount
    print("Discount/Increase:", "%.2f" % draw_amount)
    print()
    if draw_result < 0:
        for i in range(5):
            if i == 0 or i == 4:
                print(" ****            **** ")
            else:
                print("|    |          |    |")
        print()
        print("          {}          ")
        print()
        print("    ______________    ")
    else:
        for i in range(6):
            if i == 0 or i == 5:
                print(" **** ")
            else:
                print("*    *")

    print()


def bill_breakdown():
    """ Displays the total bill and the amount each person
        has to contribute after the lucky draw
    """
    print()
    print("Final Bill:")
    print("-------------------------------------------------------")
    for i in ordered_items_half:
        print(
            "Item ", i, " [Half] [", ordered_items_half[i], "]: ",
            "%.2f" % (ordered_items_half[i] * items[i][0]),
            sep=""
        )
    for i in ordered_items_full:
        print(
            "Item ", i, " [Full] [", ordered_items_full[i], "]: ",
            "%.2f" % (ordered_items_full[i] * items[i][1]),
            sep=""
        )
    print("Total Value:", "%.2f" % items_amount)
    print("Tip Percentage: ", tip_percentage, "%", sep="")
    print("Discount/Increase:", "%.2f" % draw_amount)
    print("Final Total:", "%.2f" % (total_amount + draw_amount))
    print()
    print("Each person has to contribute Rs.", "%.2f" %
          ((total_amount + draw_amount) / no_of_persons))
    print("===============================================================")
    print()
    print()


def display_transactions():
    response = session.get(
        'http://localhost:8080/getTransactions/{}'.format(username)).content
    response = response.decode()
    response = json.loads(response)
    transactions = dict()
    for trans in response:
        transactions[int(trans)] = {"tip_percentage": response[trans]["tip_percentage"],
                                    "no_of_persons": response[trans]["no_of_persons"],
                                    "half_items": json.loads(response[trans]["half_items"]),
                                    "full_items": json.loads(response[trans]["full_items"]),
                                    "items_amount": response[trans]["items_amount"],
                                    "total_amount": response[trans]["total_amount"],
                                    "draw_amount": response[trans]["draw_amount"],
                                    "date": response[trans]["date"]}

    if len(transactions) == 0:
        print("========================================")
        print('No recent orders. Order now!!')
        print("========================================")
    else:
        print("There are", len(transactions), "previous orders")
        print("===============================================================")
        print("ID\t\tDate:")
        print("----------------------------------------")
        for trans in transactions:
            print(trans, transactions[trans]["date"], sep="\t\t")
        print("===============================================================")
        id = int(input("Enter order ID to check the bill:"))
        if(id > len(transactions)):
            print("Enter valid order ID")
        else:
            ordered_items_half = transactions[id]["half_items"]
            ordered_items_full = transactions[id]["full_items"]
            tip_percentage = transactions[id]["tip_percentage"]
            no_of_persons = transactions[id]["no_of_persons"]
            items_amount = transactions[id]["items_amount"]
            draw_amount = transactions[id]["draw_amount"]
            total_amount = transactions[id]["total_amount"]
            print()
            print()
            print("===============================================================")
            print("Bill for order", id, ":")
            print("----------------------------------------")
            for i in ordered_items_half:
                print(
                    "Item ", i, " [Half] [", ordered_items_half[i], "]: ",
                    "%.2f" % (ordered_items_half[i] * items[int(i)][0]),
                    sep=""
                )
            for i in ordered_items_full:
                print(
                    "Item ", i, " [Full] [", ordered_items_full[i], "]: ",
                    "%.2f" % (ordered_items_full[i] * items[int(i)][1]),
                    sep=""
                )
            print("Total Value:", "%.2f" % items_amount)
            print("Tip Percentage: ", "%.2f" % tip_percentage, "%", sep="")
            print("Discount/Increase:", "%.2f" % draw_amount)
            print("Final Total:", "%.2f" % (total_amount + draw_amount))
            print()
            print("Each person has to contribute Rs.", "%.2f" %
                  ((total_amount + draw_amount) / no_of_persons))
            print("===============================================================")
    print()
    print()

# ========================================= User Route ============================================


def store_transaction():
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transaction = {
        "username": username,
        "tip_percentage": tip_percentage,
        "no_of_persons": no_of_persons,
        "half_items": ordered_items_half,
        "full_items": ordered_items_full,
        "items_amount": items_amount,
        "total_amount": total_amount,
        "draw_amount": draw_amount,
        "date": str(date)
    }
    jsonObj = json.dumps(transaction)
    response = session.post(
        'http://localhost:8080/storeTransaction', json=jsonObj).content
    response = response.decode()
    response = json.loads(response)
    print("========================================")
    print(response["message"])
    print("========================================")
    print()
    print()


def user_route():
    print("Welcome", username)
    while(1):
        print("Options:")
        print("----------------------------------------")
        print("1. Display Menu")
        print("2. Order items")
        print("3. Display Transactions")
        print("4. Signout")
        print("----------------------------------------")
        option = int(input("Enter an option:"))
        print()
        retrieve_menu()
        if option == 1:
            retrieve_menu()
            print_menu()
        elif option == 2:
            take_order()
            generate_bill()
            split_bill()
            test_luck()
            if interested:
                lucky_draw_result()
            bill_breakdown()
            # Store into db
            store_transaction()
        elif option == 3:
            display_transactions()
        elif option == 4:
            response = signout()
            if response:
                break
        else:
            print("Enter valid option")


# ========================================= Chef Route ============================================

def add_item():
    item_id = int(input("Enter item id:"))
    half = int(input("Enter half item cost:"))
    full = int(input("Enter full item cost:"))
    item = {
        "id": item_id,
        "half": half,
        "full": full
    }
    jsonObj = json.dumps(item)
    response = session.post(
        'http://localhost:8080/addItem', json=jsonObj).content
    response = response.decode()
    response = json.loads(response)
    print("========================================")
    print(response["message"])
    print("========================================")
    print()


def chef_route():
    print("Hello Chef!!!")
    while(1):
        print("Options:")
        print("----------------------------------------")
        print("1. Display Menu")
        print("2. Add an Item to Menu")
        print("3. Order Items")
        print("4. Display Previous Transactions")
        print("5. Signout")
        print("----------------------------------------")
        option = int(input("Enter an option:"))
        print()
        if option == 1:
            retrieve_menu()
            print_menu()
        elif option == 2:
            add_item()
        elif option == 3:
            take_order()
        elif option == 4:
            display_transactions()
        elif option == 5:
            response = signout()
            if response:
                break
        else:
            print("Enter valid option")

# ======================================== main () ====================================================


def launch():
    global launch_option
    while(1):
        print("Options:")
        print("----------------------------------------")
        print("1. Signup")
        print("2. Signin")
        print("----------------------------------------")
        launch_option = int(input("Enter an option:"))
        print()
        if launch_option == 1:
            signup()
        elif launch_option == 2:
            response = signin()
            if response == "chef":
                chef_route()
            elif response == "user":
                user_route()
        else:
            print("Enter valid Option")


launch()
