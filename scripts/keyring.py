import sqlite3


class KeyRing:
    """For a user, stores current and previous keys per username per domain."""

    def __init__(self, name):
        """Initialize KeyRing database by name."""
        self._name = name
        self._db = None

        # connect to database, create table
        self.create_connection(name)
        self.create_table()

    def create_connection(self, name):
        """Database connection."""

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

        self._db.close()

    def update_table(self, update):
        """
        update: (domain:str, username:str, key:str, date_updated:str)
        """

        sql = """
            INSERT INTO keyring(domain, username, key, date_updated)
            VALUES(?, ?, ?, ?);
            """

        self.create_connection(self._name)
        self._db.cursor().execute(sql, update)
        self._db.commit()
        self._db.close()

    def fetch_query(self, domain=False, username=False):
        """Queries KeyRing db for three scenarios:
        1. No domain = fetch domain list.
        2. Domain entered = fetch username list.
        3. Domain and username entered = fetch most recent key."""

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

        self.create_connection(self._name)
        cursor = self._db.cursor()
        cursor.execute(sql)
        result_holder = self.yield_results(cursor.fetchall())
        self._db.close()

        # remove beginning "{" and ending "}" char added when yielded
        return [x[0].strip('{').rstrip('}') for x in next(result_holder)]

    def export_txt(self):
        """Exports to a text file of all most recent key data to program root directory."""

        sql = """
            SELECT domain, username, key, date_updated
            FROM keyring
            GROUP BY domain, username
            HAVING MAX(date_updated);
            """

        self.create_connection(self._name)
        cursor = self._db.cursor()
        cursor.execute(sql)
        result_holder = self.yield_results(cursor.fetchall())
        self._db.close()

        with open(f'{self._name}s_keys.txt', 'w') as outfile:
            string = 'domain, username\n' + '-' * 30 + '\n'  # header display
            for row in next(result_holder):
                # [domain], [username]
                #       updated: [date]
                #       key:     [key]
                string += f'{row[0]}, {row[1]}\n\tupdated {row[3][:10]}\n\tkey\t{row[2]}\n'

            outfile.write(string)

    def yield_results(self, cursor_obj):
        """Generator for cursor object.
        SQL queries will call this method to allow for safe connection close."""

        new_iterator = []
        for each in cursor_obj:
            new_iterator.append(each)
        yield new_iterator
