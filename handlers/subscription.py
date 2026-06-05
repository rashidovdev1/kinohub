from aiogram import Bot
from aiogram.enums import ChatMemberStatus
import config


async def check_user_subscription(bot: Bot, user_id: int) -> dict:
    """
    Foydalanuvchining barcha kanallarga obuna bo'lganligini tekshirish
    
    Returns:
        dict: {
            'subscribed': bool,
            'not_subscribed_channels': list,
            'pending_channels': list
        }
    """
    not_subscribed = []
    pending = []
    
    for channel in config.REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(
                chat_id=channel['id'],
                user_id=user_id
            )
            
            # Obuna bo'lgan statuslar
            subscribed_statuses = [
                ChatMemberStatus.CREATOR,
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.MEMBER
            ]
            
            if member.status in subscribed_statuses:
                continue
            elif member.status == ChatMemberStatus.RESTRICTED:
                # Zapros yuborilgan, kutilmoqda
                pending.append(channel)
            else:
                # Obuna yo'q
                not_subscribed.append(channel)
                
        except Exception as e:
            print(f"Kanal {channel.get('username', channel['id'])} tekshirishda xatolik: {e}")
            not_subscribed.append(channel)
    
    return {
        'subscribed': len(not_subscribed) == 0 and len(pending) == 0,
        'not_subscribed_channels': not_subscribed,
        'pending_channels': pending
    }


async def auto_approve_join_request(bot: Bot, chat_id: int, user_id: int):
    """
    Private kanalga yuborilgan zaprosni avtomatik qabul qilish
    """
    try:
        await bot.approve_chat_join_request(
            chat_id=chat_id,
            user_id=user_id
        )
        return True
    except Exception as e:
        print(f"Zaprosni qabul qilishda xatolik: {e}")
        return False
