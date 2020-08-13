import requests
from config import *
from bs4 import BeautifulSoup
import logging
import sqlite3
from sqlite3 import Error
from time import sleep
from datetime import datetime


def create_connection(db, db_script):
    conn = None
    try:
        conn = sqlite3.connect(db)
        with open(db_script) as file:
            sql_script = file.read()
        conn.executescript(sql_script)
    except Error:
        logging.exception(f'DB Connection Error - {Error}')
    finally:
        if conn:
            conn.close()


def post_sql_query(sql_query, db=DB):
    logging.info(f'SQL query to DB - {sql_query}')
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(sql_query)
        except Error:
            logging.exception(f'SQL execute Error - {Error}')
        result = cursor.fetchall()
        return result


def search_currency(currency, main_currency=CURRENCY[MAIN_CURRENCY], headers=HEADER):
    query_url = f'{SEARCH}{currency}+к+{main_currency}'
    result = requests.get(query_url, headers=headers)
    return result


def soup_currency(page):
    parse = BeautifulSoup(page.content, 'html.parser')
    parse_result = parse.findAll("span", {"class": "DFlfde", "data-precision": "2"})
    result = float(parse_result[0].text.replace('\xa0', '').replace(',', '.'))
    return result


def main_body():
    create_connection(DB, DB_SCRIPT)
    get_all_search = {key: search_currency(value) for key, value in CURRENCY.items() if key != MAIN_CURRENCY}
    get_all_soup = {key: soup_currency(value) for key, value in get_all_search.items()}
    col = [i for i in get_all_soup.keys()]
    columns = ",".join(col) + ',datetime'
    place = [str(i) for i in get_all_soup.values()]
    placeholders = ",".join(place) + f',"{datetime.today().strftime("%Y.%m.%d %H:%M:%S")}"'
    sql_query_insert = f'INSERT OR IGNORE INTO currency_rub({columns}) VALUES({placeholders});'
    post_sql_query(sql_query_insert)
    sleep(3600)


if __name__ == '__main__':
    main_body()
