import sqlite3 as sql

contribution = 50.00

WEEK_CLOSED = False

def db_connect():
    connection = sql.connect('training.db', detect_types=sql.PARSE_DECLTYPES)
    return connection

def create_group(group_name):
    connection = db_connect()
    cur = connection.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS Groups " \
    "(id INTEGER PRIMARY KEY AUTOINCREMENT, " \
    "group_name TEXT NOT NULL)")

    cur.execute("CREATE TABLE IF NOT EXISTS Members " \
    "(id INTEGER PRIMARY KEY AUTOINCREMENT, " \
    "member_name TEXT NOT NULL, " \
    "contribution INTEGER NOT NULL, " \
    "group_id INTEGER NOT NULL, " \
    "week INTEGER NOT NULL DEFAULT 0, " \
    "receives_pot INTEGER NOT NULL DEFAULT 0, " \
    "FOREIGN KEY (group_id) REFERENCES Groups(id))")

    cur.execute("CREATE TABLE IF NOT EXISTS Payout_History " \
    "(id INTEGER PRIMARY KEY AUTOINCREMENT, " \
    "group_id INTEGER NOT NULL, " \
    "week INTEGER NOT NULL, " \
    "total_contribution INTEGER NOT NULL, " \
    "receiver TEXT NOT NULL, " \
    "FOREIGN KEY (group_id) REFERENCES Groups(id))")

    cur.execute("INSERT INTO Groups (group_name) VALUES (?)", (group_name,))
    connection.commit()
    connection.close()

member_check_query = "SELECT member_name FROM Members WHERE group_id = ?"

def list_groups():
    connection = db_connect()
    cur = connection.cursor()
    groups = cur.execute("SELECT group_name FROM Groups").fetchall()
    connection.close()
    return [group[0] for group in groups]

def check_group_exists(group_name):
    connection = db_connect()
    cur = connection.cursor()
    group_id = cur.execute("SELECT id FROM Groups WHERE group_name = ?", (group_name,)).fetchone()
    connection.close()
    if group_id is None:
        print(f"Group '{group_name}' does not exist.")
        exit(1)
    return group_id

def enter_group(group_name):
    connection = db_connect()
    cur = connection.cursor()
    check_group = check_group_exists(group_name)
    
    result = cur.execute("SELECT * FROM Members WHERE group_id = ?", (check_group[0],))
    if result is None:
        print(f"Group '{group_name}' does not exist or there are no members in it.")
        connection.close()
        return []
    return result.fetchall()

def add_member(group_name, member_name):
    connection = db_connect()
    cur = connection.cursor()
    check_group = check_group_exists(group_name)

    present_members = cur.execute(member_check_query, (check_group[0],)).fetchall()
    if member_name in [present_member[0] for present_member in present_members]:
        print(f"{member_name} already exists in {group_name}.")
        connection.close()
        return
  
    cur.execute("INSERT INTO Members (member_name, contribution, group_id) VALUES (?, ?, ?)", (member_name, 0, check_group[0]))
    connection.commit()
    connection.close()
   
def update_contribution(group_name, member_name, contribution):
    connection = db_connect()
    cur = connection.cursor()
    check_group = check_group_exists(group_name)

    member_exists = cur.execute(member_check_query, (check_group[0],)).fetchall()
    if member_name not in [present_member[0] for present_member in member_exists]:
        print(f"{member_name} does not exist in {group_name}.")
        connection.close()
        return
    
    check_week = cur.execute("SELECT week FROM Members WHERE group_id = ?", (check_group[0],)).fetchone()[0]
    if check_week == 0:
        print(f"Week for {group_name} has not been set. Cannot update contribution.")
        connection.close()
        return
    
    cur.execute("UPDATE Members SET contribution = ? WHERE member_name = ? AND group_id = ?", (contribution, member_name, check_group[0]))
    connection.commit()
    connection.close()

length_query = "SELECT COUNT(*) FROM Members WHERE group_id = ?"

def set_week(group_name, week):
    member_to_receive_pot = 0

    connection = db_connect()
    cur = connection.cursor()
    check_group = check_group_exists(group_name)

    length = cur.execute(length_query, (check_group[0],)).fetchone()[0]
    member_to_receive_pot = ((week - 1) % length) + 1

    check_week = cur.execute("SELECT week FROM Members WHERE group_id = ?", (check_group[0],)).fetchone()[0]
    if check_week == week:
        print(f"Week for {group_name} has already been set to {week}. Cannot set it again.")
        connection.close()
        return
    cur.execute("UPDATE Members SET week = ?, contribution = 0 WHERE group_id = ?", (week, check_group[0]))
    cur.execute("UPDATE Members SET receives_pot = 1 WHERE group_id = ? AND id = ?", (check_group[0], member_to_receive_pot))
    connection.commit()
    connection.close()


def close_week(group_name):
    connection = db_connect()
    cur = connection.cursor()
    check_group = check_group_exists(group_name)
    
    expected_contribution = cur.execute(length_query, (check_group[0],)).fetchone()[0] * contribution
    current_week = cur.execute("SELECT week FROM Members WHERE group_id = (SELECT id FROM Groups WHERE group_name = ?)", (group_name,)).fetchone()[0]
    current_receiver = cur.execute("SELECT member_name FROM Members WHERE receives_pot = 1 AND group_id = (SELECT id FROM Groups WHERE group_name = ?)", (group_name,)).fetchone()[0]
    total_contribution = cur.execute("SELECT SUM(contribution) FROM Members WHERE group_id = (SELECT id FROM Groups WHERE group_name = ?)", (group_name,)).fetchone()[0]

    if total_contribution < expected_contribution:
        print(f"Cannot close week {current_week} for group '{group_name}'. Some have not paid their contributions in full.")
        connection.close()
        return 
    
    print(f"Week {current_week} closed for {group_name}.")
    print(f"Current receiver: {current_receiver}")
    print(f"Total contribution: {total_contribution}")

    cur.execute("INSERT INTO Payout_History (group_id, week, total_contribution, receiver) VALUES (?, ?, ?, ?)", (check_group[0], current_week, total_contribution, current_receiver))
    cur.execute("UPDATE Members SET contribution = 0, receives_pot = 0 WHERE group_id = ?", (check_group[0],))
    connection.commit()
    connection.close()


def get_debtors(group_name):
    connection = db_connect()
    cur = connection.cursor()
    check_group = check_group_exists(group_name)

    cur.execute("SELECT member_name, contribution FROM Members WHERE group_id = ? AND contribution < 50.00", (check_group[0],))
    debtors = cur.fetchall()
    connection.close()
    return debtors


def get_records(group_name):
    connection = db_connect()
    cur = connection.cursor()
    check_group = check_group_exists(group_name)

    records = cur.execute("SELECT week, total_contribution, receiver FROM Payout_History WHERE group_id = ?", (check_group[0],)).fetchall()
    connection.close()
    debtors = get_debtors(group_name)
    return records, debtors
    