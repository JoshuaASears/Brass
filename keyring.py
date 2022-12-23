import sqlite3


class KeyRing:
    """
    For a user, stores current and previous keys per username per domain.
    """

    def __init__(self, name):
        """Initialize KeyRing data by name."""
        self._name = name
        self._db = None

        self.create_connection(name)
        self.create_table()

    def create_connection(self, name):
        try:
            self._db = sqlite3.connect(f'.\\data\\{name}.db')
        except sqlite3.Error as e:
            print(e)

    def create_table(self):
        """Creates keyring table if it doesn't exist."""
        sql_create_table = """
            CREATE TABLE IF NOT EXISTS keyring(
                domain TEXT,
                username TEXT,
                key TEXT,
                date_updated TEXT);
                """
        try:
            self._db.cursor().execute(sql_create_table)
        except sqlite3.Error as e:
            print(e)

    def update_table(self, update):
        """
        update: (domain:str, username:str, key:str, date_updated:str)
        """
        sql = """
            INSERT INTO keyring(domain, username, key, date_updated)
            VALUES(?, ?, ?, ?);
            """
        self._db.cursor().execute(sql, update)
        self._db.commit()

    def fetch_query(self, domain=False, username=False):
        """Queries KeyRing db for most recent key by domain and username."""
        sql = ''
        if not domain:
            sql = """
                SELECT DISTINCT domain
                FROM keyring
                ORDER BY domain;
                """
        elif domain and not username:
            sql = f"""
                SELECT DISTINCT username
                FROM keyring
                WHERE domain = '{domain}'
                ORDER BY username;
                """
        elif username:
            sql = f"""
                SELECT key
                FROM keyring
                WHERE date_updated = (
                    SELECT MAX(date_updated)
                    FROM keyring
                    WHERE domain = '{domain}' AND username = '{username}');
                """
        cursor = self._db.cursor()
        cursor.execute(sql)
        # remove beginning "{" and ending "}" string formatting added by SQLite
        return [x[0].strip('{').rstrip('}') for x in cursor.fetchall()]
