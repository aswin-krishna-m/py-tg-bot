from telegram import  Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from telegram.constants import ParseMode
import logging,asyncio,html,json,logging,traceback
from bot_app.modules.my_constants import *

# Setting logger
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)  

# # Error handler to admin
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling an update:", exc_info=context.error)
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = ("An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>")
    
    markup = admin_close_key()
    await context.bot.send_chat_action(chat_id=DEVELOPER_CHAT_ID,action='typing')
    await asyncio.sleep(message_action_delay)
    await context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML, reply_markup=markup)

# /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  msg_obj = update.message if update.message else update.edited_message
  auth_result = auth_user(msg_obj.chat_id)
  if auth_result =="admin" or auth_result=="approved":
    with open(GIF_PATH, 'rb') as gif:
      await msg_obj.reply_chat_action(action='upload_video')
      await asyncio.sleep(message_action_delay)
      await msg_obj.reply_animation(animation=gif, caption=f"Hello *{msg_obj.from_user.first_name}*, "+startDesc,parse_mode=ParseMode.MARKDOWN)
  else:
    if auth_result=="unapproved":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=ApprovalDesc , parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="banned":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=BanDesc, parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="request":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=UnapprovedDesc,  reply_markup= request_keyboard(msg_obj.chat_id),parse_mode=ParseMode.MARKDOWN)

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  msg_obj = update.message if update.message else update.edited_message
  auth_result = auth_user(msg_obj.chat_id)
  if auth_result =="admin" or auth_result=="approved":
    await msg_obj.reply_chat_action(action='typing')
    await asyncio.sleep(message_action_delay)
    await msg_obj.reply_text(text=helpDesc,parse_mode= ParseMode.MARKDOWN, disable_web_page_preview=True)
  else:
    if auth_result=="unapproved":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=ApprovalDesc , parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="banned":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=BanDesc, parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="request":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=UnapprovedDesc,  reply_markup= request_keyboard(msg_obj.chat_id),parse_mode=ParseMode.MARKDOWN)

# /about command
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  msg_obj = update.message if update.message else update.edited_message
  auth_result = auth_user(msg_obj.chat_id)
  if auth_result =="admin" or auth_result=="approved":
    await msg_obj.reply_chat_action(action='typing')
    await asyncio.sleep(message_action_delay)
    await msg_obj.reply_html(text=aboutDesc, disable_web_page_preview=True)
  else:
    if auth_result=="unapproved":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=ApprovalDesc , parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="banned":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=BanDesc, parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="request":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=UnapprovedDesc,  reply_markup= request_keyboard(msg_obj.chat_id),parse_mode=ParseMode.MARKDOWN)

# /admin command
async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  msg_obj = update.message if update.message else update.edited_message
  auth_result = auth_user(msg_obj.chat_id)
  if auth_result =="admin":
    await msg_obj.reply_chat_action(action='typing')
    await asyncio.sleep(message_action_delay)
    await msg_obj.reply_text(text=adminDesc,reply_markup=admin_keyboard(), disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
  else:    
    if auth_result =="approved":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=AdminUsageOnly,parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="unapproved":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=ApprovalDesc , parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="banned":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=BanDesc, parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="request":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=UnapprovedDesc,  reply_markup= request_keyboard(msg_obj.chat_id),parse_mode=ParseMode.MARKDOWN)

# Handle adminInline query button except users
async def adminInline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  query = update.callback_query
  auth_result = auth_user(query.message.chat_id)
  if auth_result =="admin":
    await query.answer()
    data = query.data
    data = query.data.split(":")
    action = data[0]

    if action == "languages":
      db, conn = db_connection()
      conn.execute(f"SELECT lang_id,language FROM {languages}")
      result = conn.fetchall()
      db.close()
      lang_list = "*LANGUAGE LIST*\n\n"
      lang_list += "*ID. LANGUAGE*\n"
      if result:
          for lang_id, language in result:
              lang_list += f"{lang_id}. {language}\n"
      else:
          lang_list = "No Languages added so far!"
      await context.bot.send_message(text=lang_list,chat_id = DEVELOPER_CHAT_ID,reply_markup=admin_close_key(), disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
      
    elif action == "user_list":
      page = int(data[1])
      context.user_data['admin_state'] = 'admin_menu'
      users_list_markup = user_list_keyboard(page)
      if users_list_markup:
        await context.bot.send_message(text="*USERS LIST*",chat_id = DEVELOPER_CHAT_ID,reply_markup=users_list_markup,parse_mode=ParseMode.MARKDOWN)
      else:
        await context.bot.send_message(text="No Users so far!",chat_id = DEVELOPER_CHAT_ID,reply_markup=admin_close_key(), disable_web_page_preview=True)

    elif action == "view_user":
      context.user_data['user_state'] = 'user_menu'
      user_id = int(data[1])
      db, conn = db_connection()
      conn.execute(f"SELECT * FROM {users} where user_id=%s",(user_id,))
      users_list = conn.fetchone()
      db.close()
      tg_name = str(users_list[3])
      tg_username = str(users_list[4])
      tg_id = str(users_list[0])
      request_msg = "*USER PROFILE\nName: "+tg_name+"\nUsername: "+tg_username+"\nTG-ID: "+tg_id+"*"
      await context.bot.send_message(text=request_msg,chat_id=DEVELOPER_CHAT_ID, reply_markup= user_profile_keyboard(user_id),parse_mode=ParseMode.MARKDOWN)
  else:
    if auth_result =="approved":
      await query.message.reply_text(text=AdminUsageOnly,parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="unapproved":
        await query.message.reply_text(text=ApprovalDesc , parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="banned":
        await query.message.reply_text(text=BanDesc, parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="request":
        await query.message.reply_text(text=UnapprovedDesc,  reply_markup= request_keyboard(query.message.chat_id),parse_mode=ParseMode.MARKDOWN)

# Add Language command
async def addlang_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  msg_obj = update.message if update.message else update.edited_message
  auth_result = auth_user(msg_obj.chat_id)
  if auth_result =="admin":
    language_name = str(msg_obj.text.split()[1]).upper()
    db,conn=db_connection()
    conn.execute(f"INSERT INTO {languages}(language) VALUES (%s)", (language_name,))
    db.commit()
    db.close()
    await msg_obj.reply_chat_action(action='typing')
    await asyncio.sleep(message_action_delay)
    await context.bot.send_message(chat_id= DEVELOPER_CHAT_ID ,text =f"*{language_name}* added to language database",parse_mode=ParseMode.MARKDOWN)
  else:
    if auth_result=="unapproved":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=ApprovalDesc , parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="banned":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=BanDesc, parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="request":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=UnapprovedDesc,  reply_markup= request_keyboard(msg_obj.chat_id),parse_mode=ParseMode.MARKDOWN)

# Broad cast command
async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  msg_obj = update.message if update.message else update.edited_message
  auth_result = auth_user(msg_obj.chat_id)
  if auth_result =="admin":
    show = msg_obj.text.split()[1]
    show_id = show if len(show)==1 and show.isdigit() else "*No Parameter/Wrong type of parameter*"
    show_obj = AdminShowDetails(show_id)
    if show_obj.show_id:
      show_id = show_obj.show_id
      poster_id = show_obj.poster_id
      title = show_obj.title
      year = show_obj.year
      s_or_m = show_obj.s_or_m
      update_msg = f"🎉 New Season of *{title}* is here!!!!🎉" if s_or_m  else f"🎉*Latest OTT release UPDATE*!!!! 🎉"
      lang_list= languages_keyboard(s_or_m,show_id)[0]
      if len(lang_list)>0:
        language = ','.join(lang_list)
      else:
        language = 'Not Declared'
      broadcast_caption = (f"{update_msg}*\n\n🎬 Title : {title}\n🗓 Year: {year}\n🔊 Language: {language}*\n")
      markup = InlineKeyboardMarkup([[InlineKeyboardButton("DOWNLOAD", callback_data=f"broadcast:{s_or_m},{show_id}")]])
      db,conn = db_connection()
      conn.execute(f"SELECT user_id FROM {users} WHERE ban = 0 AND approved = 1")
      user_result = conn.fetchall()
      db.close()
      if user_result:
        for user_id in user_result:
          await context.bot.send_chat_action(chat_id=user_id[0], action='upload_photo')
          await asyncio.sleep(message_action_delay)
          await context.bot.send_photo(chat_id=user_id[0], photo=poster_id, reply_markup=markup, caption=broadcast_caption,parse_mode=ParseMode.MARKDOWN)
      else:
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text= "*No approved users in DB to broadcast to!!*", disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
    else:
      await msg_obj.reply_chat_action(action='typing')
      await asyncio.sleep(message_action_delay)
      await msg_obj.reply_text(text= "*Show ID did not match our records*", disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
  else:
    if auth_result=="unapproved":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=ApprovalDesc , parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="banned":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=BanDesc, parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="request":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=UnapprovedDesc,  reply_markup= request_keyboard(msg_obj.chat_id),parse_mode=ParseMode.MARKDOWN)

# Manage broadcast_Inline query button - choose series resolution or movie size
async def broadcast_Inline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  query = update.callback_query
  auth_result = auth_user(query.message.chat_id)
  if auth_result =="admin" or auth_result == "approved":
    await query.answer()
    action = query.data.split(":")[0]
    data = query.data.split(":")[1]
    if action == "broadcast":
      series_movie,show_id = [int(i) for i in data.split(",")]
      markup = languages_keyboard(series_movie,show_id)[1]
      await query.edit_message_reply_markup(reply_markup=markup)

# Manage remfiles_commmand
async def remfiles_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  msg_obj = update.message if update.message else update.edited_message
  auth_result = auth_user(msg_obj.chat_id)
  if auth_result =="admin":
    show = msg_obj.text.split()
    show_id = show[1] if len(show)==2 and show[1].isdigit() else "*No Parameter/Wrong type of parameter*"
    show_obj = AdminShowDetails(show_id)
    if show_obj.show_id is not None:
      markup = show_obj.get_start_keyboard()
      rem_caption = (f"*🎬 Title : {show_obj.title}\n🗓 Year: {show_obj.year}*\n")
      await context.bot.send_chat_action(chat_id=DEVELOPER_CHAT_ID, action='upload_photo')
      await asyncio.sleep(message_action_delay)
      await context.bot.send_photo(chat_id=DEVELOPER_CHAT_ID, photo=show_obj.poster_id, reply_markup=markup, caption=rem_caption,parse_mode=ParseMode.MARKDOWN)
    else:
      await context.bot.send_chat_action(chat_id=DEVELOPER_CHAT_ID, action='typing')
      await asyncio.sleep(message_action_delay)
      await msg_obj.reply_text(text= "*Show ID did not match our records*", disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
  else:
    if auth_result=="unapproved":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=ApprovalDesc , parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="banned":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=BanDesc, parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="request":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=UnapprovedDesc,  reply_markup= request_keyboard(msg_obj.chat_id),parse_mode=ParseMode.MARKDOWN)

# Manage_show_Inline query button - choose series resolution or movie size
async def manage_show_Inline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  query = update.callback_query
  auth_result = auth_user(query.message.chat_id)
  if auth_result =="admin":
    await query.answer()
    action = query.data.split(":")[0]
    data = query.data.split(":")[1]

    if action == "Main-Menu":
      show_id = int(data)
      markup = AdminShowDetails(show_id).get_start_keyboard()
      await query.edit_message_reply_markup(markup)

    elif action == "open-inner":
      show_id = int(data)
      show_obj = AdminShowDetails(show_id)
      kb_dict = show_obj.get_langs()
      menu_name = "Language"
      prev_menu = "Main-Menu"
      backword = "Main-Menu"
      value_string = f"{show_id}"
      markup = show_obj.get_keyboard(0,8,2,kb_dict,menu_name,prev_menu,backword,value_string)
      await query.edit_message_reply_markup(markup)

    elif action == "Language":
      show_id,lang_id = [int(i) for i in data.split(",")]
      show_obj = AdminShowDetails(show_id)
      if show_obj.s_or_m:
        kb_dict = show_obj.get_resolutions(lang_id)
        menu_name = "Resolution"
        prev_menu = "Language"
      else:
        menu_name = "Filesize"
        prev_menu = "Language"
        kb_dict =show_obj.get_filesize(lang_id)
      backword = "open-inner"
      value_string = f"{show_id},{lang_id}"
      markup = show_obj.get_keyboard(0,8,2,kb_dict,menu_name,prev_menu,backword,value_string)
      await query.edit_message_reply_markup(markup)

    elif action == "Movie-Subs":
      show_id = int(data)
      show_obj = AdminShowDetails(show_id)
      kb_dict =  show_obj.get_subs()
      menu_name = "Subtitle"
      prev_menu = "Language"
      backword = "open-inner"
      value_string = f"{show_id}"
      markup = show_obj.get_keyboard(0,10,2,kb_dict,menu_name,prev_menu,backword,value_string)
      await query.edit_message_reply_markup(markup)

    elif action == "Resolution":
      show_id,lang_id,resolution = [int(i) for i in data.split(",")]
      show_obj = AdminShowDetails(show_id)
      kb_dict = show_obj.get_seasons(lang_id,resolution)
      menu_name = "Season"
      prev_menu = "Resolution"
      backword = "Language"
      value_string = f"{show_id},{lang_id},{resolution}"
      markup = show_obj.get_keyboard(0,16,4,kb_dict,menu_name,prev_menu,backword,value_string)
      await query.edit_message_reply_markup(markup)

    elif action == "Season":
      show_id,lang_id,resolution,season = [int(i) for i in data.split(",")]
      show_obj = AdminShowDetails(show_id)
      kb_dict = show_obj.get_episodes(lang_id,resolution,season)
      menu_name = "Episode"
      prev_menu = "Season"
      backword = "Resolution"
      value_string = f"{show_id},{lang_id},{resolution},{season}"
      markup = show_obj.get_keyboard(0,20,5,kb_dict,menu_name,prev_menu,backword,value_string)
      await query.edit_message_reply_markup(markup)

    elif action == "Episode":
      show_id,lang_id,resolution,season,episode_pk = [int(i) for i in data.split(",")]
      show_obj = AdminShowDetails(show_id)
      episode_dict =show_obj.get_episodes(lang_id,resolution,season)
      episode = episode_dict[episode_pk]
      kb_dict = show_obj.get_subs(season,episode)
      menu_name = "Subtitle"
      prev_menu = "Episode"
      backword = "Season"
      value_string = f"{show_id},{lang_id},{resolution},{season},{episode_pk}"
      markup = show_obj.get_keyboard(0,10,2,kb_dict,menu_name,prev_menu,backword,value_string)
      await query.edit_message_reply_markup(markup)

    elif action == "Extra":
      show_id,lang_id,resolution,season = [int(i) for i in data.split(",")]
      show_obj = AdminShowDetails(show_id)
      kb_dict = show_obj.get_extras(lang_id,resolution,season)
      menu_name = "Extra"
      prev_menu = "Season"
      backword = "Season"
      value_string = f"{show_id},{lang_id},{resolution},{season}"
      markup = show_obj.get_keyboard(0,10,2,kb_dict,menu_name,prev_menu,backword,value_string)
      await query.edit_message_reply_markup(markup)

    elif action == "rem-Show":
      sql_params = f"Yes-Show:{data}"
      back_string = f"Main-Menu:{data}"
      await query.edit_message_reply_markup(confirm_keyboard(sql_params,back_string))

    elif action == "rem-Language":
      sql_params = f"Yes-Language:{data}"
      back_string = f"Language:{data}"
      await query.edit_message_reply_markup(confirm_keyboard(sql_params,back_string))

    elif action == "rem-Resolution":
      sql_params = f"Yes-Resolution:{data}"
      back_string = f"Resolution:{data}"
      await query.edit_message_reply_markup(confirm_keyboard(sql_params,back_string))

    elif action == "rem-Season":
      sql_params = f"Yes-Season:{data}"
      back_string = f"Season:{data}"
      await query.edit_message_reply_markup(confirm_keyboard(sql_params,back_string))

    elif action == "rem-Episode":
      sql_params = f"Yes-Episode:{data}"
      back_string = f"Episode:{data}"
      await query.edit_message_reply_markup(confirm_keyboard(sql_params,back_string))

    elif action == "rem-Filesize":
      show_id, lang_id,file_pk = [int(i) for i in data.split(",")]
      sql_params = f"Yes-Filesize:{data}"
      back_string = f"Language:{show_id},{lang_id}"
      await query.edit_message_reply_markup(confirm_keyboard(sql_params,back_string))

    elif action == "rem-Extra":
      show_id, lang_id,resolution,season,extra_id = [int(i) for i in data.split(",")]
      sql_params = f"Yes-Extra:{data}"
      back_string = f"Extra:{show_id},{lang_id},{resolution},{season}"
      await query.edit_message_reply_markup(confirm_keyboard(sql_params,back_string))

    elif action == "rem-Subtitle":
      sub_data = data.split(",")
      if len(sub_data) == 2:
        show_id, subtitle_pk = [int(i) for i in sub_data]
        back_string = f"Movie-Subs:{show_id}"
        sql_params = f"Yes-Subtitle:{show_id},{subtitle_pk}"
      elif len(sub_data) ==6 :
        show_id,lang_id,resolution,season,episode_id,subtitle_pk = [int(i) for i in sub_data]
        back_string = f"Episode:{show_id},{lang_id},{resolution},{season},{episode_id}"
        sql_params = f"Yes-Subtitle:{show_id},{lang_id},{resolution},{season},{episode_id},{subtitle_pk}"
      await query.edit_message_reply_markup(confirm_keyboard(sql_params,back_string))

    elif action == "Yes-Show":
      show_id = int(data)
      sql_query = f"DELETE FROM {shows} WHERE show_id={show_id}"
      show_obj = AdminShowDetails(show_id)
      admin_ack = (f"*❗️❗️❗️ Show Removed  ❗️❗️❗️*\n"
                   f"*Title: {show_obj.title}*\n"
                   f"Year: {show_obj.year}\n")
      if query_executor(sql_query):
        await context.bot.delete_message(chat_id=DEVELOPER_CHAT_ID,message_id=query.message.id)
        await context.bot.send_message(chat_id= DEVELOPER_CHAT_ID ,text = admin_ack ,parse_mode=ParseMode.MARKDOWN)
      else:
        await context.bot.send_message(chat_id= DEVELOPER_CHAT_ID ,text = "Deletion Error" ,parse_mode=ParseMode.MARKDOWN)

    elif action == "Yes-Language":
      show_id,lang_id = [int(i) for i in data.split(",")]
      show_obj = AdminShowDetails(show_id)
      if show_obj.s_or_m:
        sql_query = f"DELETE FROM {series} WHERE series_id={show_id} AND series_lang={lang_id}"
      else:
        sql_query = f"DELETE FROM {movie} WHERE movie_id={show_id} AND movie_lang={lang_id}"
      show_language = show_obj.get_langs()[lang_id]
      admin_ack = (f"❗️❗️❗️ Language Removed from Shows  ❗️❗️❗️\n"
                   f"Title: {show_obj.title}\n"
                   f"Year: {show_obj.year}\n"
                   f"*Language: {show_language}*\n")
      del_kb_params = f"open-inner:{show_id}"
      if query_executor(sql_query):
        await context.bot.send_message(chat_id= DEVELOPER_CHAT_ID ,text =admin_ack,parse_mode=ParseMode.MARKDOWN)
        await query.message.edit_reply_markup(reply_markup = after_delete_keyboard(del_kb_params))
      else:
        await context.bot.send_message(chat_id= DEVELOPER_CHAT_ID ,text = "Deletion Error" ,parse_mode=ParseMode.MARKDOWN)

    elif action == "Yes-Filesize":
      show_id,lang_id,file_pk = [int(i) for i in data.split(",")]
      sql_query = f"DELETE FROM {movie} WHERE pk={file_pk}"
      show_obj = AdminShowDetails(show_id)
      show_language = show_obj.get_langs()[lang_id]
      removed_file_size = show_obj.get_filesize(lang_id)[file_pk]
      admin_ack = (f"❗️❗️❗️ File Removed from Shows  ❗️❗️❗️\n"
                   f"Title: {show_obj.title}\n"
                   f"Year: {show_obj.year}\n"
                   f"Language: {show_language}\n"
                   f"*Filesize: {removed_file_size}*\n")
      del_kb_params = f"Language:{show_id},{lang_id}"
      if query_executor(sql_query):
        await context.bot.send_message(chat_id= DEVELOPER_CHAT_ID ,text =admin_ack,parse_mode=ParseMode.MARKDOWN)
        await query.message.edit_reply_markup(reply_markup = after_delete_keyboard(del_kb_params))
      else:
        await context.bot.send_message(chat_id= DEVELOPER_CHAT_ID ,text = "Deletion Error" ,parse_mode=ParseMode.MARKDOWN)

    elif action == "Yes-Resolution":
      show_id,lang_id,resolution = [int(i) for i in data.split(",")]
      sql_query = f"DELETE FROM {series} WHERE series_id={show_id} AND series_lang={lang_id} AND resolution={resolution}"
      show_obj = AdminShowDetails(show_id)
      show_language = show_obj.get_langs()[lang_id]
      show_resolution = show_obj.get_resolutions(lang_id)[resolution]
      admin_ack = (f"❗️❗️❗️ Resolution Removed from Shows  ❗️❗️❗️\n"
                   f"Title: {show_obj.title}\n"
                   f"Year: {show_obj.year}\n"
                   f"Language: {show_language}\n"
                   f"Resolution: {show_resolution}p\n")
      del_kb_params = f"Language:{show_id},{lang_id}"
      if query_executor(sql_query):
        await context.bot.send_message(chat_id= DEVELOPER_CHAT_ID ,text =admin_ack,parse_mode=ParseMode.MARKDOWN)
        await query.message.edit_reply_markup(reply_markup = after_delete_keyboard(del_kb_params))
      else:
        await context.bot.send_message(chat_id= DEVELOPER_CHAT_ID ,text = "Deletion Error" ,parse_mode=ParseMode.MARKDOWN)

    elif action == "Yes-Season":
      show_id,lang_id,resolution,season = [int(i) for i in data.split(",")]
      sql_query = f"DELETE FROM {series} WHERE series_id={show_id} AND series_lang={lang_id} AND resolution={resolution} AND season={season}"
      show_obj = AdminShowDetails(show_id)
      show_language = show_obj.get_langs()[lang_id]
      show_resolution = show_obj.get_resolutions(lang_id)[resolution]
      show_season = show_obj.get_seasons(lang_id,resolution)[season]
      admin_ack = (f"❗️❗️❗️ Season Removed from Shows  ❗️❗️❗️\n"
                   f"Title: {show_obj.title}\n"
                   f"Year: {show_obj.year}\n"
                   f"Language: {show_language}\n"
                   f"Resolution: {show_resolution}p\n"
                   f"*Season: {show_season}*\n")
      del_kb_params = f"Resolution:{show_id},{lang_id},{resolution}"
      if query_executor(sql_query):
        await context.bot.send_message(chat_id= DEVELOPER_CHAT_ID ,text =admin_ack,parse_mode=ParseMode.MARKDOWN)
        await query.message.edit_reply_markup(reply_markup = after_delete_keyboard(del_kb_params))
      else:
        await context.bot.send_message(chat_id= DEVELOPER_CHAT_ID ,text = "Deletion Error" ,parse_mode=ParseMode.MARKDOWN)

    elif action == "Yes-Episode":
      show_id,lang_id,resolution,season,episode_pk = [int(i) for i in data.split(",")]
      sql_query = f"DELETE FROM {series} WHERE pk={episode_pk}"
      show_obj = AdminShowDetails(show_id)
      show_language = show_obj.get_langs()[lang_id]
      show_resolution = show_obj.get_resolutions(lang_id)[resolution]
      show_season = show_obj.get_seasons(lang_id,resolution)[season]
      show_episode = show_obj.get_episodes(lang_id,resolution,season)[episode_pk]
      admin_ack = (f"❗️❗️❗️ Episode Removed from Shows  ❗️❗️❗️\n"
                   f"Title: {show_obj.title}\n"
                   f"Year: {show_obj.year}\n"
                   f"Language: {show_language}\n"
                   f"Resolution: {show_resolution}p\n"
                   f"Season: {show_season}\n"
                   f"*Episode: {show_episode}*\n")
      del_kb_params = f"Season:{show_id},{lang_id},{resolution},{season}"
      if query_executor(sql_query):
        await context.bot.send_message(chat_id= DEVELOPER_CHAT_ID ,text =admin_ack,parse_mode=ParseMode.MARKDOWN)
        await query.message.edit_reply_markup(reply_markup = after_delete_keyboard(del_kb_params))
      else:
        await context.bot.send_message(chat_id= DEVELOPER_CHAT_ID ,text = "Deletion Error" ,parse_mode=ParseMode.MARKDOWN)

    elif action == "Yes-Extra":
      show_id,lang_id,resolution,season,extra_episode_pk = [int(i) for i in data.split(",")]
      sql_query = f"DELETE FROM {extras} WHERE pk={extra_episode_pk}"
      show_obj = AdminShowDetails(show_id)
      show_language = show_obj.get_langs()[lang_id]
      show_resolution = show_obj.get_resolutions(lang_id)[resolution]
      show_season = show_obj.get_seasons(lang_id,resolution)[season]
      show_xtra = show_obj.get_extras(lang_id,resolution,season)[extra_episode_pk]
      admin_ack = (f"❗️❗️❗️ Extra-Episode Removed from Shows  ❗️❗️❗️\n"
                   f"Title: {show_obj.title}\n"
                   f"Year: {show_obj.year}\n"
                   f"Language: {show_language}\n"
                   f"Resolution: {show_resolution}p\n"
                   f"Season: {show_season}\n"
                   f"*Extra Title : {show_xtra}*\n")
      del_kb_params = f"Extra:{show_id},{lang_id},{resolution},{season}"
      if query_executor(sql_query):
        await context.bot.send_message(chat_id= DEVELOPER_CHAT_ID ,text =admin_ack,parse_mode=ParseMode.MARKDOWN)
        await query.message.edit_reply_markup(reply_markup = after_delete_keyboard(del_kb_params))
      else:
        await context.bot.send_message(chat_id= DEVELOPER_CHAT_ID ,text = "Deletion Error" ,parse_mode=ParseMode.MARKDOWN)

    elif action == "Yes-Subtitle":
      sub_data = data.split(",")
      show_id = sub_data[0]
      show_obj = AdminShowDetails(show_id)
      if len(sub_data) == 2:
        show_id, subtitle_pk = [int(i) for i in sub_data]
        show_sub_language = show_obj.get_subs()[subtitle_pk]
        admin_ack = (f"❗️❗️❗️ Subtitle Removed from Shows  ❗️❗️❗️\n"
                   f"Title: {show_obj.title}\n"
                   f"Year: {show_obj.year}\n"
                   f"*Sub-Language: {show_sub_language}*\n")
        del_kb_params =f"Movie-Subs:{show_id}"
      elif len(sub_data) ==6 :
        show_id,lang_id,resolution,season,episode_id,subtitle_pk = [int(i) for i in sub_data]
        show_language = show_obj.get_langs()[lang_id]
        show_resolution = show_obj.get_resolutions(lang_id)[resolution]
        show_season = show_obj.get_seasons(lang_id,resolution)[season]
        show_episode = show_obj.get_episodes(lang_id,resolution,season)[episode_id]
        show_sub_language = show_obj.get_subs(season,show_episode)[subtitle_pk]
        admin_ack = (f"❗️❗️❗️ Subtitle Removed from Shows  ❗️❗️❗️\n"
                   f"Title: {show_obj.title}\n"
                   f"Year: {show_obj.year}\n"
                   f"Language: {show_language}\n"
                   f"Resolution: {show_resolution}p\n"
                   f"Season: {show_season}\n"
                   f"Episode : {show_episode}\n"
                   f"*Sub-Language: {show_sub_language}*\n")
        del_kb_params = f"Episode:{show_id},{lang_id},{resolution},{season},{episode_id}"
      sql_query = f"DELETE FROM {subtitles} WHERE pk={subtitle_pk}"
      if query_executor(sql_query):
        await context.bot.send_message(chat_id= DEVELOPER_CHAT_ID ,text =admin_ack,parse_mode=ParseMode.MARKDOWN)
        await query.message.edit_reply_markup(reply_markup = after_delete_keyboard(del_kb_params))
      else:
        await context.bot.send_message(chat_id= DEVELOPER_CHAT_ID ,text = "Deletion Error" ,parse_mode=ParseMode.MARKDOWN)

  else:
    if auth_result=="unapproved":
        await query.message.reply_text(text=ApprovalDesc , parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="banned":
        await query.message.reply_text(text=BanDesc, parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="request":
        await query.message.reply_text(text=UnapprovedDesc,  reply_markup= request_keyboard(query.message.chat_id),parse_mode=ParseMode.MARKDOWN)

# Handle img
async def handle_img(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  msg_obj = update.message if update.message else update.edited_message
  auth_result = auth_user(msg_obj.chat_id)
  if auth_result =="admin":
    try:
      file = msg_obj.photo[-1]
      file_id = file.file_id
      caption = msg_obj.caption
      if not caption:
        raise Exception("Caption is required")
      cap = caption.split("$")
      if len(cap) < 3 or cap[0]=='' :
        raise Exception("Invalid caption format")
      elif file == msg_obj.photo[-1]:
        series ,year = int(cap.pop().strip()),int(cap.pop().strip())
        title = ''.join(cap)
        db,conn = db_connection()
        conn.execute(f"INSERT INTO {shows}(poster_id, title, year, series) VALUES (%s, %s, %s, %s)", (file_id,title,year,series))
        db.commit()
        db.close()
        output = f"*{title} ({year})* has been added to the shows successfully."
    except Exception as e:
      await context.bot.send_chat_action(chat_id = DEVELOPER_CHAT_ID, action='typing')
      await asyncio.sleep(message_action_delay)
      await context.bot.send_message(chat_id=DEVELOPER_CHAT_ID,text=f"Error: {e}", parse_mode=ParseMode.MARKDOWN)
    await msg_obj.reply_chat_action(action='typing')
    await asyncio.sleep(message_action_delay)
    await msg_obj.reply_text(output,parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
  else:
    if auth_result =="approved":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=AdminUsageOnly,parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="unapproved":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=ApprovalDesc , parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="banned":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=BanDesc, parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="request":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=UnapprovedDesc,  reply_markup= request_keyboard(msg_obj.chat_id),parse_mode=ParseMode.MARKDOWN)

# Handle subtitle
async def handle_subtitle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  msg_obj = update.message if update.message else update.edited_message
  auth_result = auth_user(msg_obj.chat_id)
  if auth_result =="admin":
    try:
      file = msg_obj.document
      file_id = file.file_id
      caption = msg_obj.caption
      if not caption:
        raise Exception("Caption is required")
      caption = caption.split(",")
      cap=[]
      for i in caption:
        cap.append(int(i.strip()))

      if len(cap) < 2 or len(cap)==3 or len(cap) > 4:
        raise Exception("Invalid caption format")
      show_id,lang_id = cap[:2]
      db, conn = db_connection()
      conn.execute(f"SELECT lang_id,language FROM {languages} WHERE lang_id = %s",(lang_id,))
      lang_id, language =conn.fetchone()
      conn.execute(f"SELECT title,series FROM {shows} WHERE show_id = %s",(show_id,))
      title,series_or_not=conn.fetchone()
      if len(cap) == 2:
        if not series_or_not:
          conn.execute(f"INSERT INTO {subtitles}(file_id,show_id,lang_id) VALUES (%s, %s, %s)", (file_id,show_id,lang_id))
          output = f"*Movie : {title}\nSubtitle Language : {language}*\nNew Movie Subtitle has been added to the database successfully."
        else:
          raise Exception("Not a movie subtitle format")
      elif len(cap) == 4:
        if series_or_not:
          season, episode = cap[2:]
          conn.execute(f"INSERT INTO {subtitles}(file_id,show_id,lang_id,season,episode) VALUES (%s, %s, %s,%s, %s)", (file_id,show_id,lang_id,season,episode))
          output = f"*Series: {title}\nSubtitle Language : {language}\nSeason: {season}\nEpisode: {episode}\n*\nNew Series Subtitle has been added to the database successfully."
        else:
          raise Exception("Not a series subtitle format")
      else:
        raise Exception("Invalid subtitle caption format")
      db.commit()
      db.close()
    except Exception as e:
      await context.bot.send_chat_action(chat_id=DEVELOPER_CHAT_ID,action='typing')
      await asyncio.sleep(message_action_delay)
      await context.bot.send_message(chat_id=update.effective_chat.id,text=f"Error: {e}", parse_mode=ParseMode.MARKDOWN)
    await msg_obj.reply_chat_action(action='typing')
    await asyncio.sleep(message_action_delay)
    await msg_obj.reply_text(output,parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
  else:
    if auth_result =="approved":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=AdminUsageOnly,parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="unapproved":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=ApprovalDesc , parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="banned":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=BanDesc, parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="request":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=UnapprovedDesc,  reply_markup= request_keyboard(msg_obj.chat_id),parse_mode=ParseMode.MARKDOWN)

# Handle video file
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  msg_obj = update.message if update.message else update.edited_message
  auth_result = auth_user(msg_obj.chat_id)
  if auth_result =="admin":
    try:
      file = msg_obj.video or msg_obj.document
      file_id = file.file_id
      size = file.file_size
      file_size = convert_size(size)
      caption = msg_obj.caption
      if not caption:
        raise Exception("Caption is required")
      caption = caption.split(",")
      cap=[]
      extra_title=''
      for i in caption:
        if i.isdigit():
            cap.append(int(i))
        else:
            extra_title = i
      if len(cap) < 2 or len(cap)==3 or len(cap) > 5:
        raise Exception("Invalid caption format")
      show_id,lang_id = cap[:2]
      db, conn = db_connection()
      conn.execute(f"SELECT lang_id,language FROM {languages} WHERE lang_id = %s",(lang_id,))
      lang_id, language =conn.fetchone()[:]
      conn.execute(f"SELECT title,series FROM {shows} WHERE show_id = %s",(show_id,))
      title,series_or_not=conn.fetchone()[0:]
      if len(cap) == 2:
        if not series_or_not:
          conn.execute(f"INSERT INTO {movie}(file_id,movie_id,movie_lang,size) VALUES (%s, %s, %s, %s)", (file_id,show_id,lang_id,file_size))
          output = f"*Movie : {title}\nLanguage : {language}\nSize: {file_size}*\nNew file has been added to the Movies database successfully."
        else:
          raise Exception("Not a movie format")
      elif len(cap) == 4 and extra_title !='':
        if series_or_not:
          season,resolution = cap[2:]
          extra_title = ''.join(extra_title.strip())
          conn.execute(f"SELECT pk from {extras} WHERE series_id=%s AND series_lang=%s AND season=%s AND resolution=%s AND LOWER(title)=%s", (show_id,lang_id,season,resolution,extra_title.lower(),))
          if conn.fetchone():
            raise Exception("A file to this extra episode already exists")
          else:
            conn.execute(f"INSERT INTO {extras}(file_id,series_id,series_lang,season,resolution,title) VALUES (%s, %s, %s,%s, %s, %s)", (file_id,show_id,lang_id,season,resolution,extra_title))
            output = f"*Series: {title}\nLanguage : {language}\nSeason: {season}\nResolution: {resolution}p\nExtras title: {extra_title}*\nNew file has been added to the Extras database successfully."
        else:
          raise Exception("Not a series extra format")
      elif len(cap) == 5:
        if series_or_not:
          season, episode, resolution = cap[2:]
          conn.execute(f"SELECT pk from {series} where series_id=%s AND  series_lang=%s AND season=%s AND resolution=%s AND episode=%s", (show_id,lang_id,season,resolution,episode))
          if conn.fetchone():
            raise Exception("A file to this episode already exists")
          else:
            conn.execute(f"INSERT INTO {series}(file_id,series_id,season,episode,series_lang,resolution) VALUES (%s, %s, %s,%s, %s, %s)", (file_id,show_id,season,episode,lang_id,resolution))
            output = f"*Series: {title}\nLanguage : {language}\nSeason: {season}\nEpisode: {episode}\nResolution: {resolution}p*\nNew file has been added to the Series database successfully."
        else:
          raise Exception("Not a series format")
      else:
        raise Exception("Unknown caption format of video file")
      db.commit()
      db.close()
    except Exception as e:
      await context.bot.send_chat_action(chat_id=DEVELOPER_CHAT_ID,action='typing')
      await asyncio.sleep(message_action_delay)
      await context.bot.send_message(chat_id=update.effective_chat.id,text=f"Error: {e}", parse_mode=ParseMode.MARKDOWN)
    else:
      await msg_obj.reply_chat_action(action='typing')
      await asyncio.sleep(message_action_delay)
      await msg_obj.reply_text(text = output,parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
  else:
    if auth_result =="approved":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=AdminUsageOnly,parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="unapproved":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=ApprovalDesc , parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="banned":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=BanDesc, parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="request":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=UnapprovedDesc,  reply_markup= request_keyboard(msg_obj.chat_id),parse_mode=ParseMode.MARKDOWN)

# File search
async def search_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  msg_obj = update.message if update.message else update.edited_message
  auth_result = auth_user(msg_obj.chat_id)
  if auth_result =="admin" or auth_result=="approved":
    titlequery = (msg_obj.text).lower()
    db, conn = db_connection()
    conn.execute(f"SELECT show_id FROM {shows} WHERE LOWER(title) = %s order by show_id", (titlequery,))
    result = conn.fetchall()
    db.close()
    if result:
      for i in range(len(result)):
        show_obj=AdminShowDetails(result[i][0])
        show_id = show_obj.show_id
        poster_id = show_obj.poster_id
        title = show_obj.title
        year = show_obj.year
        s_or_m = show_obj.s_or_m
        lang_list,markup = languages_keyboard(s_or_m,show_id)
        if len(lang_list)>0:
          language = ','.join(lang_list)
        else:
          language = 'Not Declared'
        await msg_obj.reply_chat_action(action='upload_photo')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_photo(reply_to_message_id=msg_obj.message_id, photo=poster_id, caption=f"*🎬 Title : {title}\n🗓 Year: {year}\n🔊 Language: {language}*\n",parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
    else:
      await msg_obj.reply_chat_action(action='typing')
      await asyncio.sleep(message_action_delay)
      await msg_obj.reply_text(reply_to_message_id=msg_obj.message_id, text='❌ Sorry ❌, No file found with that title in our database.')
      await context.bot.send_message(text=f"*The user requested a movie that wasn't part of database*\n\nUser: {msg_obj.from_user.first_name}\nTitle: *{msg_obj.text}*",chat_id=DEVELOPER_CHAT_ID, parse_mode=ParseMode.MARKDOWN)
  else:
    if auth_result=="unapproved":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=ApprovalDesc , parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="banned":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=BanDesc, parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="request":
        await msg_obj.reply_chat_action(action='typing')
        await asyncio.sleep(message_action_delay)
        await msg_obj.reply_text(text=UnapprovedDesc,  reply_markup= request_keyboard(msg_obj.chat_id),parse_mode=ParseMode.MARKDOWN)

# Handle user_1st_Inline query button - choose series resolution or movie size
async def user_1st_Inline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  query = update.callback_query
  auth_result = auth_user(query.message.chat_id)
  if auth_result =="admin" or auth_result=="approved":
    await query.answer()
    data = query.data
    page,show_id,lang_id = [int(i) for i in data.split(',')]
    if AdminShowDetails(show_id).s_or_m:
      markup = resolution_keyboard(0,show_id,lang_id)
    else :
      markup = filesize_keyboard(page, show_id, lang_id)
    await query.edit_message_reply_markup(reply_markup=markup)
  else:
    if auth_result=="unapproved":
        await query.message.reply_text(text=ApprovalDesc , parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="banned":
        await query.message.reply_text(text=BanDesc, parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="request":
        await query.message.reply_text(text=UnapprovedDesc,  reply_markup= request_keyboard(query.message.chat_id),parse_mode=ParseMode.MARKDOWN)

# Handle user_2nd_Inline query button - choose season or send movie file
async def user_2nd_Inline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  query = update.callback_query
  auth_result = auth_user(query.message.chat_id)
  if auth_result =="admin" or auth_result=="approved":
    query = update.callback_query
    await query.answer()
    data = query.data
    page ,show_id,lang_id,pk_or_resolution = [int(i) for i in data.split(',')]
    db,conn=db_connection()
    conn.execute(f"SELECT series FROM {shows} WHERE show_id= %s", (show_id,))
    series_or_not = conn.fetchone()[0]
    db.close()
    if series_or_not:
      markup = season_keyboard(page,show_id,lang_id,pk_or_resolution)
      await query.edit_message_reply_markup(reply_markup=markup)
    else :
      db,conn = db_connection()
      conn.execute(f"SELECT file_id FROM {movie} WHERE movie_id = %s AND movie_lang=%s AND pk=%s", (show_id,lang_id,pk_or_resolution))
      file_id =conn.fetchone()[0]
      await context.bot.send_chat_action(chat_id=query.message.chat_id,action='upload_document')
      await asyncio.sleep(message_action_delay)
      await context.bot.send_document(document=file_id, chat_id= query.message.chat_id,parse_mode=ParseMode.MARKDOWN)

      db.close()
  else:
    if auth_result=="unapproved":
        await query.message.reply_text(text=ApprovalDesc , parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="banned":
        await query.message.reply_text(text=BanDesc, parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="request":
        await query.message.reply_text(text=UnapprovedDesc,  reply_markup= request_keyboard(query.message.chat_id),parse_mode=ParseMode.MARKDOWN)

# Handle user_3rd_Inline query button - episode selection
async def user_3rd_Inline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  query = update.callback_query
  auth_result = auth_user(query.message.chat_id)
  if auth_result =="admin" or auth_result=="approved":
    query = update.callback_query
    await query.answer()
    data = query.data
    page,show_id,lang_id,resolution,season = [int(i) for i in data.split(',')]
    markup = episode_keyboard(page,show_id,lang_id,resolution,season)
    await query.edit_message_reply_markup(reply_markup=markup)
  else:
    if auth_result=="unapproved":
        await query.message.reply_text(text=ApprovalDesc , parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="banned":
        await query.message.reply_text(text=BanDesc, parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="request":
        await query.message.reply_text(text=UnapprovedDesc,  reply_markup= request_keyboard(query.message.chat_id),parse_mode=ParseMode.MARKDOWN)

# Handle user_4th_Inline query - send series file
async def user_4th_Inline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  query = update.callback_query
  auth_result = auth_user(query.message.chat_id)
  if auth_result =="admin" or auth_result=="approved":
    query = update.callback_query
    await query.answer()
    data = query.data
    db,conn = db_connection()
    series_or_not ,show_id,lang_id,resolution,season,episode_id = [int(i) for i in data.split(',')]
    conn.execute(f"SELECT file_id,episode FROM {series} WHERE series_id = %s AND series_lang=%s AND resolution=%s AND season = %s AND pk=%s order by episode asc", (show_id,lang_id,resolution,season,episode_id))
    file_id,episode =conn.fetchone()
    conn.execute(f"SELECT pk FROM {subtitles} WHERE show_id = %s AND season = %s AND episode=%s", (show_id,season,episode,))
    await context.bot.send_chat_action(chat_id=query.message.chat_id,action='upload_document')
    await asyncio.sleep(message_action_delay)
    if conn.fetchone():
      markup=subs_keyboard(1,show_id,season,episode)
      await context.bot.send_document(document=file_id, caption=f"*S{season} E{episode}*", chat_id= query.message.chat_id,parse_mode=ParseMode.MARKDOWN,reply_markup=markup)
    else:
      await context.bot.send_document(document=file_id, caption=f"*S{season} E{episode}*", chat_id= query.message.chat_id,parse_mode=ParseMode.MARKDOWN)
    db.close()
  else:
    if auth_result=="unapproved":
        await query.message.reply_text(text=ApprovalDesc , parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="banned":
        await query.message.reply_text(text=BanDesc, parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="request":
        await query.message.reply_text(text=UnapprovedDesc,  reply_markup= request_keyboard(query.message.chat_id),parse_mode=ParseMode.MARKDOWN)

# Handle user_5th_Inline query - send subtitles file
async def user_5th_Inline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  query = update.callback_query
  auth_result = auth_user(query.message.chat_id)
  if auth_result =="admin" or auth_result=="approved":
    query = update.callback_query
    await query.answer()
    action = query.data.split(':')[0]
    db,conn = db_connection()
    if action=='sublist':
      show_id = int(query.data.split(':')[1])
      await query.edit_message_reply_markup(subs_keyboard(0,show_id))
    elif action=='sub':
      sub_id = int(query.data.split(':')[1])
      conn.execute(f"SELECT file_id FROM {subtitles} WHERE pk = %s", (sub_id,))
      file_id =conn.fetchone()[0]
      await context.bot.send_chat_action(chat_id=query.message.chat_id,action='upload_document')
      await asyncio.sleep(message_action_delay)
      await context.bot.send_document(document=file_id, chat_id= query.message.chat_id,parse_mode=ParseMode.MARKDOWN)
    elif action=='extra_keyboard':
      data = query.data.split(':')[1]
      page,show_id,lang_id,resolution,season = [int(i) for i in data.split(',')]
      markup = extras_keyboard(page,show_id,lang_id,resolution,season)
      await query.edit_message_reply_markup(reply_markup=markup)
    elif action=='extra_send':
      extra_id = int(query.data.split(':')[1])
      conn.execute(f"SELECT file_id,title FROM {extras} WHERE pk = %s", (extra_id,))
      file_id,title =conn.fetchone()
      await context.bot.send_chat_action(chat_id=query.message.chat_id,action='upload_document')
      await asyncio.sleep(message_action_delay)
      await context.bot.send_document(document=file_id, caption=f"*Title : {title}*", chat_id= query.message.chat_id,parse_mode=ParseMode.MARKDOWN)
    db.close()
  else:
    if auth_result=="unapproved":
        await query.message.reply_text(text=ApprovalDesc , parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="banned":
        await query.message.reply_text(text=BanDesc, parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="request":
        await query.message.reply_text(text=UnapprovedDesc,  reply_markup= request_keyboard(query.message.chat_id),parse_mode=ParseMode.MARKDOWN)

# Handle user_Inline_Back query - back button
async def user_Inline_Back (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  query = update.callback_query
  auth_result = auth_user(query.message.chat_id)
  if auth_result =="admin" or auth_result=="approved":
    query = update.callback_query
    await query.answer()
    data = query.data.split(':')[1]
    queryList = [int(i) for i in data.split(',')]
    if len(queryList)==2:
      series_or_not,show_id = queryList
      markup = languages_keyboard(series_or_not,show_id)[1]
    elif len(queryList)==3:
      series_or_not,show_id,lang_id = queryList
      if series_or_not:
          markup = resolution_keyboard(series_or_not,show_id,lang_id)
      else :
        markup = filesize_keyboard(series_or_not, show_id, lang_id)
    elif len(queryList)==4:
      page,show_id,lang_id,pk_or_resolution = queryList
      markup = season_keyboard(page,show_id,lang_id,pk_or_resolution)
    elif len(queryList)==5:
      page,show_id,lang_id,resolution,season = queryList
      markup = episode_keyboard(page,show_id,lang_id,resolution,season)
    await query.edit_message_reply_markup(reply_markup=markup)
  else:
    if auth_result=="unapproved":
        await query.message.reply_text(text=ApprovalDesc , parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="banned":
        await query.message.reply_text(text=BanDesc, parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="request":
        await query.message.reply_text(text=UnapprovedDesc,  reply_markup= request_keyboard(query.message.chat_id),parse_mode=ParseMode.MARKDOWN)

# Handle invalid Button clicks.
async def invalidButton(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  auth_result = auth_user(query.message.chat_id)
  if auth_result =="admin" or auth_result=="approved":
    query = update.callback_query
    data = query.data
    if data == "empty":
      await context.bot.answer_callback_query(callback_query_id=query.id,text=f"You clicked an Invalid button",show_alert=True)
  else:
    if auth_result=="unapproved":
        await query.message.reply_text(text=ApprovalDesc , parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="banned":
        await query.message.reply_text(text=BanDesc, parse_mode=ParseMode.MARKDOWN)
    elif auth_result=="request":
        await query.message.reply_text(text=UnapprovedDesc,  reply_markup= request_keyboard(query.message.chat_id),parse_mode=ParseMode.MARKDOWN)

# Handle user_request_Inline query button - send request to admin
async def user_request_Inline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    queryList = query.data.split(':')
    action, query_chat_id = queryList[0],int(queryList[1])
    db,conn = db_connection()
    conn.execute(f"SELECT approved,ban FROM {users} WHERE user_id = %s", (query_chat_id,))
    row = conn.fetchone()
    if row:
      approved,ban  = [int(i) for i in row]
    if action=="request":
      if row:
        await context.bot.send_chat_action(chat_id=query_chat_id,action='typing')
        await asyncio.sleep(message_action_delay)
        await context.bot.send_message(text=ApprovalDesc,chat_id= query_chat_id,parse_mode=ParseMode.MARKDOWN)
      else:
        fname = query.message.from_user.first_name
        username = query.message.from_user.username
        username = username if username else "UNAVAILABLE"
        conn.execute(f"INSERT INTO {users}(user_id,fname,username) VALUES (%s,%s,%s)", (query_chat_id,fname,username))
        db.commit()
        tg_name = str(query.from_user.full_name)
        tg_username = query.from_user.username
        tg_username = str(tg_username) if tg_username else "Unavailable"
        tg_id = str(query_chat_id)
        request_msg = "*USER REQUEST\nName: "+tg_name+"\nUsername: "+tg_username+"\nTG-ID: "+tg_id+"*"
        await context.bot.send_chat_action(chat_id=DEVELOPER_CHAT_ID,action='upload_photo')
        await asyncio.sleep(message_action_delay)
        await context.bot.send_photo(photo=REQUEST_IMG_PATH,caption=request_msg, reply_markup= approval_keyboard(query_chat_id),chat_id= DEVELOPER_CHAT_ID,parse_mode=ParseMode.MARKDOWN)
        await context.bot.send_chat_action(chat_id=query_chat_id,action='typing')
        await asyncio.sleep(message_action_delay)
        await context.bot.send_message(text="*Request is sent,*"+ApprovalDesc,chat_id=query_chat_id, parse_mode=ParseMode.MARKDOWN)

    if action=="approve":
      conn.execute(f"UPDATE {users} SET approved=1 WHERE user_id=%s", (query_chat_id,))
      db.commit()
      await query.edit_message_reply_markup(approval_keyboard(query_chat_id))
      await context.bot.send_chat_action(chat_id=DEVELOPER_CHAT_ID,action='typing')
      await asyncio.sleep(message_action_delay)
      await context.bot.send_message(text="Request approved",chat_id=DEVELOPER_CHAT_ID,parse_mode=ParseMode.MARKDOWN)
      await context.bot.send_chat_action(chat_id=query_chat_id,action='typing')
      await asyncio.sleep(message_action_delay)
      await context.bot.send_message(text=ApprovedDesc,chat_id=query_chat_id,parse_mode=ParseMode.MARKDOWN)

    elif action=="ban":
      conn.execute(f"UPDATE {users} SET ban=1 WHERE user_id=%s", (query_chat_id,))
      db.commit()
      await query.edit_message_reply_markup(approval_keyboard(query_chat_id))
      await context.bot.send_chat_action(chat_id=DEVELOPER_CHAT_ID,action='typing')
      await asyncio.sleep(message_action_delay)
      await context.bot.send_message(text="User banned",chat_id=DEVELOPER_CHAT_ID,parse_mode=ParseMode.MARKDOWN)
      await context.bot.send_chat_action(chat_id=query_chat_id,action='typing')
      await asyncio.sleep(message_action_delay)
      await context.bot.send_message(text=BanDesc,chat_id=query_chat_id,parse_mode=ParseMode.MARKDOWN)

    elif action=="unban":
      conn.execute(f"UPDATE {users} SET ban=0 WHERE user_id=%s", (query_chat_id,))
      db.commit()
      await query.edit_message_reply_markup(approval_keyboard(query_chat_id))
      await context.bot.send_chat_action(chat_id=DEVELOPER_CHAT_ID,action='typing')
      await asyncio.sleep(message_action_delay)
      await context.bot.send_message(text="User Unbanned",chat_id=DEVELOPER_CHAT_ID,parse_mode=ParseMode.MARKDOWN)
      await context.bot.send_chat_action(chat_id=query_chat_id,action='typing')
      await asyncio.sleep(message_action_delay)
      await context.bot.send_message(text=UnbanDesc,chat_id=query_chat_id,parse_mode=ParseMode.MARKDOWN)

    elif action=="remove":
      conn.execute(f"DELETE FROM {users} WHERE user_id=%s", (query_chat_id,))
      db.commit()
      await query.edit_message_reply_markup(approval_keyboard(query_chat_id))
      await context.bot.send_chat_action(chat_id=DEVELOPER_CHAT_ID,action='typing')
      await asyncio.sleep(message_action_delay)
      await context.bot.send_message(text="User removed from database",chat_id=DEVELOPER_CHAT_ID,parse_mode=ParseMode.MARKDOWN)

    elif action=="delete":
      try:
        await context.bot.delete_message(chat_id=DEVELOPER_CHAT_ID, message_id=query.message.id)
      except Exception as e:
        await context.bot.send_chat_action(chat_id=DEVELOPER_CHAT_ID,action='typing')
        await asyncio.sleep(message_action_delay)
        await context.bot.send_message(text = f"*{e}*", chat_id=DEVELOPER_CHAT_ID,parse_mode=ParseMode.MARKDOWN)
    db.close()

# Main Loop

async def bot_tele(text):
  application = (Application.builder().token(API_KEY).build())

  # Handlers
  application.add_handler(CommandHandler("start", start_command))
  application.add_handler(CommandHandler("help", help_command))
  application.add_handler(CommandHandler("about", about_command))
  application.add_handler(CommandHandler("admin", admin_command))
  application.add_handler(CallbackQueryHandler(adminInline,pattern=r'^languages:\d+$'))
  application.add_handler(CallbackQueryHandler(adminInline,pattern=r'^user_list:\d+$'))
  application.add_handler(CallbackQueryHandler(adminInline,pattern=r'^view_user:\d+$'))

  application.add_handler(CommandHandler("addlang", addlang_command))

  application.add_handler(CommandHandler("broadcast", broadcast_command))
  application.add_handler(CallbackQueryHandler(broadcast_Inline,pattern=r'^broadcast:\d+,\d+$'))

  application.add_handler(CommandHandler("remfiles", remfiles_command))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^Main-Menu:\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^open-inner:\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^Movie-Subs:\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^Language:\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^Resolution:\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^Season:\d+,\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^Extra:\d+,\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^Episode:\d+,\d+,\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^rem-Show:\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^rem-Language:\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^rem-Filesize:\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^rem-Resolution:\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^rem-Season:\d+,\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^rem-Episode:\d+,\d+,\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^rem-Extra:\d+,\d+,\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^rem-Subtitle:\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^rem-Subtitle:\d+,\d+,\d+,\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^Yes-Show:\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^Yes-Language:\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^Yes-Filesize:\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^Yes-Resolution:\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^Yes-Season:\d+,\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^Yes-Episode:\d+,\d+,\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^Yes-Extra:\d+,\d+,\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^Yes-Subtitle:\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(manage_show_Inline,pattern=r'^Yes-Subtitle:\d+,\d+,\d+,\d+,\d+,\d+$'))

  application.add_handler(CallbackQueryHandler(user_request_Inline, pattern=r'^request:\d+$'))
  application.add_handler(CallbackQueryHandler(user_request_Inline, pattern=r'^remove:\d+$'))
  application.add_handler(CallbackQueryHandler(user_request_Inline, pattern=r'^approve:\d+$'))
  application.add_handler(CallbackQueryHandler(user_request_Inline, pattern=r'^ban:\d+$'))
  application.add_handler(CallbackQueryHandler(user_request_Inline, pattern=r'^unban:\d+$'))
  application.add_handler(CallbackQueryHandler(user_request_Inline, pattern=r'^delete:\d+$'))

  application.add_handler(MessageHandler(filters.TEXT , search_file))
  application.add_handler(MessageHandler(filters.PHOTO , handle_img))
  application.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))
  application.add_handler(MessageHandler(filters.Document.FileExtension('srt',case_sensitive=False) , handle_subtitle))

  application.add_handler(CallbackQueryHandler(user_1st_Inline, pattern=r'^\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(user_2nd_Inline, pattern=r'^\d+,\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(user_3rd_Inline, pattern=r'^\d+,\d+,\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(user_4th_Inline, pattern=r'^\d+,\d+,\d+,\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(user_5th_Inline, pattern=r'^sublist:\d+'))
  application.add_handler(CallbackQueryHandler(user_5th_Inline, pattern=r'^sub:\d+'))
  application.add_handler(CallbackQueryHandler(user_5th_Inline, pattern=r'^extra_keyboard:\d+,\d+,\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(user_5th_Inline, pattern=r'^extra_send:\d+$'))

  application.add_handler(CallbackQueryHandler(user_Inline_Back, pattern=r'^b:\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(user_Inline_Back, pattern=r'^b:\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(user_Inline_Back, pattern=r'^b:\d+,\d+,\d+,\d+$'))
  application.add_handler(CallbackQueryHandler(user_Inline_Back, pattern=r'^b:\d+,\d+,\d+,\d+,\d+$'))

  application.add_handler(CallbackQueryHandler(invalidButton,pattern="empty"))

  # Error handler
  application.add_error_handler(error_handler)
        
  # Update queue
  await application.update_queue.put(Update.de_json(data=text, bot=application.bot))
  
  #Start application
  async with application:
      await application.start()
      await application.stop()