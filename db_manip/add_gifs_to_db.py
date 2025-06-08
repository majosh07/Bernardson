#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import execute_batch
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def make_connection():
    load_dotenv()
    envs = {
        'db_name' : os.environ.get('DB_NAME'),
        'db_user' : os.environ.get('DB_USER'),
        'db_password' : os.environ.get('DB_PASSWORD'),
        'db_host' : os.environ.get('DB_HOST'),
        'db_port' : os.environ.get('DB_PORT'),
    }
    missing = [key for key, val in envs.items() if val is None]
    if missing:
        raise ValueError(f"Connection failed: {', '.join(missing)}")

    connection = psycopg2.connect(
        dbname=envs['db_name'],
        user=envs['db_user'],
        password=envs['db_password'],
        host=envs['db_host'],
        port=envs['db_port']
    )
  # add logging here

    return connection


def get_all_gifs():
    connection = make_connection()

    with connection.cursor() as cur:
        cur.execute("""
        SELECT url FROM gifs
        ORDER BY id ASC; 
        """,)
        
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(15)

        gif_list = [link[0] for link in cur.fetchall()]
        new_gif_list = []
        for idx, link in enumerate(gif_list, start=1):
            try:
                driver.get(link)
            except Exception as e:
                print("Page load failed:", e)

            time.sleep(2)
            try:
                a_tag = driver.find_element('id', 'media-link')
                img = a_tag.find_element('tag name', 'img').get_attribute('src')

                new_gif_list.append((img, idx))
                print(f"Image {idx}: {new_gif_list[-1][0]}")
            except Exception as e:
                print(f"{link} --> No image found/error {e}")


        driver.close()
        execute_batch(cur, """
            UPDATE gifs
            SET url = %s
            WHERE id = %s;
        """, (new_gif_list))

        connection.commit()


get_all_gifs()
