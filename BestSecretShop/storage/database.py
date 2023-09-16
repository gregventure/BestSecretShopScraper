import logging

import pandas as pd
import mysql.connector

from BestSecretShop.credentials import HOST
from BestSecretShop.credentials import USER
from BestSecretShop.credentials import PASSWORD

from BestSecretShop.settings import MYSQL_CATALOGUE_PAGE_FULL_SHOP_DB
from BestSecretShop.settings import MYSQL_CATALOGUE_PAGE_FULL_SHOP_TB


class MySQLCataloguePageFullShopStore():

    def __init__(self):
        self.logger = logging.getLogger(__class__.__name__)
        self.conn = mysql.connector.connect(
            host = HOST,
            user = USER,
            password = PASSWORD,
            database = MYSQL_CATALOGUE_PAGE_FULL_SHOP_DB
        )

        self.table = MYSQL_CATALOGUE_PAGE_FULL_SHOP_TB
        self.logger.info(f"Database_Table: {MYSQL_CATALOGUE_PAGE_FULL_SHOP_DB}.{self.table}")

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()
        self.cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
                id int NOT NULL auto_increment,
                crawl_date DATE,
                crawl_url VARCHAR(1000),
                product_url VARCHAR(1000),
                sku VARCHAR(255),
                brand VARCHAR(255),
                uvp DECIMAL(10,2),
                price DECIMAL(10,2),
                ab_uvp BOOLEAN,
                ab_price BOOLEAN,
                PRIMARY KEY (id)
        )
        """)

        
    def upload_item(self, item):
        ## Define insert statement
        self.cur.execute(f""" insert into {self.table} (
                crawl_date,
                crawl_url,
                product_url,
                sku,
                brand,
                uvp,
                price,
                ab_uvp,
                ab_price
            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                )""", (
            item["crawl_date"],
            item["crawl_url"],
            item["product_url"],
            item["sku"],
            item["brand"],
            item["uvp"],
            item["price"],
            item["ab_uvp"],
            item["ab_price"]
        ))

        # ## Execute insert of data into database
        self.conn.commit()
        self.logger.debug(f"Upload Item: {item}")
        return item
    
    def get_table(self):
        self.cur.execute(f"SELECT * FROM {self.table}")
        table_data = self.cur.fetchall()
        self.logger.info(f"Number of Items from DatabaseTable: {len(table_data)}")
        return table_data

    def get_table_V2(self):
        sql_statement = f"SELECT * FROM {self.table}"
        return pd.read_sql_query(sql_statement, self.conn)

    def close_database(self):
        ## Close cursor & connection to database
        self.cur.close()
        self.conn.close()
        self.logger.debug("Close Database")     