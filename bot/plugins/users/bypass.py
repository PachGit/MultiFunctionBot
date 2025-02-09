import datetime
from re import search
from time import sleep, time

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from bot.config import *
from bot.helpers.database import DatabaseHelper
from bot.helpers.decorators import user_commands
from bot.helpers.functions import forcesub, get_readable_time
from bot.logging import LOGGER
from bot.modules import bypasser
from bot.modules.lists import *
from bot.modules.regex import *

prefixes = COMMAND_PREFIXES
commands = ["bypass", f"bypass@{BOT_USERNAME}"]


@Client.on_message(filters.command(commands, **prefixes))
@user_commands
async def bypass(client, message: Message):
    """
    Bypass Various Supported Shortened URLs
    """
    global link_type
    fsub = await forcesub(client, message)
    if not fsub:
        return
    msg_arg = message.text.replace("  ", " ")
    msg_args = msg_arg.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    cmd = ""
    url = ""
    if len(msg_args) > 1:
        if len(message.command) != 2:
            await message.reply_text("Sorry, Could not understand your Input!")
            return
        cmd = msg_args[0]
        url = msg_args[1]
    elif reply_to is not None:
        try:
            reply_text = search(URL_REGEX, reply_to.text)[0]
        except BaseException:
            reply_text = (
                search(URL_REGEX, reply_to.caption.markdown)[0]
                .replace("\\", "")
                .split("*")[0]
            )
        url = reply_text.strip()
        cmd = msg_args[0]
    elif message.command == (0 or 1) or reply_to is None:
        err = "<b><i>Please send a URL or reply to an URL to proceed!</i></b>"
        await message.reply_text(text=err, disable_web_page_preview=True, quote=True)
        return

    valid_url = is_a_url(url)
    if valid_url is not True:
        err = "<b><i>You did not seem to have entered a valid URL!</i></b>"
        await message.reply_text(text=err, disable_web_page_preview=True, quote=True)
        return

    uname = message.from_user.mention
    uid = f"<code>{message.from_user.id}</code>"
    user_id = message.from_user.id
    if not await DatabaseHelper().is_user_exist(user_id):
        await DatabaseHelper().add_user(user_id)
        try:
            join_dt = await DatabaseHelper().get_bot_started_on(user_id)
            msg = f"<i>A New User has started the Bot: {message.from_user.mention}.</i>\n\n<b>Join Time</b>: {join_dt}"
            await client.send_message(
                chat_id=LOG_CHANNEL,
                text=msg,
                parse_mode=enums.ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except Exception as err:
            LOGGER(__name__).error(f"BOT Log Channel Error: {err}")
    last_used_on = await DatabaseHelper().get_last_used_on(user_id)
    if last_used_on != datetime.date.today().isoformat():
        await DatabaseHelper().update_last_used_on(user_id)
    start = time()
    msg_text = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Processing your URL.....</b>"
    msg = await message.reply_text(
        text=msg_text, disable_web_page_preview=True, quote=True
    )
    sleep(1)
    if "adrinolinks." in url:
        link_type = "AdrinoLinks"
        res = bypasser.adrinolinks(url)
    elif "droplink." in url or "droplinks." in url:
        link_type = "DropLinks"
        res = bypasser.droplink(url)
    elif "dulink." in url:
        link_type = "Dulink"
        res = bypasser.dulink(url)
    elif "ez4short." in url:
        res = bypasser.ez4short(url)
    elif "gplink." in url or "gplinks." in url:
        link_type = "GPLinks"
        res = bypasser.gplinks(url)
    elif "krownlinks." in url:
        res = bypasser.krownlinks(url)
    elif any(x in url for x in linkvertise_list):
        link_type = "Linkvertise"
        res = bypasser.linkvertise(url)
    elif any(x in url for x in adfly_list):
        link_type = "AdFly"
        res = bypasser.adfly(url)
    elif "gyanilinks." in url or "gyanilink" in url:
        link_type = "GyaniLinks"
        res = bypasser.gyanilinks(url)
    elif "htpmovies." in url and "/exit.php?url" in url:
        link_type = "HTPMovies GDL"
        res = bypasser.htpmovies(url)
    elif "privatemoviez." in url and "/secret?data=" in url:
        link_type = "PrivateMoviez DL"
        res = bypasser.privatemoviez(url)
    elif "hypershort." in url:
        link_type = "HyperShort"
        res = bypasser.hypershort(url)
    elif "sirigan.my.id" in url:
        link_type = "Sirigan.my.id"
        res = bypasser.sirigan(url)
    elif "ouo.io" in url or "ouo.press" in url:
        link_type = "Ouo"
        res = bypasser.ouo(url)
    elif any(x in url for x in shst_list):
        link_type = "Shorte.st"
        res = bypasser.shorte(url)
    elif "rocklinks." in url:
        link_type = "RockLinks"
        res = bypasser.rocklinks(url)
    elif ("gtlinks." or "loan.kinemaster.cc/?token=" or "theforyou.in/?token=") in url:
        url = url.replace("&m=1", "")
        link_type = "GTLinks"
        res = bypasser.gtlinks(url)
    elif "gyanilinks." in url:
        link_type = "GyaniLinks"
        res = bypasser.gyanilinks(url)
    elif "shareus." in url:
        link_type = "Shareus"
        res = bypasser.shareus(url)
    elif "short2url." in url:
        link_type = "Short2url"
        res = bypasser.short2url(url)
    elif "shortingly." in url:
        link_type = "Shortingly"
        res = bypasser.shortingly(url)
    elif "tnlink." in url:
        link_type = "TnLink"
        res = bypasser.tnlink(url)
    elif "xpshort." in url:
        link_type = "XpShort"
        res = bypasser.xpshort(url)
    elif any(x in url for x in yandisk_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Direct Link Generator</b>\n\n<i>Use it with /direct command followed by Link</i>"
        await msg.edit(text=err)
        return
    elif any(x in url for x in fmed_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Direct Link Generator</b>\n\n<i>Use it with /direct command followed by Link</i>"
        await msg.edit(text=err)
        return
    elif any(x in url for x in sbembed_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Direct Link Generator</b>\n\n<i>Use it with /direct command followed by Link</i>"
        await msg.edit(text=err)
        return
    elif any(x in url for x in directdl_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Direct Link Generator</b>\n\n<i>Use it with /direct command followed by Link</i>"
        await msg.edit(text=err)
        return
    elif any(x in url for x in scrape_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Site Scraper</b>\n\n<i>Use it with /scrape command followed by Link</i>"
        await msg.edit(text=err)
        return
    else:
        try:
            link_type = "Script Generic"
            res = bypasser.script(url)
        except BaseException:
            err = "<b><i>Could not find Bypass for your URL!</i></b>"
            await msg.edit(text=err)
            return
    LOGGER(__name__).info(f" Received : {cmd} - {link_type} - {url}")
    abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n<b>Link Type</b> : <i>{link_type}</i>"
    await msg.edit(text=abc)
    sleep(1)
    time_taken = get_readable_time(time() - start)
    LOGGER(__name__).info(f" Destination : {cmd} - {res}")
    xyz = f"<b>Bypassed Result :\n</b>{res}\n\n<i>Time Taken : {time_taken}</i>"
    await message.reply_text(text=xyz, disable_web_page_preview=True, quote=True)
    try:
        msg = f"<b><i>User:</i></b> {uid}\n<i>User URL:</i> {url}\n<i>Destination URL:</i> {res}\n\n<b><i>Time Taken:</i></b> {time_taken}"
        await client.send_message(
            chat_id=LOG_CHANNEL,
            text=msg,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True,
        )
    except Exception as err:
        LOGGER(__name__).error(f"BOT Log Channel Error: {err}")
