# Module containing the bible books lists and dictionaries

# The dictionary to unlock the code name for the bible book
bible_dict = {

    # Standard chapters
    "gen": "Gen",
    "exo": "Exod",
    "ex": "Exod",
    "lev": "Lev",
    "num": "Num",
    "deu": "Deut",
    "jos": "Josh",
    "judg": "Judg",
    "rut": "Ruth",
    "1 sam": "1Sam",
    "2 sam": "2Sam",
    "1kin": "1Kgs",
    "1kgs": "1Kgs",
    "1 kin": "1Kgs",
    "2kin": "2Kgs",
    "2kgs": "2Kgs",
    "2 kin": "2Kgs",
    "1chr": "1Chr",
    "1 chr": "1Chr",
    "2chr": "2Chr",
    "2 chr": "2Chr",
    "ezr": "Ezra",
    "neh": "Neh",
    "est": "Esth",
    "job": "Job",
    "psa": "Ps",
    "ps": "Ps",
    "pro": "Prov",
    "ecc": "Eccl",
    "son": "Song",
    "of son": "Song",
    "sol": "Song",
    "of sol": "Song",
    "isa": "Isa",
    "jer": "Jer",
    "lam": "Lam",
    "eze": "Ezek",
    "dan": "Dan",
    "hos": "Hos",
    "joe": "Joel",
    "amo": "Amos",
    "oba": "Obad",
    "jon": "Jonah",
    "mic": "Mic",
    "nah": "Nah",
    "hab": "Hab",
    "zep": "Zeph",
    "hag": "Hag",
    "zec": "Zech",
    "mal": "Mal",
    "mt": "Matt",
    "mat": "Matt",
    "mar": "Mark",
    "mk": "Mark",
    "luk": "Luke",
    "joh": "John",
    "jhn": "John",
    "jn": "John",
    "act": "Acts",
    "rom": "Rom",
    "1cor": "1Cor",
    "1 cor": "1Cor",
    "2cor": "2Cor",
    "2 cor": "2Cor",
    "gal": "Gal",
    "eph": "Eph",
    "phili": "Phil",
    "phil": "Phil",
    "col": "Col",
    "1the": "1Thess",
    "1 the": "1Thess",
    "2the": "2Thess",
    "2 the": "2Thess",
    "1tim": "1Tim",
    "1 tim": "1Tim",
    "2tim": "2Tim",
    "2 tim": "2Tim",
    "tit": "Titus",
    "phile": "Phlm",
    "phlm": "Phlm",
    "heb": "Heb",
    "jam": "Jas",
    "jas": "Jas",
    "1pet": "1Pet",
    "1 pet": "1Pet",
    "2pet": "2Pet",
    "2 pet": "2Pet",
    "1joh": "1John",
    "1jhn": "1John",
    "1jn": "1John",
    "1 joh": "1John",
    "1 jhn": "1John",
    "1 jn": "1John",
    "2joh": "2John",
    "2jhn": "2John",
    "2jn": "2John",
    "2 joh": "2John",
    "2 jhn": "2John",
    "2 jn": "2John",
    "3joh": "3John",
    "3jhn": "3John",
    "3jn": "3John",
    "3 joh": "3John",
    "3 jhn": "3John",
    "3 jn": "3John",
    "jude": "Jude",
    "rev": "Rev",

    # Apocrypha
    "tob": "Tob",
    "jdt": "Jdt",
    "judi": "Jdt",
    "gkest": "GkEsth",
    "greek est": "GkEsth",
    "wis": "Wis",
    "sir": "Sir",
    "bar": "Bar",
    "ep jer": "EpJer",
    "of jer": "EpJer",
    "aza": "PrAzar",
    "of aza": "PrAzar",
    "sus": "Sus",
    "bel": "Bel",
    "dr": "Bel",
    "dra": "Bel",
    "1mac": "1Macc",
    "1 mac": "1Macc",
    "2mac": "2Macc",
    "2 mac": "2Macc",
    "1esd": "1Esd",
    "1 esd": "1Esd",
    "man": "PrMan",
    "of man": "PrMan",
    "3mac": "3Macc",
    "3 mac": "3Macc",
    "2esd": "2Esd",
    "2 esd": "2Esd",
    "4mac": "4Macc",
    "4 mac": "4Macc",
    "men": "SgThree",
    "to est": "AddEsth"
}


# The dictionary to unlock the code for the bible book for full chapters
bible_chapt_dict = {

    # Standard chapters
    "gen": "Gen",
    "genesis": "Gen",
    "ex": "Exod",
    "exodus": "Exod",
    "lev": "Lev",
    "leviticus": "Lev",
    "num": "Num",
    "numbers": "Num",
    "deut": "Deut",
    "deuteronomy": "Deut",
    "josh": "Josh",
    "joshua": "Josh",
    "judge": "Judg",
    "judges": "Judg",
    "ruth": "Ruth",
    "1sam": "1Sam",
    "1samuel": "1Sam",
    "1 sam": "1Sam",
    "1 samuel": "1Sam",
    "2sam": "2Sam",
    "2samuel": "2Sam",
    "2 sam": "2Sam",
    "2 samuel": "2Sam",
    "1king": "1Kgs",
    "1kings": "1Kgs",
    "1 king": "1Kgs",
    "1 kings": "1Kgs",
    "2king": "2Kgs",
    "2kings": "2Kgs",
    "2 king": "2Kgs",
    "2 kings": "2Kgs",
    "1chr": "1Chr",
    "1chron": "1Chr",
    "1chronicle": "1Chr",
    "1chronicles": "1Chr",
    "1 chr": "1Chr",
    "1 chron": "1Chr",
    "1 chronicle": "1Chr",
    "1 chronicles": "1Chr",
    "2chr": "2Chr",
    "2chron": "2Chr",
    "2chronicle": "2Chr",
    "2chronicles": "2Chr",
    "2 chr": "2Chr",
    "2 chron": "2Chr",
    "2 chronicle": "2Chr",
    "2 chronicles": "2Chr",
    "ezra": "Ezra",
    "neh": "Neh",
    "nehemiah": "Neh",
    "esth": "Esth",
    "esther": "Esth",
    "job": "Job",
    "ps": "Ps",
    "psalm": "Ps",
    "psalms": "Ps",
    "prov": "Prov",
    "proverb": "Prov",
    "proverbs": "Prov",
    "ecc": "Eccl",
    "eccl": "Eccl",
    "ecclesiastes": "Eccl",
    "song": "Song",
    "songs": "Song",
    "of song": "Song",
    "of songs": "Song",
    "of solomon": "Song",
    "solomon": "Song",
    "isa": "Isa",
    "isaiah": "Isa",
    "jer": "Jer",
    "jeremiah": "Jer",
    "lam": "Lam",
    "lamentation": "Lam",
    "lamentations": "Lam",
    "eze": "Ezek",
    "ezek": "Ezek",
    "ezekiel": "Ezek",
    "ezekial": "Ezek",
    "dan": "Dan",
    "daniel": "Dan",
    "hos": "Hos",
    "hosea": "Hos",
    "joel": "Joel",
    "amos": "Amos",
    "obad": "Obad",
    "obadiah": "Obad",
    "jon": "Jonah",
    "jonah": "Jonah",
    "micah": "Mic",
    "nah": "Nah",
    "nahum": "Nah",
    "hab": "Hab",
    "habakkuk": "Hab",
    "zep": "Zeph",
    "zeph": "Zeph",
    "zephaniah": "Zeph",
    "hag": "Hag",
    "hagg": "Hag",
    "haggai": "Hag",
    "zec": "Zech",
    "zech": "Zech",
    "zechariah": "Zech",
    "mal": "Mal",
    "malachi": "Mal",
    "mt": "Matt",
    "mat": "Matt",
    "matt": "Matt",
    "matthew": "Matt",
    "mark": "Mark",
    "luk": "Luke",
    "luke": "Luke",
    "jn": "John",
    "jhn": "John",
    "john": "John",
    "acts": "Acts",
    "rom": "Rom",
    "romans": "Rom",
    "1cor": "1Cor",
    "1corinthians": "1Cor",
    "1 cor": "1Cor",
    "1 corinthians": "1Cor",
    "2cor": "2Cor",
    "2corinthians": "2Cor",
    "2 cor": "2Cor",
    "2 corinthians": "2Cor",
    "gal": "Gal",
    "galatians": "Gal",
    "eph": "Eph",
    "ephesians": "Eph",
    "phil": "Phil",
    "phili": "Phil",
    "philippians": "Phil",
    "col": "Col",
    "colossians": "Col",
    "1thess": "1Thess",
    "1thes": "1Thess",
    "1thessalonians": "1Thess",
    "1 thess": "1Thess",
    "1 thes": "1Thess",
    "1 thessalonians": "1Thess",
    "1tim": "1Tim",
    "1timothy": "1Tim",
    "1 tim": "1Tim",
    "1 timothy": "1Tim",
    "2tim": "2Tim",
    "2timothy": "2Tim",
    "2 tim": "2Tim",
    "2 timothy": "2Tim",
    "tit": "Titus",
    "titus": "Titus",
    "phlm": "Phlm",
    "phile": "Phlm",
    "philemon": "Phlm",
    "heb": "Heb",
    "hebrew": "Heb",
    "hebrews": "Heb",
    "jas": "Jas",
    "jame": "Jas",
    "james": "Jas",
    "1pet": "1Pet",
    "1peter": "1Pet",
    "1 pet": "1Pet",
    "1 peter": "1Pet",
    "2pet": "2Pet",
    "2peter": "2Pet",
    "2 pet": "2Pet",
    "2 peter": "2Pet",
    "1jn": "1John",
    "1jhn": "1John",
    "1john": "1John",
    "1 jn": "1John",
    "1 jhn": "1John",
    "1 john": "1John",
    "2jn": "2John",
    "2jhn": "2John",
    "2john": "2John",
    "2 jn": "2John",
    "2 jhn": "2John",
    "2 john": "2John",
    "3jn": "3John",
    "3jhn": "3John",
    "3john": "3John",
    "3 jn": "3John",
    "3 jhn": "3John",
    "3 john": "3John",
    "jude": "Jude",
    "rev": "Rev",
    "revelation": "Rev",
    "revelations": "Rev",

    # Apocrypha
    "tob": "Tob",
    "tobit": "Tob",
    "tobias": "Tob",
    "jdt": "Jdt",
    "judith": "Jdt",
    "gkesth": "GkEsth",
    "gkesther": "GkEsth",
    "grkesth": "GkEsth",
    "grkesther": "GkEsth",
    "gk esth": "GkEsth",
    "gk esther": "GkEsth",
    "grk esth": "GkEsth",
    "grk esther": "GkEsth",
    "greek esth": "GkEsth",
    "greek esther": "GkEsth",
    "wis": "Wis",
    "wisdom": "Wis",
    "sir": "Sir",
    "sirach": "Sir",
    "bar": "Bar",
    "baruch": "Bar",
    "ep jer": "EpJer",
    "ep jeremiah": "EpJer",
    "of jer": "EpJer",
    "of jeremiah": "EpJer",
    "ltr of jer": "EpJer",
    "let of jer": "EpJer",
    "lett of jer": "EpJer",
    "letr of jer": "EpJer",
    "lettr of jer": "EpJer",
    "letter of jer": "EpJer",
    "let of jeremiah": "EpJer",
    "lett of jeremiah": "EpJer",
    "letr of jeremiah": "EpJer",
    "lettr of jeremiah": "EpJer",
    "letter of jeremiah": "EpJer",
    "azar": "PrAzar",
    "azariah": "PrAzar",
    "of azar": "PrAzar",
    "of azariah": "PrAzar",
    "sus": "Sus",
    "susan": "Sus",
    "susanna": "Sus",
    "bel": "Bel",
    "dr": "Bel",
    "drg": "Bel",
    "drag": "Bel",
    "dragon": "Bel",
    "1mac": "1Macc",
    "1macc": "1Macc",
    "1maccabees": "1Macc",
    "1 mac": "1Macc",
    "1 macc": "1Macc",
    "1 maccabees": "1Macc",
    "2mac": "2Macc",
    "2macc": "2Macc",
    "2maccabees": "2Macc",
    "2 mac": "2Macc",
    "2 macc": "2Macc",
    "2 maccabees": "2Macc",
    "1esd": "1Esd",
    "1esdra": "1Esd",
    "1esdras": "1Esd",
    "1 esd": "1Esd",
    "1 esdra": "1Esd",
    "1 esdras": "1Esd",
    "man": "PrMan",
    "of man": "PrMan",
    "mana": "PrMan",
    "of mana": "PrMan",
    "manasseh": "PrMan",
    "of manasseh": "PrMan",
    "3mac": "3Macc",
    "3macc": "3Macc",
    "3maccabees": "3Macc",
    "3 mac": "3Macc",
    "3 macc": "3Macc",
    "3 maccabees": "3Macc",
    "2esd": "2Esd",
    "2esdra": "2Esd",
    "2esdras": "2Esd",
    "2 esd": "2Esd",
    "2 esdra": "2Esd",
    "2 esdras": "2Esd",
    "4mac": "4Macc",
    "4macc": "4Macc",
    "4maccabees": "4Macc",
    "4 mac": "4Macc",
    "4 macc": "4Macc",
    "4 maccabees": "4Macc",
    "men": "SgThree",
    "add to esth": "AddEsth",
    "add to esther": "AddEsth",
    "addition to esth": "AddEsth",
    "addition to esther": "AddEsth",
    "additions to esth": "AddEsth",
    "additions to esther": "AddEsth"
}

# The set of bible books that only have one chapter
one_chapt_books = {

    # Standard chapters
    "Obad", "Phlm", "2John", "3John", "Jude",
    
    # Apocryphas
    "EpJer", "PrAzar", "Sus", "Bel", "PrMan", "SgThree"
}

# The set of bible books that are part of the apocrypha
biblical_apocrypha = {"Tob", "Jdt", "GkEsth", "Wis", "Sir", "Bar", "EpJer", "PrAzar", "Sus", "Bel", "1Macc", "2Macc", "1Esd", "PrMan", "3Macc", "2Esd", "4Macc", "SgThree", "AddEsth"}

# The set of bible books that are not part of the apocrypha supported by the catholic versions of the bible
apocrypha_not_supported_by_catholic_ver = {"EpJer", "PrAzar", "Sus", "Bel", "1Macc", "2Macc", "1Esd", "PrMan", "3Macc", "2Esd", "4Macc", "SgThree", "AddEsth"}
