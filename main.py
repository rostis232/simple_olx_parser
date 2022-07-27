# It`s very simple olx.ua parser. It can parse name, price, address and url.


import requests
from bs4 import BeautifulSoup
import csv

# enter category url here:
main_url = 'https://www.olx.ua/uk/detskiy-mir/'

# enter count of pages:
all_pages = 25


def write_csv(result):
    with open('file.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['ser=,'])
        for item in result:
            writer.writerow( (item['name'],
                              item['price'],
                              item['address'],
                              item['url']
                              ))


def clean(text):
    return text.replace('\t', '').replace('\n', '').strip()


def get_data(page_url):
    r = requests.get(page_url)
    soup = BeautifulSoup(r.content)
    table = soup.find('table', {'id': 'offers_table'})
    rows = table.find_all('tr', {'class': 'wrap'})
    result = []
    for row in rows:
        name = clean(row.find('h3').text)
        url = row.find('h3').find('a').get('href')
        price = clean(row.find('p', {'class': 'price'}).text)
        bottom = row.find('td', {'valign': 'bottom'})
        address = clean(bottom.find('small', {'class': 'breadcrumb x-normal'}).text)
        item = {'name': name, 'price': price, 'address': address, 'url': url,}
        result.append(item)
    return result


def main(main_url, all_pages):
    r = requests.get(main_url)
    soup = BeautifulSoup(r.content)
    result = []
    for i in range(1, all_pages+1):
        print('Parsing page ', str(i), ' of ', str(all_pages))
        page_url = main_url + '?page=' + str(i)
        result += get_data(page_url)
    write_csv(result)


if __name__ == '__main__':
    main(main_url, all_pages)