import csv
import sqlite3

# CSVファイルからデータを読み取る関数
def read_csv_file(file_path):
    data = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data

# データベースに接続
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# テーブル作成のSQLクエリ
create_table_query = """
CREATE TABLE IF NOT EXISTS your_table_name (
    column1_type TEXT,
    column2_type INTEGER,
    column3_type TEXT,
    column4_type INTEGER,
    column5_type TEXT
);
"""

# テーブル作成
cursor.execute(create_table_query)
conn.commit()

# CSVファイルのパス
csv_file_path = r".\sc\artist_url_4.csv"

# CSVファイルからデータを読み取り、データベースに挿入
with open(csv_file_path, 'r',encoding="utf-8", newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        # データの前処理: 空の要素をNoneに変換
        cleaned_row = [value if value else None for value in row]

        # データをデータベースに挿入するSQLクエリ
        insert_query = """
        INSERT INTO your_table_name (column1_type, column2_type, column3_type, column4_type, column5_type) 
        VALUES (?, ?, ?, ?, ?);
        """

        # データを挿入
        cursor.execute(insert_query, cleaned_row)

# データベースとの接続を閉じる
conn.commit()
conn.close()
