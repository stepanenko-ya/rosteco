from bs4 import BeautifulSoup
import pymssql
import requests
from fake_useragent import UserAgent
import random
from random import choice

conn = pymssql.connect(
    server="10.175.1.60:1433",
    user="importer_doc",
    password='QAZxsw123',
    database="Test")

db = conn.cursor()
GLOBAL_URL = 'https://www.rosteco.ru/'
schema_name = "Rosteco"
url = 'https://www.rosteco.ru/catalog/'

proxy_lst = ['109.89.207.252:8080']

def creating():
    db.execute(f"CREATE SCHEMA {schema_name}")
    conn.commit()

    db.execute(f"create table {schema_name}.items (vendor_code NVARCHAR (230), name NVARCHAR (230), item_url NVARCHAR (230),"
               f" photo NVARCHAR (230), categories NVARCHAR (230), discript ntext)")
    conn.commit()

    db.execute(f"create table {schema_name}.params (vendor_code NVARCHAR (130), name NVARCHAR (130), value NVARCHAR (130))")
    conn.commit()


def get_html(url):
    x = True
    while x:
        rand_ip = choice(proxy_lst)
        prox = {"http": "http://" + rand_ip, "https": "http://" + rand_ip}
        try:
            req = requests.get(url, headers={"User-Agent": UserAgent().chrome}, proxies=prox, timeout=10)
        except:
            print("Try")
        else:
            x = False
            print(req.status_code)
            return req.content



def items_url(categor_links):
    for link in categor_links:
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
        name = soup.find(class_='description').find("h2").get_text()
        discript = soup.find(class_="fulldescription").get_text().replace("\n", '')
        vendor_code = soup.find(class_="info-line red").get_text().split(":")[1]
        img = soup.find(class_="img-box").find("a").get("href")
        photo = GLOBAL_URL + img
        categories = soup.find(class_='crumbs').get_text().replace(" ", '').replace("\n", '')

        db.execute(f"INSERT INTO {schema_name}.items VALUES (N'{vendor_code}', N'{name}',N'{item.strip()}',  N'{photo}', N'{categories}', N'{discript}')")
        conn.commit()

        finders = soup.find_all(class_="info-line")
        for finder in finders:
            params = finder.get_text().split(":")
            name = params[0].strip()
            value = params[1].strip()

            db.execute(f"INSERT INTO {schema_name}.params VALUES (N'{vendor_code}', N'{name}', N'{value}')")
            conn.commit()


def categories_urls(url):
    cat_urls = []
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    categoties = soup.find(class_="production-nav").find_all("a")
    for categor in categoties:
        cat_url = categor.get("href")
        cat_urls.append(GLOBAL_URL + cat_url)
    return cat_urls

if __name__ == "__main__":

    creating()
    # categor_links = categories_urls(url)

    categor_links = ['https://www.rosteco.ru/catalog/baschmak-natyajitelya-uspokoitel', 'https://www.rosteco.ru/catalog/vtulki',
     'https://www.rosteco.ru/catalog/dempferyi', 'https://www.rosteco.ru/catalog/kronshteynyi']

    # items_url(categor_links)
    parsing_item()



