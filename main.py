from requests_html import HTMLSession
from requests.exceptions import RequestException
import re
import csv

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
        order = ['url', 'email', 'title']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)

def check_url(url):
    with open('data.csv', encoding='utf8') as file:
        fieldnames = ['url', 'email', 'title']
        reader = csv.DictReader(file, fieldnames=fieldnames)
        read_data = []
        for row in reader:
            read_data.append(row['url'])
        check = url in read_data
    return check

def check_email(email):
    with open('data.csv', encoding='utf8') as file:
        fieldnames = ['url', 'email', 'title']
        reader = csv.DictReader(file, fieldnames=fieldnames)
        read_data = []
        for row in reader:
            read_data.append(row['email'])
        check = email in read_data
    return check

def main():
    titles = set()
    with open('domains.txt', 'r') as urls:
        # Обработка для каждого ключевика из файла
        for line in urls:
            url = line.rstrip('\n')
            print(url)
            if not check_url(url):
                try:
                    resp = session.get(url)
                except RequestException:
                    pass
                try:
                    title = resp.html.xpath('//title')[0].text
                except:
                    title = " "
                info = resp.html.xpath('//a/@href')
                for key in info:
                    if re.findall('\w+@\w+.\w+', key):
                        if not check_email(key):
                            print('email' ,key)
                            data = {'url': url,
                                    'email': key,
                                    'title': title}
                            write_csv(data)

                info = resp.html.xpath('//a')
                for key in info:
                    if re.search(r'\bКонтак', key.text):
                        print('д проверки', key.xpath('//@href')[0])
                        if re.search(r'\bhtt', key.xpath('//@href')[0]):
                            email = search_email(key.xpath('//@href')[0])
                            #print('email', email)
                            if not check_email(email):
                                print('email', email)
                                data = {'url': url,
                                        'email': email,
                                        'title': title}
                                write_csv(data)
                        else:
                            print(url + key.xpath('//@href')[0])
                            email = search_email(url + key.xpath('//@href')[0])
                            #print('email', email)
                            if not check_email(email):
                                print('email', email)
                                data = {'url': url,
                                        'email': email,
                                        'title': title}
                                write_csv(data)

                #     if re.search(r'\bКонтак', key.text):
                #         print(key.text)
                #         print('д проверки', key.xpath('//@href')[0])
                #         if re.search(r'\bhtt', key.xpath('//@href')[0]):
                #             email = search_email(key.xpath('//@href')[0])
                #         else:
                #             #print(url + key.xpath('//@href')[0])
                #             email = search_email(url + key.xpath('//@href')[0])
                #
                #
                # title = resp.html.xpath('//title')[0].text
                #
                #
                # data = {'url': url,
                #         'email': email,
                #         'title': title}
                # write_csv(data)





if __name__ == '__main__':
    main()