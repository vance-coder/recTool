import sqlite3


class DBHelper():
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.cursor = self.conn.cursor()
        self.columns = ['filename', 'parent', 'confidence', 'value', 'corrected', 'uncertain', 'datetime']
        # 如果不存在表则创建表
        self.create_table()

    def create_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS data(
            `filename` varchar(50) NOT NULL,  
            `parent` varchar(50),  
            `confidence` varchar(10) NOT NULL,
            `value` varchar(128) NOT NULL,
            `corrected` NUMERIC default (0),
            `uncertain` NUMERIC default (0),
            `datetime` TIMESTAMP default (datetime('now', 'localtime')),
            PRIMARY KEY (filename));
        '''
        self.cursor.execute(sql)

    def insert(self, val):
        # sql = f"INSERT INTO DATA (`alias`, `from`, `type`, `content`) VALUES ({str(val)[1:-1]});"
        sql = f"INSERT INTO DATA (`filename`, `parent`, `confidence`, `value`) VALUES (?, ?, ?, ?);"
        res = self.cursor.execute(sql, val)
        self.conn.commit()
        print(f"Insert into data, {res.rowcount} rows effected!")
        return res.lastrowid

    def select(self, limit=10):
        sql = f"SELECT * FROM DATA ORDER BY filename DESC LIMIT {limit};"
        res = self.cursor.execute(sql)
        return [dict(zip(self.columns, row)) for row in res.fetchall()]

    def select_by_filename(self, filename):
        sql = f"SELECT * FROM DATA WHERE id={filename};"
        res = self.cursor.execute(sql)
        return dict(zip(self.columns, res.fetchall()[0]))

    def close(self):
        self.cursor.close()


if __name__ == '__main__':
    db = DBHelper()
    lst = ['3801_anyone got.png', '1837878_3.png', '0.95', 'Value paste My OCR ']
    # db.insert(lst)
    print(db.select())
