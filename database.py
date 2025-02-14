import sqlitecloud
import csv
conn = sqlitecloud.connect("sqlitecloud://cpzwofi5hz.g1.sqlite.cloud:8860/chinook.sqlite?apikey=BGasV9g3GJsU4FCLb18zlArPh6SqfqRwKIXFxljvUpo")
cursor = conn.cursor()
cursor.execute("SELECT * FROM Love")
rows = cursor.fetchall()
csv_file = "valentines/love_data.csv"


with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)    
    writer.writerow(["ID", "Name", "Status", "Date Created"]) 
    writer.writerows(rows)
conn.close()

print(f"Data successfully exported to {csv_file}")
