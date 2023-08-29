import argparse
import json
import socket
import time
import psycopg2

def connectPsqlRoot(autocommit = False):
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="123qwe"
    )
    cur = conn.cursor()
    conn.autocommit = autocommit
    return conn, cur

dbName = 'db_postgres_test'
dbUser = 'db_postgres_test'
dbPass = 'db_postgres_test'
def connectPsql(autocommit = False):
    conn = psycopg2.connect(
        host="localhost",
        database=dbName,
        user=dbUser,
        password=dbPass
    )
    cur = conn.cursor()
    conn.autocommit = autocommit
    return conn, cur

def psqlQuery(cur, sql, autocommit = False):
    cur.execute(sql)
    records = cur.fetchall()
    print(f'result: {records}')
    return records


_, cur = connectPsqlRoot()
result = psqlQuery(cur, f"""
SELECT 1 FROM pg_user WHERE usename = '{dbUser}';
""")
if result:
    pass
else:
    result = psqlQuery(cur, f"""
    CREATE USER {dbUser} WITH PASSWORD '{dbPass}';
    """)


result = psqlQuery(cur, """
SELECT 1 FROM pg_database WHERE datname = 'db_postgres_test';
""")
if result:
    pass
else: 
    conn, cursor = connectPsqlRoot(autocommit=True)
    cursor.execute(f'CREATE DATABASE {dbName}')
    cursor.execute(f'GRANT ALL PRIVILEGES ON DATABASE {dbName} TO {dbUser}')
    cursor.close()
    conn.close()



result = psqlQuery(cur, """
SELECT 1 FROM pg_database WHERE datname = 'db_postgres_test';
""")
if result:
    pass
else: 
    conn, cursor = connectPsql(autocommit=True)
    cursor.execute(f'CREATE DATABASE {dbName}')
    cursor.execute(f'GRANT ALL PRIVILEGES ON DATABASE {dbName} TO {dbUser}')
    cursor.close()
    conn.close()

conn, cur = connectPsql(autocommit=True)
cur.execute(f"""
CREATE TABLE IF NOT EXISTS test (
    did     integer PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    title   varchar(40) NOT NULL
);
""")
cur.close()
conn.close()





parser = argparse.ArgumentParser()
parser.add_argument('--count', type = int, default = 1, help='count of iterations')
args = parser.parse_args()
# print(f'args: {args}')
count = args.count
print(f'count: {count}')

obj = {
    # "auth_token": "123zxy456!@#",
    # "id": "123",
    # "sql": {
    #     "database": "database1",
    #     "sql": "select 1;",
    # },
    # "python": {
    #     "script": "py-test",
    #     "params": {
    #         "a": 4,
    #         "b": 7,
    #     },
    # },
    # "executable": {
    #     "name": "executable-test",
    #     "params": {
    #         "a": 4,
    #         "b": 7,
    #     },
    # }
}

if obj:
    requestJsonStr = json.dumps(obj)
    print(f'requestJsonStr: {requestJsonStr}')
    sendBytes = requestJsonStr.encode('utf-8')
    for i in range(count):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect(('127.0.0.1', 8899))
        clientSocket.sendall(sendBytes)
        data = clientSocket.recv(4096)
        received = json.loads(data)
        print(f'received: {json.dumps(received, indent = 4)}')
        clientSocket.close()
        # time.sleep(100 / 1000)

# exit()
invalidJson = [
    # '"auth_token": "123zxy456!@#", "id": "123", "sql": {"database": "database", "sql": "select 1;"}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "sql": {"database": "database", "sql": "select 1;"}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "sql": {"database": "databas',

    # '"auth_token": "123zxy456!@#", "id": "123", "python": {"script": "py-test", "params": {"a": 4, "b": 7}}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "python": {"script": "py-test", "params": {"a": 4, "b": 7}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "python": {"script": "py-test", ',

    # '"auth_token": "123zxy456!@#", "id": "123", "executable": {"name": "executable-test", "params": {"a": 4, "b": 7}}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "executable": {"name": "executable-test", "params": {"a": 4, "b": 7}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "executable": {"name": "executable-test", ',

    # '{"auth_tokenNNN": "123zxy456!@#", "id": "123", "sql": {"database": "database", "sql": "select 1;"}}',
    # '{"auth_token": "123zxy456!@#", "idDDD": "123", "sql": {"database": "database", "sql": "select 1;"}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "sql@@@": {"database": "database", "sql": "select 1;"}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "python@@@": {"script": "py-test", "params": {"a": 4, "b": 7}}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "executable@@@": {"name": "executable-test", "params": {"a": 4, "b": 7}}}',

    # '{"auth_token": "123zxy456!@#", "id": "123", "sql": {"database": "database", "sql": "select 1;"}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "sql": {"database@@@": "database", "sql": "select 1;"}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "sql": {"database": "database", "sql@@@": "select 1;"}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "sql": {"database": "database@@@", "sql": "select 1;"}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "sql": {"database": "database", "sql": "select@ 1;"}}',

    '{"auth_token": "123zxy456!@#", "id": "123", "sql": {"database": "db-postgres-test", "sql": "select 1;"}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "sql": {"database@@@": "db-postgres", "sql": "select 1;"}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "sql": {"database": "db-postgres", "sql@@@": "select 1;"}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "sql": {"database": "db-postgres@@@", "sql": "select 1;"}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "sql": {"database": "db-postgres", "sql": "select@ 1;"}}',

    # '{"auth_token": "123zxy456!@#", "id": "123", "python": {"script": "py-test", "params": {"a": 4, "b": 7}}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "python": {"script@@@": "py-test", "params": {"a": 4, "b": 7}}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "python": {"script": "py-test@@@", "params": {"a": 4, "b": 7}}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "python": {"script": "py-test", "params@@@": {"a": 4, "b": 7}}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "python": {"script": "py-test", "params": "invalid params"}}',

    # '{"auth_token": "123zxy456!@#", "id": "123", "executable": {"name": "executable-test", "params": {"a": 4, "b": 7}}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "executable": {"name@@@": "executable-test", "params": {"a": 4, "b": 7}}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "executable": {"name": "executable-test@@@", "params": {"a": 4, "b": 7}}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "executable": {"name": "executable-test", "params@@@": {"a": 4, "b": 7}}}',
    # '{"auth_token": "123zxy456!@#", "id": "123", "executable": {"name": "executable-test", "params": "invalid params"}}',
]


print(f'\n\n\t INVALID QUERIES')
for requestJsonStr in invalidJson:
    print(f'\requestJsonStr: {requestJsonStr}')
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(('127.0.0.1', 8899))
    sendBytes = requestJsonStr.encode('utf-8')
    clientSocket.sendall(sendBytes)
    data = clientSocket.recv(4096)
    try:
        received = json.loads(data)
        print(f'received: {json.dumps(received, indent = 4)}')
    except Exception as err:
        print(f'received: {received}')
    clientSocket.close()

