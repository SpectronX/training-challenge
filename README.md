### coding challenge
---------------------

this coding challenge required a small programme to manage a savings group (Susu). the programme creates a group for the members, for which they contribute a fixed amount of money on a weekly basis. as to when members joined the group, they are assigned a turn to receive the total amount contributed by the group per week. 

the programme allows for the creation of a group, adding members to a group, recording contributions (for which partial payments are allowed), and assigning turns to members to receive the total amount contributed by the group per week. as long as the contributions for a particular week are not complete, the programme will not issue a closure for that particular week. the programme will also allow for the viewing of the total contributions made by each member, as well as the total amount contributed by the group.


### modular programme structure
---------------------------

the programme has two main modules, the database module with functions that handle interactions with the database, and the main module that handles the user interface (through the command line) and calls the database module functions to perform the required operations. a summary of the functions in the database module is provided below: 

- database module
    - create_group(group_name). creates a new group with the given name and other required tables related to the group in the database.
    - add_member(group_name, member_name). adds a new member to the specified group.
    - update_contribution(group_name, member_name, contribution). records a contribution made by a member to the specified group.
    - set_week(group_name, week). sets the current week for which contributions are being recorded and also sets the turn for members who will receive the total contributions for that week.
    - close_week(group_name). closes the current week for the specified group, provided that all contributions have been made.
    - get_records(group_name). retrieves the payout history as well as the deptors for the specified group.
