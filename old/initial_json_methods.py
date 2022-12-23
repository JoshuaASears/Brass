# methods from keyring.py with JSON only data persistence
import json
import csv


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