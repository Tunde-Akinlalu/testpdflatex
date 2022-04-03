import sqlite3
from datetime import date

class Database:
    def __init__(self, mydb):
        self.con = sqlite3.connect(mydb)
        self.cur = self.con.cursor()
        qiu = """
        CREATE TABLE IF NOT EXISTS survey_px(
            id Integer Primary Key,
            EMR text,
            age text,
            gender text,
            ward text,
            cubicle text
        )
        """
        self.cur.execute(qiu)
        self.con.commit()

    # Insert Function
    def insert(self, emr, age_group, gender, ward, cubicle):
        self.cur.execute("insert into survey_px values (NULL,?,?,?,?,?)",
                         (emr, age_group, gender, ward, cubicle))
        self.con.commit()

    # Fetch All Data from DB
    def fetch(self):
        self.cur.execute("SELECT * from survey_px")
        rows = self.cur.fetchall()
        # print(rows)
        return rows

    # Delete a Record in DB
    def remove(self, id):
        self.cur.execute("delete from survey_px where id=?", (id,))
        self.con.commit()

    # Update a Record in DB
    def update(self, id, emr, age_group, gender, ward, cubicle):
        self.cur.execute(
            "update survey_px set emr=?, age=?, ward=?, gender=?, cubicle=?, where id=?",
            (emr, age_group, ward, gender, cubicle, id))
        self.con.commit()

    # Print a pdf
    def pdf_print(self, id):
        self.cur.execute("SELECT 'ward'||'cubicle' from survey_px, where id =?", (id, ))
        self.con.commit()

        # dcode = '''SELECT 'ward'||'cubicle' FROM survey_px'''
        # dcode = self.cur.execute(dcode)
        # dday = date.today()
        # dday = dday.strftime(format='%y%m%d')
        # d = dday+dcode


