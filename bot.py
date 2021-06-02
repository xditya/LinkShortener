# < (c) @xditya >
# This file is a part of LinkShortener < https://github.com/xditya/LinkShortener >

import logging
from telethon import TelegramClient, events, Button
from decouple import config
import requests
from telethon.errors.rpcerrorlist import QueryIdInvalidError
import re

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.INFO
)

bottoken = None
# start the bot
print("Starting...")
apiid = 6
apihash = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
try:
    bottoken = config("BOT_TOKEN")
except:
    print("Environment vars are missing! Kindly recheck.")
    print("Bot is quiting...")
    exit()

if bottoken != None:
    try:
        BotzHub = TelegramClient("bot", apiid, apihash).start(bot_token=bottoken)
    except Exception as e:
        print(f"ERROR!\n{str(e)}")
        print("Bot is quiting...")
        exit()
else:
    print("Environment vars are missing! Kindly recheck.")
    print("Bot is quiting...")
    exit()

base_url = "https://is.gd/create.php?format=simple&url="
dagd_url = "https://da.gd/s?url="

@BotzHub.on(events.NewMessage(incoming=True, pattern="^/start$"))
async def msgg(event):
    await send_start(event, "msg")


@BotzHub.on(events.NewMessage(incoming=True, pattern="^/start xx"))
async def msgg(event):
    await send_start(event, "msg")


@BotzHub.on(events.callbackquery.CallbackQuery(data="help"))
async def send_help(event):
    await event.edit(
        "**URL Shortener.**\n\nSend me any URL and I'll shorten it for you!\nJoin @BotzHub if you liked this bot!",
        buttons=[
            [Button.switch_inline("Go Inline", query="", same_peer=True)],
            [Button.inline("« Back", data="bck")],
        ],
    )


@BotzHub.on(events.callbackquery.CallbackQuery(data="bck"))
async def bk(event):
    await send_start(event, "")


@BotzHub.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def fn_(event):
    if event.text.startswith("/"):
        return  # ignore commands.
    await event.reply(
        "Select the shortenert service.",
        buttons=[
            Button.inline("is.gd", data=f"i_{event.text}"),
            Button.inline("da.gd", data=f"d_{event.text}")
        ])

@BotzHub.on(events.callbackquery.CallbackQuery(data=re.compile(b"i_(.*)")))
async def in_pl(event):
    await event.answer("Processing...")
    tmp = event.data_match.group(1).decode("UTF-8")
    return await event.edit(link_shortener(tmp))


@BotzHub.on(events.callbackquery.CallbackQuery(data=re.compile(b"d_(.*)")))
async def in_pl(event):
    await event.answer("Processing...")
    tmp = event.data_match.group(1).decode("UTF-8")
    return await event.edit(dagd_shrt(tmp))


@BotzHub.on(events.InlineQuery)
async def in_q(event):
    if len(event.text) == 0:
        await event.answer(
            [], switch_pm="Enter a URL to shorten it.", switch_pm_param="xx"
        )
    else:
        try:
            await event.answer(
                [
                    await event.builder.article(
                        title="is.gd shortener.",
                        description=link_shortener(event.text),
                        text=link_shortener(event.text),
                    ),
                    await event.builder.article(
                        title="da.gd shortener.",
                        description=dagd_shrt(event.text),
                        text=dagd_shrt(event.text),
                    ),
                ],
                switch_pm="Shortener",
                switch_pm_param="xx",
            )
        except QueryIdInvalidError:
            await event.answer([], switch_pm="Busy. Please try again.", switch_pm_param="xx")

buttons = [
    [Button.inline("Help", data="help")],
    [
        Button.url("Channel", url="t.me/BotzHub"),
        Button.url("Source", url="https://github.com/xditya/LinkShortener"),
    ],
]


async def send_start(event, mode):
    user_ = await BotzHub.get_entity(event.sender_id)
    if mode == "msg":
        await event.reply(
            f"Hi {user_.first_name}.\n\nI am a URL shortener bot!", buttons=buttons
        )
    else:
        await event.edit(
            f"Hi {user_.first_name}.\n\nI am a URL shortener bot!", buttons=buttons
        )


def link_shortener(url):
    req_ = f"{base_url}{url}"
    try:
        requests.get(req_)
    except requests.exceptions.ConnectionError:
        return "Invalid URL!"
    return requests.get(req_).text


def dagd_shrt(url):
    if not (url.startswith("http://") or url.startswith("https://")):
        r = f"http://{url}"
    else:
        r = url
    try:
        requests.get(r)
    except requests.exceptions.ConnectionError:
        return "Invalid URL!"
    tmp = requests.get(f"{dagd_url}{r}").text
    if tmp:
        return tmp
    else:
        return "404. Not Available."

print("Bot has started.")
print("Do visit @BotzHub..")
BotzHub.run_until_disconnected()
