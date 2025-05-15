import mysql.connector

try:
    connection = mysql.connector.connect(
        host = "localhost",
        user= "root",
        password = "Optimusisarobot",
        database = "testdb"
    )

    if connection.is_connected():
        print("succses")

        cursor = connection.cursor()
        sql = "INSERT INTO project (idproject, id, name, num) VALUES (%s,%s, %s, %s)"
        values = (34, 1, "Alex the great", 45)

        cursor.execute(sql, values)
        connection.commit()

        print("wow")

        # row = cursor.fetchall()

        # for r in row:
        #     print(r)


except mysql.connector.Error as e:
    print( e) 

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed.")