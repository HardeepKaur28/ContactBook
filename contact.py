from tabulate import tabulate
import json
import os
import re

# Load contacts from file if exists
if os.path.exists("contacts.json"):
    with open("contacts.json", "r") as f:
        contacts = json.load(f)
else:
    contacts = {}

def save_contacts():
    with open("contacts.json", "w") as f:
        json.dump(contacts, f, indent=4)

def is_valid_name(name):
    return bool(name.strip())

def is_valid_age(age):
    return age.isdigit() and 0 < int(age) < 120

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_mobile(mobile):
    return mobile.isdigit() and len(mobile) == 10

def is_unique_email(email, exclude_name=None):
    for contact_name, contact in contacts.items():
        if contact['email'].lower() == email.lower() and contact_name != exclude_name:
            return False
    return True

def is_unique_mobile(mobile, exclude_name=None):
    for contact_name, contact in contacts.items():
        if contact['mobile'] == mobile and contact_name != exclude_name:
            return False
    return True

while True:
    print('\nContact Book App')
    print('1. Create contact')
    print('2. View contact')
    print('3. Update contact')
    print('4. Delete contact')
    print('5. Search contact')
    print('6. Count contact')
    print('7. All contacts')
    print('8. Exit')

    choice = input("enter your choice : ")

    if choice == '1':
        print("Choice 1 Selected")
        name = input('Enter your name : ')
        if not is_valid_name(name):
            print("Invalid name! Name cannot be empty.")
            continue
        if name in contacts:
            print(f'Contact name {name} already exists!')
            continue

        age = input('Enter age : ')
        if not is_valid_age(age):
            print("Invalid age! Must be a number between 1-119.")
            continue

        email = input('Enter email : ')
        if not is_valid_email(email):
            print("Invalid email format!")
            continue
            # email unique check
        if any(contact['email'].lower() == email.lower() for contact in contacts.values()):
            print("Email already exists!")
            continue

        mobile = input('Enter mobile number : ')
        if not is_valid_mobile(mobile):
            print("Invalid mobile! Must be 10 digits.")
            continue
        # mobile unique check
        if any(contact['mobile'] == mobile for contact in contacts.values()):
            print("Mobile number already exists!")
            continue

        contacts[name] = {'age': int(age), 'email': email, 'mobile': mobile}
        save_contacts()
        print(f'Contact name {name} has been created successfully!')

    elif choice == '2':
        print("Choice 2 Selected")

        name = input('Enter contact name to view : ')
        if name in contacts:
            contact = contacts[name]
            print(f"Name : {name} , Age : {contact['age']} , Mobile Number: {contact['mobile']} , Email : {contact['email']}")
        else:
            print('Contact not found!!')

    elif choice == '3':
        print("Choice 3 Selected")

        name = input('Enter name to update contact : ')
        if name in contacts:
            age = input('Enter updated age : ')
            if not is_valid_age(age):
                print("Invalid age! Must be a number between 1-119.")
                continue

            email = input('Enter updated email : ')
            if not is_valid_email(email):
                print("Invalid email format!")
                continue
            if not is_unique_email(email, exclude_name=name):
                print("Email already exists!")
                continue

            mobile = input('Enter updated mobile number : ')
            if not is_valid_mobile(mobile):
                print("Invalid mobile! Must be 10 digits.")
                continue
            if not is_unique_mobile(mobile, exclude_name=name):
                print("Mobile number already exists!")
                continue

            contacts[name] = {'age': int(age), 'email': email, 'mobile': mobile}
            save_contacts()
            print(f'Contact "{name}" updated successfully!')
        else:
            print('Contact Not Found , Press 1 to Create contact.')

    elif choice == '4':
        print("Choice 4 Selected")

        name = input('Enter contact name to delete : ')
        if name in contacts:
            del contacts[name]
            save_contacts()
            print(f'Contact name {name} has been deleted successfully!!')
        else:
            print('Contact not found')

    elif choice == '5':
        print("Choice 5 Selected")

        search_name = input("Enter contact name to search : ")
        found = False
        for name, contact in contacts.items():
            if search_name.lower() in name.lower():
                print(f"Found - Name : {name} , Age : {contact['age']} , Mobile : {contact['mobile']} , Email : {contact['email']}")
                found = True
        if not found:
            print("No contact found with that name.")

    elif choice == '6':
        print("Choice 6 Selected")

        print(f'Total contacts in your book : {len(contacts)}')

    elif choice =='7':  # ya 2 ke jagah ya jo bhi tu chah
        print("Choice 7 Selected : All Contacts:")
        if not contacts:
            print("No contacts found.")
        else:
            table = []
            for name in sorted(contacts.keys()):
                contact = contacts[name]
                table.append([name, contact['age'], contact['mobile'], contact['email']])
            headers = ["Name", "Age", "Mobile", "Email"]
            print(tabulate(table, headers, tablefmt="grid"))

    elif choice == '8':
        print("Choice 8 Selected")

        print("Good bye.. Closing the program!!")
        break

    else:
        print('Invalid Input')

