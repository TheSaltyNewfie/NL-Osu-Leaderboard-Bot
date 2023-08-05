import mysql.connector
import os

db_host = os.environ.get("MYSQL_IP")
db_user = os.environ.get("MYSQL_USER")
db_password = os.environ.get("MYSQL_PASS")
db_name = os.environ.get("MYSQL_DB_NAME")

def add_players(username, osu_id, country, is_nl):
    try:
        connection = mysql.connector.connect(
        host=db_host,
        user = db_user,
        password=db_password,
        database=db_name
        )

        cursor = connection.cursor()

        insert_query =  """
                        INSERT INTO osu_players (username, osu_id, country, is_nl)
                        VALUES (%s, %s, %s, %s)
                        """

        player_data = (username, osu_id, country, is_nl)

        cursor.execute(insert_query, player_data)

        connection.commit()

        return "Player added successfully!"
    except mysql.connector.Error as error:
        return f"Error while executing: {error}"
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

