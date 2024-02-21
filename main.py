from telethon import TelegramClient, events, sync
import asyncio
from loguru import logger


enter_main_channel = input("Введите канал куда отправлять сообщения: ")


a = 0
tg_list = []
tg_keywords = []

async def read_tg_channels():
    global a
    global tg_list
    b = 0
    while b != 1:
        try:
            with open('tg_channels.txt', 'r') as tg:
                line = tg.readlines()[a].strip()
            a += 1
            tg_list.append(line)
        except Exception as E:
            print(E)
            b = 1

async def read_keywords():
    global a
    global tg_keywords
    a = 0
    b = 0
    while b != 1:
        try:
            with open('keywords.txt', 'r') as tg:
                line = tg.readlines()[a].strip()
            a += 1
            tg_keywords.append(line)
        except:
            b = 1

asyncio.run(read_tg_channels())

logger.success("Каналы загружены -->  " + str(tg_list))

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

asyncio.run(read_keywords())

logger.success("Ключи загружены -->  " + str(tg_keywords))

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


messages = []
#ДАННЫЕ БРАТЬ С My.telegram.org
api_id = 0 #api_id (int)
api_hash = '' # api hash (str)
client = TelegramClient('+7...', api_id, api_hash)

logger.success("Начинаю монииторинг сообщений в чатах...")

@client.on(events.NewMessage(chats=tg_list))
async def my_event_handler(event):
    logger.success("Нашел новое сообщение")
    await client.download_media(event.media, "hui.png")
    await create_message(event.raw_text, event.media, event.chat.title)


async def create_message(message, check_media, chat_title):
    try:
        if message != None and check_media == None:
            if 't.me' not in message:
                for key in tg_keywords:
                    if key.lower() in message.lower():
                        await client.send_message(enter_main_channel, 'Key: ' + str(key) + '\n' + 'Chat: ' + str(chat_title) + '\n\n' + str(message))
                        break
        elif message == None and check_media != None:
            await client.send_file(enter_main_channel, 'hui.png')
        elif message != None and check_media != None:
                for key in tg_keywords:
                    if key.lower() in message.lower():
                        await client.send_message(enter_main_channel, 'Key: ' + str(key) + '\n' + 'Chat: ' + str(chat_title) + '\n\n' + str(message))
                        break
    except Exception as E:
        print(E)
        pass



client.start()

client.run_until_disconnected()