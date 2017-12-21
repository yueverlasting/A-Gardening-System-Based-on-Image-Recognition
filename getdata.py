import pymysql.cursors
import string

connection = pymysql.connect(host='localhost',
							 user='root',
							 password='',
							 db='plant_system',
							 charset='utf8',
							 cursorclass=pymysql.cursors.DictCursor)
							 
cursor = connection.cursor()

cursor.execute("SELECT temp_high FROM plant_info WHERE type='mint'")

row = cursor.fetchone()
while row is not None:
  print(row)
  row = cursor.fetchone()
  [int(s) for row in row.split() if s.isdigit()]
  print(s)
  
print('')
print('connection start')