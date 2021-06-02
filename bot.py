# < (c) @xditya >
# This file is a part of LinkShortener < https://github.com/xditya/LinkShortener >

import logging
from telethon import TelegramClient, events, Button
from decouple import config
from requests import get

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


@BotzHub.on(events.NewMessage(incoming=True, pattern="^/start"))
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
    await event.reply(link_shortener(event.text))


@BotzHub.on(events.InlineQuery)
async def in_q(event):
    if len(event.text) == 0:
        await event.answer(
            [], switch_pm="Enter a URL to shorten it.", switch_pm_param="xx"
        )
    else:
        await event.answer(
            [
                await event.builder.article(
                    title="Click Here.",
                    description=link_shortener(event.text),
                    text=link_shortener(event.text),
                )
            ],
            switch_pm="Shortener",
            switch_pm_param="xx",
        )


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
    return get(req_).text


print("Bot has started.")
print("Do visit @BotzHub..")
BotzHub.run_until_disconnected()
