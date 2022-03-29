from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

table_names = ['dell', 'hp1', 'thinkpad', 'apple', 'huawei', 'hp2']

# 首页
@app.route('/')
def default():
    return render_template('index.html')

# 首页
@app.route('/index')
def index():
    return default()


# 评论页面
@app.route('/comment/<name>')
def comment(name):
    con = sqlite3.connect('comment.db')
    cur = con.cursor()
    sql = f'select * from {name}'
    data = cur.execute(sql)
    comments = []
    for comment in data:
        comments.append(comment)
    return render_template(f'comment/{name}.html', comments=comments)

# 评分页面
@app.route('/score<i>')
def score(i):
    con = sqlite3.connect('comment.db')
    cur = con.cursor()
    score = [1, 2, 3, 4, 5]
    num1, num2, num3 = [], [], []
    if i == '1':
        for n in range(3):
            sql = f'select score, count(score) from {table_names[n]} group by score'
            data = cur.execute(sql)
            for item in data:
                if n == 0:
                    num1.append(item[1])
                elif n == 1:
                    num2.append(item[1])
                elif n == 2:
                    num3.append(item[1])
    elif i == '2':
        for n in range(3):
            sql = f'select score, count(score) from {table_names[n + 3]} group by score'
            data = cur.execute(sql)
            for item in data:
                if n == 0:
                    num1.append(item[1])
                elif n == 1:
                    num2.append(item[1])
                elif n == 2:
                    num3.append(item[1])
    cur.close()
    con.close()
    return render_template(f'score{i}.html', score=score, num1=num1, num2=num2, num3=num3)

# 评论页面
@app.route('/classification')
def classification():
    con = sqlite3.connect('comment.db')
    cur = con.cursor()
    num = []
    for table_name in table_names:
        sql = f'select sentiment, count(sentiment) from {table_name} group by sentiment'
        data = cur.execute(sql)
        for item in data:
            num.append(item[1])
    return render_template('classification.html', num=num)

# 追评页面
@app.route('/days')
def days():
    con = sqlite3.connect('comment.db')
    cur = con.cursor()
    days = []
    for table_name in table_names:
        sql = f'select avg(days) from {table_name}'
        data = cur.execute(sql)
        for item in data:
            days.append(item[0])
    return render_template('days.html', days=days)

# 总分页面
@app.route('/total_score')
def total_score():
    con = sqlite3.connect('comment.db')
    cur = con.cursor()
    score, sentiment, days= [], [], []
    for table_name in table_names:
        sql = f'select avg(score), avg(sentiment), avg(days) from {table_name}'
        data = cur.execute(sql)
        for item in data:
            score.append(item[0] * 6)
            sentiment.append(item[1] * 50)
            days.append(20 - item[2])
    return render_template('total_score.html', score=score, sentiment=sentiment, days=days)


if __name__ == '__main__':
    app.run(debug=True)