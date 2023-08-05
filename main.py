# Telegram bible_verses_bot

# References:
# Pyrogram's documentation: https://docs.pyrogram.org/ 
# Pyrogram's pdf documentation: https://buildmedia.readthedocs.org/media/pdf/pyrogram/stable/pyrogram.pdf
# Conversations in pyrogram: https://nippycodes.com/coding/conversations-in-pyrogram-no-extra-package-needed/

import re, os, datetime, time, threading, logging, asyncio, traceback
import keep_alive, regexes
import httpx
from request_sess import s
from telebot import TeleBot, types
from telebot.apihelper import ApiTelegramException
from bs4 import BeautifulSoup
from firebase_wrapper import Database
from typing import List, Tuple, Optional, Callable, Dict
from bible_versions import bible_version_tuple, apocrypha_supported, bible_version_set, version_map
from message_match import MessageMatch
from verse_match import VerseMatch
from next_step_handler import NextStepHandler

# The set of errors to stop sending the message when encountered
ERRORS_TO_BREAK_ON = {
    "Bad Request: chat not found",
    "Bad Request: replied message not found",
    "Bad Request: group chat was upgraded to a supergroup chat",
    "Bad Request: TOPIC_CLOSED",
    "Forbidden: bot was kicked from the supergroup chat",
    "Forbidden: bot was kicked from the group chat",
    "Forbidden: bot was blocked by the user",
    "Forbidden: user is deactivated",
    "Forbidden: bot was kicked from the channel chat",
    "Forbidden: bot is not a member of the channel chat",
}

# Sets the timezone to Singapore's timezone
# The default timezone on Replit is UTC+0
os.environ["TZ"] = "Asia/Singapore"
time.tzset()

# Logging configuration
logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s', level=logging.DEBUG)
#logging.disable("CRITICAL")

# Disable the logging for httpcore
logging.getLogger("httpcore").setLevel(logging.CRITICAL)

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
                asyncio.run(send_verse_of_the_day())

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
                    asyncio.run(send_verse_of_the_day())
  
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


# The function to debounce the inline query
def debounce_inline_query(duration: float) -> Callable:

    # The decorator within to decorate the inline query handler with the debounce
    def decorator(inline_query_handler: Callable[[types.InlineQuery], None]) -> Callable[[types.InlineQuery], None]:

        # The dictionary of inline queries from different users
        inline_query_dict: Dict[str, threading.Timer] = {}

        # The actual debounce function that pauses the inline query handler until the wait duration has passed
        def actual_debounce(inline_query: types.InlineQuery) -> None:

            # Grabs the inline query dictionary from the decorator
            nonlocal inline_query_dict

            # Gets the user id from the inline query
            user_id: int = inline_query.from_user.id

            # The function to wrap the inline query handler so it can be called in a thread
            def call_handler(user_id: int) -> None:

                # Remove the inline query handler for the user from the dictionary
                inline_query_dict.pop(user_id, None)

                # Calls the inline query handler
                inline_query_handler(inline_query)

            # Tries to cancel the timer on the current calling inline query handler
            try:
                inline_query_dict[user_id].cancel()

            # If the current inline query is not found in the dictionary, skip cancelling the timer
            except KeyError:
                pass

            # Add the handler for this inline query to the dictionary
            inline_query_dict[user_id] = threading.Timer(duration, call_handler, [user_id])

            # Starts the timer
            inline_query_dict[user_id].start()


        # Returns the actual debounce function
        return actual_debounce

    # Returns the decorator
    return decorator

  
# The function to call when there is an inline query
@bot.inline_handler(lambda query: quick_check(query.query))
@debounce_inline_query(1)
def inline_handler(inline_query: types.InlineQuery) -> None:

    # Calls the answer function using a thread
    threading.Thread(target=inline_answer, args=(inline_query, )).start()


# Function to respond to the inline query
def inline_answer(inline_query: types.InlineQuery) -> None:

    # Get the verse using the search_verse function
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
The verse of the day would be sent at 12:00pm daily and it will be in the bible version that you have set for the chat. If the bible version you have set for your chat doesn't have the verse of the day, the bot will send the NIV version instead.

You can unsubscribe from the verse of the day using the /stopverseoftheday or the /svotd command.

For any bug reports, enquiries or feedback, please contact @hankertrix.

Hopefully you'll find this bot useful!'''
    
    send_message(message.chat.id, help_msg)


# A function to get the version from the database and returns NIV if there is no default version found
def get_version(message: types.Message) -> str:
    return db["chats_version"].get(str(message.chat.id), "NIV")


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

    # Gets the version dictionary from the database
    version_dict = db["chats_version"]
      
    # Checks if the bible version given is an accepted one
    if version_given in bible_version_set:

        # Gets the message ID as a string
        message_id = str(message.chat.id)
        
        # Removes the saved version if found
        if message_id in version_dict:
            del version_dict[message_id]

        # Checks if the version is not NIV
        if version_given != "NIV":

            # Saves the new version given to the database only when it's not NIV to save space
            version_dict[message_id] = version_given

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
    db["chats_version"] = version_dict

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

    # Gets the saved version
    saved_version = db["chats_version"].get(str(message.chat.id), "NIV")

    # Gets the verse message
    verse_msg = asyncio.run(get_verse_of_the_day(saved_version))

    # Gets the list of subscribers to the verse of the day message
    sub_list = db["subbed"]

    # Appends the user's chat id to the database
    sub_list.append(message.chat.id)

    # Sets the data in the database to the new list and remove all duplicate entries
    db["subbed"] = list(dict.fromkeys(sub_list))
    
    # Message to be sent to the user
    sub_msg = f"You are now subscribed to the verse of the day! \n\nYou will now receive the verse of the day at 12:00pm daily. \n\nToday's verse is: \n\n{verse_msg}"

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

# Function to get the verse of the day
async def get_verse_of_the_day(version = "NIV") -> Tuple[str]:

    # Initialise the verse message
    verse_msg = ""

    # While the verse message is nothing
    while verse_msg == "":

        # Using the httpx async client
        async with httpx.AsyncClient() as session:
    
            # Gets the verse of the day page from bible gateway
            verse_of_the_day_page = await session.get(f"https://www.biblegateway.com/reading-plans/verse-of-the-day/next?version={version}")
    
        # Adds line breaks before the headings in HTML
        text = re.sub("</h[1-6]>", add_line_break, verse_of_the_day_page.text)
    
        # Initialise the beautiful soup parser with lxml
        soup = BeautifulSoup(text, "lxml")
    
        # Delete the footnotes and the cross references from the HTML
        for unwanted_tag in soup.select(".passage-other-trans, .footnote, .footnotes, .crossreference, .crossrefs"):
            unwanted_tag.decompose()
    
        # Selects all of the verses
        verses_soup = soup.select(".rp-passage")
    
        # The list to store the verse message
        verse_msg_list = []
    
        # Iterate over all of the verses
        for verse_soup in verses_soup:
    
            # Gets the verse name from the HTML
            verse_name = verse_soup.find("div", class_="rp-passage-display").get_text().strip()
    
            # Gets the text of the verse from the HTML
            verse_text = verse_soup.find("div", class_="rp-passage-text").get_text()
          
            # Adds a left to right mark in front of the verse to force all text to be displayed left to right (stops the Hebrew symbols from appearing at the end of the line instead of the start of the line in Psalms 119)
            # Also removes all the spaces after a new line character
            verse_text = "\u200e" + re.sub("\n +", "\n", verse_text.strip())
    
            # Creates the verse and adds it to the list
            verse_msg_list.append(f"{verse_name} {version}\n{verse_text}")
    
        # The verse message containing the verse name and the verse of the day
        verse_msg = "\n\n".join(verse_msg_list).strip()

        # If the verse message is nothing, change the version to NIV
        if verse_msg == "":
            version = "NIV"

    # Returns the verse message
    return verse_msg


# Function to send the verse of the day
async def send_verse_of_the_day() -> None:

    # asyncio.sleep(15)

    # Gets the list of people who have subscribed to the verse of the day
    subbed_list = db["subbed"]

    # Gets the stored version for each chat
    chats_version = db["chats_version"]

    # An empty dictionary to add the version and their respective messages to
    # It will always contain NIV
    verse_of_the_day_msg_dict = {
      "NIV": ""
    }

    # Iterates over the list of chat IDs that have subscribed to the verse of the day
    for chat_id in subbed_list:

        # Gets the saved version for the chat ID
        saved_version = chats_version.get(str(chat_id))

        # Checks if the chat has saved a version
        if saved_version is not None:

            # Adds the version to the dictionary
            verse_of_the_day_msg_dict[saved_version] = ""

    # The list of tasks
    tasks = []

    # Iterates over all of the versions in the dictionary
    for version in verse_of_the_day_msg_dict:

        # Adds the task to get the verse of the day to the list of tasks
        tasks.append(get_verse_of_the_day(version))

    # Gathers all of the verses of the day
    verses_of_the_day = await asyncio.gather(*tasks)

    # Iterates over the versions in the dictionary
    for index, version in enumerate(verse_of_the_day_msg_dict.keys()):

        # Sets the version in the dictionary to the verse of the day message
        verse_of_the_day_msg_dict[version] = f"Today's verse is: \n\n{verses_of_the_day[index]}"

    # Iterates the list of chat ids that have subscribed to the verse of the day
    for chat_id in subbed_list:
      
        # Gets the saved version for the chat ID
        saved_version = chats_version.get(str(chat_id))

        # The verse message to send to the person
        verse_msg = verse_of_the_day_msg_dict.get(saved_version, verse_of_the_day_msg_dict["NIV"])

        # Sends the verse of the day message to all of the chats using a thread
        threading.Thread(target=send_message, args=(chat_id, verse_msg)).start()

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

            # Appends the task to get the webpage asynchronously to the tasks list
            tasks.append(session.get(url))

        # Infinite loop so the bot keeps trying
        while True:
            
            try:
                
                # The response objects
                reqs = await asyncio.gather(*tasks)
    
                # Breaks the loop if successful
                break;

            # Catch any error and logs them
            except Exception:
                traceback.print_exc()
    
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
    for [book, chapter, start_verse, end_verse, version] in dic.values():

        # Create a match object for every match in the dictionary
        # The match object grabs the data from the message match object
        match_obj = VerseMatch(msg=msg, book=book, match=[chapter, start_verse, end_verse], version=choose_version(default_version, version))

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
def quick_check(message: str) -> bool:

    # Makes the message lower case
    msg = message.lower()

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
@bot.channel_post_handler(func=lambda message: quick_check(message.text))
@bot.message_handler(func=lambda message: quick_check(message.text))
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
def split_message(message: types.Message, text: str, max_len: int = 4096, **kwargs) -> None:

    # List to append the parts of the long message
    splitted_list = []

    # Get the length of the text
    text_len = len(text)

    # Checks if the length of the message is within the Telegram Bot API limit
    if text_len <= max_len:

        # Sends the text directly without splitting if the message is within the limit
        splitted_list.append(text)
    
    # Splits the long message into different parts
    else:

        # The start index of the text part, which is zero at the start
        start_index = 0

        # The end index of the text part, which is the sum of the start index and the maximum length
        end_index = start_index + max_len

        # Starts a while loop without a condition
        while True:

            # Gets the part of the text that is within the Telegram Bot API limit
            text_part = text[start_index:end_index]

            # Get the index of the last newline character in the text part using the iterate_text() function
            index = iterate_text(start_index, text_part)

            # Appends the part of the message
            splitted_list.append(text[start_index:index])
            
            # Sets the start index to the index previously gotten from the iterate_text() function
            start_index = index

            # Sets the end index to the sum of the start index and the maximum length
            end_index = start_index + max_len

            # If the end index is greater or equal to the length of the text
            if end_index >= text_len:

                # Appends the final part of the text to send to the list of message parts
                splitted_list.append(text[start_index:])

                # Breaks the loop
                break

    # Iterates the list of the parts of the message
    for index, part in enumerate(splitted_list):
        
        # Makes the first message a reply to the user's message
        if index == 0:
            reply_to(message, part, **kwargs)
        
        # All other messages after the first is sent as a normal message
        else:
            send_message(message.chat.id, part, **kwargs)


# Iterates the parts of the long message backwards to find the newline character
def iterate_text(first_index: int, text: str) -> None:

    # Subtract 1 from the length of the text as indexing starts from 0
    index = len(text) - 1
    # logging.debug(index)

    # Iterates backwards through the string
    for i in range(index, -1, -1):

        # Checks if the message at the index is a newline character
        if text[i] == "\n":

            # Returns the index of the entire message (not the message part) and calls the check_backticks function so that the message wouldn't have superscripts that aren't formatted to monospace
            return first_index + check_backticks(i, text)


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

                # Returns the index of the 201st backtick
                return backtick.start()
    
    # Returns the index + 1 as I want to include the newline character at the end of the message part (Telegram will automatically trim the message when it's sent so it's alright)
    return index + 1


# Function to remove the specific message id from the database
def remove_from_db(message_id: int) -> None:

    # Filters to remove the message id from the verse of the day database
    db["subbed"] = [sub for sub in db["subbed"] if sub != message_id]

    # Change the message ID into a string
    message_id = str(message_id)

    # Gets the dictionary containing the bible version for each chat
    chats_version = db["chats_version"]

    # Removes the chat ID from the dictionary if it exists
    if message_id in chats_version:
        del chats_version[message_id]

    # Sets the dictionary in the database to the new one with the chat ID removed
    db["chats_version"] = chats_version


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
            
            # Checks if the error is a Telegram API exception
            if isinstance(e, ApiTelegramException):

                # Checks if the error is one of those in the set
                if e.description in ERRORS_TO_BREAK_ON:

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

            # If the error is one of those in the set
            if e.description in ERRORS_TO_BREAK_ON:
                
                # Remove the user from the database
                remove_from_db(message.chat.id)
    
                # Logs the user deleted
                logging.debug(message.chat.id)
                
                # Exits the function
                return

            # Otherwise, logs the error
            else:
                logging.error(e)


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
                s.get("https://bible-verses-bot-8u5d.onrender.com")

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

    msg = f'db["subbed"] = {db["subbed"]}\n\ndb["chats_version"] = {db["chats_version"]}\n\ndb["previous_sent_time"] = {repr(db["previous_sent_time"])}'
    split_message(message, msg)

# Name safeguard
if __name__ == "__main__":
    
    # Makes sure the bot runs continuously
    while True:
        
        try:

            # Starts the time checking thread to send the verse of the day message daily
            # Also starts the send update thread to make sure the bot remains up
            run_threads()

            # threading.Thread(target=lambda: asyncio.run(send_verse_of_the_day())).start()
            
            # Polls the telegram servers for a response
            bot.infinity_polling()

        # Handles a ConnectionResetError or a RequestTimedOutError
        except Exception:
            
            # Logs the error
            traceback.print_exc()




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
2John 5
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
1Chronicles chapter 3
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
2John 5
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
1Chronicles chapter 3
'''
