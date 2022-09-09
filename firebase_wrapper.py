# The module containing the wrapper for the firebase database

import os
from collections import abc
from typing import Any, Iterator, AbstractSet
from firebase_admin import initialize_app, credentials, db

# The firebase keys
firebase_keys = {
  "type": os.environ["FIREBASE_TYPE"],
  "project_id" : os.environ["FIREBASE_PROJECT_ID"],
  "private_key_id": os.environ["FIREBASE_PRIVATE_KEY_ID"],
  "private_key": os.environ["FIREBASE_PRIVATE_KEY"],
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

# The database reference for the bot
bot = "/bible_verses_bot"

# The database class (mimics a Python dictionary)
class Database(abc.MutableMapping):
  """A dictionary-like database wrapper for firebase"""

  
  def __init__(self) -> None:
    self.db = db

  
  def __getitem__(self, key: str) -> Any:
    """Gets a value for a key in the database"""

    # Gets the value from the database
    value =  self.db.reference(f"/{bot}/{key}").get()

    # If the value is empty, raise a key error
    if not value:
      raise KeyError(key)

    # Otherwise returns the value
    return value

  
  def __setitem__(self, key: str, value: Any) -> None:
    """Sets a value for a key in the database"""

    # Sets the value in the database
    self.db.reference(f"/{bot}/{key}").set(value)

  
  def __delitem__(self, key: str) -> None:
    """Deletes a key from the database"""

    # Deletes the item from the database
    self.db.reference(f"/{bot}/{key}").delete()


  def __iter__(self) -> Iterator[Any]:
    """The iterator for the database"""

    # Returns an iterator of all the keys in the database
    return iter(self.db.reference(f"/{bot}").get())


  def __len__(self) -> int:
    """The number of keys in the database"""

    # Returns the number of keys
    return len(self.db.reference(f"/{bot}").get())


  def keys(self) -> AbstractSet[str]:
    """Gets all the keys in the database"""

    # Returns all the keys as a set
    return set(self.db.reference(f"/{bot}").get())




