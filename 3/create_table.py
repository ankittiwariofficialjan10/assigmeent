import sqlite3

# Connecting to sqlite
# connection object
connection_obj = sqlite3.connect('fx.db')
#


# cursor object
cursor_obj = connection_obj.cursor()


# Drop the GEEK table if already exists.
cursor_obj.execute("DROP TABLE IF EXISTS records")

# Creating table
table = """ CREATE TABLE records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            process_id INTEGER NOT NULL,
			SourceCurrency VARCHAR(255) NOT NULL,
			DestinationCurrency CHAR(25) NOT NULL,
			SourceAmount INT,
            ConvertedAmount INT,
			TimeUpdated TEXT,
            FX_rate INT
		); """

cursor_obj.execute(table)

print("Table is Ready")

# Close the connection
connection_obj.close()
