import pymssql
from bs4 import BeautifulSoup
import pymssql
import psycopg2
import requests
from fake_useragent import UserAgent
import random
from random import choice


# schema_name = "Rosteco"
file = open("copy.txt", "r")
f = file.readlines()
print(f)
# it = f.strip().split("|")
# print(it)
#
# db.execute(f" INSERT INTO www.items VALUES (N'{it[0]}', N'{it[1]}',N'{it[2]}',  N'{it[3]}', N'{it[4]}', N'{it[5]}')")
# conn.commit()
# conn = psycopg2.connect(user='step',
#                         password='Stomatolog',
#                         host='localhost',
#                         dbname='yana_db')
# db = conn.cursor()


# conn2 = pymssql.connect(
#     server="10.175.1.60:1433",
#     user="importer_doc",
#     password='QAZxsw123',
#     database="Test")
#
# msdb = conn2.cursor()


# db.execute('SELECT * from ros.items')
# result = db.fetchall()
#
# for row in result:
#
#     msdb.execute('INSERT INTO  Rosteco.items VALUES %s', (row,))
#     conn2.commit()
