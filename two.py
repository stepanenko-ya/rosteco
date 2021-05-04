from bs4 import BeautifulSoup
import pymssql
import psycopg2
import requests
from fake_useragent import UserAgent
import random
from random import choice
proxy_lst = ['183.88.226.50:8080']
GLOBAL_URL = 'https://www.rosteco.ru/'
schema_name = "Rosteco"
url = 'https://www.rosteco.ru/catalog/'


conn = pymssql.connect(
    server="10.175.1.60:1433",
    user="importer_doc",
    password='QAZxsw123',
    database="Test")

db = conn.cursor()

def creating():
    # db.execute(f"CREATE SCHEMA {schema_name}")
    # conn.commit()

    db.execute(f"CREATE TABLE {schema_name}.items (id int IDENTITY(1,1), "
               f"vendor_code NVARCHAR(230), "
               f"name NVARCHAR(355), "
               f"item_url NVARCHAR(330),"
               f" photo NVARCHAR(255), "
               f"categories NVARCHAR(330), "
               f"discript ntext)")
    conn.commit()

    # db.execute(f"CREATE TABLE {schema_name}.params (id int IDENTITY(1,1),  vendor_code NVARCHAR (130), name NVARCHAR (130), value NVARCHAR (330))")
    # conn.commit()


def get_html(url):
    print(url)
    req = requests.get(url, headers={"User-Agent": UserAgent().chrome}, timeout=10)

    return req.content



def parsing_item():
    a = 0
    file_item_url = open("items.txt", "r")
    items = file_item_url.readlines()
    for item in items:
        item_html = get_html(item.strip())
        soup = BeautifulSoup(item_html, "html.parser")
        name = soup.find(class_='description').find("h2").get_text()
        discript = soup.find(class_="fulldescription").get_text()
        item_discript = discript.replace("\r\n", '')
        description_text = item_discript.replace('\n', '')
        vendor_code = soup.find(class_="info-line red").get_text().split(":")[1]
        img = soup.find(class_="img-box").find("a").get("href")
        photo = GLOBAL_URL + img
        categories = soup.find(class_='crumbs').get_text().replace(" ", '').replace("\n", '')
        # file_params = open("result.csv", "a+")
        # file_params.write(vendor_code + "|" + name + "|" + item.strip() + "|" + photo + "|" + categories + "|" + description_text + "\n")
        # file_params.close()

    # db.execute(f" insert into ros.items (vendor_code, name, item_url, photo, categories, discript) values('{vendor_code}', '{name}','{items[2].strip()}',  '{photo}', '{categories}', '{item_discript}')")
    # conn.commit()

        finders = soup.find_all(class_="info-line")
        file_par = open("params.csv", "a+")
        a += 1
        for finder in finders:
            p = finder.get_text().strip()
            params = p.replace('\n', " ")
            w = params.replace("\r     ", '')
            x = w.split(":")

            name = x[0]
            value = x[1]
            file_par.write(vendor_code + "|" + name + "|" + value + "\n")
            print(a)
        file_par.close()


def write_db():
    # with open("params.csv") as params:
    #     res_par = params.readlines()
    #     for val in res_par:
    #         param_result = val.strip().split("|")
    #         p = param_result[2].replace("        ", "").replace("'", '')
    #         db.execute(f"INSERT INTO {schema_name}.params (vendor_code, name, value) "
    #                    f"VALUES (N'{param_result[0]}', N'{param_result[1]}', N'{p.strip()}')")
    #         conn.commit()
    with open("result.csv") as file_items:
        res_items = file_items.readlines()
        for item in res_items:
            item = item.replace("'", '')
            item_value = item.strip().split("|")
            db.execute(f"INSERT INTO {schema_name}.items (vendor_code, name, item_url, photo,  categories, discript) "
                       f"VALUES (N'{item_value[0]}', N'{item_value[1]}', N'{item_value[2]}', "
                       f"N'{item_value[3]}', N'{item_value[4]}', N'{item_value[5]}')")
            conn.commit()





if __name__ == "__main__":
    creating()
    # parsing_item()
    write_db()
