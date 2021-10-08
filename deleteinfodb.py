import sqlite3
def delete_user():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("delete from name")
    conn.commit()

delete_user()