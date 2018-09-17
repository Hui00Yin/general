import psycopg2

try:
    conn = psycopg2.connect("dbname='file_changesdb' user='tester' host='HuiDocker' password='W4terl001'")
    cur = conn.cursor()
    cur.execute("""SELECT datname from pg_database""")
    print "{}".format(cur)
except:
    print "I am unable to connect to the database"
