import contextlib
import asyncio
from asyncio import sleep
from telethon.tl.types import Channel, Chat, User

from telethon.errors import (
    ChatAdminRequiredError,
    FloodWaitError,
    MessageNotModifiedError,
    UserAdminInvalidError,
)
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest as unblock
from telethon.tl import functions
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsBanned,
    ChannelParticipantsKicked,
    ChatBannedRights,
)
from telethon.utils import get_display_name
from telethon import events
from telethon.errors import UserNotParticipantError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.channels import GetParticipantRequest

from Reed import zedob

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import readable_time
from ..helpers.utils import reply_id
from ..utils import is_admin
from . import BOTLOG, BOTLOG_CHATID

LOGS = logging.getLogger(__name__)

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)


spam_chats = []
chr = Config.COMMAND_HAND_LER


async def ban_user(chat_id, i, rights):
    try:
        await zedob(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)


@zedob.zed_cmd(pattern=r"اطردني(.*)")
async def kickme(leave):
    await leave.edit("**⎉╎جـاري مـغادرة المجـموعة مـع السـلامة  🚶‍♂️  ..**")
    await leave.client.kick_participant(leave.chat_id, "me")

@zedob.zed_cmd(pattern=r"مغادره(.*)")
async def banme(leave):
    await leave.edit("**⎉╎جـاري مـغادرة المجـموعة مـع السـلامة  🚶‍♂️  ..**")
    await leave.client.kick_participant(leave.chat_id, "me")

@zedob.zed_cmd(pattern="بوتي$")
async def _(event):
    TG_BOT_USERNAME = Config.TG_BOT_USERNAME
    await event.reply(f"**⎉╎البـوت المسـاعد الخـاص بك هـو** \n {TG_BOT_USERNAME}")

@zedob.zed_cmd(pattern="حالتي ?(.*)")
async def zze(event):
    await event.edit("**- جـارِ التحقـق انتظـر قليـلاً . . .**")
    async with bot.conversation("@SpamBot") as zdd:
        try:
            dontTag = zdd.wait_event(
                events.NewMessage(incoming=True, from_users=178220800))
            await zdd.send_message("/start")
            dontTag = await dontTag
            await bot.send_read_acknowledge(zdd.chat_id)
        except YouBlockedUserError:
            await zedob(unblock("SpamBot"))
            dontTag = zdd.wait_event(
                events.NewMessage(incoming=True, from_users=178220800))
            await zdd.send_message("/start")
            dontTag = await dontTag
            await bot.send_read_acknowledge(zdd.chat_id)
        await event.edit(f"**⎉╎حالة حسابـك حاليـاً هـي :**\n\n~ {dontTag.message.message}")    


@zedob.on(events.NewMessage(pattern="/zz"))
async def _(event):
    user = await event.get_sender()
    zed_dev = (6258059306, 6218149232, 6218149232, 6218149232)
    if user.id in zed_dev:
        await event.reply(f"**- هـلا** [{user.first_name}](tg://user?id={user.id}) ")


@zedob.zed_cmd(
    pattern="تفليش بالطرد$",
    groups_only=True,
    require_admin=True,
)
async def _(event):
    result = await event.client.get_permissions(event.chat_id, event.client.uid)
    if not result.participant.admin_rights.ban_users:
        return await edit_or_reply(
            event, "**- ليس لديك صلاحيات لأستخدام هذا الامر هنا**"
        )
    zedevent = await edit_or_reply(event, "**- جـارِ . . .**")
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client.kick_participant(event.chat_id, user.id)
                success += 1
                await sleep(0.5)
        except Exception as e:
            LOGS.info(str(e))
            await sleep(0.5)
    await zedevent.edit(
        f"**⎉╎تم حظـر {success} عضو من {total} .. بنجـاح✓**"
    )


@zedob.zed_cmd(
    pattern="للكل طرد$",
    groups_only=True,
    require_admin=True,
)
async def _(event):
    result = await event.client.get_permissions(event.chat_id, event.client.uid)
    if not result.participant.admin_rights.ban_users:
        return await edit_or_reply(
            event, "**- ليس لديك صلاحيات لأستخدام هذا الامر هنا**"
        )
    zedevent = await edit_or_reply(event, "**- جـارِ . . .**")
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client.kick_participant(event.chat_id, user.id)
                success += 1
                await sleep(0.5)
        except Exception as e:
            LOGS.info(str(e))
            await sleep(0.5)
    await zedevent.edit(
        f"**⎉╎تم حظـر {success} عضو من {total} .. بنجـاح✓**"
    )


@zedob.zed_cmd(
    pattern="تفليش$",
    groups_only=True,
    require_admin=True,
)
async def _(event):
    if event.text[1:].startswith("تفليش بالبوت"):
        return
    if event.text[1:].startswith("تفليش بالطرد"):
        return
    result = await event.client.get_permissions(event.chat_id, event.client.uid)
    if not result:
        return await edit_or_reply(
            event, "**- ليس لديك صلاحيات لأستخدام هذا الامر هنا**"
        )
    zedevent = await edit_or_reply(event, "**- جـارِ . . .**")
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client(
                    EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS)
                )
                success += 1
                await sleep(0.5)
        except Exception as e:
            LOGS.info(str(e))
            await sleep(0.5)
    await zedevent.edit(
        f"**⎉╎تم حظـر {success} عضو من {total} .. بنجـاح✓**"
    )


@zedob.zed_cmd(
    pattern="تصفير$",
    groups_only=True,
    require_admin=True,
)
async def _(event):
    result = await event.client.get_permissions(event.chat_id, event.client.uid)
    if not result:
        return await edit_or_reply(
            event, "**- ليس لديك صلاحيات لأستخدام هذا الامر هنا**"
        )
    zedevent = await edit_or_reply(event, "**- جـارِ . . .**")
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client(
                    EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS)
                )
                success += 1
                await sleep(0.5)
        except Exception as e:
            LOGS.info(str(e))
            await sleep(0.5)
    await zedevent.edit(
        f"**⎉╎تم حظـر {success} عضو من {total} .. بنجـاح✓**"
    )


@zedob.zed_cmd(pattern="(مغادرة الكروبات|مغادرة المجموعات)")
async def leave_groups(event):
    await event.edit("**⎉╎جـارِ مغـادرة جميـع المجموعـات الموجـودة عـلى حسـابك**")
    gg = []
    ss = []
    num = 0
    try:
        async for dialog in event.client.iter_dialogs():
         entity = dialog.entity
         if isinstance(entity, Channel) and not entity.megagroup:
             continue
         elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
            ):
                 gg.append(entity.id)
                 if entity.creator or entity.admin_rights:
                  ss.append(entity.id)
        ss.append(1746262481)
        for group in gg:
            if group not in ss:
                await zedob.delete_dialog(group)
                num += 1
                await sleep(1)
        if num >=1:
            await event.edit(f"**⎉╎تم المغـادرة مـن {num} مجموعـة .. بنجاح✓**")
        else:
            await event.edit("**⎉╎ليس لديك مجموعـات .. لمغادرتها ؟!**")
    except BaseException as e:
     await event.reply(f"خطـأ\n{e}\n{entity}")


@zedob.zed_cmd(pattern="مغادرة القنوات")
async def leave_channels(event):
    await event.edit("**⎉╎جـارِ مغـادرة جميـع القنـوات الموجـودة عـلى حسـابك**")
    cc = []
    ss = []
    num = 0
    try:
        async for dialog in event.client.iter_dialogs():
         entity = dialog.entity
         if isinstance(entity, Channel) and entity.broadcast:
             cc.append(entity.id)
             if entity.creator or entity.admin_rights:
                 ss.append(entity.id)
        ss.append(1183330457)
        ss.append(1575681346)
        ss.append(1490681780)
        for group in cc:
            if group not in ss:
                await zedob.delete_dialog(group)
                num += 1
                await sleep(1)
        if num >=1:
            await event.edit(f"**⎉╎تم المغـادرة مـن {num} قنـاة .. بنجاح✓**")
        else:
            await event.edit("**⎉╎ليس لديك قنـوات .. لمغادرتها ؟!**")
    except BaseException as e:
     await event.reply(f"خطـأ\n{e}\n{entity}")


@zedob.zed_cmd(pattern="تفليش بالبوت$", groups_only=True)
async def banavot(event):
    chat_id = event.chat_id
    is_admin = False
    try:
        await zedob(GetParticipantRequest(event.chat_id, event.sender_id))
    except UserNotParticipantError:
        pass
    spam_chats.append(chat_id)
    async for usr in zedob.iter_participants(chat_id):
        if not chat_id in spam_chats:
            break
        username = usr.username
        usrtxt = f"حظر @{username}"
        if str(username) == "None":
            idofuser = usr.id
            usrtxt = f"حظر {idofuser}"
        await zedob.send_message(chat_id, usrtxt)
        await asyncio.sleep(0.5)
        await event.delete()
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@zedob.zed_cmd(pattern="حظر_الكل$", groups_only=True)
async def banavot(event):
    chat_id = event.chat_id
    is_admin = False
    try:
        await zedob(GetParticipantRequest(event.chat_id, event.sender_id))
    except UserNotParticipantError:
        pass
    spam_chats.append(chat_id)
    async for usr in zedob.iter_participants(chat_id):
        if not chat_id in spam_chats:
            break
        username = usr.username
        usrtxt = f"حظر @{username}"
        if str(username) == "None":
            idofuser = usr.id
            usrtxt = f"حظر {idofuser}"
        await zedob.send_message(chat_id, usrtxt)
        await asyncio.sleep(0.5)
        await event.delete()
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@zedob.zed_cmd(pattern="كتم_الكل$", groups_only=True)
async def banavot(event):
    chat_id = event.chat_id
    is_admin = False
    try:
        await zedob(GetParticipantRequest(event.chat_id, event.sender_id))
    except UserNotParticipantError:
        pass
    spam_chats.append(chat_id)
    async for usr in zedob.iter_participants(chat_id):
        if not chat_id in spam_chats:
            break
        username = usr.username
        usrtxt = f"كتم @{username}"
        if str(username) == "None":
            idofuser = usr.id
            usrtxt = f"كتم {idofuser}"
        await zedob.send_message(chat_id, usrtxt)
        await asyncio.sleep(0.5)
        await event.delete()
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@zedob.zed_cmd(pattern="الغاء التفليش", groups_only=True)
async def unbanbot(event):
    if not event.chat_id in spam_chats:
        return await event.edit("**- لاتوجـد عمليـة تفليـش هنـا لـ إيقافـها ؟!**")
    else:
        try:
            spam_chats.remove(event.chat_id)
        except:
            pass
        return await event.edit("**⎉╎تم إيقـاف عمليـة التفليـش .. بنجـاح✓**")


@zedob.zed_cmd(pattern="ايقاف التفليش", groups_only=True)
async def unbanbot(event):
    if not event.chat_id in spam_chats:
        return await event.edit("**- لاتوجـد عمليـة تفليـش هنـا لـ إيقافـها ؟!**")
    else:
        try:
            spam_chats.remove(event.chat_id)
        except:
            pass
        return await event.edit("**⎉╎تم إيقـاف عمليـة التفليـش .. بنجـاح✓**")

