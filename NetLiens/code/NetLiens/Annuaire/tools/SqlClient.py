import mysql.connector

""" *******************************************************************************************************************
   SQL Connection
******************************************************************************************************************* """
class SqlClient:

  def __init__(self, pHost, pUser, pPassword, pDatabase):

    self.Database = pDatabase

    self.conn = mysql.connector.connect(host=pHost, user=pUser, password=pPassword, database=pDatabase)

    if self.conn.is_connected():
      self.cursor = self.conn.cursor()

  def __del__(self):
    self.conn.close()

  """ SQL Command ------------------------------------------------------------------------------------------------- """
  def set_command(self, pText):
    self.cursor.execute(str(pText))
    return self.cursor.fetchall()