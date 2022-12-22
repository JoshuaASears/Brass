from string import ascii_uppercase, ascii_lowercase, digits
from random import choice, shuffle
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

    def create_new_key(self, length=14, contains=("U", "L", "D", "S"), special="!@#$%^&*+=?[]()`~"):
        """
        Randomly generates a key for the domain and username.
        *contains toggles use of Uppercase, Lowercase, Digits, and Special characters.
        *Special is set to a default set but can receive a custom string.
        Returns new key as string.
        """

        # possible sets of characters which *contains will cross-reference
        characters = {
            "U": ascii_uppercase,
            "L": ascii_lowercase,
            "D": digits,
            "S": special
        }

        new_key_builder = []
        all_characters = ""

        for mand_char in contains:
            # add one of each mandatory character
            new_key_builder.append(choice(characters[mand_char]))
            # build total character set for next stage
            all_characters = all_characters + characters[mand_char]
            length -= 1

        # populate remaining length with random char from all_character set
        while length > 0:
            new_key_builder.append(choice(all_characters))
            length -= 1

        # shuffle, join to string, add to KeyRing
        shuffle(new_key_builder)
        new_key = ''.join(new_key_builder)

        return new_key

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

    def query_domain(self):
        """Queries KeyRing db for domains."""
        sql = """
            SELECT DISTINCT domain
            FROM keyring
            ORDER BY domain
            """
        cursor = self._db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()

    def query_username(self, domain=''):
        """Queries KeyRing db for domains."""
        sql = f"""
            SELECT DISTINCT username
            FROM keyring
            WHERE domain = '{domain}'
            ORDER BY username
            """
        cursor = self._db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()
