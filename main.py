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
    cur.execute("SELECT id FROM Groups WHERE group_name = ?", (group_name,))
    group_id = cur.fetchone()

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
    cur.execute("SELECT id FROM Groups WHERE group_name = ?", (group_name,))

    group_id = cur.fetchone()
    if group_id:
        cur.execute("UPDATE Members SET contribution = ? WHERE member_name = ? AND group_id = ?", (contribution, member_name, group_id[0]))
        connection.commit()
        connection.close()
    else:
        print(f"Group '{group_name}' does not exist.")
        connection.close()
    
def get_debtors(group_name):
    connection = db_connect()
    cur = connection.cursor()
    cur.execute("SELECT id FROM Groups WHERE group_name = ?", (group_name,))
    group_id = cur.fetchone()

    if group_id:
        cur.execute("SELECT member_name, contribution FROM Members WHERE group_id = ? AND contribution < 50.00", (group_id[0],))
        debtors = cur.fetchall()
        connection.close()
        return debtors
    else:
        print(f"Group '{group_name}' does not exist.")
        connection.close()
        return []

