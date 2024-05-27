import re
import secrets
import string
import asyncio
def normalize_phone_number(phone_number):
    # removing all digits except digits
    digits = re.sub(r'\D', '', phone_number)
    
    # check if phone format is correct
    if len(digits) == 11 and digits[0] == '8':
        return '+7' + digits[1:]
    elif len(digits) == 11 and digits.startswith('7'):
        return '+' + digits
    elif len(digits) == 10:
        return '+7' + digits
    else:
        # if phone format is incorrect
        return None

def generate_unique_code(length=10):
    # defining symbols that will be used in the code
    characters = string.ascii_letters + string.digits
    # generating random code
    code = ''.join(secrets.choice(characters) for _ in range(length))
    return code


async def mail(users: list, message):
    from bot.bot import bot
    coros = [bot.send_message(user.get('chat_id'), text=message) for user in users]

    await asyncio.gather(*coros)
  