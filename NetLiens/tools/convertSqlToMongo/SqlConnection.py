import mysql.connector
from mysql.connector import Error


""" *******************************************************************************************************************
   SQL Connection
******************************************************************************************************************* """
class SqlConnection:

  def __init__(self, pHost, pUser, pPassword, pDatabase):
    self.Database = pDatabase
    try:
      self.conn = mysql.connector.connect(host=pHost, user=pUser, password=pPassword, database=pDatabase)
      if self.conn.is_connected():
        print("Connected to \'"+pDatabase+"\' MySQL database")
        self.cursor = self.conn.cursor()

    except Error as e:
      print(e)
      self.conn.close()

  def __del__(self):
    print("Delete SqlConnection instance from database \'"+self.Database+"\'")
    self.conn.close()

  """ SQL Command ------------------------------------------------------------------------------------------------- """
  def set_command(self, pText):
    self.cursor.execute(str(pText))
    return self.cursor.fetchall()

