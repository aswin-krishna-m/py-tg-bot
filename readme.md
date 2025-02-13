# Django based Telegram Bot

## Environment variables

**WEBHOOK_HOST** hostname without https:// and /webhook endpoint
**API_KEY** Bot API
**DEVELOPER_CHAT_ID** Your TG ID
**host** DB host
**user** DB username
**password** DB Password
**database** DB Name
**port** DB Port

This Telegram bot allows users to add files to a database and retrieve them by their titles. 
Here's an overview of its features and usage instructions:

## Features

- **File Management:**
  - Admins can add files to the bot's database.
  - Users can request files by their titles.
  
- **Admin Controls:**
  - Admins have the following additional privileges:
    - Remove files from the database.
    - Remove users.
    - Ban users if necessary.

- **User Interaction:**
  - Users can only request files and do not have access to administrative functions.

- **Group Chat Limitation:**
  - This bot is designed for use in individual chats, not group chats.

## Notes

- Ensure that all commands are entered in the bot's private chat with the user. It can't be part of a group.
- For security reasons, avoid sharing administrative privileges with unauthorized users.
- Should be used for smaller circles or keeping files personally. Always obey copyright laws while handling such files.

---
