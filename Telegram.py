from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Application, ApplicationBuilder, ContextTypes
from telegram.constants import ChatAction
import requests
import asyncio
import json
from time import sleep
import time
from googlenewscrape import scrapemain
import schedule
import _osx_support


TOKEN = ''
getTGURL = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
contain_info = ""

#requestGET = requests.get(getTGURL)
#print(requestGET.status_code)
#msg_info = requestGET.json()
chatid =  #msg_info.get("result",{})[0].get('message').get('chat',{})['id'] = 1692512416
#print(chatid)

def read_pendingupload():
    pendingfilepath = r"C:\Users\PC\Desktop\program\LMcrawler\latestnewssavejson\pendingupload.json"
    try:
        with open(pendingfilepath, 'r',encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        pendingfile=[{}]

def format_caption(title:str, url:str, link_text:str) -> str:
    """
    This function is to present the information in a more structural format.
    Return:
        title with bold, url replace by custom text from link_text.
    """
    return f"<b>🗞️🔥-- BREAKING NEWS!!</b>\n<b>🗞️⚡--{title}</b>\n<a href='{url}'>📰{link_text}📰</a>"


async def sendmsg(bot: Bot,chat_id:int, topic:str, article_url:str):
    """
    This is send message function through telegram
    """
    caption = format_caption(title=topic, url=article_url, link_text="Read this news article!")
    await bot.send_message(chat_id=chatid, text=caption, parse_mode='HTML')


def splitcontain(contain_info:str):
    websource= contain_info.get("websource")
    topic=contain_info.get("topic")
    url = contain_info.get("url")
    return websource, topic, url

async def telegrammain():
    """
    This function is to send the information from pendingupload.json to user through telegram
    
    After the information is done upload to telegram, the new in pendingupload.json will move to latestnews.json before empty to ensure no repetitive news upload to users.
    """
    chat_id = chatid
    articles = read_pendingupload()
    bot = Bot(token=TOKEN)
    uploadfile = []
    
    if not articles:
        print('No new news from yesterday.')
    else:
        for idx,article in enumerate(articles):
            if idx<=5: 
                websource, topic, article_url = splitcontain(article)
                await bot.send_chat_action(chat_id, action=ChatAction.TYPING)
                sleep(2)
                await sendmsg(bot, chat_id, topic, article_url)             
                uploadfile.append(article)
        print(f"Total of {len(articles)} news done upload to chatid:{chatid}") 
        uploadfile.extend(read_pendingupload())
        ##update content in latestnews document
        with open(r"C:\Users\PC\Desktop\program\LMcrawler\latestnewssavejson\latestnews.json", 'w', encoding='utf-8') as outfile:
            json.dump(uploadfile, outfile, indent=2, ensure_ascii=False) 
        
        with open(r"C:\Users\PC\Desktop\program\LMcrawler\latestnewssavejson\pendingupload.json", 'w',encoding='utf-8') as f:
            json.dump([],f)  

def main():
    scrapemain()
    print(f"Your every 8am Breaking News")
    asyncio.run(telegrammain()) 

schedule.every().day.at("08:00").do(main)


while True:
    schedule.run_pending()

    time.sleep(1)
