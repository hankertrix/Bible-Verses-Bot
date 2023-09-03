# The module containing the utility functions used in the bot

# The dictionary of normal characters to superscript characters
sups = {
    u'0': u'\u2070',
    u'1': u'\xb9',
    u'2': u'\xb2',
    u'3': u'\xb3',
    u'4': u'\u2074',
    u'5': u'\u2075',
    u'6': u'\u2076',
    u'7': u'\u2077',
    u'8': u'\u2078',
    u'9': u'\u2079',
    u'-': u'\u207b',
    u'–': u'\u207b',
    u'a': u'\u1d43',
    u'b': u'\u1d47',
    u'L': u'\u1d38',
    u'T': u'\u1d40',
    u'C': u'\u1d9c',
    u'(': u'\u207d',
    u')': u'\u207e',
    u':': u'\x60\ufeff\u1804\x20\x60'
}


# Function to makes the verse numbers, dashes and the small markers superscript
def to_sups(text):

    # The converted text with superscripts
    sup_text = "".join(sups.get(char, char) for char in text)

    # Adds backticks and a zero-width non-breaking space to fix Telegram's ugly superscript characters
    return "`" + sup_text + "`\xa0"