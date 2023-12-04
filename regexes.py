# Module to contain the regular expressions used in the main file

import re

# Regex for finding the "3:14" number portion of the bible verse
number_regex = re.compile(r"\d{1,3}:\d{1,3},?[ \d,:\-]*\b(?:rcu17[ts]s|[A-Za-z\-]*)?")

# Regex for finding a verse with chapter ... verse ...
chapter_regex = re.compile(r"\bchapter \d{1,3} verses? \d{1,3}-?\d{0,3} *(?:to)?\d{0,3}[ \d,\-]*\b *?(?:rcu17[ts]s|[A-Za-z\-]*)?")

# Regex for finding the full chapter
full_chapter_num_regex = re.compile(r"\b(?!chapter|verse|to\b)(?:[A-Za-z]+?|gr?e?e?k esth?e?r?|addi?t?i?o?n?s? *(?:to)? *esth?e?r?|(?:lett?e?r?|ep) *(?:of)? *jere?m?i?a?h?) *\d[\d, \-]*(?! :|:)\b ?(?:rcu17[ts]s|[A-Za-z\-]*)?")

# Regex for finding the full chapter with the word "chapter"
full_chapter_chapt_regex = re.compile(r"\b[1234]? ?(?:[A-Za-z]+?|gr?e?e?k esth?e?r?|addi?t?i?o?n?s? *(?:to)? *esth?e?r?|(?:lett?e?r?|ep) *(?:of)? *jere?m?i?a?h?) chapters? \d[\d, \-]*\b(?! verse|verse) ?(?:rcu17[ts]s|[A-Za-z\-]*)?")

# Regex to find the bible version at the end of the string
bible_version_regex = re.compile(r" +(?:[A-Za-z\-]*|rcu17[ts]s)\Z")

# Regex to find the number portion of the bible verse
num_portion_regex = re.compile(r" *\d[\d, \-]*(?:$|\Z)")
