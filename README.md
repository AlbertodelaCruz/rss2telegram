# 📨 rss2telegram

Rss2Telegram gets publication info from several sources (blog and twitter) and push them to Telegram.
Its main purpose is to keep parents updated with school feeds in a unique interface like Telegram. 

## 🧾 What do you need
Rss2Telegram uses .env files to retrieve setting information. To get a full feature app, you need to configure these settings:

### Telegram config
- BOT_TOKEN
- BOT_CHATID

### Blog config
- BLOG_URL 
- FEED_TAGS 

### Twitter config
- TWITTER_API_KEY
- TWITTER_API_SECRET
- TWITTER_ACCESS_TOKEN
- TWITTER_ACCESS_SECRET
- TWITTER_ACCOUNT

### File config (it saves last publication datetime in order to keep track)
- LAST_ENTRY_FILE_PATH