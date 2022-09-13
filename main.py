# Telegram bible_verses_bot

# Bible Verses Bot V9 changes
# Moving the bot off of replit to another hosting platform so the bot can truly be up 24/7.
# Replit is becoming more and more unreliable for bot hosting which is why I changed the telegram bot library to use long polling instead of TCP sockets in the previous version in the first place.
# Wrote a database wrapper so I don't need to use the replit python package
# Moved the httpx client to a separate folder so it can be used in the database wrapper to make requests to the database
# All further changes after the previous are documented on the the Github page for the bot, which is https://github.com/hankertrix/Bible-Verses-Bot

# Bible Verses Bot V8 changes
# Changed the telegram bot library from pyrogram to pytelegrambotapi as the current bot will miss a ton of messages when it is offline thanks to it using a persistent TCP connection.

# Bible Verses Bot V7 changes
# Moved the lists and dictionaries of bible books into a separate file called bible_books.py
# Moved the lists of bible versions into a separate file called bible_versions.py
# Moved the VerseMatch class to a separate file called verse_match.pyx
# Wrote the VerseMatch class in Cython so that it is compiled in C and the bot can run faster (in certain instances, like running it on my home computer it's way faster, but for some reason the previous version runs much faster on the work computer than this version)
# Removed slots from the VerseMatch class and also added a new attribute verses that is used to store and then output the verses
# Added a thread to send updates to the monitoring bots so the bots can update me if the bot goes down
# Changed the normal httpx client to follow redirects
# Changed the comparisons to None to use "is" instead of the == equality operator
# Changed the multi_num_convert function to continue the loop if the matches list is just a list with one empty character
# Changed the remove_empty function to check the length of the string in the list and use str.isspace() to cover more types of spaces
# Changed a bunch of lists that weren't needed as lists to sets so the program can run faster, like versions_w_additions and one_chapt_books
# Created a bible_version_set that is the same as bible_version_list (now bible_version_tuple) for faster checking
# Also created an apocrypha_supported_set that is the same as apocrypha_supported for faster checking
# Removed all the list to set conversions as it only introduces overhead and doesn't speed up the code (probably slows it down instead)
# Changed the hardcoded lists (bible_version_list -> bible_version_tuple, biblecode, bibleshort, bible_chapt, bible_chapt_code, apocrypha_supported) to tuples to save memory and hopefully make the code run faster
# Added another check to the send_message function to check for the channel being deleted and then remove the channel from the database
# Added a check to the /verse command handler function verse_handler to be able to search verses immediately instead of prompting again when the verse is passed together with the command
# Changed how the thread works so the bot will keep trying to send the update if the server responds with a 404 and also the bot will not keep trying both requests only one errors out
# Moved the sending of the verse of the day portion of the DayCheck thread into a function so I can call it anytime
# Changed all references to NRSV to NRSVUE as biblegateway only supports NRSVUE, especially in the VerseMatch class and the function to handle the /help command
# Added a line in the reply to the /help command to say that searches using NRSV as the bible version will be automatically changed to NRSVUE
# Added a version map so older versions like NRSV that are no longer supported by biblegateway are mapped to the new, supported version, like NRSVUE
# Changed the set_version function to try getting the version from the version map first before updating the version
# Changed the search_version function of the MessageMatch class to get the bible version from the version mapping if it is inside the map
# Changed the sending of the verse of the day to be more robust
# Now it saves the previous time that the bot has sent the message and sends the message only when that previous time is a day before and the current time is after 12pm
# Removed the trusty sleep of 2 minutes after sending the verse of the day as that is not neccessary anymore
# This means that I no longer have to manually send the verse of the day message if the bot fails to do so because it's down
# Made the time to send the verse of the day a variable, which is a tuple representing the hour and minute for easier testing
# Made the program pause for 10 seconds in the event of the bot failing to send the message at the correct time so that errors don't occur
# Added a one second pause after the program is done sleeping so it doesn't miss the timing to send the verse of the day

# Bible Verses Bot V6 changes
# Used slots for the MessageMatch and VerseMatch class to speed up the bot and also use less memory
# Added type hinting for every function so the code is easier to maintain
# Forked the code and made it a new version because the previous one was using quite a bit more memory than this one
# Removed the remove_duplicates and the output_verse functions from the VerseMatch class
# Moved the functionality of the remove_duplicates and the output_verse function to search_verse
# This allows the bot to handle multiple searches concurrently instead of waiting for the previous one to finish
# Removed the class attribute instances in the VerseMatch class since there is no need for it any more
# Removed the get_match class method of the VerseMatch class since there is no need for it any more
# Removed the class attribute threads in the Find Verse and GetVerse classes
# Changed how search_verse works so that the function can take inline queries as well as normal messages
# Removed the functions search_verse_inline and get_verse_inline
# Used lxml as the BeautifulSoup parser for the find_verse_of_the_day function and for the html_soup object in the get_verses function of the VerseMatch class

# Bible Verses Bot V5 changes
# Placed all the regex for the searching of the bible verses in a separate file so I don't have to keep changing every one when I edit one
# Edited all the regex to include the bible version behind
# Added a function to pull out the bible version from the text
# Removed default values from the class initialisation arguments that are never passed and just set the property to the value
# Removed the unused message object being passed to the VerseMatch and MessageMatch class
# Moved the clearing of VerseMatch instances to the VerseMatch class output_verse method
# Added inline mode so it's much easier to send a bible verse to any chat
# Changed the /help and /start description to include inline mode and the support for bible versions at the back of the verses
# Changed the name of the help and start command handlers so that the function doesn't override python's native functions
# Updated the user agent in the request headers to use an updated version of chrome and edge
# Removed the unused match argument in MessageMatch's find_book_title function
# Edited an earlier comment that mentioned TgCrypto compiling the entire codebase in C
# TgCrypto just implements the encryption algorithm for Telegram in C, not the entire codebase
# Changed all the lists in the if statements to sets for faster computation

# Bible Verses Bot V4 changes
# Changed how the bot gets its html from the biblegateway.com
# Now it does so asynchronously via the httpx module which should increase the speed of the bot, especially when handling a large number of verses
# The url is now passed to a general function called get_webpages that returns the html response and the VerseMatch object method get_webpage is now called get_url which returns the url only
# The VerseMatch object main method load_up_verses no longer contains the get_url function (used to be get_webpage) and regular expressions fixing up the html have been passed to the next function being called, get_verses
# Changed relevant if statements to elif statements
# Changed the remove_duplicates function to use a faster and more concise way by using the dictionary fromkeys method rather than iterating the list obtained from the get match function
# Changed the sending of the verse of the day message to use threads so that all users will be able to get the message if the message fails to send to a user
# Changed the send_message function so that it'll automatically remove the user from the database if the user blocks the bot
# Used a list comprehension for the remove_empty function instead of the while loop, try and except and some checks

# Bible Verses Bot V3 changes
# The bot's verse searching function has rewritten so the bible verses just follow the format provided by Bible Gateway.

# Bible Verses Bot V2 changes
# This is just a rewrite of the old bot using a new library called pyrogram
# The MTProto API makes this bot much less susceptible to attacks as it uses Telegram's proprietary encrpytion protocol called MTProto instead of HTTPS
# It is now also much faster thanks to TgCrpyto using C instead of Python for Telegram's encryption protocol
# Update: I have decided to add new functionality, including support for multiple verses separated by commas and full chapters, chapter ranges, multiple chapters (again separated by commas) and searching different version of the bible.
# The reading portion of the VerseMatch class in the previous bot has been entirely moved to the MessageMatch class
# The VerseMatch class now only handles the searching of the bible verse while the MessageMatch class comprehends the verses in the message and sends it in a standard format that the VerseMatch class understands
# Tons of new functions have been added to deal with chapter ranges in bible versions like The Message

# References:
# Pyrogram's documentation: https://docs.pyrogram.org/ 
# Pyrogram's pdf documentation: https://buildmedia.readthedocs.org/media/pdf/pyrogram/stable/pyrogram.pdf
# Conversations in pyrogram: https://nippycodes.com/coding/conversations-in-pyrogram-no-extra-package-needed/

import re, os, datetime, time, threading, logging, keep_alive, asyncio, regexes
import httpx
from request_sess import s
from telebot import TeleBot, types
from telebot.apihelper import ApiTelegramException
from bs4 import BeautifulSoup
from firebase_wrapper import Database
from typing import List, Tuple, Optional
from bible_books import bible_dict, bible_chapt_dict
from bible_versions import bible_version_tuple, apocrypha_supported, bible_version_set, version_map
from verse_match import VerseMatch
from next_step_handler import NextStepHandler

# Sets the timezone to Singapore's timezone
# The default timezone on Replit is UTC+0
os.environ["TZ"] = "Asia/Singapore"
time.tzset()

# Logging configuration
logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s', level=logging.DEBUG)
#logging.disable("CRITICAL")

# Starts the server
keep_alive.keep_alive()

# Initialise the database
db = Database()

# Bot API key
API_KEY = os.environ["API_KEY"]

# Initialise the bot
bot = TeleBot(API_KEY)

# Initialise the next step handler
handler = NextStepHandler(max_step=1)

# The time to send out the verse of the day message in 24 hours
# It should be set to (12, 0) for 12:00pm
verse_of_the_day_time: Tuple[int] = (12, 0)

# Multi-threading so the bot can still run while giving the verse of the day daily
class TimeCheck(threading.Thread):

    # Have empty slots so the a dictionary isn't created for this class
    __slots__ = []
    
    # List of TimeCheck instances
    instances = []

    def __init__(self) -> None:
        threading.Thread.__init__(self)
        self.daemon = True
        TimeCheck.instances.append(self)
    
    # Function to start the thread for the user to receive the verse of the day
    def run(self) -> None:

        # Loop to ensure that the function runs continuously
        while True:

            # Gets the current time
            current_time = datetime.datetime.now()

            # For testing purposes
            #if current_time.minute == 0:

            # Checks if the time of the day is the time to send out the verse of the day and the previous sent time is a day ago
            if (current_time.hour, current_time.minute) == (verse_of_the_day_time[0], verse_of_the_day_time[1]) and current_time.day != datetime.datetime.fromisoformat(db["previous_sent_time"]).day:

                # Calls the function to send the verse of the day message
                send_verse_of_the_day()

                # Set the previous sent time to the current time
                db["previous_sent_time"] = datetime.datetime.now().isoformat()

            # Pauses the execution of the thread for the required amount of time until the next day's 12pm
            else:

                # Gets the current time
                current_time = datetime.datetime.now()

                # Checks if the previous sent time was one day ago and the current time is after 12pm
                if datetime.datetime.fromisoformat(db["previous_sent_time"]).day != current_time.day and current_time.hour >= verse_of_the_day_time[0]:

                    # Pauses the program for 10 seconds to avoid errors
                    time.sleep(10)

                    # Sends the verse of the day
                    send_verse_of_the_day()
  
                    # Set the previous sent time to the current time
                    db["previous_sent_time"] = datetime.datetime.now().isoformat()
                
                # The time now 
                now = datetime.datetime.now()
                
                # The time that the verse of the day is supposed to be sent
                next_time = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=verse_of_the_day_time[0], minute=verse_of_the_day_time[1])

                # For testing purposes
                #next_time = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=now.hour)

                logging.info(f"{next_time}")

                # Checks if the next_time is later than the current time
                if next_time > now:

                    # Pauses the execution until the current day's 12pm
                    trusty_sleep((next_time-now).seconds)

                    # Pauses the program for one second so that it doesn't miss the timing to send the verse of the day
                    time.sleep(1)
                
                # If next_time is before or equal to the current time
                else:

                    # Set the next time to be the next day's 12pm
                    next_time = next_time + datetime.timedelta(days=1)

                    # For testing purposes
                    #next_time = next_time + datetime.timedelta(hours=1)

                    logging.info(f"Edited next_time is {next_time}")

                    # Pauses the execution until the next day's 12pm
                    trusty_sleep((next_time-now).seconds)

                    # Pauses the program for one second so that it doesn't miss the timing to send the verse of the day
                    time.sleep(1)

# The function to call when there is an inline query
@bot.inline_handler(lambda query: True)
def inline_handler(inline_query: types.InlineQuery) -> None:

    # Calls the answer function using a thread
    threading.Thread(target=inline_answer, args=(inline_query, )).start()

# Function to respond to the inline query
def inline_answer(inline_query: types.InlineQuery) -> None:

    # Get the verse using the search_verse_inline function
    verse = search_verse(inline_query=inline_query, inline=True)

    # Checks if the verse is too long
    if len(verse) > 4096:

        # Answers the inline query with an error message
        bot.answer_inline_query(inline_query.id, cache_time=0, 
            results=[
                types.InlineQueryResultArticle(
                    "Message is too long, try searching for a shorter verse.",
                    "Message is too long, try searching for a shorter verse.",
                    types.InputTextMessageContent("Sorry, the requested verse was too long to be sent.")
                    )
                ]
            )

    # If the verse is not too long
    elif verse:

        # Gets the title of the verse
        verse_title = verse.split("\n")[0]

        # Answers the inline query
        bot.answer_inline_query(inline_query.id, cache_time=0, 
            results=[
                types.InlineQueryResultArticle(
                    verse_title,
                    verse_title,
                    types.InputTextMessageContent(verse, parse_mode="markdown")
                    )
                ]
            )

# Handles the /start command
@bot.channel_post_handler(commands=["start"])
@bot.message_handler(commands=["start"])
def start_handler(message: types.Message) -> None:
    
    start_msg = '''Hello! Add this bot to your Christian group chats and any bible verses shared to the group will be automatically detected by the bot and displayed as a reply to the message with the bible verse.
You can also subscribe to the verse of the day in your group chat or through the messaging the bot with the /verseoftheday command.
To unsubscribe from the verse of the day, use the /stopverseoftheday command.
Use inline mode by tagging the bot, @bible_verses_bot, and then typing your desired verse to send the entire verse to your chat.
To see more information about the bot, use the /help command.

Hopefully this bot will help you in your journey with God!'''
    
    send_message(message.chat.id, start_msg)

# Handles the /help command
@bot.channel_post_handler(commands=["help"])
@bot.message_handler(commands=["help"])
def help_handler(message: types.Message) -> None:

    help_msg = '''To use this bot, add the bot to a group and any bible verses shared to the group will be automatically detected and displayed as a separate message.

The default bible version used is the New International Version (NIV).

The default bible version used to search the Apocrypha is the New Revised Standard Version Updated Edition (NRSVUE).

All searches using the New Revised Standard Version (NRSV) as the bible version will be automatically changed to use the New Revised Standard Version Updated Edition (NRSVUE) as the bible version instead.
    
The bot will only detect bible verses written in these formats:
- 1 John 1:9 NIV
- Luke 9:1-10
- Deuteronomy 1:3,5-7,10,4:2-4,6,8-10 KJV
- Ezra 3:1, 3-7, 5:3, 6:3-7, 10
- Titus 1 NKJV
- Hebrews 3, 5-7, 10
- 2 Chronicles Chapter 2 Verse 6 NCV
- 3 John Chapter 1 Verses 1-13
- Genesis Chapter 1 Verse 9 to 11 NASB
- Job Chapter 1 Verse 1,4-8,11
- Daniel Chapter 5 Verses 4 to 6, 10-13, 17
- Nehemiah Chapter 10 ESV
- Hosea Chapters 3-4,8

You can use the bot's inline mode by tagging the bot, @bible_verses_bot, and then searching for the verse that you want to send to the chat.

You can also use the /verse command to find the verse you're looking for.

You can use the /version command to see the default bible version the bot is set to.

Use the /setversion command to change the default bible version.

You can also use the /listversions command to see the list of bible versions you can change to.
    
The bot can also send you the verse of the day by using the /verseoftheday or the /votd command.
The verse of the day would be sent at 12:00pm daily.

You can unsubscribe from the verse of the day using the /stopverseoftheday or the /svotd command.

For any bug reports, enquiries or feedback, please contact @hankertrix.

Hopefully you'll find this bot useful!'''
    
    send_message(message.chat.id, help_msg)

# Function to obtain the bible version of the chat from the chat id
def obtain_version(chat_id: int) -> str:
    
    # Initialises the saved version variable
    saved_version = ""

    # Tries to retrieve a string with the chat id and the saved bible version from the database
    for i in db["chats_version"]:

        # If the string exists
        if i.startswith(str(chat_id)):
            
            # Assign the variable saved version to it and breaks the loop
            saved_version = i
            break
    
    # Returns the string
    return saved_version

# A function to get the version from the database and returns NIV if there is no default version found
def get_version(message: types.Message) -> str:
    
    # Gets the saved version string using the obtain version function
    saved_version = obtain_version(message.chat.id)

    # Check if there isn't a saved version
    if saved_version == "":
        
        # If there isn't, set the bible version to NIV (default)
        version = "NIV"
    
    # If there is a saved version
    else:

        # Gets the saved bible version from the database
        version = saved_version.split()[1]
    
    # Returns the bible version
    return version

# Handles the /version command
@bot.channel_post_handler(commands=["version"])
@bot.message_handler(commands=["version"])
def display_version(message: types.Message) -> None:

    # Gets the version using the get_version function
    version = get_version(message)

    # The message to send to the chat
    version_message = f"The current bible version is {version}."

    # Sends the message
    send_message(message.chat.id, version_message)

# Handles the /setversion command
@bot.channel_post_handler(commands=["setversion"])
@bot.message_handler(commands=["setversion"])
def handle_version(message: types.Message) -> None:

    # The content of the message behind the /setversion command
    msg_ctx = re.sub("/setversion ?", "", message.text.lower())

    # Checks if there is nothing behind the /setversion command
    if msg_ctx == "":

        # Sends the message to the user
        send_message(message.chat.id, "Please enter your bible version.")

        # Register the next step handler
        handler.register_next_step_handler("setversion", message)

    # If there is text written behind the /setversion command
    else:

        # Calls the set_version function
        set_version(message, msg_ctx)

# The function to read the user's message and save the new bible version given if it's accepted
@bot.channel_post_handler(func=lambda message: handler.check_step("setversion", message, 1))
@bot.message_handler(func=lambda message: handler.check_step("setversion", message, 1))
def set_version(message: types.Message, ctx: str = "") -> None:

    # Checks if the context is not given
    if ctx == "":

        # Sets the version to the entire message given by the user
        version_given = message.text.upper().strip()

    # If the context is given
    else:

        # Sets the version to be the text behind the /setversion command
        version_given = ctx.upper().strip()

    # Gets the version from the version mapping
    version_given = version_map.get(version_given, version_given)

    # Gets the version list from the database
    version_list = db["chats_version"]
      
    # Checks if the bible version given is an accepted one
    if version_given in bible_version_set:
        
        # The list containing the chat id and the saved bible version
        saved_version = obtain_version(message.chat.id)

        # Removes the saved version if found
        version_list = [version for version in version_list if version != saved_version]

        # Checks if the version is not NIV
        if version_given != "NIV":

            # Saves the new version given to the database only when it's not NIV to save space
            version_list.append(f"{message.chat.id} {version_given}")

        # The message to notifiy the chat that the version has changed
        version_changed_msg = f"The current bible version has changed to {version_given}."

        # Sends the message
        send_message(message.chat.id, version_changed_msg)
 
    # If the bible version given is not in the list
    else:
        
        # The message to send to the chat
        invalid_msg = f"You have given me an invalid bible version. \n{get_version(message)} remains as the current bible version.\nUse the /setversion command to try again."
        
        # Sends the message
        reply_to(message, invalid_msg)

    # Finally, set the version list in the database to the updated one
    db["chats_version"] = list(dict.fromkeys(version_list))

    # Removes the next step handler
    handler.clear_step_handler("setversion", message)

# Handles the /listversions command
@bot.channel_post_handler(commands=["listversions", "listversion"])
@bot.message_handler(commands=["listversions", "listversion"])
def list_bible_versions(message: types.Message) -> None:

    # Gets the list of accepted English bible versions and joins them with a line break
    english_versions = "\n".join(bible_version_tuple[:-13])

    # Gets the list of accepted Chinese bible versions and joins them with a line break
    chinese_versions = "\n".join(bible_version_tuple[-13:])

    # Gets the list of bible versions that support apocrypha and joins them with a line break
    apocrypha_versions = "\n".join(apocrypha_supported)
    
    # The message to be sent to the chat
    list_version_msg = f"Accepted bible versions: \n\n\nEnglish versions: \n\n{english_versions} \n\n\nChinese versions: \n\n{chinese_versions} \n\n\nBible versions that support Apocrypha (English only): \n\n{apocrypha_versions}"

    # Sends the message
    send_message(message.chat.id, list_version_msg)

# Gets the specific message id from the database
def get_id(message_id: int) -> List[int]:
    return [chat_id for chat_id in db["subbed"] if chat_id == message_id]

# Handles the /verseoftheday command
@bot.channel_post_handler(commands=["verseoftheday","votd"])
@bot.message_handler(commands=["verseoftheday","votd"])
def verse_start(message: types.Message) -> None:

    # List containing the specific verse of the day and it's text
    verse_list = find_verse_of_the_day()

    # Gets the list of subscribers to the verse of the day message
    sub_list = db["subbed"]

    # Appends the user's chat id to the database
    sub_list.append(message.chat.id)

    # Sets the data in the database to the new list and remove all duplicate entries
    db["subbed"] = list(dict.fromkeys(sub_list))
    
    # Message to be sent to the user
    sub_msg = f"You are now subscribed to the verse of the day! \n\nYou will now receive the verse of the day at 12:00pm daily. \n\nToday's verse is: \n\n{verse_list[0]} NIV \n{verse_list[1]}"

    # Sends the message        
    send_message(message.chat.id, sub_msg)

# Handles the /stopverseoftheday command
@bot.channel_post_handler(commands=["stopverseoftheday","svotd"])
@bot.message_handler(commands=["stopverseoftheday","svotd"])
def verse_stop(message: types.Message) -> None:

    # Gets list of chat ids for the user (should be 0 or 1 in length)
    chat_id_list = get_id(message.chat.id)

    # Checks if the user has subscribed before
    if len(chat_id_list) != 0:

        # Gets their chat id from the database and removes it
        db["subbed"] = [sub for sub in db["subbed"] if sub != chat_id_list[0]]

        # Message to acknowledge that they have been unsubscribed
        stop_msg = "You will no longer receive the verse of the day daily. To re-enable, use the /verseoftheday or /votd command."
        send_message(message.chat.id, stop_msg)
    
    # Sends them a message to tell them to subscribe first
    else:
        not_subbed_msg = "You haven't subscribed to receive the verse of the day. Please subscribe first using the /verseoftheday or the /votd command."
        send_message(message.chat.id, not_subbed_msg)

# More reliable time.sleep() because I'm pausing the verse of the day thread execution for a long time
def trusty_sleep(sleeptime: int) -> None:
    start = time.time()
    while (time.time() - start < sleeptime):
        time.sleep(sleeptime - (time.time()-start))

# Function to add a line break before a title
def add_line_break(match_obj: re.Match) -> str:
  text = match_obj.group()
  return f"\n{text}"

# Function to find the verse of the day
def find_verse_of_the_day() -> List[str]:
    main_page = s.get("https://www.biblegateway.com/")
    text = re.sub("</h[1-6]>", add_line_break, main_page.text)
    soup_search = BeautifulSoup(text, "lxml")
    verse_name = soup_search.find("span", {"class" : "citation"}).get_text()
    verse_name = re.sub(r",\d\d?", "", verse_name)
    verse_of_the_day_raw = soup_search.find("div", {"id" : "verse-text"}).get_text()
    verse_of_the_day = "\u200e" + re.sub("\n +", "\n", verse_of_the_day_raw.strip())
    vlist = [verse_name, verse_of_the_day]
    return vlist

# Function to send the verse of the day
def send_verse_of_the_day() -> None:

    # time.sleep(15)

    # List containing the specific verse of the day and it's text
    daily_verse_list = find_verse_of_the_day()
    verse_msg = f"Today's verse is: \n\n{daily_verse_list[0]} NIV \n{daily_verse_list[1]}"

    # Iterates the list of chat ids that have subscribed to the verse of the day
    for chat_id in db["subbed"]:

        # Sends the verse of the day message to all of the chats using a thread
        threading.Thread(target=send_message, args=(chat_id, verse_msg)).start()

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
        for i in range(len(match_list)):
            match_list[i] = int(match_list[i])
        
        # Returns the match_list
        return match_list
    
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
                
                # If not
                else:

                    # Returns nothing
                    return ""

            # Checks if the "book number" is f
            elif booknum == "f":

                # Checks if f is part of the word of
                if self.msg[bookindex-1:bookindex+1] == "of":
                    
                    # Returns the word "of"
                    return "of"
                
                # If not
                else:

                    # Returns nothing
                    return ""
            
            # Checks if the "book number" is o
            elif booknum == "o":
                
                # Checks if o is part of the word to
                if self.msg[bookindex-1:bookindex+1] == "to":

                    # Returns the word "to"
                    return "to"

            # Sets the book number to nothing otherwise
            else:
                return ""

    # Makes the book title the recognisable by the list of shortened bible book titles in bibleshort
    def shorten_book(self, book: str) -> str:

        # Removes the ( bracket
        book = book.replace("(","")
        
        # For Philippians and Philemon
        book_title = book.strip()[:5]
        
        # For Judges
        if book_title not in bible_dict:
            book_title = book.strip()[:4]
            
            # For the rest of the books
            if book_title not in bible_dict:
                book_title = book.strip()[:3]
        
        # Returns the book name
        return book_title

    # Finds the title of the book
    def find_book_title(self, match_index: int) -> str:
        msg = self.msg
        index = match_index - 1
        bookindex = 0
        
        # Iterating backwards from the previously matched start index
        while index > 0:
            index -= 1

            try:

                # Finds a space and returns the bookindex
                if msg[index].isspace():
                    break

                # Immediately invalidates if a symbol other than a bracket is found
                if msg[index] in "!@#$%^&*_-+={}[],?<>":
                    break

            # To handle an index error (no idea how it happens but it happens)
            except:
                break

        # In the case of no spaces before the words
        bookindex = index
        
        # Gets the book number
        booknum = self.find_book_num(bookindex)

        # Assigns the book title to the book attribute
        book = self.shorten_book(msg[index:match_index-1])

        # Makes the full book title
        full_book_title = booknum + " " + book

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

        # Checks if the match exists:
        if match_obj:

            # Remove the version from the match
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
        
        # If it doesn't exist
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
    
    # The function to add a pipe character in front of the numbers in full chapters for easier splitting
    def add_pipe(self, match: re.Match) -> str:

        # Adds a pipe character to the front of the match
        return f"|{match.group()[1:]}"

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
        piped_match = re.sub(r" \d\d?\d?[\d, -]*", self.add_pipe, match)

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
        piped_match = re.sub(r" \d\d?\d?[\d, -]*", self.add_pipe, match)

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

# Function to get the webpage asynchronously
async def get_webpages(match_obj_list: List[VerseMatch]) -> List[str]:

    # Use the httpx async client to get the webpages
    async with httpx.AsyncClient() as session:

        # List of tasks
        tasks = []

        # Iterates the list of match objects
        for obj in match_obj_list:

            # Calls the match object's get url function
            url = obj.get_url()

            # Creates a task to get the webpage asynchronously
            task = asyncio.create_task(session.get(url))

            # Appends the task to the tasks list
            tasks.append(task)
        
        # The response objects
        reqs = await asyncio.gather(*tasks)
    
    # Returns the list of htmls returned by the httpx module
    return [req.text for req in reqs]

# Function to determine the version to be passed to the VerseMatch object
def choose_version(default_version: str, bible_version: str) -> str:

    # Returns the bible version if it's not empty, otherwise, return the default version
    return bible_version if bible_version != "" else default_version

# A function to search the bible verse and return the verse message so I don't have to write the same thing twice for the two threading classes to search the verse
def search_verse(message: Optional[types.Message] = "", inline_query: Optional[types.InlineQuery] = "", inline: Optional[bool] = False) -> str:

    # For measuring performance
    # start_time = time.perf_counter()

    # Checks if the function is called from the inline handler
    if inline:

        # Sets the default version to NIV
        default_version = "NIV"

        # Gets the inline query and makes it lowercase
        msg = inline_query.query.lower()

    # If the function is called from a message
    else:

        # Gets the default version from the chat
        default_version = get_version(message)

        # Rips the message content and makes the message lowercase
        msg = message.text.lower()

    # Create a message match object to store data
    msg_obj = MessageMatch(msg=msg)
    
    # Calls the message match object function to simplify and organise the data
    msg_obj.make_dic()
    dic = msg_obj.dic

    # List of match objects
    match_obj_list = []

    # Iterates through the dictionary created by the message match object
    for index in dic:
        
        # Create a match object for every match in the dictionary
        # The match object grabs the data from the message match object
        match_obj = VerseMatch(msg=msg, book=dic[index][0], match=[dic[index][1], dic[index][2], dic[index][3]], version=choose_version(default_version, dic[index][4]))

        # Appends the match object to a list
        match_obj_list.append(match_obj)

    # List of htmls returned by the get webpages function
    htmls = asyncio.run(get_webpages(match_obj_list))

    # For measuring performance
    verse_match_start_time = time.perf_counter()

    # Iterates the match object list
    for index, obj in enumerate(match_obj_list):

        # Assigns the match object's res property to the html response
        obj.res = htmls[index]

        # Calls the match object function to parse the message and return the bible verse
        obj.get_verses()
    
    # Gets the resulting string from the objects if the object is valid
    verse_msg = "\n\n\n\n\n".join(dict.fromkeys(obj.verses for obj in match_obj_list if obj.valid))

    # For measuring performance
    # with open("time.txt", "a") as f:
    #   f.write(f"{time.perf_counter() - verse_match_start_time}\n")
    logging.debug(f"VerseMatch time taken: {time.perf_counter() - verse_match_start_time}")
    # logging.debug(f"Total time taken: {time.perf_counter() - start_time}")

    # Returns the verse message
    return verse_msg

# A class to handle the get_verse() function
class GetVerse(threading.Thread):

    # Slots to save memory
    __slots__ = ["message"]
    
    def __init__(self, message: types.Message) -> None:
        threading.Thread.__init__(self)
        self.message = message
        self.daemon = False
    
    # Overriding the thread's run function
    def run(self) -> None:

        # Calls the search_verse function to get the verse message to be sent
        verse_msg = search_verse(message=self.message)
    
        # Checks if the verse message is empty
        if verse_msg != "":
        
            # Sends a reply if it's not empty
            split_message(self.message, verse_msg, parse_mode="markdown")
    
        # Asks the user to try again
        else:

            invalid_msg = '''You have given me an invalid bible verse. Check your spelling and try again by using the /verse command.'''
        
            reply_to(self.message, invalid_msg)

# Handles the command /verse
@bot.channel_post_handler(commands=["verse"])
@bot.message_handler(commands=["verse"])
def verse_handler(message: types.Message) -> None:

    # Removes the command from the message
    msg = message.text.lower().replace(r"/verse", "").strip()

    # Checks if the msg still has other words
    if msg:

        # Initialise a GetVerse thread
        thread = GetVerse(message)

        # Starts the thread
        thread.start()

    # If the message is empty
    else:
  
        # Sends the message to the user
        send_message(message.chat.id, "Please enter your bible verses.")

        # Registers the next step handler
        handler.register_next_step_handler("verse", message)
    
# Searches for the bible verse given previously through the command /verse
@bot.channel_post_handler(func=lambda message: handler.check_step("verse", message, 1))
@bot.message_handler(func=lambda message: handler.check_step("verse", message, 1))
def get_verse(message: types.Message) -> None:

    # Initialises a thread from the GetVerse class
    thread = GetVerse(message)
    
    # Starts the thread
    thread.start()

    # Removes the next step handler
    handler.clear_step_handler("verse", message)

# A function to quickly check if a message contains a bible verse
def quick_check(message: types.Message) -> bool:

    # Makes the message lower case
    msg = message.text.lower()

    # Runs through all the different checks
    if check_num_portion(msg):
        return True
    elif check_chapter_portion(msg):
        return True
    elif check_full_num_chapter(msg):
        return True
    elif check_full_chapt_chapter(msg):
        return True
    else:
        return False

# A class to handle the find_verse() function
class FindVerse(threading.Thread):

    # Slots to save memory
    __slots__ = ["message"]

    def __init__(self, message: types.Message) -> None:
        threading.Thread.__init__(self)
        self.message = message
        self.daemon = False
    
    # Overriding the thread's run function
    def run(self) -> None:

        # Calls the search verse function to get the verse message to be sent
        verse_msg = search_verse(message=self.message)
    
        # Checks if the verse message is empty
        if verse_msg != "":
        
            # Sends a reply if it's not empty
            split_message(self.message, verse_msg, parse_mode="markdown")
    
        # The bot does nothing if there are no valid bible verses


# The message handler function that runs only when quick_check() is true
# Main function of the bible verse search part of the bot
@bot.channel_post_handler(func=quick_check)
@bot.message_handler(func=quick_check)
def find_verse(message: types.Message) -> None:
            
    # If there aren't, initialises a thread from the FindVerse class
    thread = FindVerse(message)
    
    # Starts the thread
    thread.start()

# Checks the number portion of the bible verse
def check_num_portion(message: str) -> bool:
    number_regex = regexes.number_regex
    num_portion = number_regex.findall(message)
    if len(num_portion) > 0:
        return True
    else:
        return False

# Checks the chapter ... verse ... portion of the bible verse
def check_chapter_portion(message: str) -> bool:
    chapter_regex = regexes.chapter_regex
    chapter_portion = chapter_regex.findall(message)
    if len(chapter_portion) > 0:
        return True
    else:
        return False

# Checks if there is any chapters mentioned without the word chapter
def check_full_num_chapter(message: str) -> bool:
    full_chapter_num_regex = regexes.full_chapter_num_regex
    full_chapter_num = full_chapter_num_regex.findall(message)
    if len(full_chapter_num) > 0:
        return True
    else:
        return False

# Checks if there is any chapters mentioned with the word chapter
def check_full_chapt_chapter(message: str) -> bool:
    full_chapter_chapt_regex = regexes.full_chapter_chapt_regex
    full_chapter_chapt = full_chapter_chapt_regex.findall(message)
    if len(full_chapter_chapt) > 0:
        return True
    else:
        return False

# Split a long message into different messages
def split_message(message: types.Message, text: str, **kwargs) -> None:

    # List to append the parts of the long message
    splitted_list = []

    # Checks if the length of the message is within the Telegram Bot API limit
    if len(text) <= 4096:

        # Sends the text directly without splitting if the message is within the limit
        splitted_list.append(text)
    
    # Splits the long message into different parts
    else:

        # Takes the first 4096 characters of the message
        text_part = text[:4097]

        # First index of the text part, which is zero at the start
        first_index = 0

        # Starts a while loop without a condition
        while True:

            # Get the last index that has the newline character using the iterate_text() function
            index = iterate_text(first_index, text_part)

            # Appends the first part of the message
            splitted_list.append(text[first_index:index])
            
            # Sets text_part to the next part of the message that is within the Telegram Bot API limit
            text_part = text[index:index+4097]

            # Sets the first index to the index previously gotten from the iterate_text() function
            first_index = index

            # Checks if the text part is within the Telegram Bot API limit
            if len(text_part) <= 4096:
                
                # Adds the final part of the message to the list of the parts of the message and breaks the loop
                splitted_list.append(text_part)
                break
    
    # Iterates the list of the parts of the message
    for i in range(len(splitted_list)):
        
        # Makes the first message a reply to the user's message
        if i == 0:
            reply_to(message, splitted_list[i], **kwargs)
        
        # All other messages after the first is sent as a normal message
        else:
            send_message(message.chat.id, splitted_list[i], **kwargs)

# Iterates the parts of the long message backwards to find the newline character
def iterate_text(first_index: int, text: str) -> None:

    # Subtract 1 from the length of the text as indexing starts from 0
    index = len(text)-1
    logging.debug(index)
    
    # Starts a while loop for indexes greater than 0
    while index > 0:

        # Checks if the message at the index is a newline character
        if text[index] == "\n":

            # Returns the index of the long message (not the message part) and calls the check_backticks function so that the message wouldn't have superscripts that aren't formatted to monospace
            return first_index + check_backticks(index, text) + 1

        # Decrease the index by 1 if the newline character is not found
        index -= 1

        # Safeguard to prevent an infinite loop in case a newline character cannot be found
        if index == 0:
          break

# A function to check the number of backticks to make sure the message sent does not exceed 100 monospace formatted parts
def check_backticks(index: int, text: str) -> int:

    # Checks if the number of backticks is more than 200
    if len(re.findall("`", text)) > 200:

        # The number of backticks
        count = 0

        # Iterates the backticks found in the text
        for backtick in re.finditer("`", text):

            # Increase the count by 1 for every backtick found
            count += 1

            # Checks if the number of backticks is 201
            if count == 201:

                # Sets the index to the 1 before the 201st backtick
                index = backtick.start() - 2
    
    # Returns the index
    return index

# Function to remove the specific message id from the database
def remove_from_db(message_id: int) -> None:

    # Filters to remove the message id from the verse of the day database
    db["subbed"] = [sub for sub in db["subbed"] if sub != message_id]

    # Filters the version database to remove the message id from the list
    db["chats_version"] = [version for version in db["chats_version"] if not version.startswith(str(message_id))]

# The function to use in place of bot.send_message() to force the bot to send a message even if the connection is lost or an error occurs while sending the message
def send_message(message_id: int, bot_message: str, **kwargs) -> None:

    # While the message is not sent successfully
    while True:
        try:

            # Sends the message
            bot.send_message(message_id, bot_message, **kwargs)

            # Breaks the loop if the message is sent successfully
            break
        
        # Catch block
        except Exception as e:
            
            # Logs the error
            logging.error(e)
            
            # Checks if the error is a Telegram API exception
            if isinstance(e, ApiTelegramException):

                # Checks if the error is one of those in the set
                if e.description in {"Bad Request: chat not found", "Forbidden: bot was kicked from the supergroup chat"}:

                    # Remove the user from the database
                    remove_from_db(message_id)
    
                    # Logs the user deleted
                    logging.debug(message_id)
    
                    # Exit the function
                    return

                # If it's some other error
                else:

                    # Logs the exception description
                    logging.error(e.description)


# The function to use in place of bot.reply_to() to force the bot to send a reply even if the connection is lost or an error occurs while sending the reply
def reply_to(message: types.Message, bot_message: str, **kwargs) -> None:

    # While the message is not sent successfully
    while True:
        
        try:

            # Sends the message
            bot.reply_to(message, bot_message, **kwargs)
            
            # Breaks the loop if successful
            break
        
        # Logs the error if the message isn't sent successfully
        except Exception as e:
            logging.error(e)

            # If the error is that the replied message isn't found then exit the function
            if e.description in {"Bad Request: replied message not found"}:
                return

# Function to start the time checking thread
def check_time() -> None:

    # Checks if there are no time check instances currently
    if len(TimeCheck.instances) == 0:
        
        # Starts a time checker if there is no time check instance
        time_checker = TimeCheck()
        time_checker.start()
    
    # Does nothing if there is already a time check instance running

# Function to send a post request to the monitoring bots
def send_update() -> None:

    # The post data to send to the monitoring bots
    data = {
      "bot_name" : "Bible Verses Bot"
    }

    # An infinite loop to keep sending updates to the monitoring bots
    while True:

        # Iterates the two bots
        for number in {1, 2}:
      
            # Infinite loop to keep running
            while True:
        
                try:
        
                    # Sends the data to the monitoring bots
                    response = s.post(f"https://Monitoring-Bot-No-{number}.hankertrix.repl.co", data=data)
    
                    # Breaks the loop if the response status code is not within the 400 range
                    if response.status_code < 400 or response.status_code >= 500:
                        break
        
                # Catch the exception
                except Exception as e:
        
                    # Logs the error
                    logging.error(e)
        
        # Pauses the function for 5 minutes
        time.sleep(300)

# Function to keep the bot alive
def keep_bot_alive() -> None:

    # Infinite loop for the bot to keep running
    while True:

        # Continuously try until the request is successful
        while True:

            try:

                # Gets the bot url
                s.get("https://bible-verses-bot.onrender.com")

                # Breaks the loop if its successful
                break

            # Catch and log any exceptions
            except Exception as e:
                logging.error(e)

        # Pauses the function for 5 minutes before trying again
        time.sleep(300)

    
      
# Function to run all the threads
def run_threads() -> None:

    # Calls the check_day function
    check_time()

    # Calls the send update function in a thread
    threading.Thread(target=send_update, daemon=True).start()

    # Calls the function to keep the bot alive in a thread
    threading.Thread(target=keep_bot_alive, daemon=True).start()

# A test function for debugging and testing purposes
def test() -> None:
    time.sleep(10)

# For debugging purposes
@bot.message_handler(commands=["debug"])
def debug(message: types.Message) -> None:

    if message.chat.id != int(os.environ["DEV_ID"]):
        return

    msg = f'db["subbed"] = {db["subbed"]}\n\ndb["chats_version"] = {db["chats_version"]}\n\ndb["previous_sent_time"] = {repr(db["previous_sent_time"])}\n\n{TimeCheck.instances[0].__dict__}'
    send_message(message.chat.id, msg)

# Name safeguard
if __name__ == "__main__":
    
    # Makes sure the bot runs continuously
    while True:
        
        try:

            # Starts the time checking thread to send the verse of the day message daily
            # Also starts the send update thread to make sure the bot remains up
            run_threads()

            #threading.Thread(target=send_verse_of_the_day).start()
            
            # Polls the telegram servers for a response
            bot.infinity_polling()

        # Handles a ConnectionResetError or a RequestTimedOutError
        except Exception as e:
            
            # Logs the error after handling the lost message
            logging.error(e)




# Regex to find the number portion of the bible verse
# number_regex = re.compile(r'\d\d?\d?:\d\d?\d?-?\d?\d?\d?\b')

# Regex to find the chapter ... verse ... portion of the bible verse
# chapter_regex = re.compile(r"\bchapter \d\d?\d? verses? \d\d?\d?-?\d?\d? ? ?t?o? ?\d?\d?\d?\b")

# Does not work
# Regex to find the book title of the bible verse
# bible_regex = re.compile(f'[^\d\W][^\d\W][^\d\W]?[^\d\W]? ?[^\d\W]?[^\d\W]? ?[^\d\W]?[^\d\W]?[^\d\W]?[^\d\W]?[^\d\W]?.*?(?={aboveMatchResult})')

# Regex to find the title of the verse
# page_title_regex = re.compile("(?<=<meta property="og:title" content="Bible Gateway passage: ).*?(?= - New International Version"\/>)")

# Regex to find the number portion of the bible verse with multiple verses
# multi_num_regex = re.compile(r'\d\d?\d?:\d\d?\d?,?[ \d,:-]*\b')

# Regex to find the chapter... verse... portion of the bible verse with multiple verses
# multi_chapt_regex = re.compile(r'\bchapter \d\d?\d? verses? \d\d?\d?-?\d?\d? ? ?t?o? ?\d?\d?\d?[ \d,-]*\b')

# Regex to find the full chapter without the word chapter
# full_chapter_num_regex = re.compile(r'\b(?!chapter|verse|to\b)[A-Za-z]+? \d\d?\d?[\d, -]*(?! :|:)\b|gr?e?e?k esthe?r? \d\d?\d?[\d, -]*(?! :|:)\b|addi?t?i?o?n?s? to esthe?r? \d\d?\d?[\d, -]*(?! :|:)\b|lett?e?r? of jere?m?i?a?h? \d\d?\d?[\d, -]*(?! :|:)\b')

# Regex to find the full chapter with the word chapter
# full_chapter_chapt_regex = re.compile(r'\b[1234]? ?[A-Za-z]* chapters? \d\d?\d?[\d, -]*\b(?! verse|verse)|gr?e?e?k esthe?r? chapters? \d\d?\d?[\d, -]*\b(?! verse|verse)|addi?t?i?o?n?s? to esthe?r? chapters? \d\d?\d?[\d, -]*\b(?! verse|verse)|lett?e?r? of jere?m?i?a?h? chapters? \d\d?\d?[\d, -]*\b(?! verse|verse)')

# Regex for finding the "3:14" number portion of the bible verse with the bible version behind
#number_regex = re.compile(r'\d\d?\d?:\d\d?\d?,?[ \d,:-]*\b ?[\w-]*')

# Regex for finding a verse with chapter ... verse ... with the bible version behind
#chapter_regex = re.compile(r'\bchapter \d\d?\d? verses? \d\d?\d?-?\d?\d? ? ?t?o? ?\d?\d?\d?[ \d,-]*\b ?[\w-]*')

# Regex for finding the full chapter with the bible version behind
#full_chapter_num_regex = re.compile(r'\b(?!chapter|verse|to\b)[A-Za-z]+? \d\d?\d?[\d, -]*(?! :|:)\b ?[\w-]*|gr?e?e?k esthe?r? \d\d?\d?[\d, -]*(?! :|:)\b ?[\w-]*|addi?t?i?o?n?s? to esthe?r? \d\d?\d?[\d, -]*(?! :|:)\b ?[\w-]*|lett?e?r? of jere?m?i?a?h? \d\d?\d?[\d, -]*(?! :|:)\b ?[\w-]*')

# Regex for finding the full chapter with the word "chapter" with the bible version behind
#full_chapter_chapt_regex = re.compile(r'\b[1234]? ?[A-Za-z]* chapters? \d\d?\d?[\d, -]*\b(?! verse|verse) ?[\w-]*|gr?e?e?k esthe?r? chapters? \d\d?\d?[\d, -]*\b(?! verse|verse) ?[\w-]*|addi?t?i?o?n?s? to esthe?r? chapters? \d\d?\d?[\d, -]*\b(?! verse|verse) ?[\w-]*|lett?e?r? of jere?m?i?a?h? chapters? \d\d?\d?[\d, -]*\b(?! verse|verse) ?[\w-]*')

# Regex to find the bible version at the end of the string
#bible_version_regex = re.compile(r' [\w-]*\Z')


# Text to test regex

'''
1 Thessalonians 300:200-311
Luke 3:16
1 Timothy 3:1-9
John 1:1,5,10,15,13:5
Genesis 3:2,6,9,11,17, 1:3
Jonah 1, 3, 5, 7
Psalm 119-122
Titus 5,6-10,14
Ezekiel 5
Song of songs 4, 9
3:00pm
4:00 pm

Luke chapter 1 verse 9
Matthew chapter 100 verse 200-300
Philemon chapter 100 verses 200 to 300
Jonah chapter 200 verse 300 to 500
Mark chapter 1 verse 122
Numbers chapter 1 verse 1,5,7,9,16,20
Exodus chapter 3 verses 2 to 3, 5, 8, 10, 11, 16
Deuteronomy chapter 377
Obadiah chapters 1,4,6
James chapter 5-10, 15, 16
Song of songs chapter 5-9
'''

# Test message
'''
- 1 John 1:9
- Luke 9:1-10
- Deuteronomy 1:3,5-7,10,4:2-4,6,8-10
- Ezra 3:1, 3-7, 5:3, 6:3-7, 10
- Titus 1
- Hebrews 3, 5-7, 10
- 2 Chronicles Chapter 2 Verse 6
- 3 John Chapter 1 Verses 1-13
- Genesis Chapter 1 Verse 9 to 11
- Job Chapter 1 Verse 1,4-8,11
- Daniel Chapter 5 Verses 4 to 6, 10-13, 17
- Nehemiah Chapter 10
- Hosea Chapter 3-4,8

1 Thessalonians 300:200-311
Luke 3:16
1 Timothy 3:1-9
John 1:1,5,10,15,13:5
Genesis 3:2,6,9,11,17, 1:3
Jonah 1, 3, 5, 7
Psalm 119-122
Titus 5,6-10,14
Ezekiel 5
Song of songs 4, 9
3:00pm
4:00 pm

Luke chapter 1 verse 9
Matthew chapter 100 verse 200-300
Philemon chapter 100 verses 200 to 300
Jonah chapter 200 verse 300 to 500
Mark chapter 1 verse 122
Numbers chapter 1 verse 1,5,7,9,16,20
Exodus chapter 3 verses 2 to 3, 5, 8, 10, 11, 16
Deuteronomy chapter 377
Obadiah chapters 1,4,6
James chapter 5-10, 15, 16
Song of songs chapter 5-9
'''
