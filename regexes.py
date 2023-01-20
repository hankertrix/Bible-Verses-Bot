# Module to contain the regular expressions used in the main file

import re

# Regex for finding the "3:14" number portion of the bible verse
number_regex = re.compile(r"\d{1,3}:\d{1,3},?[ \d,:\-]*\b ?(?:rcu17[ts]s)?[A-Za-z\-]*")

# Regex for finding a verse with chapter ... verse ...
chapter_regex = re.compile(r"\bchapter \d{1,3} verses? \d{1,3}-?\d{0,3} ? ?t?o? ?\d{0,3}[ \d,\-]*\b ?(?:rcu17[ts]s)?[A-Za-z\-]*")

# Regex for finding the full chapter
full_chapter_num_regex = re.compile(r"\b(?!chapter|verse|to\b)\w+? \d{1,3}[\d, \-]*(?! :|:)\b ?(?:rcu17[ts]s)?[A-Za-z\-]*|gr?e?e?k esthe?r? \d{1,3}[\d, \-]*(?! :|:)\b ?(?:rcu17[ts]s)?[A-Za-z\-]*|addi?t?i?o?n?s? to esthe?r? \d{1,3}[\d, \-]*(?! :|:)\b ?(?:rcu17[ts]s)?[A-Za-z\-]*|(?:lett?e?r?|ep) ?(?:of)? ?jere?m?i?a?h? \d{1,3}[\d, \-]*(?! :|:)\b ?(?:rcu17[ts]s)?[A-Za-z\-]*")

# Regex for finding the full chapter with the word "chapter"
full_chapter_chapt_regex = re.compile(r"\b[1234]? ?\w+? chapters? \d{1,3}[\d, \-]*\b(?! verse|verse) ?(?:rcu17[ts]s)?[A-Za-z\-]*|gr?e?e?k esthe?r? chapters? \d{1,3}[\d, \-]*\b(?! verse|verse) ?(?:rcu17[ts]s)?[A-Za-z\-]*|addi?t?i?o?n?s? to esthe?r? chapters? \d{1,3}[\d, \-]*\b(?! verse|verse) ?(?:rcu17[ts]s)?[A-Za-z\-]*|(?:lett?e?r?|ep) ?(?:of)? ?jere?m?i?a?h? chapters? \d{1,3}[\d, \-]*\b(?! verse|verse) ?(?:rcu17[ts]s)?[A-Za-z\-]*")

# Regex to find the bible version at the end of the string
bible_version_regex = re.compile(r" [A-Za-z\-]*\Z| rcu17[ts]s\Z")
