import sqlite3
print("connect", flush=True)
conn = sqlite3.connect("./chroma_db/chroma.sqlite3")
print("cursor", flush=True)
c = conn.cursor()
print("execute", flush=True)
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("fetch", flush=True)
print(c.fetchall())
