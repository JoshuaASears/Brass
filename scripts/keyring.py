import sqlite3


class KeyRing:
    """Within the keyring.db, creates a table for each profile and
    stores current and previous keys per username per domain."""

    def __init__(self, name):
        """Initialize KeyRing database by name."""
        self._name = name
        self._db = None

        # connect to database, create table
        self.create_connection()
        self.create_table()

    def create_connection(self):
        """Database connection."""

        try:
            self._db = sqlite3.connect(f'.\\data\\keyring.db')
        except sqlite3.Error as e:
            print(e)

    def create_table(self):
        """Creates keyring table if it doesn't exist."""

        sql_create_table = f"""
            CREATE TABLE IF NOT EXISTS {self._name}(
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

    def conn_ex_com_close(self, sql, update=None):
        """Handler for SQLite processing:
        Connect, cursor object, execute, [commit], close, and return result."""
        self.create_connection()
        cursor = self._db.cursor()

        qry_result = None

        # fetch request from db or commit to db
        if update is None:
            cursor.execute(sql)
            qry_result = self.yield_results(cursor.fetchall())
        else:
            cursor.execute(sql, update)
            self._db.commit()

        self._db.close()
        return qry_result

    def update_table(self, update):
        """
        update: (domain:str, username:str, key:str, date_updated:str)
        """

        sql = f"""
            INSERT INTO {self._name}(domain, username, key, date_updated)
            VALUES(?, ?, ?, ?);
            """

        self.conn_ex_com_close(sql, update)

    def fetch_query(self, domain=False, username=False):
        """Queries KeyRing db for three scenarios:
        1. No domain = fetch domain list.
        2. Domain entered = fetch username list.
        3. Domain and username entered = fetch most recent key."""

        sql = ''
        if not domain:
            sql = f"""
                SELECT DISTINCT domain
                FROM {self._name}
                ORDER BY domain;
                """
        elif domain and not username:
            sql = f"""
                SELECT DISTINCT username
                FROM {self._name}
                WHERE domain = '{domain}'
                ORDER BY username;
                """
        elif username:
            sql = f"""
                SELECT key
                FROM {self._name}
                WHERE date_updated = (
                    SELECT MAX(date_updated)
                    FROM {self._name}
                    WHERE domain = '{domain}' AND username = '{username}');
                """

        qry_result = self.conn_ex_com_close(sql)

        # remove beginning "{" and ending "}" char added when yielded
        return [x[0].strip('{').rstrip('}') for x in next(qry_result)]

    def export_txt(self):
        """Exports to a text file of all most recent key data to program root directory."""

        sql = f"""
            SELECT domain, username, key, date_updated
            FROM {self._name}
            GROUP BY domain, username
            HAVING MAX(date_updated);
            """

        qry_result = self.conn_ex_com_close(sql)

        with open('data\\exported_keyring.txt', 'w') as outfile:
            string = 'domain, username\n' + '-' * 30 + '\n'  # header display
            for row in next(qry_result):
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
