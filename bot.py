import os
import easyocr

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# OCR Reader
reader = easyocr.Reader(["en"], gpu=False)


# =========================
# /start
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔆 Photo များသိမ်းနိုင်ပါပြီ\n"
        "📍 file size ကြီးသောပုံများပို့ပါက တစ်ပုံခြင်းပို့ပေးပါ"
    )


# =========================
# Receive Photo + OCR
# =========================
async def read_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Telegram ကပို့လာတဲ့ photo ကိုယူ
    photo = update.message.photo[-1]

    # Telegram server က file ကိုယူ
    file = await context.bot.get_file(photo.file_id)

    # Photo ကို temporary file အဖြစ် download လုပ်
    await file.download_to_drive("receipt.jpg")

    # OCR နဲ့ photo ထဲကစာဖတ်
    result = reader.readtext("receipt.jpg", detail=0)

    print("RESULT:", result)

    text = " ".join(result)

    print("OCR:", text)

    # Channel ထဲသိမ်း
    await save_photo(update, context, photo)

    # User ကို OCR ဖတ်ထားတဲ့စာပြ
    await update.message.reply_text(
        f"📖 OCR Result:\n{text}"
    )


# =========================
# Save Photo to Channel
# =========================
async def save_photo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    photo
):

    await update.message.reply_text("Saving.....")

    await context.bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=photo.file_id,
        caption=f"User ID: {update.message.from_user.id}"
    )

    await update.message.reply_text(
        "✅ သိမ်းပြီးပါပြီ"
    )


# =========================
# /myphotos
# =========================
async def myphotos(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "Owner သို့ဆက်သွယ်ပါ :-: @Moehtetr"
    )


# =========================
# /my_id
# =========================
async def my_id(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    await update.message.reply_text(
        f"Your ID : {user.id}"
    )


# =========================
# Unknown Command / Text
# =========================
async def unknown(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "Not Action ?"
    )


# =========================
# Run Bot
# =========================
def run_bot():

    app = Application.builder().token(TOKEN).build()

    # /start
    app.add_handler(
        CommandHandler("start", start)
    )

    # Photo
    app.add_handler(
        MessageHandler(filters.PHOTO, read_photo)
    )

    # /myphotos
    app.add_handler(
        CommandHandler("myphotos", myphotos)
    )

    # /my_id /id /user_id
    app.add_handler(
        CommandHandler(
            ["my_id", "id", "user_id"],my_id
        )
    )

    # Unknown text / command
    app.add_handler(
        MessageHandler(
            filters.TEXT | filters.COMMAND,unknown
        )
    )

    app.run_polling()


# =========================
# Start
# =========================
if __name__ == "__main__":
    run_bot()