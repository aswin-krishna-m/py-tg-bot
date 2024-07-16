import math,os,asyncio
from dotenv import load_dotenv
from mysql.connector import connect,Error
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
from django.contrib.staticfiles.storage import staticfiles_storage

# Loading Environment variables
load_dotenv()

API_KEY = os.getenv('API_KEY')
DEVELOPER_CHAT_ID = int(os.getenv('DEVELOPER_CHAT_ID'))
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')

# MySQL variables &  MySQL Database connection management
db_cred = {'host': os.getenv('host'),'user': os.getenv('user'),'password': os.getenv('password'),'database': os.getenv('database'),'port': os.getenv('port')}
def db_connection():
    try: 
        db = connect(**db_cred)
        conn = db.cursor()
        return db,conn
    except Error as e:
        print("MySQL connection Failed!! Reason: ", e)

# MySQL Tables

languages = "language"
movie = "movie_detail"
series = "series_detail"
shows = "shows"
users = "auth_users"
extras = "series_extras"
subtitles = "subtitles"

# Bot files path
GIF_PATH = staticfiles_storage.path("startup.gif")
REQUEST_IMG_PATH = staticfiles_storage.path("avengers.jpg")


message_action_delay= 1

# Bot /start command description reply

startDesc = ("Welcome to my world🌏\n"
             "*Tips to improve search result*\n"
            "1. Title should be precise(Use google search)\n"
            "2. Title names can be same but show may be different choose accordingly!\n"
            "Have a good search 😉\n")

# Bot /help command description reply
helpDesc = ("Hi, I'm a python3 modular bot.🤖" 
            "The prime purpose of my existence is to serve you with different movies and tv shows on demand.\n"
            "\nLet me introduce you to the commands.\n"
            "1. /start - Start the bot to use it\n"
            "2. /help - Opens help menu\n"
            "3. /about - Know about the bot\n"
            f"*\nNOTE\nForward the files to Saved Messages to avoid copyright infringement❗️*\n")

# Bot /about command description reply
aboutDesc = ("<b>TG FILE HANDLER 🤖</b>\n"
            f"○ <b>👨‍💻 Creator</b> : <a href='tg://user?id={str(DEVELOPER_CHAT_ID)}'>This person</a>\n"
            "○ <b> 🔊 Language</b> : <a href='https://docs.python.org/3/'>Python3</a>\n"
            "○ <b> 📚Library</b> : <a href='https://github.com/python-telegram-bot/python-telegram-bot'>Python-Telegram-Bot v20.3</a>\n"
            "○ <b>🖥 Source Code</b> : NOT AVAILABLE TO USERS\n"
            "○ <b>📢 Channel</b> : Under development\n"
            "○ <b>👥Support Group</b> : Under development\n")

# Bot /admin command description reply
adminDesc = ("*FORMATS TO SEND FILE TO BOT*\n\n"
            "○ *POSTER* \n Image file with caption in the format:\n"
            "*{Title $ Year $ 0/1(Movie/Series) }*\n\n"
            "○ *MOVIE FILES* \nSend the file captioned with *{Show_ID,Language_ID}*\n\n"
            "○ *SERIES EPISODES* \nSend the file captioned with format\n"
            "*{Show_id,Language_ID,Season,Episode,Resolution(720 for 720p)}*\n\n"
            "○ *SERIES EXTRA EPISODES* \nSend the .SRT file captioned with format\n"
            "*{Show_id,Language_ID,Season,Resolution(720 for 720p),Title of Extra Episode}*\n\n"
            "○ *SUBTITLES (MOVIES)* \nSend the file captioned with*{Show_ID,Language_ID of Subtitle}*\n\n"
            "○ *SUBTITLE(SERIES EPISODES)* \nSend the .SRT file captioned with format\n"
            "*{Show_id,Language_ID of Subtitle,Season,Episode}*\n\n"
            "*ADMIN COMMANDS*\n"
            "1. /admin\n"
            "2. /broadcast showid \n"
            "3. /remfiles showid \n"
            "4. /addlang language \n"
            "\nFor more choose the options below 👇\n")

# Bot auth replies
AdminUsageOnly = "*ACCESS DENIED*\nOnly *ADMIN* can perform this action"

BanDesc = ("*You are BANNED🚫 from using the bot\n*")

UnbanDesc = ("*You have been UNBANNED🔓 Happy to have you back\n*")

UnapprovedDesc = ("*❌ACCESS DENIED❌*\n"
                  "*\nYou're not an authorized user❗️\n*"
                  "*Click the button below👇 to request access\n*")

ApprovalDesc = ("*⌛️Please wait until admin approves your request⌛️*\n")

ApprovedDesc = (f"*Hello, your request has been approved ✅. You can now start browsing the bot🎉🥳*\n")

# Authorization
def auth_user(chat_id):
    if chat_id == DEVELOPER_CHAT_ID:
        return "admin"
    db,conn = db_connection()
    conn.execute(f"SELECT user_id,approved,ban FROM {users} WHERE user_id = %s", (chat_id,))
    row = conn.fetchone()
    if row:
        id,approved,ban  = [int(i) for i in row]
        if chat_id==id and approved and not ban:
            return "approved"
        elif not approved and not ban:
            return "unapproved"
        elif ban:
            return "banned"
    else:
        return "request"
    db.close()

# Convert file sizes to different sizes
def convert_size(size_bytes: int) -> str:
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

# Inline Keyboards
                
# User keyboards
def request_keyboard(chat_id):
    keyboard = [[InlineKeyboardButton("➕ Send Access Request ➕", callback_data=f"request:{chat_id}")]]
    return InlineKeyboardMarkup(keyboard)

def languages_keyboard(series_or_not,show_id):
    db, conn = db_connection()
    keyboard,new_row,lang_list = [],[],[]
    if series_or_not:
        conn.execute(f"SELECT DISTINCT series_lang FROM {series} WHERE series_id = %s order by series_lang asc", (show_id,))
    else :
        conn.execute(f"SELECT DISTINCT movie_lang FROM {movie} WHERE movie_id = %s order by movie_lang asc", (show_id,))
    language_result = conn.fetchall()
    if language_result:
        keyboard.append([InlineKeyboardButton(f"Choose Language",callback_data="empty")])
    for i,row in enumerate(language_result):
        lang_id = row[0]
        conn.execute(f"SELECT language FROM {languages} WHERE lang_id = %s", (lang_id,))
        language_name = conn.fetchone()[0]
        lang_list.append(language_name)
        new_row.append(InlineKeyboardButton(f"{language_name}", callback_data=f"{series_or_not},{show_id},{lang_id}"))
        if (i + 1) % 2 == 0:
            keyboard.append(new_row)
            new_row = []
    if new_row:
        keyboard.append(new_row)
    conn.execute(f"SELECT pk FROM {subtitles} WHERE show_id = %s ", (show_id,))
    if conn.fetchone() and not series_or_not:
        keyboard.append([InlineKeyboardButton("Open Subtitles", callback_data=f"sublist:{show_id}")])
    db.close()
    return lang_list,InlineKeyboardMarkup(keyboard)

def resolution_keyboard(series_or_not,show_id,lang_id):
    db,conn = db_connection()
    keyboard,new_row,resolution_list  = [],[],[]
    conn.execute(f"SELECT DISTINCT resolution FROM {series} WHERE series_id = %s AND series_lang=%s order by resolution asc", (show_id,lang_id,))
    for resolution in conn.fetchall():
        resolution_list.append(resolution[0])
    keyboard.append([InlineKeyboardButton(f"Choose Resolution",callback_data="empty")])
    for i,resolution in enumerate(resolution_list):
        new_row.append(InlineKeyboardButton(f"{resolution}p", callback_data=f"0,{show_id},{lang_id},{resolution}"))
        if (i + 1) % 3 == 0:
            keyboard.append(new_row)
            new_row = []
    if new_row:
        keyboard.append(new_row)
    keyboard.append([InlineKeyboardButton("⬅️ Back to Languages", callback_data=f"b:1,{show_id}")])
    db.close()
    return InlineKeyboardMarkup(keyboard)
    
def filesize_keyboard(page, show_id, lang_id):
    db,conn = db_connection()
    keyboard,new_row,size_list,pagination_buttons,end_kb  = [],[],[],[],[]
    conn.execute(f"SELECT pk, size FROM {movie} WHERE movie_id = %s AND movie_lang=%s order by size asc", (show_id,lang_id,))     
    for pk,size in conn.fetchall():
        size_list.append([pk,size])
    keyboard.append([InlineKeyboardButton(f"Choose File Size",callback_data="empty")])
    ITEMS_PER_PAGE = 6
    total_pages = math.ceil(len(size_list)/ITEMS_PER_PAGE)
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    for i,pk_size in enumerate(size_list[start:end]):
        new_row.append(InlineKeyboardButton(f"{pk_size[1]}", callback_data=f"0,{show_id},{lang_id},{pk_size[0]}"))
        if (i + 1) % 2 == 0:
          keyboard.append(new_row)
          new_row = []
    if new_row:
        keyboard.append(new_row)
        
    if start > 0:
        pagination_buttons.append(InlineKeyboardButton('⏪ Previous', callback_data=f'{page-1},{show_id},{lang_id}'))
    pagination_buttons.append(InlineKeyboardButton(f'📄 {page+1} /{total_pages}',callback_data="empty"))
    if end < len(size_list):
        pagination_buttons.append(InlineKeyboardButton('Next ⏩', callback_data=f'{page+1},{show_id},{lang_id}'))
    if len(pagination_buttons)>1:
        keyboard.append(pagination_buttons)  
    keyboard.append([InlineKeyboardButton("⬅️ Back to Languages", callback_data=f"b:0,{show_id}")])
    db.close()
    return InlineKeyboardMarkup(keyboard)
    
def season_keyboard(page,show_id,lang_id,pk_or_resolution):
    db,conn = db_connection()
    keyboard,new_row,pagination_buttons,season_list  = [],[],[],[]
    conn.execute(f"SELECT DISTINCT season FROM {series} WHERE series_id = %s AND series_lang=%s AND resolution=%s order by season asc", (show_id,lang_id,pk_or_resolution))
    for row in conn.fetchall():
        season_list.append(row)
    keyboard.append([InlineKeyboardButton(f"Choose Season",callback_data="empty")])
        
    ITEMS_PER_PAGE = 12
    total_pages = math.ceil(len(season_list)/ITEMS_PER_PAGE)
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    
    for i,season in enumerate(season_list[start:end]):
        new_row.append(InlineKeyboardButton(f"S{season[0]}", callback_data=f"0,{show_id},{lang_id},{pk_or_resolution},{season[0]}"))
        if (i + 1) % 4 == 0:
            keyboard.append(new_row)
            new_row = []
    if new_row:
        keyboard.append(new_row)
        
    if start > 0:
        pagination_buttons.append(InlineKeyboardButton('⏪ Previous', callback_data=f'{page-1},{show_id},{lang_id},{pk_or_resolution}'))
    pagination_buttons.append(InlineKeyboardButton(f'📄 {page+1} /{total_pages}',callback_data="empty"))
    if end < len(season_list):
        pagination_buttons.append(InlineKeyboardButton('Next ⏩', callback_data=f'{page+1},{show_id},{lang_id},{pk_or_resolution}'))
    if len(pagination_buttons)>1:
        keyboard.append(pagination_buttons)    

    keyboard.append([InlineKeyboardButton("⬅️ Back to Resolution", callback_data=f"b:1,{show_id},{lang_id}")])
    db.close()
    return InlineKeyboardMarkup(keyboard)
    
def episode_keyboard(page,show_id,lang_id,resolution,season):
    db,conn = db_connection()
    keyboard,new_row,pagination_buttons,episode_list,extra_kb  = [],[],[],[],[]
    conn.execute(f"SELECT pk,episode FROM {series} WHERE series_id = %s AND series_lang=%s AND resolution=%s AND season = %s order by episode asc", (show_id,lang_id,resolution,season))
    for pk,episode in conn.fetchall():
        episode_list.append([pk,episode])
        
    ITEMS_PER_PAGE = 15
    total_pages = math.ceil(len(episode_list)/ITEMS_PER_PAGE)
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    
    keyboard.append([InlineKeyboardButton(f"Choose Episode",callback_data="empty")])
    for i,episode in enumerate(episode_list[start:end]):
        new_row.append(InlineKeyboardButton(f"E{episode[1]}", callback_data=f"{page},{show_id},{lang_id},{resolution},{season},{episode[0]}"))
        if (i + 1) % 5 == 0:
          keyboard.append(new_row)
          new_row = []
    if new_row:
        keyboard.append(new_row)
        
    if start > 0:
        pagination_buttons.append(InlineKeyboardButton('⏪ Previous', callback_data=f'{page-1},{show_id},{lang_id},{resolution},{season}'))
    pagination_buttons.append(InlineKeyboardButton(f'📄 {page+1} /{total_pages}',callback_data="empty"))
    if end < len(episode_list):
        pagination_buttons.append(InlineKeyboardButton('Next ⏩', callback_data=f'{page+1},{show_id},{lang_id},{resolution},{season}'))
    
    if len(pagination_buttons)>1:
        keyboard.append(pagination_buttons)
    extra_kb.append(InlineKeyboardButton("⬅️ Back to Seasons", callback_data=f"b:0,{show_id},{lang_id},{resolution}"))
    conn.execute(f"SELECT * FROM {extras} where series_id = %s AND series_lang=%s AND resolution=%s AND season = %s ",(show_id,lang_id,resolution,season))
    if conn.fetchone():
        extra_kb.append(InlineKeyboardButton("Extras ✨", callback_data=f"extra_keyboard:0,{show_id},{lang_id},{resolution},{season}"))
    keyboard.append(extra_kb)
    db.close()
    return InlineKeyboardMarkup(keyboard)

def subs_keyboard(series_or_not,show_id,season=0,episode=0):
    db,conn = db_connection()
    keyboard,new_row  = [],[]
    if series_or_not:
        conn.execute(f"SELECT s.pk,l.language FROM {subtitles} s INNER JOIN {languages} l ON s.lang_id = l.lang_id where show_id = %s AND season = %s AND episode=%s order by l.lang_id asc", (show_id ,season ,episode,))
    else:
        conn.execute(f"SELECT s.pk,l.language FROM {subtitles} s INNER JOIN {languages} l ON s.lang_id = l.lang_id where show_id = %s order by l.lang_id asc", (show_id,))
    keyboard.append([InlineKeyboardButton(f"Choose Subtitle Language",callback_data="empty")])
    for i,sub_id_lang in enumerate(conn.fetchall()):
        new_row.append(InlineKeyboardButton(f"{sub_id_lang[1]}", callback_data=f"sub:{sub_id_lang[0]}"))
        if (i + 1) % 2 == 0:
          keyboard.append(new_row)
          new_row = []
    if new_row:
        keyboard.append(new_row)
    db.close()
    if not series_or_not:
        keyboard.append([InlineKeyboardButton("⬅️ Back to Languages", callback_data=f"b:0,{show_id}")])
    return InlineKeyboardMarkup(keyboard)

def extras_keyboard(page,show_id,language,resolution,season):
    db,conn = db_connection()
    keyboard,new_row,pagination_buttons,extra_list  = [],[],[],[]
    conn.execute(f"SELECT pk,title FROM {extras} WHERE series_id = %s AND series_lang=%s AND resolution=%s AND season = %s order by title asc", (show_id,language,resolution,season))
    for row in conn.fetchall():
        extra_list.append(row)
    ITEMS_PER_PAGE = 10
    total_pages = math.ceil(len(extra_list)/ITEMS_PER_PAGE)
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    
    keyboard.append([InlineKeyboardButton(f"Choose Season Extras",callback_data="empty")])
    for i,extra in enumerate(extra_list[start:end]):
        new_row.append(InlineKeyboardButton(f"{extra[1]}", callback_data=f"extra_send:{extra[0]}"))
        if (i + 1) % 2 == 0:
          keyboard.append(new_row)
          new_row = []
    if new_row:
        keyboard.append(new_row)
        
    if start > 0:
        pagination_buttons.append(InlineKeyboardButton('⏪ Previous', callback_data=f'extra_keyboard:{page-1},{show_id},{language},{resolution},{season}'))
    pagination_buttons.append(InlineKeyboardButton(f'📄 {page+1} /{total_pages}',callback_data="empty"))
    if end < len(extra_list):
        pagination_buttons.append(InlineKeyboardButton('Next ⏩', callback_data=f'extra_keyboard:{page+1},{show_id},{language},{resolution},{season}'))
    if len(pagination_buttons)>1:
        keyboard.append(pagination_buttons)
    keyboard.append([InlineKeyboardButton("⬅️ Back to Episodes", callback_data=f"b:0,{show_id},{language},{resolution},{season}")])
    db.close()
    return InlineKeyboardMarkup(keyboard)



#Admin Keyboards

def admin_keyboard():
    keyboard = [[InlineKeyboardButton("🔊  Languages", callback_data=f"languages:{0}"),
                InlineKeyboardButton("👤 Users", callback_data=f"user_list:{0}")],
                [InlineKeyboardButton("✖️ Close Message ✖️", callback_data=f"delete:{DEVELOPER_CHAT_ID}")]]
    return InlineKeyboardMarkup(keyboard)
    
def admin_close_key():
    return InlineKeyboardMarkup([[InlineKeyboardButton("✖️ Close Message ✖️", callback_data=f"delete:{DEVELOPER_CHAT_ID}")]])
    
def approval_keyboard(chat_id):
    db,conn = db_connection()
    conn.execute(f"SELECT approved,ban FROM {users} WHERE user_id = %s", (chat_id,))
    row = conn.fetchone()
    keyboard,keyboard_list,new_row = [],[],[]
    if row:
        approved,ban  = [int(i) for i in row]
    if row and not approved and not ban:
        keyboard_list.append(InlineKeyboardButton("Approve✅", callback_data=f"approve:{chat_id}"))
    if row and not ban:
        keyboard_list.append(InlineKeyboardButton("Ban🚫", callback_data=f"ban:{chat_id}"))
    if row and ban:
        keyboard_list.append(InlineKeyboardButton("Unban⭕️", callback_data=f"unban:{chat_id}"))
    if row:
        keyboard_list.append(InlineKeyboardButton("Remove🗑", callback_data=f"remove:{chat_id}"))
    for i,keys in enumerate(keyboard_list):
        new_row.append(keys)
        if (i + 1) % 2 == 0:
            keyboard.append(new_row)
            new_row = []
    if new_row:
        keyboard.append(new_row)
    keyboard.append([InlineKeyboardButton("✖️ Close User Profile ✖️", callback_data=f"delete:{chat_id}")])
    db.close()
    return InlineKeyboardMarkup(keyboard)

def user_profile_keyboard(chat_id):
    db,conn = db_connection()
    conn.execute(f"SELECT approved,ban FROM {users} WHERE user_id = %s", (chat_id,))
    row = conn.fetchone()
    keyboard,keyboard_list,new_row = [],[],[]
    if row:
        approved,ban  = [int(i) for i in row]
    if row and not approved and not ban:
        keyboard_list.append(InlineKeyboardButton("Approve✅", callback_data=f"approve:{chat_id}"))
    if row and not ban:
        keyboard_list.append(InlineKeyboardButton("Ban🚫", callback_data=f"ban:{chat_id}"))
    if row and ban:
        keyboard_list.append(InlineKeyboardButton("Unban⭕️", callback_data=f"unban:{chat_id}"))
    if row:
        keyboard_list.append(InlineKeyboardButton("Remove🗑", callback_data=f"remove:{chat_id}"))
    for i,keys in enumerate(keyboard_list):
        new_row.append(keys)
        if (i + 1) % 2 == 0:
            keyboard.append(new_row)
            new_row = []
    if new_row:
        keyboard.append(new_row)
    keyboard.append([InlineKeyboardButton("✖️ Close Message ✖️", callback_data=f"delete:{DEVELOPER_CHAT_ID}")])
    db.close()
    return InlineKeyboardMarkup(keyboard)

def user_list_keyboard(page):
    keyboard,new_row,pagination_buttons= [],[],[]
    db, conn = db_connection()
    conn.execute(f"SELECT * FROM {users}")
    users_list = conn.fetchall()
    db.close()
    if users_list:
        ITEMS_PER_PAGE = 6
        total_pages = math.ceil(len(users_list)/ITEMS_PER_PAGE)
        start = page * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        for i,user_row in enumerate(users_list[start:end]):
            new_row.append(InlineKeyboardButton(f"{user_row[3]}", callback_data=f"view_user:{user_row[0]}"))
            if (i + 1) % 2 == 0:
                keyboard.append(new_row)
                new_row = []
        if new_row:
            keyboard.append(new_row)
        
        if start > 0:
            pagination_buttons.append(InlineKeyboardButton('⏪ Previous', callback_data=f'user_list:{page-1}'))
        pagination_buttons.append(InlineKeyboardButton(f'📄{page+1} /{total_pages}',callback_data="empty"))
        if end < len(users_list):
            pagination_buttons.append(InlineKeyboardButton('Next ⏩', callback_data=f'user_list:{page+1}'))

        if len(pagination_buttons)>1:
            keyboard.append(pagination_buttons)
        keyboard.append([InlineKeyboardButton("✖️ Close Message ✖️", callback_data=f"delete:{DEVELOPER_CHAT_ID}")])
        return InlineKeyboardMarkup(keyboard)
    else:
        return False                


# Admin show surfing class
class AdminShowDetails():
    def __init__(self,show_id):
        self.show_id = show_id
        self.lang_dict = dict()
        self.resolution_dict = dict()
        self.file_size_dict = dict()
        self.seasons_dict = dict()
        self.episodes_dict = dict()
        self.extras_dict = dict()
        self.subs_dict = dict()
        db, conn = db_connection()
        conn.execute(f"SELECT * FROM {shows} WHERE show_id= %s", (self.show_id,))
        result = conn.fetchone()
        db.close()
        if result:
            self.show_id = result[0]
            self.poster_id = result[1]
            self.title = result[2]
            self.year = result[3]
            self.s_or_m = result[4]
        else:
            self.show_id = None
            return None
        
    def get_langs(self):
        db, conn = db_connection()
        if self.s_or_m :
                conn.execute(f"SELECT DISTINCT series_lang FROM {series} WHERE series_id = %s order by series_lang asc", (self.show_id,))
        else :
            conn.execute(f"SELECT DISTINCT movie_lang FROM {movie} WHERE movie_id = %s order by movie_lang asc", (self.show_id,))
        for row in conn.fetchall():
            lang_id = row[0]
            conn.execute(f"SELECT language FROM {languages} WHERE lang_id = %s", (lang_id,))
            language_name = conn.fetchone()[0]
            if lang_id not in self.lang_dict:
                self.lang_dict[lang_id] = language_name
        db.close()
        return self.lang_dict
    
    def get_filesize(self,lang_id):
        db, conn = db_connection()
        conn.execute(f"SELECT pk,size FROM {movie} WHERE movie_id = %s AND movie_lang=%s order by size asc", (self.show_id,lang_id))
        for row in conn.fetchall():  
            pk,size = row
            if pk not in self.file_size_dict:
                self.file_size_dict[pk] = size
        db.close()
        return self.file_size_dict
    
    def get_resolutions(self,lang_id):
        db, conn = db_connection()
        conn.execute(f"SELECT DISTINCT resolution FROM {series} WHERE series_id = %s AND series_lang=%s order by resolution asc", (self.show_id,lang_id))
        for row in conn.fetchall():  
            resolution = row[0]
            if resolution not in self.resolution_dict:
                self.resolution_dict[resolution] = resolution
        db.close()
        return self.resolution_dict
    
    def get_seasons(self,lang_id,resolution):
        db, conn = db_connection()
        conn.execute(f"SELECT DISTINCT season FROM {series} WHERE series_id = %s AND series_lang=%s AND resolution=%s order by season asc", (self.show_id,lang_id,resolution))
        for row in conn.fetchall():  
            season = row[0]
            if season not in self.seasons_dict:
                self.seasons_dict[season] = season
        db.close()
        return self.seasons_dict

    def get_episodes(self,lang_id,resolution,season):
        db, conn = db_connection()
        conn.execute(f"SELECT pk,episode FROM {series} WHERE series_id = %s AND series_lang=%s AND resolution=%s AND season=%s order by episode asc", (self.show_id,lang_id,resolution,season))
        for row in conn.fetchall():  
            pk,episode = row
            if pk not in self.episodes_dict:
                self.episodes_dict[pk] = episode
        db.close()
        return self.episodes_dict

    def get_extras(self,lang_id,resolution,season):
        db, conn = db_connection()
        conn.execute(f"SELECT pk,title FROM {extras} WHERE series_id = %s AND series_lang=%s AND resolution=%s AND season=%s order by title asc", (self.show_id,lang_id,resolution,season))
        for row in conn.fetchall():  
            pk,title = row
            if pk not in self.extras_dict:
                self.extras_dict[pk] = title
        db.close()
        return self.extras_dict
    
    def get_subs(self,season=0,episode=0):
        db,conn = db_connection()
        keyboard,new_row  = [],[]
        if self.s_or_m:
            conn.execute(f"SELECT s.pk,l.language FROM {subtitles} s INNER JOIN {languages} l ON s.lang_id = l.lang_id where show_id = %s AND season = %s AND episode=%s order by l.lang_id asc", (self.show_id,season ,episode,))
        else:
            conn.execute(f"SELECT s.pk,l.language FROM {subtitles} s INNER JOIN {languages} l ON s.lang_id = l.lang_id where show_id = %s order by l.lang_id asc", (self.show_id,))
        keyboard.append([InlineKeyboardButton(f"Choose Subtitle Language",callback_data="empty")])
        for row in conn.fetchall():  
            pk,language = row
            if pk not in self.subs_dict:
                self.subs_dict[pk] = language
        db.close()
        return self.subs_dict
    
    def get_start_keyboard(self):
        keyboard = []
        if len(self.get_langs())>0:
            keyboard.append(InlineKeyboardButton("Open Inner Menu",callback_data=f"open-inner:{self.show_id}"))
        keyboard.append(InlineKeyboardButton("Delete Show",callback_data=f"rem-Show:{self.show_id}"))
        return InlineKeyboardMarkup([keyboard])
    
    def get_keyboard(self,page,per_page,per_row,menu_dict,menu_name,prev_menu,backword,value_string=""):
        keyboard,new_row,pagination_buttons,end_kb = [],[],[],[]
        total_pages = math.ceil(len(menu_dict)/per_page)
        start = page * per_page
        end = start + per_page
        values_count = list(menu_dict.keys())
        if menu_dict != {}:
            keyboard.append([InlineKeyboardButton(f"Choose {menu_name}",callback_data="empty")])
        
        for i,key in enumerate(values_count[start:end]): 
            button_text = menu_dict[key]
            cb_data = f"{menu_name}:{value_string},{key}"
            if menu_name =="Resolution":
                button_text = f"{menu_dict[key]}p" 
                
            if menu_name =="Season":
                button_text = f"S{menu_dict[key]}" 
            if menu_name =="Episode":
                button_text = f"E{menu_dict[key]}"
            if menu_name =="Extra":
                cb_data = f"rem-{menu_name}:{value_string},{key}"
            if menu_name =="Filesize":
                cb_data = f"rem-{menu_name}:{value_string},{key}"
            if menu_name =="Subtitle":
                if self.s_or_m:
                    show_id,lang_id,resolution,season,episode_id = [int(i) for i in value_string.split(",")]
                    cb_data = f"rem-{menu_name}:{show_id},{lang_id},{resolution},{season},{episode_id},{key}"   
                else:
                    cb_data = f"rem-{menu_name}:{self.show_id},{key}"
                                
            new_row.append(InlineKeyboardButton(f"{button_text}", callback_data=cb_data))
            if (i + 1) % per_row == 0:
                keyboard.append(new_row)
                new_row = []
        if new_row:
            keyboard.append(new_row)
        
        if len(pagination_buttons)>1:
            if start > 0:
                pagination_buttons.append(InlineKeyboardButton('⏪ Previous', callback_data=f'next:{page-1},{value_string}'))
            pagination_buttons.append(InlineKeyboardButton(f'📄 {page+1} /{total_pages}',callback_data="empty"))
            if end < len(menu_dict):
                pagination_buttons.append(InlineKeyboardButton('Next ⏩', callback_data=f'prev:{page+1},{value_string}'))
            if len(pagination_buttons)>1:
                keyboard.append(pagination_buttons)
                
        if menu_name == "Episode":
            db,conn = db_connection()
            ex_show_id,ex_lang_id,ex_resolution,ex_season = [int(i) for i in value_string.split(",")]
            extras_dict = AdminShowDetails(ex_show_id).get_extras(ex_lang_id,ex_resolution,ex_season)
            if extras_dict != {}:
                keyboard.append([InlineKeyboardButton("Extras ✨", callback_data=f"Extra:{value_string}")])
            db.close()
        
        
        if prev_menu == "Language" and menu_name == "Subtitle":
            end_kb.append(InlineKeyboardButton(f"⬅️ Goto {prev_menu}", callback_data=f"{backword}:{value_string}"))
        elif prev_menu != "Main-Menu" and menu_name != "Extra":
            back_string = ",".join(value_string.split(",")[:-1])
            end_kb.append(InlineKeyboardButton(f"⬅️ Goto {prev_menu}", callback_data=f"{backword}:{back_string}"))
            end_kb.append(InlineKeyboardButton(f"Delete {prev_menu}", callback_data=f"rem-{prev_menu}:{value_string}"))
        else:
            end_kb.append(InlineKeyboardButton(f"⬅️ Goto {prev_menu}", callback_data=f"{backword}:{value_string}"))
            if menu_name =="Language" and not self.s_or_m:
                end_kb.append(InlineKeyboardButton(f"Open Subtitles", callback_data=f"Movie-Subs:{value_string}"))
        
        keyboard.append(end_kb)
        return InlineKeyboardMarkup(keyboard)

def confirm_keyboard(sql_params,back_string):
    keyboard = []
    keyboard.append([InlineKeyboardButton("Confirm Deletion?",callback_data=f"empty")])
    keyboard.append([InlineKeyboardButton("Delete",callback_data=f"{sql_params}"),InlineKeyboardButton("Cancel",callback_data=f"{back_string}")])
    return InlineKeyboardMarkup(keyboard)
     
def query_executor(sql_query):
    db,conn = db_connection()
    try:
        conn.execute(sql_query)
        db.commit()
        return True
    except Error as e:
        print(e)
        return False
    
def after_delete_keyboard(back_parameters):
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️Go to Previous Menu",callback_data=f"{back_parameters}")]])