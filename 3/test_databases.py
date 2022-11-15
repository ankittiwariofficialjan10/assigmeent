import sqlite3

# Connecting to sqlite
# connection object
connection_obj = sqlite3.connect('fx.db')
#


# cursor object
cursor_obj = connection_obj.cursor()

cursor_obj.execute("select * from records")
print("All the data")
output = cursor_obj.fetchall()
print(len(output))
for row in output:
  print(row)