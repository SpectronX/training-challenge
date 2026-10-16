from db_func import *

print("Welcome to the Group Contribution Tracker! \n")

print("1. Create a new group (press 100 to create a new group)")

print("\nGroups present on the system: ")

try:
    groups = list_groups()
    print("Existing groups:")
    for group in groups:
        print(f"--> {group}")
except Exception as e:
        print(f"No groups found -> {e}")

group_num = int(input("\nSelect a group or create a new one (press 0 to exit): "))

if group_num == 100:
    group_name = input("Enter the name of the new group: ")
    create_group(group_name)
    print(f"\n{group_name} created successfully.")
    exit()

if group_num == 0:
    print("Exiting")
    exit()

while True:
    group_name = groups[group_num - 1]
    check_group = check_group_exists(group_name)

    print(f"\n Welcome to {group_name}! Let's take a look at the available options.\n")

    print(f"1. View membership")
    print(f"2. Add a member")
    print("3. Update a member's contribution")
    print(f"4. Set the current week")
    print(f"5. Close the current week")
    print(f"6. Get the records")
    print("0. Exit")

    choice = input("Enter your choice (1-6): ")
    if choice == "1":
        try:
            members = enter_group(group_name)
            if not members:
                print(f"\nNo members found.")
            else:
                for member in members:
                    print(f"\nMember Name: {member[1]}, Contribution: {member[2]:.2f}, Week: {member[4]}")
        except Exception as e:
            print(f"\nAn error occurred while viewing members: {e}")
   
    elif choice == "2":
        member_name = input("\nEnter the name of the new member: ")
        add_member(group_name, member_name)

    elif choice == "3":
        member_name = input("\nEnter the name of the member: ")
        contribution = float(input("Enter the new contribution amount: "))
        update_contribution(group_name, member_name, contribution)

    elif choice == "4":
        week = int(input("\nEnter the current week: "))
        set_week(group_name, week)
 
    elif choice == "5":
        close_week(group_name)
        
    elif choice == "6":
        records, debtors = get_records(group_name)
        print("\nPayout History:")
        for record in records:
            print(f"\nWeek {record[0]}: GHS {record[1]:.2f} potted to {record[2]}")

        print("\nDebtors:")
        for debtor in debtors:
            print(f"\n{debtor[0]} | Amount contributed: GHS {debtor[1]:.2f} | Amount owed: GHS {50.00 - debtor[1]:.2f}")

    elif choice == "0":
        print("\nExiting")
        exit()