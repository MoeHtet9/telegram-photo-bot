from multiprocessing import context
import os
import easyocr
from PIL import Image
from turtle import update
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

# Channel ID
CHANNEL_ID = os.getenv("CHANNEL_ID")

# reader
reader = easyocr.Reader(['en'], gpu=False)

# reseived photo
photo = update.message.photo[-1]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text ("🔆 Photo များသိမ်းနိုင်ပါပြီ   📍 file size ကြီးသောပုံများပို့ပါက တစ်ပုံခြင်းပို့ပေးပါ")

async def read_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Telegram server က file ကိုယူ
    file = await context.bot.get_file(photo.file_id)

    await file.download_to_drive("receipt.jpg")

    result = reader.readtext("receipt.jpg", detail=0)
    text = " ".join(result)
    save_photo()
    await update.message.reply_text(text)

async def save_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # Telegram server က file ကိုယူ
    file = await context.bot.get_file(photo.file_id)

    await update.message.reply_text("Saveing.....")

    await context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=photo.file_id,
            caption=f"User ID: {update.message.from_user.id}"
        )

    await update.message.reply_text("သိမ်းပြီးပါပြီ")

#myphoto
async def myphotos(updute: Update, context:ContextTypes.DEFAULT_TYPE):
    await updute.message.reply_text("Owner သို့ဆက်သွယ်ပါ :-: @Moehtetr")
    
#my id
async def my_id(update: Update, context:ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Your ID : {user.id}")

#Not Action,unknowcommand
async def unknown(updute: Update, context:ContextTypes.DEFAULT_TYPE):
    await updute.message.reply_text("Not Action ?")

def run_bot():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start" , start))
    app.add_handler(MessageHandler(filters.PHOTO, read_photo))
    app.add_handler(CommandHandler("myphotos",myphotos))
    app.add_handler(CommandHandler(["my_id" , "id" , "user_id"], my_id))
    app.add_handler(MessageHandler(filters.TEXT | filters.COMMAND, unknown))

    app.run_polling()


if __name__ == "__main__":
     run_bot()