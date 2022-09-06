# The database wrapper to use in place of replit's

import json, os
from collections import abc
from request_sess import s
from typing import Any, Iterator, Tuple, AbstractSet
import urllib

# The database class (mimics a Python dictionary)
class Database(abc.MutableMapping):
  """A dictionary-like interface for Repl.it Database."""

  def __init__(self, database_url: str) -> None:
    self.url = database_url
    self.sess = s

  
  def __getitem__(self, key: str) -> Any:
    """Gets a value for a key from the database"""

    # Sends a request to the database
    res = self.sess.get(f"{self.url}/{urllib.parse.quote(key)}")

    # If the key isn't found, raise a key error
    if res.status_code == 404:
      raise KeyError(key)

    # Returns the value for the key
    return json.loads(res.text)


  def __setitem__(self, key: str, value: Any) -> None:
    """Sets a value for a key in the database"""

    # Sends a post request to the database to set the value
    self.sess.post(self.url, data={key: json.dumps(value)})


  def __delitem__(self, key: str) -> None:
    """Deletes a key from the database"""

    # Sends a delete request to the database
    res = self.sess.delete(f"{self.url}/{urllib.parse.quote(key)}")

    # If key isn't found, raise a key error
    if res.status_code == 404:
      raise KeyError(key)


  def __iter__(self) -> Iterator[str]:
    """The iterator for the database"""

    # Returns an iterator of all the keys in the database
    return iter(self.prefix(""))


  def __len__(self) -> int:
    """The number of keys in the database"""

    # Returns the number of keys
    return len(self.prefix(""))


  def prefix(self, prefix: str) -> Tuple[str, ...]:
    """The method to find all the keys in the database with the given prefix"""

    # Sends a request to the database to get all the keys
    res = self.sess.get(self.url, params={"prefix": prefix, "encode": "true"})

    # Returns a tuple of nothing if the response doesn't have any text
    if not res.text:
      return tuple()

    # Otherwise returns the keys found
    else:
      return tuple(urllib.parse.unquote(key) for key in res.text.split("\n"))


  def keys(self) -> AbstractSet[str]:
    """Returns all the keys in the database"""

    return set(self.prefix(""))


  def __repr(self) -> str:
    """A string representation of the database"""

    return f"<{self.__class__.name}(database_url={self.url!r})>"


# The database to use
db = Database(os.environ["DB_URL"])


