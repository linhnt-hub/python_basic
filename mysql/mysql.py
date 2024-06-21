import mysql.connector
##### Connect MySQL ###################
 mydb = mysql.connector.connect(
   host="localhost",
   user="linhnt",
   password="Linhnt@123",
   database="tableviews",
   auth_plugin='mysql_native_password',
 )
 mycursor = mydb.cursor()
 
## SQL Command to insert DB ###
 mycursor.execute("DELETE from tables") # Delete tables on Database before INSERT
 sql= "INSERT INTO tables (name, view, file) VALUES (%s, %s, %s)"
 mycursor.executemany(sql,val)
 mydb.commit()
