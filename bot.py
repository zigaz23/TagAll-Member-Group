from telegraph import upload_file
from telethon import Button
import os, logging, asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.errors import UserNotParticipantError
from telethon.tl import types
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
DB_URL = os.environ.get("DB_URL")
ADMINS = int(os.environ.get("ADMINS"))
ribot = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)


moment_worker = []


#start
@ribot.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("👏 Hallo!!, Selamat datang di menu bantuan mention bot\nSaya dapat menge Tag all seluruh anggota member di group,dan anggota member di saluran channel.\nButuh bantuan? /help ",
                    buttons=(
                      [
                         Button.url('✨ 𝙼𝚊𝚗𝚊𝚐𝚎 𝚋𝚢 ✨', 'https://t.me/SilenceSpe4ks'), 
                         Button.url('🔥 𝚂𝚞𝚙𝚙𝚘𝚛𝚝 𝚋𝚢 🔥', 'https://t.me/SharingUserbot'), 
                      ], 
                      [
                        Button.url('➕ 𝙰𝙳𝙳 𝙼𝙴 𝚃𝙾 𝚈𝙾𝚄𝚁 𝙶𝚁𝙾𝚄𝙿𝚂 ➕ ', 'https://t.me/MEMBER_TAGERBOT?startgroup=true'),   
                      ]
                   ), 
                    link_preview=False
                   )

#help
@ribot.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Tag Help Bot's Help Menu**\n\nCommand: @all \n Anda dapat menggunakan perintah ini dengan teks yang ingin Anda beri tahu pada orang lain \n`Contoh: @all Good morning!` \nAtau Anda dapat menggunakan perintah ini sebagai jawaban,Dan Bot akan menandai pengguna untuk membalas pesan"
  await event.reply(helptext,
                    buttons=(
                      [
                         Button.url('✨ 𝙼𝚊𝚗𝚊𝚐𝚎 𝚋𝚢✨', 'https://t.me/SilenceSpe4ks'), 
                         Button.url('🔥 𝚂𝚞𝚙𝚙𝚘𝚛𝚝 𝚋𝚢 🔥', 'https://t.me/SharingUserbot'), 
                      ], 
                      [
                        Button.url('➕ 𝙰𝙳𝙳 𝙼𝙴 𝚃𝙾 𝚈𝙾𝚄𝚁 𝙶𝚁𝙾𝚄𝙿𝚂 ➕ ', 'https://t.me/MEMBER_TAGERBOT?startgroup=true'),   
                      ]
                   ), 
                    link_preview=False
                   )

# command atau perintah

#tag
@ribot.on(events.NewMessage(pattern="^/tagall|/call|/tall|/all|#all|@all?(.*)"))
async def mentionall(event):
  global moment_worker
  if event.is_private:
    return await event.respond("Gunakan perintah ini di channel atau di group Goblog!")
  
  admins = []
  async for admin in ribot.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("Hanya admin yang bisa menggunakannya.")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("Saya tidak bisa menyebutkan anggota untuk posting lama!")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("Berikan saya argumentasi. Contoh: `/tag Naik, Ada giveaway !!`")
  else:
    return await event.respond("Balas ke pesan atau berikan beberapa teks untuk disebutkan pada member!")
    
  if mode == "text_on_cmd":
    moment_worker.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in ribot.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in moment_worker:
        await event.respond("MentionAll Berhasil di cancel!")
        return
      if usrnum == 5:
        await ribot.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    moment_worker.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in ribot.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in moment_worker:
        await event.respond("MentionAll Berhasil di cancel!")
        return
      if usrnum == 5:
        await ribot.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


# Cancel
@ribot.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
    is_admin = False
    try:
        partici_ = await ribot(GetParticipantRequest(
            event.chat_id,
            event.sender_id
        ))
    except UserNotParticipantError:
        is_admin = False
    else:
        if (
                isinstance(
                    partici_.participant,
                    (
                            ChannelParticipantAdmin,
                            ChannelParticipantCreator
                    )
                )
        ):
            is_admin = True
    if not is_admin:
        return await event.reply("__Hanya admin yang dapat menjalankan perintah ini!__")
    if not event.chat_id in moment_worker:
        return await event.reply("__Tidak ada proses yang berjalan...__")
    else:
        try:
            moment_worker.remove(event.chat_id)
        except:
            pass
        return await event.respond('**__Mention all berhenti__**\n\n**__Manage By:__ @SilenceSpe4ks ☕**')


print("🔥 Bot berhasil di aktifkan 🔥")
print("Butuh bantuan? Silahkan chat @SilenceSpe4ks ☕")
ribot.run_until_disconnected()
