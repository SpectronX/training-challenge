### assumptions made
--------------------

- the programme is handled by a single user, who is the administrator of all the groups created. as such, much of security was not taken into consideration provided the admin alone is responsible for all the actions. hence, the programme does not handle any form of authentication or authorization.

- the programme is to handle only one group at a time, and as such, it does not allow for operating multiple groups at once.

### decision made
--------------------

while I tried to implement a database module using regular python data structures, I realized it wouldn't be efficient to handle much data and processing, hence i decided to use a minimal database module using sqlite3. this also allows for data persistence, which is crucial for the programme to function properly.

weeks have to set before commencing any operation on the programme. this is to ensure that the programme can track the contributions. if contributions are made before the weeks are set, the admin will have to set the week and re-add the contributions made. any user added within a week, will have to make full contributions for that week, since the programme does not close a week until all members have contributed their quota for that week.

### future improvements
--------------------

the programme doesn't track the tiny increments in contributions made by members. so if a member contributes GHS 10.00 and later adds GHS 5.00, the programme will only track the latest contribution and record the total contribution of GHS 15.00. this can be improved upon in time. 

late when a week is closed, the programme would automatically set the next week so the user doesn't have to do that manually.

the debtors function should list debtors per the active week and if a week has been closed, and none set yet, no debtors should be listed.
