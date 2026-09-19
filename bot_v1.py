from multiprocessing import context
import os
from turtle import update
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

print ("bot running")

# Channel ID
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Save folder
SAVE_DIR = r"C:\tg_bot_photos"

# folder မရှိရင် create လုပ်
os.makedirs(SAVE_DIR, exist_ok=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text ("🔆 Photo များပို့နိုင်ပါပြီ   📍 file size ကြီးသောပုံများပို့ပါက တစ်ပုံခြင်းပို့ပေးပါ   🚨 '' Saveing..... '' ကြာနေပါက ထက်မံပို့ပေးပါ")


async def save_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]

    # Telegram server က file ကိုယူ
    file = await context.bot.get_file(photo.file_id)

    print ("User sending photo")

    # file name တစ်ခုလုပ်
    filename = f"{update.message.from_user.id}_{update.message.message_id}.jpg"

    await update.message.reply_text("Saveing.....")

    file_path = os.path.join(SAVE_DIR, filename)

    # PC ထဲ download
    await file.download_to_drive(file_path)

    await update.message.reply_text("သိမ်းပြီးပါပြီ")

    await context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=photo.file_id,
            caption=f"User ID: {update.message.from_user.id}"
        )
    await update.message.reply_text("🤖 bot active time ( 9:00pm to 9:30pm )")

    print ("Saved in PC/Channel")

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
    app.add_handler(MessageHandler(filters.PHOTO, save_photo))
    app.add_handler(CommandHandler("myphotos",myphotos))
    app.add_handler(CommandHandler(["my_id" , "id" , "user_id"], my_id))
    app.add_handler(MessageHandler(filters.TEXT | filters.COMMAND, unknown))

    app.run_polling()


if __name__ == "__main__":
     run_bot()