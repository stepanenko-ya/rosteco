from bs4 import BeautifulSoup
import pymssql
import requests
from fake_useragent import UserAgent
import random
from random import choice
#
# conn = pymssql.connect(
#     server="10.175.1.60:1433",
#     user="importer_doc",
#     password='QAZxsw123',
#     database="Test")

# db = conn.cursor()
GLOBAL_URL = 'https://www.rosteco.ru/'
schema_name = "Rosteco"
url = 'https://www.rosteco.ru/catalog/'
proxy_lst = ['202.61.51.204:3128', '132.248.196.2:8080', '45.153.33.166:3128', '8.208.91.118:8888',
              '163.172.221.209:443',
              '157.90.4.42:8099', '51.79.157.202:443', '132.248.196.2:8080',
              '168.119.137.56:3128', '183.88.226.50:8080', '219.92.3.149:8080',
              '51.79.157.202:443', '159.89.221.73:3128', '202.61.51.204:3128',
              '128.199.203.131:80', '183.88.226.50:8080', '80.73.87.198:59175',
             '197.211.207.18:3128',
              '169.204.52.13:8080', '46.151.145.4:53281', '79.120.177.106:8080',
              '190.119.211.74:8080', '191.103.254.145:47324', '45.167.72.22:8080',
              '178.217.140.70:443', '157.90.4.42:8003', '141.98.51.66:8080']


# def creating():
#     db.execute(f"CREATE SCHEMA {schema_name}")
#     conn.commit()
#
#     db.execute(f"create table {schema_name}.items (vendor_code NVARCHAR (230), name NVARCHAR (230), item_url NVARCHAR (230),"
#                f" photo NVARCHAR (230), categories NVARCHAR (230), discript ntext)")
#     conn.commit()
#
#     db.execute(f"create table {schema_name}.params (vendor_code NVARCHAR (130), name NVARCHAR (130), value NVARCHAR (330))")
#     conn.commit()
#



# def get_html(url):
#     x = True
#     while x:
#         rand_ip = choice(proxy_lst)
#         print(rand_ip)
#         prox = {"http": "http://" + rand_ip, "https": "http://" + rand_ip}
#         try:
#             req = requests.get(url, headers={"User-Agent": UserAgent().chrome}, proxies=prox, timeout=10)
#
#         except:
#             print("Try")
#         else:
#             x = False
#             return req.content

def get_html(url):
    print(url)
    rand_ip = '202.61.51.204:3128'

    prox = {"http": "http://" + rand_ip, "https": "http://" + rand_ip}

    req = requests.get(url, headers={"User-Agent": UserAgent().chrome}, timeout=10)

    return req.content


def items_url(categor_links):
    for link in categor_links:
        print(link)
        item_html = get_html(link)
        items_soup = BeautifulSoup(item_html, "html.parser")
        items_u = items_soup.find_all(class_="product")
        file_item = open("items.txt", "a+")
        for item in items_u:
            path = item.find("a").get("href")
            direct_link = GLOBAL_URL + path
            file_item.write(direct_link + "\n")
        file_item.close()


def parsing_item():
    file_item_url = open("items.txt", "r")
    items = file_item_url.readlines()

    for item in items:
        item_html = get_html(item.strip())
        soup = BeautifulSoup(item_html, "html.parser")
        name = soup.find(class_='description').find("h2").get_text().replace('"', "'")
        discript = soup.find(class_="fulldescription").get_text().replace("\n", '')
        vendor_code = soup.find(class_="info-line red").get_text().split(":")[1]
        img = soup.find(class_="img-box").find("a").get("href")
        photo = GLOBAL_URL + img
        categories = soup.find(class_='crumbs').get_text().replace(" ", '').replace("\n", '')

        db.execute(f"INSERT INTO {schema_name}.items VALUES (N'{vendor_code}', N'{name}',N'{item.strip()}',  N'{photo}', N'{categories}', N'{discript}')")
        conn.commit()

        # finders = soup.find_all(class_="info-line")
        # for finder in finders:
        #     params = finder.get_text().split(":")
        #     name = params[0].strip()
        #     value = params[1].strip()
        #
        #
        #     db.execute(f"INSERT INTO {schema_name}.params VALUES (N'{vendor_code}', N'{name}', N'{value}')")
        #     conn.commit()


def categories_urls(url):
    cat_urls = []
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    categoties = soup.find(class_="production-nav").find_all("a")
    for categor in categoties:
        cat_url = categor.get("href")
        cat_urls.append(GLOBAL_URL + cat_url)
    print(cat_urls)
    return cat_urls


if __name__ == "__main__":

    # creating()
    categor_links = categories_urls(url)
    items_url(categor_links)
    # parsing_item()



