import psycopg2
from datetime import datetime
import traceback
import properties
import os


class DatabaseUtil:
    mydb = psycopg2.connect(
        host=properties.host,
        port=properties.port,
        user=properties.user,
        password=properties.password,
        database=properties.database
    )
    mydb.autocommit = True
    mycursor = mydb.cursor()

    # Generting log file with error
    @staticmethod
    def log(txt):
        os.makedirs("logs", exist_ok=True)
        db_log_file_name = 'logs/' + "database_log"
        timestamp = str(datetime.now()) + ': \n'
        try:
            with open(db_log_file_name + '.txt', 'a+') as fp:
                fp.write(timestamp + str(txt) + '\n\n')
        except Exception:
            pass

    # Listing all items from table
    def list_all_items(self):
        query = "Select item_id, item_name, item_description, item_price from items"
        results = []
        try:
            self.mycursor.execute(query)
            results = self.mycursor.fetchall()
        except Exception as db_error:
            self.log("FETCH ERROR: " + query + str(db_error))
        return results

    # Inserting new item in table
    def insert_item_row(self, name, description, price):
        query = "INSERT INTO items(item_name, item_description, item_price) VALUES ('" + \
                str(name) + "', '" + \
                str(description) + "', " + \
                str(price) + ") returning item_id"
        try:
            self.mycursor.execute(query)
            results = self.mycursor.fetchall()
            return results
        except Exception as db_error:
            self.log("Insert ERROR: " + query + str(db_error))
            self.log(traceback.format_exc())
            return None

    # Get item detail using Item ID
    def get_item_detail(self, item_id):
        query = "Select item_id, item_name, item_description, item_price from items where item_id=" + str(item_id)
        results = None
        try:
            self.mycursor.execute(query)
            results = self.mycursor.fetchall()
        except Exception as db_error:
            self.log("FETCH ERROR: " + query + str(db_error))
        return results

    # Deleting the item by Item id
    def delete_item(self, item_id):
        query = "Delete from items where item_id=" + str(item_id)
        try:
            self.mycursor.execute(query)
        except Exception as db_error:
            self.log("Update ERROR: " + query + str(db_error))
            self.log(traceback.format_exc())
