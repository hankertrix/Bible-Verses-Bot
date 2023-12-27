# The module containing the wrapper for the firebase database

import os
from collections import abc
from typing import Any, Iterator, KeysView

from firebase_admin import credentials, db, initialize_app

# The firebase keys
firebase_keys = {
    "type": os.environ["FIREBASE_TYPE"],
    "project_id": os.environ["FIREBASE_PROJECT_ID"],
    "private_key_id": os.environ["FIREBASE_PRIVATE_KEY_ID"],
    "private_key": os.environ["FIREBASE_PRIVATE_KEY"].replace("\\n", "\n"),
    "client_email": os.environ["FIREBASE_CLIENT_EMAIL"],
    "client_id": os.environ["FIREBASE_CLIENT_ID"],
    "auth_uri": os.environ["FIREBASE_AUTH_URI"],
    "token_uri": os.environ["FIREBASE_TOKEN_URI"],
    "auth_provider_x509_cert_url": os.environ["FIREBASE_AUTH_PROVIDER_X509_CERT_URL"],
    "client_x509_cert_url": os.environ["FIREBASE_CLIENT_X509_CERT_URL"]
}

# Change the firebase keys into credentials
creds = credentials.Certificate(firebase_keys)

# Initialise the application
initialize_app(creds, {"databaseURL": os.environ["FIREBASE_DB_URL"]})


class Database(abc.MutableMapping):
    "A dictionary-like database wrapper for firebase."

    # Slots to save memory
    __slots__ = ("db", "reference_str", "dic")

    def __init__(
        self,
        reference_str: str,
        dic: abc.Mapping | None = None
    ) -> None:

        self.db = db
        self.reference_str = reference_str

        # Checks if the dictionary of the database is not given
        if dic is None:

            # Sets the dictionary to the value obtained from the database
            self.dic = db.reference(reference_str).get()

        # Otherwise, set the dictionary to the value given
        else:
            self.dic = dic

    def __str__(self) -> str:
        return str(self.dic)

    def __getitem__(self, key: str) -> Any:
        "Gets a value for a key in the database."

        # Gets the value from the dictionary in-memory
        # This should be in sync with the database
        value = self.dic.get(key)

        # If the value is empty, raise a key error
        if not value:
            raise KeyError(key)

        # If the value is a dictionary
        if isinstance(value, abc.Mapping):

            # Returns another instance of the database object
            # with the reference string set to the current
            # reference string and the key, as well as the
            # dictionary of the database set to the value
            # obtained
            return Database(f"{self.reference_str}/{key}", value)

        # Otherwise returns the value
        return value

    def __setitem__(self, key: str, value: Any) -> None:
        "Sets a value for a key in the database."

        # Sets the value in the in-memory dictionary
        self.dic[key] = value

        # Sets the value in the database
        self.db.reference(f"{self.reference_str}/{key}").set(value)

    def __delitem__(self, key: str) -> None:
        "Deletes a key from the database."

        # Deletes the item from the in-memory dictionary
        self.dic.popitem(key)

        # Deletes the item from the database
        self.db.reference(f"{self.reference_str}/{key}").delete()

    def __iter__(self) -> Iterator[Any]:
        "The iterator for the database."

        # Returns an iterator of all the keys in the in-memory dictionary
        # This should be in sync with the database
        return iter(self.dic)

    def __len__(self) -> int:
        "The number of keys in the database."

        # Returns the number of keys in the in-memory dictionary
        # This should be in sync with the database
        return len(self.dic)

    def keys(self) -> KeysView[Any]:
        "Gets all the keys in the database."

        # Returns all the keys
        return self.dic.keys()

    def update_db(self) -> None:
        "Updates the in-memory database with new data."

        # Gets the new data from the database
        # And sets it to the dic property
        self.dic = db.reference(self.reference_str).get()
