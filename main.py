# -*- coding: utf-8 -*-

from requests_html import HTMLSession
from requests.exceptions import RequestException
import re
import csv
from multiprocessing import Pool
import sys

csv.field_size_limit(sys.maxsize)

session = HTMLSession()

def search_email(link):
    emails = []
    resp = session.get(link)
    emails.append([email for email in re.findall('\w+@\w+.\w+', resp.text)])
    info = resp.html.xpath('//a/@href')
    for key in info:
        if re.findall('\w+@\w+.\w+', key):
            return key

def write_csv(data):
    with open('data.csv', 'a') as f:
        order = ['url', 'email', 'title', 'description', 'keywords']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)

def check_url(url):
    with open('data.csv', 'r') as file:
        fieldnames = ['url', 'email', 'title', 'description', 'keywords']
        reader = csv.DictReader((x.replace('\0', '') for x in file), fieldnames=fieldnames)
        read_data = []
        for row in reader:
            read_data.append(row['url'])
        check = url in read_data
    return check

def check_email(email):
    with open('data.csv', 'r') as file:
        fieldnames = ['url', 'email', 'title', 'description', 'keywords']
        reader = csv.DictReader(file, fieldnames=fieldnames)
        read_data = []
        for row in reader:
            read_data.append(row['email'])
        check = email in read_data
    return check

def run(url):
    with open('used_domains.txt', 'a') as used:
        used.write(url + '\n')
    if not check_url(url):
        try:
            resp = session.get(url, timeout=3)
            print(resp.status_code)
        except Exception:
            # except RequestException:
            print('resp error')
            #print(resp.status_code)
        # print(info)
        try:
            title = resp.html.xpath('//title')[0].text
            desc = resp.html.xpath('//meta[@name = "description"]/@content')
            keywords = resp.html.xpath('//meta[@name = "keywords"]/@content')
        except Exception:
            print('Title Error')
        try:
            for email in re.findall("[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", resp.text):
                if not check_email(email):
                    print(email)
                    data = {'url': url,
                            'email': email,
                            'title': title,
                            'description': desc,
                            'keywords': keywords}
                    write_csv(data)
        except Exception:
            print('email error')
        try:
            for key in resp.html.xpath('//a'):
                if re.search(r'\bКонтак', key.text):
                    if re.search(r'\bhtt', key.xpath('//@href')[0]):
                        # print('проверк', key.xpath('//@href')[0])
                        try:
                            for email in re.findall('\w+@\w+.\w+', session.get(key.xpath('//@href')[0]).text):
                                if not check_email(email):
                                    print(email)
                                    data = {'url': url,
                                            'email': email,
                                            'title': title,
                                            'description': desc,
                                            'keywords': keywords}
                                    write_csv(data)
                        except RequestException:
                            pass
                    else:
                        # print(url + key.xpath('//@href')[0])
                        try:
                            for email in re.findall('\w+@\w+.\w+', session.get(url + key.xpath('//@href')[0]).text):
                                if not check_email(email):
                                    print(email)
                                    data = {'url': url,
                                            'email': email,
                                            'title': title,
                                            'description': desc,
                                            'keywords': keywords}
                                    write_csv(data)
                        except RequestException:
                            pass
        except Exception:
            print('key error')

def main():
    used_urls = []
    with open('used_domains.txt', 'r') as used:
        for i in used:
            used_urls.append(i.rstrip('\n'))
    print(used_urls)
    urls_list= []
    start_list = []
    with open('domains.txt', 'r') as urls:
        # Обработка для каждого ключевика из файла
        for i, line in enumerate(urls):
            url = 'http://' + line.rstrip('\n').lower()
            start_list.append(url)
            if url not in used_urls:
                print(i, ' ', url)
                urls_list.append(url)
                #run(url)
    with Pool(30) as p:
        p.map(run, urls_list)
    # print(len(start_list))
    # print(len(urls_list))

if __name__ == '__main__':
    main()