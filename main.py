from db_func import *

print("Welcome to the Group Contribution Tracker! \n")
print("1. List existing groups")
print("2. View members of a group")
print("3. Create a new group")
print("4. Add a member to a group")
print("5. Update a member's contribution")
print("6. Set the current week for a group")
print("7. Close the current week for a group")
print("8. Get the records of a group")

choice = input("Enter your choice (1-8): ")
if choice == "1":
    try:
        groups = list_groups()
        print("Existing groups:")
        for group in groups:
            print(group)
    except Exception as e:
        print(f"An error occurred while listing groups: {e}")

elif choice == "2":
    try:
        group_name = input("Enter the name of the group to view members: ")
        check_group = check_group_exists(group_name)
        members = enter_group(group_name)
        if not members:
            print(f"No members found in {group_name}.")
        else:
            for member in members:
                print(f"Member Name: {member[1]}, Contribution: {member[2]}, Week: {member[3]}")
    except Exception as e:
        print(f"An error occurred while viewing members: {e}")
   
elif choice == "3":
    group_name = input("Enter the name of the new group: ")
    create_group(group_name)
    print(f"{group_name} created successfully.")

elif choice == "4":
    group_name = input("Name of the group to add member to: ")
    check_group = check_group_exists(group_name)
    member_name = input("Enter the name of the new member: ")
    add_member(group_name, member_name)
    print(f"{member_name} added to {group_name}.")

elif choice == "5":
    group_name = input("Enter the name of the group: ")
    check_group = check_group_exists(group_name)
    member_name = input("Enter the name of the member: ")
    contribution = float(input("Enter the new contribution amount: "))
    update_contribution(group_name, member_name, contribution)

elif choice == "6":
    group_name = input("Enter the name of the group: ")
    check_group = check_group_exists(group_name)
    week = int(input("Enter the current week number: "))
    set_week(group_name, week)
 
elif choice == "7":
    group_name = input("Enter the name of the group: ")
    check_group = check_group_exists(group_name)
    close_week(group_name)

elif choice == "8":
    group_name = input("Enter the name of the group: ")
    check_group = check_group_exists(group_name)

    records, debtors = get_records(group_name)
    print("Payout History:")
    for record in records:
        print(f"Week {record[0]}: GHS {record[1]} potted to {record[2]}")

    print("Debtors:")
    for debtor in debtors:
        print(f"{debtor[0]}: {debtor[1]}")