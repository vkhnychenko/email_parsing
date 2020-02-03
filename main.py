from requests_html import HTMLSession
from requests.exceptions import RequestException
import re
import csv
from multiprocessing import Pool

session = HTMLSession()

def search_email(link):
    emails = []
    resp = session.get(link)
    emails.append([email for email in re.findall('\w+@\w+.\w+', resp.text)])
    info = resp.html.xpath('//a/@href')
    for key in info:
        if re.findall('\w+@\w+.\w+', key):
            return key
    # try:
    #     emails = re.findall('\w+@\w+.\w+', resp.text)
    #     emaile = emails[0]
    # except:
    #     emaile = " "
    #
    # print(emaile)
    # return emaile
    # if len(emails) >= 1:
    #     for key in emails:
    #         emailse.add(key)
    # print(emailse)

def write_csv(data):
    with open('data.csv', 'a') as f:
        order = ['url', 'email', 'title', 'description', 'keywords']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)

def check_url(url):
    with open('data.csv', encoding='utf8') as file:
        fieldnames = ['url', 'email', 'title', 'description', 'keywords']
        reader = csv.DictReader(file, fieldnames=fieldnames)
        read_data = []
        for row in reader:
            read_data.append(row['url'])
        check = url in read_data
    return check

def check_email(email):
    with open('data.csv', encoding='utf8') as file:
        fieldnames = ['url', 'email', 'title', 'description', 'keywords']
        reader = csv.DictReader(file, fieldnames=fieldnames)
        read_data = []
        for row in reader:
            read_data.append(row['email'])
        check = email in read_data
    return check

def run(url):
    if not check_url(url):
        try:
            resp = session.get(url)
        except Exception:
            # except RequestException:
            print('resp error')
        # print(info)
        try:
            title = resp.html.xpath('//title')[0].text
            desc = resp.html.xpath('//meta[@name = "description"]/@content')
            keywords = resp.html.xpath('//meta[@name = "keywords"]/@content')
        except Exception:
            print('Title Error')
        for email in re.findall('\w+@\w+.\w+', resp.text):
            if not check_email(email):
                print(email)
                data = {'url': url,
                        'email': email,
                        'title': title,
                        'description': desc,
                        'keywords': keywords}
                write_csv(data)
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
    urls_list= []
    with open('domains.txt', 'r') as urls:
        # Обработка для каждого ключевика из файла
        for line in urls:
            url = line.rstrip('\n')
            urls_list.append(url)
            print(url)
            #run(url)
    with Pool(3) as p:
        p.map(run, urls_list)
    #print(urls_list)


            #         title = resp.html.xpath('//title')[0].text
            #     except:
            #         title = " "
            #     info = resp.html.xpath('//a/@href')
            #     for key in info:
            #         if re.findall('\w+@\w+.\w+', key):
            #             if not check_email(key):
            #                 print('email' ,key)
            #                 data = {'url': url,
            #                         'email': key,
            #                         'title': title}
            #                 write_csv(data)
            #
            #     info = resp.html.xpath('//a')
            #     for key in info:
            #         if re.search(r'\bКонтак', key.text):
            #             print('д проверки', key.xpath('//@href')[0])
            #             if re.search(r'\bhtt', key.xpath('//@href')[0]):
            #                 email = search_email(key.xpath('//@href')[0])
            #                 #print('email', email)
            #                 if not check_email(email):
            #                     print('email', email)
            #                     data = {'url': url,
            #                             'email': email,
            #                             'title': title}
            #                     write_csv(data)
            #             else:
            #                 print(url + key.xpath('//@href')[0])
            #                 email = search_email(url + key.xpath('//@href')[0])
            #                 #print('email', email)
            #                 if not check_email(email):
            #                     print('email', email)
            #                     data = {'url': url,
            #                             'email': email,
            #                             'title': title}
            #                     write_csv(data)

if __name__ == '__main__':
    main()