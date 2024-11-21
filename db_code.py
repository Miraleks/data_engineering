import sqlite3
import pandas as pd

db_name = "STAFF.db"

conn = sqlite3.connect(db_name)

# Table 1
table_name = "INSTRUCTOR"
attribute_list = ["ID", "FNAME", "LNAME", "CITY", "CCODE"]


file_path = "/home/project/INSTRUCTOR.csv"
df = pd.read_csv(file_path, names=attribute_list)

df.to_sql(table_name, conn, if_exists="replace", index=False)
print(f"Table {table_name} is ready")

# Table 2
table_name1 = "Departments"
attribute_list1 = ["DEPT_ID", "DEP_NAME", "MANAGER_ID", "LOC_ID"]


file_path1 = "/home/project/Departments.csv"
df1 = pd.read_csv(file_path1, names=attribute_list1)

df1.to_sql(table_name1, conn, if_exists="replace", index=False)
print(f"Table {table_name1} is ready")

query_statement = f"SELECT * FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

query_statement = f"SELECT FNAME FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

query_statement = f"SELECT COUNT(*) FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

data_dict = {
    "ID": [100],
    "FNAME": ["John"],
    "LNAME": ["Doe"],
    "CITY": ["Paris"],
    "CCODE": ["FR"],
}
data_append = pd.DataFrame(data_dict)

data_append.to_sql(table_name, conn, if_exists="append", index=False)
print("Data appended successfully")

query_statement = f"SELECT COUNT(*) FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)


data_dict1 = {
    "DEPT_ID": [9],
    "DEP_NAME": ["Quality Assurance"],
    "MANAGER_ID": [30010],
    "LOC_ID": ["L0010"],
}
data_append = pd.DataFrame(data_dict1)
data_append.to_sql(table_name1, conn, if_exists="append", index=False)
print("Data appended successfully")

query_statement = f"SELECT * FROM {table_name1}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

query_statement = f"SELECT DEP_NAME FROM {table_name1}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

query_statement = f"SELECT COUNT(*) FROM {table_name1}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

conn.close()
