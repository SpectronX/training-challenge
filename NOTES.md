### assumptions made
--------------------

- the programme is handled by a single user, who is the administrator of all the groups created. as such, much of security was not taken into consideration provided the admin alone is responsible for all the actions. hence, the programme does not handle any form of authentication or authorization.

- the programme is to handle only one group at a time, and as such, it does not allow for the spawning of multiple groups.

### decision made
--------------------

while I tried to implement a database module using regular python data structures, I realized it wouldn't be efficient to handle much data and processing, hence i decided to use a minimal database module using sqlite3. this also allows for data persistence, which is crucial for the programme to function properly.

### future improvements
--------------------

