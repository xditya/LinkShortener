# < (c) @xditya >
# This file is a part of LinkShortener < https://github.com/xditya/LinkShortener >

import logging
from decouple import config
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputTextMessageContent,
    InlineQueryResultArticle,
)
import requests

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)

bottoken = None

# start the bot
print("Starting...")
try:
    bottoken = config("BOT_TOKEN")
except:
    print("Environment vars are missing! Kindly recheck.")
    print("Bot is quiting...")
    exit()

if bottoken != None:
    try:
        app = Client(
            "bot",
            api_id=6,
            api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
            bot_token=bottoken,
        )
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


@app.on_message(filters.command("start") & filters.private)
async def start_message(_, message):
    await send_start(message)


@app.on_message(filters.command("start xx") & filters.private)
async def start_message_scam(_, message):
    await send_start(message)


@app.on_message(filters.private)
async def shorten(_, message):
    url = message.text
    if url.startswith("/"):
        return  # ignore commands.
    await message.reply_text(
        "Choose the shortening service.",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("is.gd", callback_data=f"i_{url}")],
                [InlineKeyboardButton("da.gd", callback_data=f"d_{url}")],
            ]
        ),
    )


@app.on_callback_query(filters.regex("i_(.*)"))
async def shrt_is(_, update):
    url = update.data.split("_")[1]
    await update.answer("Please wait...")
    shrt = link_shortener(url)
    await update.message.edit(f"**Shortened!**\n{shrt}")


@app.on_callback_query(filters.regex("d_(.*)"))
async def shrt_da(_, update):
    url = update.data.split("_")[1]
    await update.answer("Please wait...")
    shrt = dagd_shrt(url)
    await update.message.edit(f"**Shortened!**\n{shrt}")


@app.on_callback_query(filters.regex("help"))
async def help_me(_, update):
    await update.message.edit(
        "**URL Shortener.**\n\nSend me any URL and I'll shorten it for you!\nJoin @BotzHub if you liked this bot!",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Go Inline",
                        switch_inline_query_current_chat="https://youtube.com/xditya",
                    )
                ],
                [InlineKeyboardButton("« Back", callback_data="bck")],
            ]
        ),
    )


@app.on_callback_query(filters.regex("bck"))
async def backk(_, update):
    user = update.from_user.mention
    await update.message.edit(
        f"Hi {user}! Welcome to my bot.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Channel", url="https://t.me/BotzHub"),
                    InlineKeyboardButton("Help", callback_data="help"),
                ]
            ]
        ),
    )


@app.on_inline_query()
async def query_ans(client, query):
    if query.query == "":
        await client.answer_inline_query(
            query.id,
            results=[],
            cache_time=0,
            switch_pm_text="Enter a URL",
            switch_pm_parameter="xx",
        )
    else:
        url = query.query
        shrt = link_shortener(url)
        da_shrt = dagd_shrt(url)
        await client.answer_inline_query(
            query.id,
            results=[
                InlineQueryResultArticle(
                    title="is.gd",
                    description=shrt,
                    input_message_content=InputTextMessageContent(shrt),
                ),
                InlineQueryResultArticle(
                    title="da.gd",
                    description=da_shrt,
                    input_message_content=InputTextMessageContent(da_shrt),
                ),
            ],
            cache_time=0,
            switch_pm_text="Shortened!",
            switch_pm_parameter="xx",
        )


async def send_start(message):
    user = message.from_user.mention
    await message.reply_text(
        f"Hi {user}! Welcome to my bot.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Channel", url="https://t.me/BotzHub"),
                    InlineKeyboardButton("Help", callback_data="help"),
                ]
            ]
        ),
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


app.set_parse_mode("markdown")
print("Started.")
app.run()
