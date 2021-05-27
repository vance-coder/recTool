import os
import shutil
import zipfile
import sqlite3
from glob import glob


class DBHelper():
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.cursor = self.conn.cursor()
        self.columns = ['filename', 'parent', 'confidence', 'value', 'status', 'datetime']
        # 如果不存在表则创建表
        self.create_table()

    def create_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS data(
            `filename` varchar(50) NOT NULL,  
            `parent` varchar(50),  
            `confidence` varchar(10) NOT NULL,
            `value` varchar(128) NOT NULL,
            `status` NUMERIC default (0),
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

    def select(self, limit=10000000, offset=0):
        sql = f"SELECT * FROM DATA ORDER BY filename DESC LIMIT {limit} OFFSET {offset};"
        res = self.cursor.execute(sql)
        return [dict(zip(self.columns, row)) for row in res.fetchall()]

    def select_by_filename(self, filename):
        sql = f"SELECT * FROM DATA WHERE filename='{filename}';"
        res = self.cursor.execute(sql)
        return dict(zip(self.columns, res.fetchall()[0]))

    def select_by_status(self, value):
        sql = f"SELECT * FROM DATA WHERE status={value};"
        res = self.cursor.execute(sql)
        return [dict(zip(self.columns, row)) for row in res.fetchall()]

    def update(self, filename, value, status):
        sql = f'UPDATE data SET value="{value}", status = {status} WHERE filename="{filename}";'
        res = self.cursor.execute(sql)
        self.conn.commit()
        print(f"Insert into data, {res.rowcount} rows effected!")
        return res.lastrowid

    def update_status(self, filename, status):
        sql = f"UPDATE data SET status = {status} WHERE filename='{filename}';"
        res = self.cursor.execute(sql)
        self.conn.commit()
        print(f"Insert into data, {res.rowcount} rows effected!")
        return res.lastrowid

    def delete(self, filename):
        sql = f"DELETE FROM data WHERE filename='{filename}';"
        res = self.cursor.execute(sql)
        self.conn.commit()
        print(f"Insert into data, {res.rowcount} rows effected!")
        return res.lastrowid

    def close(self):
        self.cursor.close()

    def export(self):
        image_folder = 'static/images/result/'
        output = 'output/'
        try:
            shutil.rmtree(output)
        except Exception as e:
            print(e)
        os.mkdir(output)
        text = []
        for row in self.select_by_status(1):
            filepath = image_folder + row['filename']
            output_path = output + row['filename']
            row_text = f"{row['filename']}\t{row['value']}"
            shutil.copy(filepath, output_path)
            text.append(row_text)
        label_file = output + 'label.txt'
        with open(label_file, 'w+', encoding='utf-8') as fp:
            fp.write('\n'.join(text))
        with zipfile.ZipFile('static/label.zip', "w", zipfile.ZIP_DEFLATED) as zf:
            for f in glob(output + '*'):
                fs, filename = f.split('\\')
                zf.write(f, filename)


if __name__ == '__main__':
    db = DBHelper()
    lst = ['3801_anyone got.png', '1837878_3.png', '0.95', 'Value paste My OCR ']
    # db.insert(lst)
    # print(db.select(limit=1, offset=1))
    # print(db.select_by_filename('fea4028b88809fff.png'))
    # print(db.select_by_status(1))
    # print(db.update_correct('ff9fd0e0e0c080df.png', 1))
    db.export()
