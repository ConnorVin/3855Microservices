import mysql.connector

db_conn = mysql.connector.connect(host="docker-3855.eastus.cloudapp.azure.com", user="root", password="password", database="events")

db_cursor = db_conn.cursor()
db_cursor.execute('''
          DROP TABLE race_information, athlete_information
          ''')

db_conn.commit()
db_conn.close()