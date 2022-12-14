

import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r"C:\Users\fchee\Downloads\instantclient_21_6")

# Connect as user "hr" with password "welcome" to the "orclpdb1" service running on this computer.
connection = cx_Oracle.connect(user="fcheema4", password="pteewool",
                               dsn="@artemis.vsnet.gmu.edu:1521/vse18c.vsnet.gmu.edu")

cursor = connection.cursor()
cursor.execute("""
        SELECT first_name, last_name
        FROM employees
        WHERE department_id = :did AND employee_id > :eid""",
        did = 50,
        eid = 190)
for fname, lname in cursor:
    print("Values:", fname, lname)