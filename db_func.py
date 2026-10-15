import sqlite3 as sql

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

    cur.execute("INSERT INTO Groups (group_name) VALUES (?)", (group_name,))
    connection.commit()
    connection.close()

def enter_group(group_name):
    connection = db_connect()
    cur = connection.cursor()
    result = cur.execute("SELECT * FROM Members WHERE group_id = (SELECT id FROM Groups WHERE group_name = ?)", (group_name,))
    if result is None:
        print(f"Group '{group_name}' does not exist or there are no members in it.")
        connection.close()
        return []
    return result.fetchall()

def add_member(group_name, member_name):
    connection = db_connect()
    cur = connection.cursor()
    group_id = cur.execute("SELECT id FROM Groups WHERE group_name = ?", (group_name,)).fetchone()

    if group_id:
        cur.execute("INSERT INTO Members (member_name, contribution, group_id) VALUES (?, ?, ?)", (member_name, 0, group_id[0]))
        connection.commit()
        connection.close()
    else:
        print(f"Group '{group_name}' does not exist.")
        connection.close()

def update_contribution(group_name, member_name, contribution):
    connection = db_connect()
    cur = connection.cursor()
    group_id = cur.execute("SELECT id FROM Groups WHERE group_name = ?", (group_name,)).fetchone()

    if group_id:
        check_week = cur.execute("SELECT week FROM Members WHERE group_id = ?", (group_id[0],)).fetchone()[0]
        if check_week == 0:
            print(f"Week for group '{group_name}' has not been set. Cannot update contribution.")
            connection.close()
            return
        cur.execute("UPDATE Members SET contribution = ? WHERE member_name = ? AND group_id = ?", (contribution, member_name, group_id[0]))
        connection.commit()
        connection.close()
    else:
        print(f"Group '{group_name}' does not exist.")
        connection.close()
    
def get_debtors(group_name):
    connection = db_connect()
    cur = connection.cursor()
    group_id = cur.execute("SELECT id FROM Groups WHERE group_name = ?", (group_name,)).fetchone()
    
    if group_id:
        cur.execute("SELECT member_name, contribution FROM Members WHERE group_id = ? AND contribution < 50.00", (group_id[0],))
        debtors = cur.fetchall()
        connection.close()
        return debtors
    else:
        print(f"Group '{group_name}' does not exist.")
        connection.close()
        return []

def set_week(group_name, week):
    member_to_receive_pot = 0

    connection = db_connect()
    cur = connection.cursor()
    group_id = cur.execute("SELECT id FROM Groups WHERE group_name = ?", (group_name,)).fetchone()

    if group_id:
        length = cur.execute("SELECT COUNT(*) FROM Members WHERE group_id = ?", (group_id[0],)).fetchone()[0]
        member_to_receive_pot = (member_to_receive_pot + week) % length
        cur.execute("UPDATE Members SET week = ?, contribution = 0 WHERE group_id = ?", (week, group_id[0]))
        cur.execute("UPDATE Members SET member_to_receive_pot = ? WHERE group_id = ?", (member_to_receive_pot, group_id[0]))
        connection.commit()
        connection.close()
    else:
        print(f"Group '{group_name}' does not exist.")
        connection.close()

def close_week(group_name):
    connection = db_connect()
    cur = connection.cursor()
    group_id = cur.execute("SELECT id FROM Groups WHERE group_name = ?", (group_name,)).fetchone()

    if group_id:
        current_week = cur.execute("SELECT week FROM Members WHERE group_id = (SELECT id FROM Groups WHERE group_name = ?)", (group_name,)).fetchone()[0]
        current_receiver = cur.execute("SELECT member_name FROM Members WHERE group_id = (SELECT id FROM Groups WHERE group_name = ?) AND member_to_receive_pot = 1", (group_name,)).fetchone()[0]
        total_contribution = cur.execute("SELECT SUM(contribution) FROM Members WHERE group_id = (SELECT id FROM Groups WHERE group_name = ?)", (group_name,)).fetchone()[0]

        print(f"Week {current_week} closed for group '{group_name}'.")
        print(f"Current receiver: {current_receiver}")
        print(f"Total contribution: {total_contribution}")

        cur.execute("UPDATE Members SET contribution = 0, receives_pot = 0 WHERE group_id = ?", (group_id,))
        connection.commit()
        connection.close()
    else:
        print(f"Group '{group_name}' does not exist.")
        connection.close()