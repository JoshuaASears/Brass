from string import ascii_uppercase, ascii_lowercase, digits
from random import choice, shuffle
import json
import csv

# TODO: date/time stamp for creating new key
# TODO: switch data persistence from JSON to db using sqlite


class KeyRing:
    """
    For a user, stores a history of keys per username per domain.
    """

    def __init__(self, name):
        self._owner = name
        self._keys = dict()  # {domain: {username: [history of keys]}}

    def get_owner(self):
        """Returns name of KeyRing as string."""
        return self._owner

    def get_keys(self):
        """Returns KeyRing as dictionary {domain: {username: [history of keys]}}"""
        return self._keys

    def get_domains_usernames(self):
        """Returns list [(domain, [usernames])]."""
        domains_usernames = []
        for domain in self._keys:
            domains_usernames.append((domain, list(self._keys[domain])))
        return domains_usernames

    def get_current_key(self, domain, username):
        """Returns last key in the history of keys for that domain and username."""
        if domain in self._keys:
            if username in self._keys[domain]:
                return self._keys[domain][username][-1]

    def add_domain(self, domain):
        """Adds domain to keys dictionary."""
        if domain not in self._keys:
            self._keys[domain] = dict()

    def add_username(self, domain, username):
        """Adds username to a domain in the keys dictionary."""
        if domain in self._keys:
            if username not in self._keys[domain]:
                self._keys[domain][username] = []

    def create_new_key(self, domain, username, length=14, contains=("U", "L", "D", "S"), special="!@#$%^&*+=?[]()`~"):
        """
        Randomly generates a key for the domain and username.
        *contains specifies which of Uppercase, Lowercase, Digits, and Special characters are included.
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
        self._keys[domain][username].append(new_key)

    def export_keyring_json(self):
        """Exports object as self._owner.JSON"""
        with open(f'.\\data\\{self._owner}.json', 'w') as outfile:
            json.dump({self._owner: self._keys}, outfile, indent=4, sort_keys=True)

    def import_keyring_json(self):
        """Imports over current data. Returns error message if file not found."""
        try:
            with open(f'.\\data\\{self._owner}.json', 'r') as infile:
                self._keys = json.load(infile)[self._owner]
        except FileNotFoundError as error:
            return error

    def export_keyring_csv(self):
        pass

    def import_keyring_csv(self):
        pass

    def save_db(self):
        pass

    def load_db(self):
        pass
