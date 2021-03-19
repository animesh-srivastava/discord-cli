from discord_cli import dbpath
from sqlite3 import connect
from sqlite3 import OperationalError, IntegrityError

def create_database():
    """
    This function create the database
    """
    conn = connect(dbpath)
    c = conn.cursor()
    print("Creating database")
    try:
        c.execute("""
            CREATE TABLE "webhooks" (
                "name"	TEXT UNIQUE,
                "url"	TEXT UNIQUE
            );
        """)
    except OperationalError:
        print("Table already exists")
    conn.commit()
    conn.close()

def checking_if_table_exists():
    """
    Checking if table exists or not
    """
    conn = connect(dbpath)
    c = conn.cursor()
    try:
        c.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' 
            AND name='webhooks';
        """)
        res = c.fetchall()
        conn.close()    
        if res != []:   
            return True
        return False
    except:
        pass
    conn.close()


def add_url(name, url):
    """
    This function will take in a name, and a URL and enter it to the database
    """
    conn = connect(dbpath)
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO "webhooks"(name, url) VALUES(?, ?);
        """, (name, url))
    except IntegrityError:
        print("Values not unique")
    conn.commit()
    conn.close()

def change_url(name, url):
    """
    This function will take in a name, and a URL and change the entry of the
    URL for that name
    """
    conn = connect(dbpath)
    c = conn.cursor()
    try:
        c.execute("""
            UPDATE webhooks SET url = ? WHERE name = ?
        """, (url, name))
    except:
        pass
    conn.commit()
    conn.close()

def delete_url(name):
    """
    This function will delete the URL from the database
    """
    conn = connect(dbpath)
    c = conn.cursor()
    try:
        c.execute("""
            DELETE FROM webhooks WHERE name = ?
        """, (name, ))
    except:
        print("Could not delete from database")
    conn.commit()
    conn.close()


def fetch_url(name):
    """
    This function will fetch the URL for a name
    """
    conn = connect(dbpath)
    c = conn.cursor()
    try:
        c.execute("""
            SELECT url FROM "webhooks"
            WHERE name = ?
        """, (name, ))
        res = c.fetchall()
        conn.close()
        if res != []:
            return res[0][0]
        else:
            print("No value of URL found for name: {}".format(name))
            return False
    except Exception as e:
        print(e)
        print("Could not fetch url")
    conn.close()

def fetch_name(url):
    """
    This function will fetch the name for a url
    """
    conn = connect(dbpath)
    c = conn.cursor()
    try:
        c.execute("""
            SELECT name FROM "webhooks"
            WHERE url = ?
        """, (url, ))
        res = c.fetchall()
        conn.close()
        if res != []:
            return res[0][0]
        else:
            print("No value for name found for URL: {}".format(url))
            return False
    except:
        print("Could not fetch url")
    conn.close()

def list_all():
    """
    This function will list all the urls stored in db
    """
    conn = connect(dbpath)
    c = conn.cursor()
    try:
        c.execute("""
            SELECT name FROM webhooks
        """)
        res = c.fetchall()
        conn.close()
        if res != []:
            return [r[0] for r in res]
        else:
            pass
    except:
        print("Could not list entries.")
    conn.close()
