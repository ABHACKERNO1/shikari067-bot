import os
import qrcode
from io import BytesIO
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

TOKEN = os.getenv("TOKEN")
UPI_ID = os.getenv("UPI_ID")

PRICE = {
    "1d": 120,
    "7d": 300,
    "30d": 800
}

def start(update, context):
    keyboard = [
        [InlineKeyboardButton("🔥 1 Day - ₹120", callback_data="1d")],
        [InlineKeyboardButton("⚡ 7 Days - ₹300", callback_data="7d")],
        [InlineKeyboardButton("💀 30 Days - ₹800", callback_data="30d")]
    ]

    update.message.reply_text(
        "💀 Welcome to Shikari Store",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def plan(update, context):
    query = update.callback_query
    query.answer()

    plan_name = query.data
    amount = PRICE[plan_name]

    upi_link = f"upi://pay?pa={UPI_ID}&pn=Shikari&am={amount}"

    qr = qrcode.make(upi_link)

    bio = BytesIO()
    bio.name = "qr.png"

    qr.save(bio, "PNG")
    bio.seek(0)

    keyboard = [
        [InlineKeyboardButton("✅ I'VE PAID", callback_data="paid")]
    ]

    query.message.reply_photo(
        photo=bio,
        caption=f"💰 Amount: ₹{amount}\n\nUPI: {UPI_ID}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def paid(update, context):
    query = update.callback_query
    query.answer()

    query.message.reply_text(
        "✅ Payment request received"
    )

updater = Updater(TOKEN, use_context=True)

dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(plan, pattern="^(1d|7d|30d)$"))
dispatcher.add_handler(CallbackQueryHandler(paid, pattern="^paid$"))

print("Bot running...")

updater.start_polling()
updater.idle()
