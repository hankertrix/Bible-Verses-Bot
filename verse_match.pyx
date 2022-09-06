# Module containing the VerseMatch class and the sups dictionary

import re
import cython
from bs4 import BeautifulSoup, element
from bible_books import biblecode, one_chapt_books
from bible_versions import versions_w_additions, apocrypha_supported_set

# The dictionary of normal characters to superscript characters
cdef dict sups = {
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

# Class of objects representing the verses matched in a message
cdef class VerseMatch:

    cdef str msg
    cdef list match
    cdef str book
    cdef str version
    cdef public str res
    cdef list final
    cdef public int valid
    cdef public str verses
    
    def __cinit__(self, str msg, list match, str book, str version) -> cython.void:
        self.msg = msg
        self.match = match
        self.book = book
        self.version = version
        self.res = ""
        self.final = []
        self.valid = 1
        self.verses = ""
    
    # Function to check whether the chapter requested is Esther 5:1-2 NRSVCE or Esther 5:1-2 NRSVACE
    cdef bint check_esth(self):
        
        # Checks whether the chapter requested is Esther 5:1-2 NRSVCE or Esther 5:1-2 NRSVACE
        if (self.version, self.book, self.match[0]) in {("NRSVACE", "Esth", 5), ("NRSVCE", "Esth", 5)}:

            # Checks if the verses requested is in Esther 5:1-2
            if self.match[1] in range(1,3) and self.match[2] in range(1,4):
                
                # Returns True
                return True
        
        # Return false otherwise
        return False

    # Function to check whether the chapter requested is Greek Esther 5:1-2 NRSVUE or Greek Esther 5:1-2 NRSVA
    cdef bint check_greek_esth(self):
        
        # Checks whether the chapter requested is Esther 5:1-2 NRSVCE or Esther 5:1-2 NRSVACE
        if (self.version, self.book, self.match[0]) in {("NRSVUE", "GkEsth", 5), ("NRSVA", "GkEsth", 5)}:

            # Checks if the verses requested is in Esther 5:1-2
            if self.match[1] in range(1,3) and self.match[2] in range(1,4):
                
                # Returns True
                return True
        
        # Return false otherwise
        return False

    # Function to check whether the chapter requested is Greek Esther 5:1-2 CEB
    cdef bint check_CEB_greek_esth(self):

        # Checks whether the chapter requested is Greek Esther 5:1-2 CEB
        if (self.version, self.book, self.match[0]) == ("CEB", "GkEsth", 5):

            # Checks if the verses requested is in Esther 5:1-2
            if self.match[1] in range(1,3) and self.match[2] in range(1,4):
                
                # Returns True
                return True
        
        # Return false otherwise
        return False

    # Function to edit the book to match with the version requested
    cdef str fix_book_and_version(self):
        
        # Checks if the bible version doesn't support apocrypha
        if self.version not in apocrypha_supported_set and self.book in biblecode[-21:]:

            # Changes the version to the default version that supports apocrypha, NRSVUE
            self.version = "NRSVUE"

        # Checks if the chapter requested is Psalm 151 and the version doesn't support Psalm 151
        if (self.book, self.match[0]) == ("Ps", 151) and self.version not in {"CEB", "NRSVUE", "NRSVA", "RSV"}:

            # Changes the version to the default version that supports Psalm 151
            self.version = "NRSVUE"

        # Checks if the version still does not support apocrypha or if the book is not part of the apocrypha
        if self.book not in biblecode[-21:] + ("Esth","Ps") or self.version not in apocrypha_supported_set:

            # Immediately returns the book
            return self.book

        # Checks if the book requested is in the apocrypha not supported by the catholic bible
        if self.book in biblecode[-15:] and self.version not in {"CEB","NRSVUE","NRSVA","RSV","WYC"}:

            # Change the version to the default version that supports all books of the apocrypha, NRSVUE
            self.version = "NRSVUE"
        
        # Checks if the book requested is unavailable in WYC
        elif self.version == "WYC" and self.book in {"3Macc","2Esd","4Macc"}:

            # Change the version to the default version that supports all books of the apocrypha, NRSVUE
            self.version = "NRSVUE"

        # Checks if the book requested is Greek Esther but the version is a catholic bible version
        if self.book == "GkEsth" and self.version in {"NCB","NRSVACE","NRSVCE","RSVCE"}:

            # Change the book to Esther
            self.book = "Esth"

        # Check whether the chapter requested is Esther 5:1-2 NRSVCE or Esther 5:1-2 NRSVACE (first function), or Greek Esther 5:1-2 NRSVUE or Greek Esther 5:1-2 NRSVA (second function), or Greek Esther 5:1-2 CEB (third function)
        if self.check_esth() or self.check_greek_esth() or self.check_CEB_greek_esth():

            # Changes the first verse to 1
            self.match[1] = 1

            # Changes the last verse to 2
            self.match[2] = 2

        # Checks if the bible book requested is Additions to Esther
        elif self.book == "AddEsth":

            # Changes the version to WYC
            self.version = "WYC"

            # Checks if the chapter requested is less than 7
            if self.match[0] < 7:

                # Increases the chapter by 9
                self.match[0] += 9
            
            # Checks if the bible verses requested is Additions to Esther 10:1-3
            elif self.match[0] == 10 and self.match[1] in range(1,4) and self.match[2] in range(2,5):

                # Changes the first verse to 4
                self.match[1] = 4

                # Changes the last verse to 5
                self.match[2] = 5

        # Checks if the bible book requested is the Song of the Three Young Men but the version is not RSV or WYC
        elif self.book == "SgThree" and self.version not in {"RSV","WYC"}:

            # Changes the bible book requested to The Prayer of Azariah (the same thing but different name)
            self.book = "PrAzar"
        
        # Checks if the bible book requested is the Prayer of Azariah but the version is RSV or WYC
        elif self.book == "PrAzar" and self.version in {"RSV","WYC"}:

            # Changes the bible book requested to the Song of the Three Young Men (same thing but different name)
            self.book = "SgThree"

        # Returns the book code for the search
        return self.book

    # Gets the specific page that corresponds to the bible chapter given
    cpdef str get_url(self):

        cdef str book_search
        cdef str book_url

        book_search = self.fix_book_and_version()
        book_url = str(f"{book_search}+{self.match[0]}%3A{self.match[1]}-{self.match[2]-1}")

        # If the chapter requested is Greek Esther 5 CEB
        if self.check_CEB_greek_esth():

            # Changes the url to search for the last verse of Greek Esther 4
            book_url = str(f"{book_search}+4%3A17")

        # Checks if the chapter requested is Psalms 151
        elif self.book == "Ps" and self.match[0] == 151:

            # Changes the book url to work with biblegateway
            book_url = str(f"{book_search}+{self.match[0]}+{self.match[1]}-{self.match[2]-1}")
        
        # Checks if the verse requested is Greek Esther 5:1-2 NRSVA
        elif (self.version, self.book, self.match) == ("NRSVA", "GkEsth", [5,1,2]):

            # Changes the book url to search for the last verse of Greek Esther 4
            book_url = str(f"{book_search}+4%3A17")

        # Checks if the verse requested is Esther 5:1-2 NRSVACE
        elif (self.version, self.book, self.match) == ("NRSVACE", "Esth", [5,1,2]):

            # Changes the book url to search for the last verse of Esther 4
            book_url = str(f"{book_search}+4%3A17")

        # Returns the url
        return str(f"https://www.biblegateway.com/passage/?search={book_url}&version={self.version}")
    
    # Gets the book title and chapter number from the webpage
    cdef str get_title(self):
        
        cdef str page
        cdef str book_part
        cdef int first_verse
        cdef int last_verse
        cdef str title

        page = self.res
        title_regex = re.compile(r'(?<=<meta property="og:title" content="Bible Gateway passage: )\d? ?.*?(?= \d| -)')

        try:
            book_part = title_regex.search(page).group()
        except:
            self.valid = 0
            book_part = ""
        
        first_verse = self.match[1]
        last_verse = self.match[2]
        
        # Checks if only 1 verse was given
        if first_verse == last_verse:
            title = str(f'{book_part} {self.match[0]}:{first_verse}')
        
        # For the case that multiple verses are given
        else:
            title = str(f'{book_part} {self.match[0]}:{first_verse}-{last_verse}')
        
        # Returns the book title
        return title

    # Function to make superscript characters back into normal characters
    cdef str to_norm(self, str sup_text):

        cdef dict unsups
        cdef str i

        # The reverse of the superscript dictionary with the keys and values swapped
        unsups = {}

        # Iterates the superscript dictionary to create a reverse dictionary
        for i in sups:

            # Sets the key of the unsups dictionary to the superscript and the value to the normal character
            unsups[sups[i]] = i
        
        # Returns the converted text with normal characters instead of superscript
        return "".join(unsups.get(char, char) for char in sup_text).strip().replace("`","")

    # Function to find the chapter number and return true if found and false otherwise
    cdef bint chapt_num_found(self):

        # Tries to find the chapter number
        try:
            
            # Regex to find the chapter number
            re.search("\d\d?\d?\xa0", " ".join(self.final).strip()).group()
            
            # If it succeeds, return true
            return True
        
        # If it fails
        except:

            # Return false
            return False

    # Function to get the relevant part of the verse to search for the highest and lowest verse number
    cdef str relevant_verses(self, str verses):

        cdef str relevant_verses
        
        # Initialise the variable relevant_verses
        relevant_verses = verses

        # Checks if the version is in the set of bible versions with additions and only carry out the below checks if it is
        if self.version in versions_w_additions:

            # Checks if the bible version is NRSVCE or NRSVACE and the book requested is Esther
            if self.version in {"NRSVCE", "NRSVACE"} and self.book == "Esth":

                # Checks if the chapter requested is Esther 1
                if self.match[0] == 1:
                
                    # Changes the relevant verses to the part after the end of addition A
                    relevant_verses = verses[verses.find("End of Addition A"):]
            
                # Checks if the chapter requested is Esther 4 NRSVACE
                elif self.match[0] == 4 and self.version == "NRSVACE":
                
                    # Changes the relevant verses to the part before addition C
                    relevant_verses = verses[:verses.find("Addition C")]
            
                # Checks if the chapter requested is Esther 5 NRSVCE
                elif self.match[0] == 5 and self.version == "NRSVCE":

                    # Changes the relevant verses to the part after the end of addition D
                    relevant_verses = verses[verses.find("End of Addition D"):]
            
                # Checks if the chapter requested is Esther 8
                elif self.match[0] == 8:
                
                    # Changes the relevant verses to the parts not in addition E
                    relevant_verses = verses[:verses.find("Addition E")] + "\n"

                    # Checks if the end of addition E can be found
                    if verses.find("End of Addition E") != -1:
                    
                        # Add the part behind addition E to the relevant verses
                        relevant_verses += verses[verses.find("End of Addition E"):]
            
                # Checks if the chapter requested is Esther 10
                elif self.match[0] == 10:

                    # Changes the relevant verses to the parts before addition F
                    relevant_verses = verses[:verses.find("Addition F")]

            # Checks if the version is RSVCE and the book requested is Esther
            elif self.version == "RSVCE" and self.book == "Esth":

                # Checks if the chapter requested is Esther 1
                if self.match[0] == 1:

                    # Changes the relevant verses to the parts after the title "King Ahasu-erus Deposes Queen Vashti"
                    relevant_verses = verses[verses.find("King Ahasu-erus Deposes Queen Vashti"):]
                
                # Checks if the chapter requested is Esther 4
                elif self.match[0] == 4:

                    # Changes the relevant verses to the parts before the title "Mordecai’s Prayer"
                    relevant_verses = verses[:verses.find("Mordecai’s Prayer")]
                
                # Checks if the chapter requested is Esther 5
                elif self.match[0] == 5:

                    # Changes the relevant verses to the parts not under the title "Esther Is Received by the King"
                    relevant_verses = verses[:verses.find("Esther Is Received by the King")] + "\n"

                    # Checks if the beginning of the next part can be found
                    if verses.find("sought to comfort her.") != -1:

                        # Adds the next part to the relevant verses
                        relevant_verses += verses[verses.find("sought to comfort her."):]
                
                # Checks if the chapter requested is Esther 8
                elif self.match[0] == 8:

                    # Changes the relevant verses to the parts not under the title "The Decree of Ahasu-erus"
                    relevant_verses = verses[:verses.find("The Decree of Ahasu-erus")] + "\n"

                    # Checks if the beginning of the next part can be found
                    if verses.find("to beasts and birds.”") != -1:

                        # Adds the next part to the relevant verses
                        relevant_verses += verses[verses.find("to beasts and birds.”"):]

            # Checks if the version is NRSVUE or NRSVA and the book requested is Greek Esther
            elif self.version in {"NRSVUE", "NRSVA"} and self.book == "GkEsth":
            
                # Checks if the chapter requested is Greek Esther 1
                if self.match[0] == 1:

                    # Changes the relevant verses to the part after the end of addition A
                    relevant_verses = verses[verses.find("End of Addition A"):]
            
                # Checks if the chapter requested is Greek Esther 4 NRSVA
                elif self.match[0] == 4 and self.version == "NRSVA":

                    # Changes the relevant verses to the part before addition C
                    relevant_verses = verses[:verses.find("Addition C")]
            
                # Checks if the chapter requested is Greek Esther 5 NRSVUE
                elif self.match[0] == 5 and self.version == "NRSVUE":

                    # Changes the relevant verses to the part after the end of addition D
                    relevant_verses = verses[verses.find("End of Addition D"):]
            
                # Checks if the chapter requested is Greek Esther 8
                elif self.match[0] == 8:
                
                    # Changes the relevant verses to the parts not in addition E
                    relevant_verses = verses[:verses.find("Addition E")] + "\n"

                    # Checks if the end of addition E can be found
                    if verses.find("End of Addition E") != -1:
                    
                        # Add the part behind addition E to the relevant verses
                        relevant_verses += verses[verses.find("End of Addition E"):]
            
                # Checks if the chapter requested is Greek Esther 10
                elif self.match[0] == 10:

                    # Changes the relevant verses to the parts before addition F
                    relevant_verses = verses[:verses.find("Addition F")]

            # Checks if the bible book requested is Greek Esther RSV
            elif self.version == "RSV" and self.book == "GkEsth":

                # Checks if the chapter requested is Greek Esther 4
                if self.match[0] == 4:

                    # Changes the relevant verses to the parts before the title "Mordecai’s Prayer"
                    relevant_verses = verses[:verses.find("Mordecai’s Prayer")]
                
                # Checks if the chapter requested is Greek Esther 5
                elif self.match[0] == 5:

                    # Changes the relevant verses to the parts not under the title "Esther Is Received by the King"
                    relevant_verses = verses[:verses.find("Esther Is Received by the King")] + "\n"

                    # Checks if the beginning of the next part can be found
                    if verses.find("sought to comfort her.") != -1:

                        # Adds the next part to the relevant verses
                        relevant_verses += verses[verses.find("sought to comfort her."):]
                  
                # Checks if the chapter requested is Greek Esther 8
                elif self.match[0] == 8:

                    # Changes the relevant verses to the parts not under the title "The Decree of Ahasu-erus"
                    relevant_verses = verses[:verses.find("The Decree of Ahasu-erus")] + "\n"

                    # Checks if the beginning of the next part can be found
                    if verses.find("to beasts and birds.”") != -1:

                        # Adds the next part to the relevant verses
                        relevant_verses += verses[verses.find("to beasts and birds.”"):]

            # Checks if the bible book requested is Greek Esther CEB
            elif self.version == "CEB" and self.book == "GkEsth":

                # Checks if the chapter requested is Greek Esther 1
                if self.match[0] == 1:

                    # Changes the relevant verses to the parts after the title "Queen Vashti"
                    relevant_verses = verses[verses.find("Queen Vashti"):]
                
                # Checks if the chapter requested is Greek Esther 3
                elif self.match[0] == 3:

                    # Changes the relevant verses to the parts before addition B
                    relevant_verses = verses[:verses.find("Addition B")]
                
                # Checks if the chapter requested is Greek Esther 4
                elif self.match[0] == 4:
                    
                    # Changes the relevant verses to the parts before addition C
                    relevant_verses = verses[:verses.find("Addition C")]

                # Checks if the chapter requested is Greek Esther 8
                elif self.match[0] == 8:

                      # Changes the relevant verses to the parts before addition E
                      relevant_verses = verses[:verses.find("Addition E")]
                
                # Checks if the chapter requested is Greek Esther 10
                elif self.match[0] == 10:

                    # Changes the relevant verses to the parts before addition F
                    relevant_verses = verses[:verses.find("Addition F")]

        # Returns the relevant verses
        return relevant_verses

    # Function to search the lowest verse
    cdef int get_lowest_verse(self, soup, str book_code, str verses):

        try:

            # Tries searching in the first verse for the first number in the range or the second verse number
            match_obj = re.search("`[⁰¹²³⁴⁵⁶⁷⁸⁹][⁰¹²³⁴⁵⁶⁷⁸⁹]?[⁰¹²³⁴⁵⁶⁷⁸⁹]?(?=⁻[⁰¹²³⁴⁵⁶⁷⁸⁹][⁰¹²³⁴⁵⁶⁷⁸⁹]?[⁰¹²³⁴⁵⁶⁷⁸⁹]?`\xa0)|`[⁰¹²³⁴⁵⁶⁷⁸⁹][⁰¹²³⁴⁵⁶⁷⁸⁹]?[⁰¹²³⁴⁵⁶⁷⁸⁹]?`\xa0", self.relevant_verses(verses))

            # Checks if the match has a chapter number before it
            if self.chapt_num_found():

                # Converts it to a normal integer and set the correct_verse_num to it
                correct_verse_num = int(self.to_norm(match_obj.group().strip()))
            
            # If it doesn't
            else:
              
                # Converts it to a normal integer and set the correct_verse_num to 1 more than the integer
                correct_verse_num = int(self.to_norm(match_obj.group())) + 1

        # If that fails
        except:

            try:

                # Tries to find the verse after the first verse given
                verse_after_objs = soup.find_all("span", {"class" : f"{book_code}-{self.match[1]+1}"})

                # Gets the number from the verse after
                correct_verse_num = int(re.search(r"\d\d?\d?\xa0", verse_after_objs[0].get_text()).group())
                
            # If that fails as well
            except:
                    
                # Sets the correct verse number to the first verse given by the user
                correct_verse_num = self.match[1] + 1
        
        # Returns the lowest verse number
        return correct_verse_num if correct_verse_num > 1 else 2

    # Function to makes the verse numbers, dashes and the small markers in EXB superscript
    cdef str to_sup(self, str text):
        
        # The converted text with superscripts
        sup_text = "".join(sups.get(char, char) for char in text)

        # Adds backticks and a zero-width non-breaking space to fix Telegram's ugly superscript characters
        return "`" + sup_text + "`\xa0"

    # Function to edit the chapter number
    def edit_chapter_num(self, match_obj: re.Match) -> str:

        # Gets the text from the match
        text = match_obj.group()

        # Checks if the character at the end of the text is a backtick (which means it has been changed to superscript)
        if text[-1] == "`" or self.version == "GNV":
            
            # Return only the backtick to remove the chapter number
            return text[-1]
        
        # If the character at the end is not a backtick
        else:

            # Changes the chapter number to superscript
            return self.to_sup(text.strip())

    # Function to format the html tables
    cdef void format_table(self, tag, int count):
        
        # Checks if the count variable is odd
        if count % 2 != 0:

            # Adds a semicolon and a space behind the text within the tag if there is no other symbols present
            # If there are other symbols present, just add the space only
            tag.string = tag.text.strip() + ": " if tag.text.strip()[-1] not in {":"} else tag.text.strip() + " "
        
        # If the count variable is even
        else:

            # Checks if the tag is a table header
            if tag.name == "th":

                # Adds a double line break behind the text within the tag
                tag.string = tag.text + "\n\n"
            
            # If it's not a table header
            else:

                # Adds a single line break behind the text within the tag
                tag.string = tag.text + "\n"

    # Function to correct the starting verse numbers in ERV
    cdef str ERV_change_verse_num(self, correct_verse_num):

        # Checks if the starting verse requested is within Hebrew 6:1-2 ERV or Ezekiel 5:1-2 ERV
        if (self.book, self.match[0]) in {("Heb", 6), ("Ezek", 5)} and self.match[1] in range(1,3):

            # Changes the correct verse number to 1
            self.match[1] = 1

            # Changes correct_verse_num to 1-2
            correct_verse_num = self.to_sup("1-2").replace("\xa0", "", 1)

        # Checks if the starting verse requested is within Ezekiel 1:1-3 ERV
        elif (self.book, self.match[0]) in {("Ezek", 1)} and self.match[1] in range(1,4):

            # Changes the correct verse number to 1
            self.match[1] = 1

            # Changes correct_verse_num to 1-3
            correct_verse_num = self.to_sup("1-3").replace("\xa0", "", 1)
          
        # Checks if the starting verse requested is within Ezekiel 48:1-7 ERV
        elif (self.book, self.match[0]) in {("Ezek", 48)} and self.match[1] in range(1,8):

            # Changes the correct verse number to 1
            self.match[1] = 1

            # Changes correct_verse_num to 1-7
            correct_verse_num = self.to_sup("1-7").replace("\xa0", "", 1)

        # Returns the correct_verse_num variable
        return correct_verse_num

    # Function to add in the correct verse number for bible versions like CJB that only give the bracketed verse number after the chapter number
    def add_verse_num(self, match_obj: re.Match) -> str:

        # Gets the text from the match object
        text = match_obj.group()

        # Adds the correct verse number in front of the bracketed verse number
        return self.to_sup(str(self.match[1])) + text

    # Function to fix the right to left hebrew characters
    def fix_hebrew(self, match_obj: re.Match) -> str:
        
        # Gets the text of the match
        text = match_obj.group()

        # Returns the right to left override unicode character with the text
        return str(f"\u200e{text}")

    # Function to check if the chapter requested has additions
    cdef bint have_additions(self):
        
        # The set of chapters in Esther with additions in NRSVACE
        esth_additions = [1,3,8,10,4]

        # The list of chapters in Greek Esther with additions in NRSVUE and NRSVA
        greek_esth_additions = [1,3,8,10]

        # Checks if the bible version requested is NRSVACE and the chapter requested is in the list of chapters in Esther with additions
        if [self.version, self.book] == ["NRSVACE", "Esth"] and self.match[0] in esth_additions:

            # Returns true
            return True

        # Checks if the bible version requested is NRSVCE and the chapter requested is in the list of chapters in Esther with additions, except for chapter 4
        elif [self.version, self.book] == ["NRSVCE", "Esth"] and self.match[0] in esth_additions[:-1] + [5]:

            # Returns true
            return True

        # Checks if the bible version requested is RSVCE and the chapter requested is Esther 1,3,4,5,8 or 10
        elif [self.version, self.book] == ["RSVCE", "Esth"] and self.match[0] in esth_additions + [5]:

            # Returns true
            return True

        # Checks if the bible version requested is NRSVUE and the chapter requested is in the list of chapters in Greek Esther with additions, adding chapter 5
        elif [self.version, self.book] == ["NRSVUE", "GkEsth"] and self.match[0] in greek_esth_additions + [5]:

            # Returns true
            return True
        
        # Checks if the bible version requested is NRSVA and the chapter requested is in the list of chapters in Greek Esther with additions, adding chapter 4
        elif [self.version, self.book] == ["NRSVA", "GkEsth"] and self.match[0] in greek_esth_additions + [4]:

            # Returns true
            return True
        
        # Checks if the bible version requested is RSV and the chapter requested is Greek Esther 3,4,5,8 and 10
        elif [self.version, self.book] == ["RSV", "GkEsth"] and self.match[0] in {3,4,5,8,10}:

            # Returns true
            return True

        # Checks if the bible version requested is CEB and the chapter requested is Greek Esther 1,3,4,8 or 10
        elif [self.version, self.book] == ["CEB", "GkEsth"] and self.match[0] in greek_esth_additions + [4]:

            # Returns true
            return True

        # Checks if the bible chapter requested is Greek Esther 5:1-2 CEB, NRSVUE or NRSVA or Esther 5:1-2 NRSVCE or NRSVACE
        elif self.check_CEB_greek_esth() or self.check_greek_esth() or self.check_esth():

            # Returns true
            return True

        # Returns false otherwise
        return False
    
    # Function to check if the entire chapter of Esther 5 NRSVCE or NRSVACE or Greek Esther 5 NRSVUE or NRSVA is requested
    cdef bint check_esth_5(self):

        # Checks if the version is NRSVCE or NRSVACE and if the chapter requested is Esther 5
        if self.version in {"NRSVACE"} and [self.book, self.match[0], self.match[2]] == ["Esth", 5, 177]:

            # Returns true
            return True
        
        # Checks if the version is NRSVUE or NRSVA or CEB and if the chapter requested is Esther 5
        elif self.version in {"CEB", "NRSVA"} and [self.book, self.match[0], self.match[2]] == ["GkEsth", 5, 177]:

            # Returns true
            return True
        
        # Returns false otherwise
        return False

    # Function to get the specific verses given
    cpdef void get_verses(self):
        
        cdef str WANTED
        cdef str UNWANTED
        cdef int count
        cdef int i
        cdef str verses
        cdef str book_code
        cdef int highest
        cdef str title
        cdef str title_verses

        # Replace the backticks in the response with a different backtick
        self.res = re.sub("`", "\u02cb", self.res)

        # Removes all spaces between tables
        self.res = re.sub("</tr> <tr>", "</tr><tr>", self.res)

        # Checks if the bible chapter requested is 1 Timothy 3 NCB
        if [self.version, self.book, self.match[0]] == ["NCB", "1Tim", 3]:

            # Adds the p tag to the front of the first verse
            self.res = re.sub('<b class="inline-h3">Qualifications of Bishops.</b>', '<p><b class="inline-h3">Qualifications of Bishops.</b>', self.res)

        # The beautiful soup parser for the document
        soup = BeautifulSoup(self.res, "lxml").select_one(".passage-text")

        # If the parser is nothing, invalidates the verse and stops the execution
        if soup is None:
            self.valid = 0
            return

        # The tags that are wanted
        WANTED = "bot-text"

        # The tags that are unwanted
        UNWANTED = ".passage-other-trans, .footnote, .footnotes, .crossreference, .crossrefs"

        # Gets rid of the tags that are unwanted
        for tag in soup.select(UNWANTED):
            tag.decompose()

        # Removes the ugly cross references in WEB
        # Checks if the bible version is WEB
        if self.version == "WEB":

            # Iterates all the crossref tags and removes them
            for tag in soup.select("crossref"):
                tag.string = f" ({tag.text.strip()})"
        
        # Selects all the titles, paragraphs, tables and lists and adds the WANTED class attribute to them
        for tag in soup.select("h1, h2, h3, h4, h5, h6, p, table, ul"):
            tag["class"] = WANTED

        # Makes all the br tags span tags containing a line break character
        for tag in soup.select("br"):
            tag.name = "span"
            tag.string = "\n"
        
        # Iterates the html lists
        for list_soup in soup.select("ul"):
            
            # Iterates all the sup tags inside and converts the text inside the tags to superscript
            for tag in list_soup.select("sup"):
                tag.string = self.to_sup(tag.text.strip())

        # For every item in the list
        for tag in soup.select("li"):
            
            # Adds a line break after every item in the list
            tag.string = tag.text + "\n"

        # Initialises the count variable
        count = 0

        # The list of html table tags
        table_objs = soup.select("th, td")

        # Iterates through all the th (table headers) and td tags
        for i in range(len(table_objs)):

            # Selects all the sup tags and changes everything inside to superscript
            for tag in table_objs[i].select("sup"):
                tag.string = self.to_sup(tag.text.strip())

            # Increases the count variable by one
            count += 1

            # Stops the iteration immediately if the object is the last one in the list
            if i == len(table_objs) - 1:
                break

            # Calls the format table function to format the table
            self.format_table(table_objs[i], count)

        # Selects all the sup tags and changes them to superscript characters
        for tag in soup.select("sup"):

            # Makes all the characters superscript and removes the non-breaking space automatically added by the to_sup function
            temp_text = self.to_sup(tag.text.strip()).replace("\xa0","")

            # Checks if the last character in the string is a space character
            if tag.text[-1] in {"\xa0","\u202f"}:

                # If it is, add on that last character
                tag.string = temp_text + tag.text[-1]
            
            # If it's not
            else:

                # Sets the tag string to the temporary text
                tag.string = temp_text

        # Checks if the bible chapter requested has additions
        if self.have_additions():
            
            # Iterates all the tags with the class chapternum
            for tag in soup.select(".chapternum"):

                # Checks if the tag is a number
                if tag.text.strip().isdigit() and self.version != "CEB":
                    
                    # Adds a superscript 1 to the back of the chapter number (for the chapter numbers without verse numbers at the back, those with verse numbers will be removed)
                    # Makes the chapter number bold as well
                    tag.string = f"<b>{tag.text.strip()}</b>\xa0" + self.to_sup("1")
                
                # If the tag is not a number like in CEB's Greek Esther
                else:

                    # Replace the text in the tag with a superscript 1
                    tag.string = self.to_sup("1")

        # Iterates the tags that have the special wanted class
        for tag in soup(class_=WANTED):

            # Appends the contents to the final list
            self.final.append(tag.text)
        
        # Joins all the paragraphs together with double line break
        verses = "\n\n".join(self.final).strip()

        # If the verses are Apocrypha verses that have additions
        if self.have_additions():
            
            # Remove the additional verse numbers
            verses = re.sub(r"`[¹²³⁴⁵⁶⁷⁸⁹⁰]`\xa0 *(?=`[¹²³⁴⁵⁶⁷⁸⁹][¹²³⁴⁵⁶⁷⁸⁹⁰]?[¹²³⁴⁵⁶⁷⁸⁹⁰]?`\xa0)", "", verses)
        

        ## Replaces the number on the first verse as 1 instead of the book number ##
        
        # Gets the attribute of the span tag that contains the verse
        # The format is 'class="text Luke-1-1"'
        book_code = str(f"text {self.book}-{self.match[0]}")
        html_soup = BeautifulSoup(self.res, "lxml")

        # Calls the get lowest verse function
        correct_verse_num = self.get_lowest_verse(html_soup, book_code,verses)

        # Grabs the verse number and subtracts 1 from it
        correct_verse_num = int(correct_verse_num) - 1
        
        # Checks if the book requested is one of the books with a single chapter
        if self.book in one_chapt_books:

            # Changes the chapter number to 1
            self.match[0] = 1

        # To add the verse number to the starting verse in bible books with a single chapter as they are not given
        # Checks if the version is EHV or HCSB
        if self.version in {"EHV","HCSB","MEV"}:

            # Checks if the bible book requested is a book with a single chapter and the first verse requested is 1
            if (self.book, self.match[0], self.match[1]) in {("Jude",1,1), ("2John",1,1), ("3John",1,1), ("Obad",1,1), ("Phlm",1,1)}:

                # Changes the correct verse number and the first verse to 1
                correct_verse_num = 1
            
                # Adds the verse number to the front of the first line in those verses
                verses = re.sub("Jude, a|The Elder|The elder|The vision of Obadiah.|Paul, a prisoner of Christ Jesus,", self.add_verse_num, verses)

        # Checks if the first bible verse requested is 1 Timothy 3:1 NCB
        elif [self.version, self.book, self.match[0], self.match[1]] == ["NCB", "1Tim", 3, 1]:

            # Changes the correct verse number to 1
            correct_verse_num = 1

            # Adds the verse number to the front of the first line in the verse
            verses = re.sub("This saying can be trusted:", self.add_verse_num, verses)
        
        # Checks if the first bible verse requested is Esther 5:1 or Esther 5:2 NRSVACE or NRSVCE or Greek Esther 5:1-2 NRSVUE or NRSVA
        elif self.check_esth() or self.check_greek_esth() or self.check_CEB_greek_esth():

            # Changes the correct verse number and the first verse to 1
            correct_verse_num = 1

        # Checks if the entire chapter of Greek Esther 5 or Esther 5 is called when the version is in the list of versions with additions
        elif self.check_esth_5():

            # Changes the correct verse number and the first verse to 3
            correct_verse_num = 3

        # Changes the first verse to the correct verse number found
        self.match[1] = correct_verse_num

        # To deal with the ERV version not giving the verse number of the starting few verses
        # Checks if the version is ERV
        if self.version == "ERV":
          
            # Calls the ERV_change_verse_num function to correct the verse number of the starting few verses
            correct_verse_num = self.ERV_change_verse_num(correct_verse_num)
        
        # Replace the verse number in the first verse given
        verses = re.sub("(?<!-)\d\d?\d?\xa0", f'{correct_verse_num}\xa0', verses, 1)

        ## ---------------------------------------------------------------------- ##


        # Gets rid of - at the back of the verses
        verses = verses.strip("—")

        # Removes other random characters with spaces
        verses = re.sub("[¶] ", "", verses)

        # Removes other random characters without spaces
        verses = re.sub("[*]","", verses)

        # Fixes all the hebrew characters being right to left
        verses = re.sub("[אבגדהוזחטיכלמנסעפצקרשתשׂשׁשׂשׁ]", self.fix_hebrew, verses)

        # Removes the book number for bible versions that have multiple verses like The Message version and also the Geneva bible and converts the chapter number to a verse number
        verses = re.sub(r"\d\d?\d?\xa0 *`?", self.edit_chapter_num, verses)
        
        # Adds the correct verse number in brackets for bible versions like CJB that don't give the correct verse number of the starting verse but instead give only the bracketed verse number like in 2 Chronicles 2:1 CJB
        # Only adds the verse number if the bracketed verse is not 0
        verses = re.sub(r"(?<![¹²³⁴⁵⁶⁷⁸⁹⁰]`\xa0)`⁽[¹²³⁴⁵⁶⁷⁸⁹][¹²³⁴⁵⁶⁷⁸⁹⁰]?[¹²³⁴⁵⁶⁷⁸⁹⁰]?⁾`\xa0", self.add_verse_num, verses)

        # Adds the correct verse number in front of the bracketed verse reference for bible versions like CJB when the correct verse number is not given like in Nehemiah 10:1 CJB
        verses = re.sub(r"(?<![¹²³⁴⁵⁶⁷⁸⁹⁰]`\xa0)`⁽[¹²³⁴⁵⁶⁷⁸⁹][¹²³⁴⁵⁶⁷⁸⁹⁰]?[¹²³⁴⁵⁶⁷⁸⁹⁰]?`\ufeff᠄ `[¹²³⁴⁵⁶⁷⁸⁹⁰]?[¹²³⁴⁵⁶⁷⁸⁹⁰]?[¹²³⁴⁵⁶⁷⁸⁹⁰]?⁾`\xa0", self.add_verse_num, verses)

        # Remove multiple spaces if it comes after a verse number
        verses = re.sub(r"`\xa0\xa0+|`\xa0 +","`\xa0", verses)

        # Remove line breaks if it comes after a verse number
        verses = re.sub(r"`\xa0\n+", "`\xa0", verses)

        # Changes all the hyphen-minus to a hyphen to stop accidental underlining of the verse message
        verses = re.sub(r"--", "\u2010\u2010", verses)

        # Checks if the chapter given is Matthew 1 WE
        if [self.version, self.book, self.match[0]] == ["WE", "Matt", 1]:

            # Adds the letter J before the verse 2-16
            verses = re.sub("esus' family line:", "Jesus' family line:", verses)
        
        # Checks whether the chapter requested is Greek Esther 5:1-2 CEB or Greek Esther 5:1-2 NRSVA
        if self.check_CEB_greek_esth() or (self.version, self.book, self.match) == ("NRSVA", "GkEsth", [5,1,2]):

            # Only takes the part of the verse after addition C
            verses = verses[verses.find("Addition C"):]

        # Checks whether the chapter requested is Esther 5:1-2 NRSVCE or Esther 5:1-2 NRSVACE or Greek Esther 5:1-2 NRSVA or NRSVUE or Greek Esther 4 NRSVA
        if self.check_esth() or self.check_greek_esth() or [self.version, self.book, self.match[0]] == ["NRSVA", "GkEsth", 4]:

            # Removes everything after "End of Addition D"
            verses = re.sub("End of Addition D.*", "End of Addition D", verses, flags=re.DOTALL)

        # Checks if the chapter given is Esther 5 NRSVACE
        if [self.version, self.book, self.match[0]] == ["NRSVACE", "Esth", 5]:

            # Removes the "End of Addition D"
            verses = re.sub("End of Addition D\n\n", "", verses)

        # Checks if the verse requested is Esther 5:1-2 NRSVACE
        if (self.version, self.book, self.match) == ("NRSVACE", "Esth", [5,1,2]):

            # Only takes the part of the verse after addition C and adds End of Addition D to the end
            verses = verses[verses.find("Addition C"):] + "\n\nEnd of Addition D"

        # Replace 3 or more line break characters with 2 line break characters
        verses = re.sub("\n\n\n+", "\n\n", verses)

        print(self.final)

        # Clears all the extra whitespace characters
        verses = verses.strip()

        # Clear the list
        self.final.clear()

        # To correct overshooting verses in books without the ending verse number
        highest = 176
        while self.to_sup(str(highest)).replace("`", "", 1) not in self.relevant_verses(verses):
            highest -= 1
            if highest == 0:
                highest = self.match[1]
                break
        
        # Checks if the bible verse requested is Esther 5:1 or 2 NRSVCE or NRSVACE or Greek Esther 5:1 or 2 NRSVUE or NRSVA
        if self.check_esth() or self.check_greek_esth() or self.check_CEB_greek_esth():
            
            # Sets the highest number to the first verse
            self.match[2] = self.match[1] + 1
        
        # If not
        else:

            # Sets the last verse to the highest verse number found
            self.match[2] = highest

        # Get the title using the get_title() function
        title = self.get_title()

        # Place the title in front of the verse
        title_verses = str(f'{title} {self.version} \n\n{verses}')

        # Override the previous list to set the final attribute to the text of a full verse match
        self.verses = title_verses
