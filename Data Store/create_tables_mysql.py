import mysql.connector

db_conn = mysql.connector.connect(host="localhost", user="root", password="password", database="events")

db_cursor = db_conn.cursor()
db_cursor.execute('''
          CREATE TABLE race_information
          (id INT NOT NULL AUTO_INCREMENT,
           race_id VARCHAR(250) NOT NULL,
           swim VARCHAR(250) NOT NULL,
           distance INTEGER NOT NULL,
           distance_measurement VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT race_information_pk PRIMARY KEY (id))
          ''')

db_cursor.execute('''
          CREATE TABLE athlete_information
          (id INT NOT NULL AUTO_INCREMENT, 
           first_name VARCHAR(25) NOT NULL,
           last_name VARCHAR(25) NOT NULL,
           age INTEGER NOT NULL,
           height INTEGER NOT NULL,
           weight VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT athlete_information_pk PRIMARY KEY (id))
          ''')

db_conn.commit()
db_conn.close()