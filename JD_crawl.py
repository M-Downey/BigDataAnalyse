import requests
import json
import time
import csv
import random

url = 'https://club.jd.com/comment/productPageComments.action'
headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/95.0.4638.69 Safari/537.36'
}

# brand: dell  hp1  ThinkPad  apple huawei  hp2
products_id = ['100012779151', '100027683422', '100021725644', '10030539565679', '100024403104', '100021318642']

columns = ['referenceTime', 'creationTime', 'days', 'productColor', 'productSize', 'content', 'score']
column_name = ['buy_time', 'comment_time', 'days', 'color', 'size', 'content', 'score']

def get_comments(product_id):
      for i in range(30):
            param = {
                  'callback': 'fetchJSON_comment98',
                  'productId': product_id,
                  'score': 0,       # 3 好 2中 1差 0所有
                  'sortType': 6,    # 评论排序，5是推荐，6是时间
                  'page': i,        # 一个产品最多能爬1000条评论，我爬300条
                  'pageSize': 10,
                  'isShadowSku': 0,
                  'rid': 0,
                  'fold': 1,
            }
            resp = requests.get(url, headers=headers, params=param)
            # fetchJSON_comment98
            # print(resp.status_code)
            dic = json.loads(resp.text[20: -2])
            resp.close()
            print(f'page:{i}')
            for i in range(10):
                  buy_time = dic['comments'][i][columns[0]]
                  comment_time = dic['comments'][i][columns[1]]
                  days = dic['comments'][i][columns[2]]
                  color = dic['comments'][i][columns[3]]
                  size = dic['comments'][i][columns[4]]
                  content = dic['comments'][i][columns[5]].replace('\n', '')
                  score = dic['comments'][i][columns[6]]
                  yield (buy_time, comment_time, days, color, size, content, score)
            time.sleep(random.random() + 1)
            print('over')
            if i % 10 == 0:
                  time.sleep(3)


def save_data():
      for product_id in products_id:
            f = open(f'data/{product_id}.csv', 'w', encoding='utf-8', newline='')
            w = csv.writer(f)
            w.writerow(column_name)
            comments = get_comments(product_id)
            for comment in comments:
                  w.writerow(comment)
            f.close()


def main():
      save_data()

if __name__ == '__main__':
      main()