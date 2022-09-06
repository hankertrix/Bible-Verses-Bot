# Module to contain the regular expressions used in the main file

import re

# Regex for finding the "3:14" number portion of the bible verse
number_regex = re.compile(r'\d\d?\d?:\d\d?\d?,?[ \d,:-]*\b ?(?:rcu17ss|rcu17ts)?[A-Za-z-]*')

# Regex for finding a verse with chapter ... verse ...
chapter_regex = re.compile(r'\bchapter \d\d?\d? verses? \d\d?\d?-?\d?\d? ? ?t?o? ?\d?\d?\d?[ \d,-]*\b ?(?:rcu17ss|rcu17ts)?[A-Za-z-]*')

# Regex for finding the full chapter
full_chapter_num_regex = re.compile(r'\b(?!chapter|verse|to\b)[A-Za-z]+? \d\d?\d?[\d, -]*(?! :|:)\b ?(?:rcu17ss|rcu17ts)?[A-Za-z-]*|gr?e?e?k esthe?r? \d\d?\d?[\d, -]*(?! :|:)\b ?(?:rcu17ss|rcu17ts)?[A-Za-z-]*|addi?t?i?o?n?s? to esthe?r? \d\d?\d?[\d, -]*(?! :|:)\b ?(?:rcu17ss|rcu17ts)?[A-Za-z-]*|lett?e?r? of jere?m?i?a?h? \d\d?\d?[\d, -]*(?! :|:)\b ?(?:rcu17ss|rcu17ts)?[A-Za-z-]*')

# Regex for finding the full chapter with the word "chapter"
full_chapter_chapt_regex = re.compile(r'\b[1234]? ?[A-Za-z]* chapters? \d\d?\d?[\d, -]*\b(?! verse|verse) ?(?:rcu17ss|rcu17ts)?[A-Za-z-]*|gr?e?e?k esthe?r? chapters? \d\d?\d?[\d, -]*\b(?! verse|verse) ?(?:rcu17ss|rcu17ts)?[A-Za-z-]*|addi?t?i?o?n?s? to esthe?r? chapters? \d\d?\d?[\d, -]*\b(?! verse|verse) ?(?:rcu17ss|rcu17ts)?[A-Za-z-]*|lett?e?r? of jere?m?i?a?h? chapters? \d\d?\d?[\d, -]*\b(?! verse|verse) ?(?:rcu17ss|rcu17ts)?[A-Za-z-]*')

# Regex to find the bible version at the end of the string
bible_version_regex = re.compile(r' [A-Za-z-]*\Z| rcu17ss\Z| rcu17ts\Z')