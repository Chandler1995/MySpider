import requests
from bs4 import BeautifulSoup 
import re
import json
import time


def get_one(url):
    response = requests.get(url)
    return response.text


def parse_one(html, page_num):
    soup_list = BeautifulSoup(html).find_all('li', 'subject-item')
    book_index = 20 * page_num - 19
    for one_book in soup_list:
        title = one_book.find('a', title = True).get_text().strip().replace(' ', '').replace('\n', '')
        info = one_book.find('div', 'pub').get_text().strip().replace(' ', '').replace('\n', '')
        if info.count('/') == 3:
            info_list = re.match('(.*?)/(.*?)/(.*?)/(.*?)$', info)
            yield {
                'index': int(book_index),
                'title': title,
                'writer': info_list.group(1),
                'translator' : None,
                'company': info_list.group(2),
                'date': info_list.group(3),
                'price': info_list.group(4)
            }
            book_index = book_index + 1
        else:
            info_list = re.match('(.*?)/(.*?)/(.*?)/(.*?)/(.*?)$', info)
            yield {
                'index': int(book_index),
                'title': title,
                'writer': info_list.group(1),
                'translator': info_list.group(2),
                'company': info_list.group(3),
                'date': info_list.group(4),
                'price': info_list.group(5)
            }
            book_index = book_index + 1


def download_write(content):
    with open('douban_book_rank', 'a', encoding = 'utf-8') as f:
        f.write(json.dumps(content, ensure_ascii = False) + '\n')


def main(start):
    url = 'https://book.douban.com/tag/小说?start=' + str(start) + '&type=T'
    html = get_one(url)
    page_num = start / 20 + 1
    for one_book_dict in parse_one(html, page_num):
        print(one_book_dict)
        download_write(one_book_dict)


if __name__ == '__main__':
    for i in range(100):
        main(start = i * 20)
        time.sleep(1)
