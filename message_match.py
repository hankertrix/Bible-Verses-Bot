# Module containing the MessageMatch class

import re
from typing import List
import regexes
from bible_books import bible_dict, bible_chapt_dict
from bible_versions import bible_version_set, version_map

# Class of objects representing the initial matches found in the message
class MessageMatch:

    # Using slots so the bot runs faster and uses less memory
    __slots__ = ("msg", "matches", "matches_index", "dic")
    
    def __init__(self, msg: str) -> None:
        self.msg = msg
        self.matches = []
        self.matches_index = []
        self.dic = {}
    
    # Converts the string in the matches to integers
    def convert_to_int(self, match_list: List[str]) -> List[int]:
        return [int(i) for i in match_list]
    
    # The function to add a pipe character in front of the numbers in full chapters for easier splitting
    def add_pipe(self, match: re.Match) -> str:

        # Adds a pipe character to the front of the match and removes all the spaces
        return f"|{match.group()}".replace(" ", "")

    # Makes the match list have 3 items
    # For easier manipulation when the match is placed into a range
    def standardise(self, match_list: List[str]) -> List[int]:
        match_list = self.convert_to_int(match_list)
        if len(match_list) < 3:
            last_verse = match_list[1] + 1
            match_list.append(last_verse)
        
        else:
            last_verse = match_list[2] + 1
            match_list[2] = last_verse
        
        # Returns the match list
        return match_list

    # Finds the book number, like 1 John or 1 Timothy
    def find_book_num(self, book_index: int) -> str:
        bookindex = book_index-1

        # Checks if the book index is negative
        if bookindex < 0:
            
            # Sets the booknum to nothing
            return ""
        
        # If the book index is positive
        else:

            # Gets the book number
            booknum = self.msg[bookindex]

            # Checks if the character right before the book title is a newline character
            if self.msg[bookindex+1] == "\n":
                
                # Set the book number to nothing if the character before the book title is a newline character
                return ""
            
            # Checks if the book number is 1, 2 or 3 and sets the book number to the respective number
            elif booknum in "1234":
                return booknum
            
            # Checks if the "book number" is k
            elif booknum == "k":
                
                # Checks the k is part of the word greek or grk or gk
                if self.msg[bookindex-4:bookindex+1] == "greek" or self.msg[bookindex-2:bookindex+1] == "grk" or self.msg[bookindex-1] == "g":

                    # Returns the word "greek"
                    return "greek"
                
            # Checks if the "book number" is f
            elif booknum == "f":

                # Checks if f is part of the word of
                if self.msg[bookindex-1:bookindex+1] == "of":
                    
                    # Returns the word "of"
                    return "of"
                
            # Checks if the "book number" is o
            elif booknum == "o":
                
                # Checks if o is part of the word to
                if self.msg[bookindex-1:bookindex+1] == "to":

                    # Returns the word "to"
                    return "to"

            # Checks if the "book number" is p
            elif booknum == "p":

                # Checks if p is part of the word ep
                if self.msg[bookindex-1:bookindex+1] == "ep":

                    # Returns the word "ep"
                    return "ep"
                
            # Sets the book number to nothing otherwise
            else:
                return ""

    # Makes the book title the recognisable by the list of shortened bible book titles in bibleshort
    def shorten_book(self, book: str) -> str:

        # Removes the ( bracket
        book = book.replace("(","").strip()
        
        # For Philippians, Philemon, Prayer of Azariah, Letter of Jeremiah, Greek Esther and Prayer of Manasseh
        book_title = book[:5]
        
        # For Judges and all the books with numbers in front of them (e.g. 1 John, 2 Chronicles and 1 Esdras)
        if book_title not in bible_dict:
            book_title = book[:4]
            
            # For the rest of the books
            if book_title not in bible_dict:
                book_title = book[:3]
        
        # Returns the book title
        return book_title.strip()

    # Finds the title of the book
    def find_book_title(self, match_index: int) -> str:
        msg = self.msg
        index = match_index
        book_index = 0
        
        # Iterating backwards from the previously matched start index
        while index > 0:
            index -= 1

            try:

                # If the current index isn't one less than the match index, finds a space and returns the bookindex
                if index != match_index - 1 and msg[index].isspace():
                    break

                # Immediately invalidates if a symbol other than a bracket is found
                elif msg[index] in "!@#$%^&*_-+={}[],?<>":
                    break

            # To handle an index error (no idea how it happens but it happens)
            except:
                break

        # In the case of no spaces before the words
        book_index = index
        
        # Gets the book number
        book_num = self.find_book_num(book_index)

        # Assigns the book title to the book attribute
        book = self.shorten_book(msg[index:match_index])

        # Makes the full book title
        full_book_title = f"{book_num} {book}"

        # Returns the book title
        return full_book_title.strip()

    # Combines the standardisation, the insertion of the book title and adding to the list into object lists into one single function
    def add_to_lists(self, book_code: str, match_index: int, match_list: List[str], bible_version: str) -> None:

        # Converts all the numbers in the list to integers and standardises the list
        match_list = self.standardise(match_list)

        # Insert the book title into the match list
        match_list.insert(0, book_code)

        # Appends the version to the back of the list
        match_list.append(bible_version)

        # Checks if the match_index already exists in the list
        if match_index in self.matches_index or match_list in self.matches:

            # Stops the program from adding the duplicates to the list
            return
        
        # Appends the match index to the list of match indexes
        self.matches_index.append(match_index)

        # Appends the match list to the list of matches
        self.matches.append(match_list)

    # Function to search the match for the bible version
    def search_version(self, match: str) -> (str, str):

        # Use the version regex in the regexes file
        regex = regexes.bible_version_regex

        # Searches the string for the bible version
        match_obj = regex.search(match.strip())

        # Checks if the bible version is not given
        if not match_obj:
            
            # Returns a tuple of the match and an empty string
            return (match, "")

        # Otherwise, temove the version from the match
        match = regex.sub("", match).strip()

        # Gets the bible version
        bible_version = match_obj.group().strip().upper()

        # Gets the bible version from the version mapping
        bible_version = version_map.get(bible_version, bible_version)

        # Check if the version is in the set of accepted versions
        if bible_version in bible_version_set:

            # Returns a tuple of the match and the version
            return (match, bible_version)
        
        # If it's not
        else:

            # Returns a tuple of the match and an empty string
            return (match, "")
        
    # The function to convert the multiple bible verses with a semicolon into multiple lists
    def multi_num_convert(self, book_code: str, match_index: int, match: str) -> None:

        # Gets the match and bible version from the search_version function
        match, bible_version = self.search_version(match)

        # Split the match using commas to get a list of verses
        verses_list = match.split(",")

        # The default chapter number
        default_chapter = 0

        # The index to increase by 1 so that the verses will be sorted in the order that they are mentioned
        current_index = match_index

        # Iterates the list of matches
        for verse in verses_list:
          
            # Checks if the item in the list contains a semicolon
            if ":" in verse:

                # Splits the item in the list using the semicolon
                verse_list = verse.split(":")

                # Assigns the default chapter to the first number of the list
                default_chapter = int(verse_list[0])

                # Splits the message like a normal number bible verse to get the bible chapter, the starting and ending verse
                match_list = verse.replace(":","-").split("-")

                # Adds the match list and the match index to the object list
                self.add_to_lists(book_code, current_index, match_list, bible_version)
            
            # If there is no semicolon
            else:

                # Splits the message using a dash
                matches_list = verse.split("-")

                # Checks if the matches list just contains an empty character
                if len(matches_list[0]) == 0:

                    # Continues the iteration
                    continue

                # Adds the default chapter to the start of the list
                matches_list.insert(0, default_chapter)

                # Adds the match list and the match index to the object list
                self.add_to_lists(book_code, current_index, matches_list, bible_version)

            # Increases the match index by 1 so the verses are sorted correctly
            current_index += 1

    # The function to convert a single bible verse to a list
    def num_convert(self, book_code: str, match_index: int, match: str) -> None:
        
        # Gets the match and bible version from the search_version function
        match, bible_version = self.search_version(match)

        # Replaces the dashes with spaces in the match
        match_no_dash = match.replace("-"," ")

        # The list containing the bible chapter and the bible verse
        match_list = match_no_dash.replace(":"," ").split()

        # Adds the match list and the match index to the object list
        self.add_to_lists(book_code, match_index, match_list, bible_version)

    # The converter to decide if the number portion has multiple verses and passes the information to the respective convert functions
    def num_converter(self, match_index: int, match: str) -> None:

        # The book title
        book_title = self.find_book_title(match_index)

        # Checks if the book title is not in the dictionary and stops any further execution of the program
        if book_title not in bible_dict:
            return
        
        # The book code that is going to be passed to the other functions
        book_code = bible_dict[book_title]

        # If there are multiple bible verses
        if "," in match:
            self.multi_num_convert(book_code, match_index, match)
        
        # Single bible verse
        else:
            self.num_convert(book_code, match_index, match)
    
    # The function to convert multiple bible verses with the chapter ... verse ... format into multiple lists to pass to the VerseMatch class
    def multi_chapt_convert(self, book_code: str, match_index: int, match: str) -> None:
        
        # Gets the match and bible version from the search_version function
        match, bible_version = self.search_version(match)

        # Splits the match based on commas
        verse_list = match.split(",")

        # The front portion of the match
        front_part = verse_list[0].replace("-", " ").split()

        # The current match index
        current_index = match_index + 1

        # Iterates the front part list and removes the items that are not digits
        for part in front_part.copy():
            
            # Checks if the item is not a digit
            if not part.isdigit():

                # Removes the item from the list
                front_part.remove(part)

        # The chapter number of the bible book
        chapter_num = int(front_part[0])

        # Appends the front part to the object list
        self.add_to_lists(book_code, match_index, front_part, bible_version)

        # Iterates the list of verses behind the front part
        for verse in verse_list[1:]:

            # Splits the match based on a dash
            match_list = verse.split("-")

            # Adds the chapter number to the front of the list
            match_list.insert(0, chapter_num)

            # Appends the verse to the object list
            self.add_to_lists(book_code, current_index, match_list, bible_version)

            # Increases the current index by 1 so the verses are sorted correctly
            current_index += 1

    # The function to convert a single bible verse with the format chapter ... verse ... to a list to pass to the VerseMatch class
    def chapt_convert(self, book_code: str, match_index: int, match: str) -> None:

        # Gets the match and bible version from the search_version function
        match, bible_version = self.search_version(match)
        
        # The list containing the important information about the match
        match_list = match.replace("-"," ").split()

        # Iterates the match list and removes all the words
        for i in match_list.copy():
            
            # If the item is not a digit, remove it, leaving the list with only numbers
            if not i.isdigit():
                match_list.remove(i)
        
        # Adds the match list and the match index to the object list
        self.add_to_lists(book_code, match_index, match_list, bible_version)

    # The converter to decide if the chapter ... verse ... portion has multiple verses and passes the information to the respective convert functions
    def chapt_converter(self, match_index: int, match: str) -> None:

        # The book title
        book_title = self.find_book_title(match_index)

        # Checks if the book title is not in the dictionary and stops any further execution of the program
        if book_title not in bible_dict:
            return
        
        # The book code that is going to be passed to the other functions
        book_code = bible_dict[book_title]

        # If there are multiple bible verses
        if "," in match:
            self.multi_chapt_convert(book_code, match_index, match)
        
        # Single bible verse
        else:
            self.chapt_convert(book_code, match_index, match)
    
    # Function to iterate the chapter list and add it to the object list
    def append_chapters(self, match_index: int, book_code: str, chapter_list: List[str], bible_version: str) -> None:

        # The current index so that the matches will be in order
        current_index = match_index

        # Iterates the list of chapters
        for chapter in chapter_list:

            # Splits the chapter using dashes
            chapter_nums = chapter.split("-")

            # Check if the list has a length of one
            if len(chapter_nums) == 1:

                # Appends the chapter information to the object list
                self.add_to_lists(book_code, current_index, [chapter_nums[0], 1, 176], bible_version)
            
            # If the length is not one
            else:

                # Iterates the chapters
                for i in range(int(chapter_nums[0]), int(chapter_nums[1])+1):
                    
                    # Adds the chapter information to the object list
                    self.add_to_lists(book_code, current_index, [i, 1, 176], bible_version)

                    # Increases the current index by 1
                    current_index += 1
            
            # Increases the current index by 1 so the verses will be sorted correctly
            current_index += 1

    # Removes empty characters from the chapter list
    def remove_empty(self, chapter_list: List[str]) -> List[str]:
        
        # Returns the chapter list without any empty characters
        return [char for char in chapter_list if len(char) != 0 or not char.isspace()]

    # The converter to convert the chapter match with the word chapter in it to a list to pass to the VerseMatch class
    def full_chapt_converter(self, match_index: int, match: str) -> None:
        
        # Gets the match and bible version from the search_version function
        match, bible_version = self.search_version(match)

        # Places a pipe character (|) in front of the numbers for easy splitting
        piped_match = regexes.num_portion_regex.sub(self.add_pipe, match)

        # Splits the match at the pipe character
        match_list = piped_match.split("|")

        # The front portion of the match
        front_part = match_list[0]

        # Makes a list from the front part
        front_list = front_part.split()

        # Removes the word chapter from the list
        try:
            front_list.remove("chapter")
        
        # If it doesn't exist, remove the word chapters from the list
        except:
            front_list.remove("chapters")

        # The book of the bible mentioned
        book_title = " ".join(front_list).strip()

        # Checks if the book title is not inside the dictionary
        if book_title not in bible_chapt_dict:
            
            # Stops further execution if it's not
            return
        
        # The book code that is going to be used to search the bible verses
        book_code = bible_chapt_dict[book_title]

        # Splits the chapter number portion into a list using commas
        chapter_list = self.remove_empty(match_list[1].split(","))

        # Adds the chapters to the object list
        self.append_chapters(match_index, book_code, chapter_list, bible_version)
                
    
    # The converter to convert the chapter match without the word chapter in it to a list to be passed to the VerseMatch class
    def full_num_converter(self, match_index: int, match: str) -> None:
        
        # Gets the match and bible version from the search_version function
        match, bible_version = self.search_version(match)

        # Places a pipe character (|) in front of the numbers for easy splitting
        piped_match = regexes.num_portion_regex.sub(self.add_pipe, match)

        # Gets the book number
        book_num = self.find_book_num(match_index)

        # Splits the piped match using the pipe character
        match_list = piped_match.split("|")

        # Gets the book title from the book number and the front part of the match
        book_title = f"{book_num} {match_list[0]}".strip()

        # Checks if the book title is not in the list of accepted bible books
        if book_title not in bible_chapt_dict:

            # Stops any further execution
            return
        
        # Gets the book code to pass to the VerseMatch class
        book_code = bible_chapt_dict[book_title]

        # Splits the chapter number portion of the match using commas
        chapter_list = self.remove_empty(match_list[1].split(","))

        # Makes the current index variable so the matches can be sorted
        self.append_chapters(match_index, book_code, chapter_list, bible_version)
    
    # The reading phase of the previous version of the bot is now fully contained in this function
    # Converter function that decides what to do with the different types of matches and pass them to their respective converters
    def converter(self, match_index: int, match: str) -> None:
        
        # For bible verses that are in the format John 3:16
        if ":" in match:
            self.num_converter(match_index, match)
        
        # For bible verses that are in the format John Chapter 3 Verse 16
        elif "chapter" in match and "verse" in match:
            self.chapt_converter(match_index, match)
        
        # For bible chapters that are in the format John Chapter 3
        elif "chapter" in match:
            self.full_chapt_converter(match_index, match)
        
        # For bible chapters that are in the format John 3
        else:
            self.full_num_converter(match_index-1, match)

    # Finds the number portion of the bible verse and passes the match and the match index to the converter function
    def find_num(self) -> None:
        text = self.msg
        num_regex = regexes.number_regex
        self.matches.clear()
        self.matches_index.clear()
        for match in num_regex.finditer(text):
            self.converter(match.start(), match.group())
    
    # Finds the chapter ... verse ... portion of the bible verse and passes the match and the match index to the converter function
    def find_chapt(self) -> None:
        text = self.msg
        chapt_regex = regexes.chapter_regex
        for match in chapt_regex.finditer(text):
            self.converter(match.start(), match.group())

    # Finds the chapters mentioned without the word chapter and passes the match and the match index to the converter function
    def find_full_num(self) -> None:
        text = self.msg
        full_num_regex = regexes.full_chapter_num_regex
        for match in full_num_regex.finditer(text):
            self.converter(match.start(), match.group())
    
    # Finds the chapters mentioned with the word chapter and passes the match and the match index to the converter function
    def find_full_chapt(self) -> None:
        text = self.msg
        full_chapt_regex = regexes.full_chapter_chapt_regex
        for match in full_chapt_regex.finditer(text):
            self.converter(match.start(), match.group())

    # A function to call all the 4 find functions above
    def find_all(self) -> None:
        self.find_num()
        self.find_chapt()
        self.find_full_chapt()
        self.find_full_num()
        
    # Makes a dictionary of matches sorted by the match index
    def make_dic(self) -> None:

        # For measuring performance
        # start_time = time.perf_counter()

        self.find_all()
        self.dic = {}
        
        # Create a temporary dictionary to sort through
        temp_dic = dict(zip(self.matches_index, self.matches))
        
        # Sorting according to the match index
        for i in sorted(temp_dic):
            
            # Sets the key and value pair in the new dictionary to the one in the temporary dictionary
            self.dic[i] = temp_dic[i]
        
        # For measuring performance
        # logging.debug(f"MessageMatch time taken: {time.perf_counter() - start_time}")