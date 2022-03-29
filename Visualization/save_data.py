import sqlite3
import pandas as pd

def get_data(path):
    df = pd.read_csv(path)
    # 第一列加1
    df.iloc[:, :1] += 1
    datalist = []
    for i in range(len(df)):
        data = list(df.iloc[i])
        datalist.append(data)
    return datalist

def save2db(datalist, dbpath, table_name):
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    for data in datalist:
        sql = f'''
            insert into {table_name} (
            id, buy_time, comment_time, days, color, size, content, score, sentiment)
            values({data[0]}, "{data[1]}", "{data[2]}", {data[3]}, "{data[4]}",
            "{data[5]}", "{data[6]}", {data[7]}, {data[8]})
        '''
        print(sql)
        cur.execute(sql)
        conn.commit()
        #break
    cur.close()
    conn.close()


def create_table(dbpath, table_name):
    # id,buy_time,comment_time,days,color,size,content,score,sentiment
    sql = f'''
        create table {table_name}
        (
        id integer primary key autoincrement,
        buy_time varchar,
        comment_time varchar,
        days integer,
        color varchar,
        size varchar,
        content varchar,
        score integer,
        sentiment integer
        ) 
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    dbpath = 'comment.db'
    table_names = ['dell', 'hp1', 'thinkpad', 'apple', 'huawei', 'hp2']
    products_id = ['100012779151', '100027683422', '100021725644', '10030539565679',
                   '100024403104', '100021318642']
    for table_name in table_names:
        create_table(dbpath, table_name)
    i = 0
    for product_id in products_id:
        path = f'../data/{product_id}.csv'
        datalist = get_data(path)
        save2db(datalist, dbpath, table_names[i])
        i += 1
    #save2db(datalist,  'comment.db', 'dell')