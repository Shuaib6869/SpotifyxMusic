import asyncio

from pyrogram.types import Message

from Userbot import Userbot
from Userbot.utils import command, send, sudo_filter
from Userbot.utils.helpers import ReplyCheck

__mod_name__ = "Mᴜsɪᴄ"

__alt_name__ = [
    "music",
    "inline",
    "song",
]

__help__ = """
<b>Cᴏᴍᴍᴀɴᴅs :</b>
๏ .music ᴏʀ song sᴏɴɢ ɴᴀᴍᴇ : get a Song 
"""

"""
@Userbot.on_message(command("play") & sudo_filter)
async def play_music(bot: Userbot, m: Message):
    hmm = await send(m=m, text="<code>Processing....</code>")
    await hmm.edit(
        "[ᴛʀʏ](https://t.me/KristineMusicBot?startgroup=True&admin=delete_messages+invite_users) : @SpotifyxmusicBot",
        disable_web_page_preview=True,
    )
    return
"""


@Userbot.on_message(command(["song", "music"]) & sudo_filter)
async def send_music(bot: Userbot, message: Message):
    try:
        cmd = message.command
        hmm = await send(m=message, text="<code>Processing....</code>")

        song_name = ""
        if len(cmd) > 1:
            song_name = " ".join(cmd[1:])
        elif message.reply_to_message and len(cmd) == 1:
            song_name = (
                message.reply_to_message.text or message.reply_to_message.caption
            )
        elif not message.reply_to_message and len(cmd) == 1:
            await hmm.edit("Give me song name")
            await asyncio.sleep(2)
            await message.delete()
            return

        song_results = await bot.get_inline_bot_results("deezermusicbot", song_name)

        try:
            # send to Saved Messages because hide_via doesn't work sometimes
            saved = await bot.send_inline_bot_result(
                chat_id="me",
                query_id=song_results.query_id,
                result_id=song_results.results[0].id,
            )

            # forward as a new message from Saved Messages
            saved = await bot.get_messages("me", int(saved.updates[1].message.id))
            reply_to = message.reply_to_message.id if message.reply_to_message else None
            await bot.send_audio(
                chat_id=message.chat.id,
                audio=str(saved.audio.file_id),
                reply_to_message_id=ReplyCheck(message),
            )

            # delete the message from Saved Messages
            await bot.delete_messages("me", saved.id)
        except TimeoutError:
            await hmm.edit("That didn't work out")
            await asyncio.sleep(2)
        await message.delete()
    except Exception as e:
        await hmm.edit(f"`Failed to find song` \n\n{e}")
        await asyncio.sleep(2)
        await message.delete()
