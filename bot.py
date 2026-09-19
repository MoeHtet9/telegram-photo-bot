import os
import warnings

warnings.filterwarnings("ignore")

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

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

    photo = update.message.photo[-1]

    file = await context.bot.get_file(photo.file_id)

    await file.download_to_drive("receipt.jpg")

    with open("receipt.jpg", "rb") as image_file:
        image_data = image_file.read()

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": """
                        Read this payment receipt image.

                        Return ONLY these 5 fields:

                        Amount:
                        Name:
                        Transaction ID:
                        Date:
                        Payment method:

                        If a field cannot be found, write:
                        Not found

                        Do not add any other explanation.
                        """
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{__import__('base64').b64encode(image_data).decode()}"
                    }
                ]
            }
        ]
    )

    result = response.output_text

    await update.message.reply_text(result)


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