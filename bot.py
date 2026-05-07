import os
import telebot
import qrcode
from io import BytesIO
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN")
UPI_ID = os.getenv("UPI_ID")

bot = telebot.TeleBot(TOKEN)

PRICE = {
    "1d": 120,
    "7d": 300,
    "30d": 800
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton("🔥 1 Day - ₹120", callback_data="1d"))
    markup.add(InlineKeyboardButton("⚡ 7 Days - ₹300", callback_data="7d"))
    markup.add(InlineKeyboardButton("💀 30 Days - ₹800", callback_data="30d"))

    bot.send_message(
        message.chat.id,
        "💀 Welcome to Shikari Store",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    if call.data in PRICE:

        amount = PRICE[call.data]

        upi_link = f"upi://pay?pa={UPI_ID}&pn=Shikari&am={amount}"

        qr = qrcode.make(upi_link)

        bio = BytesIO()
        bio.name = "qr.png"

        qr.save(bio, "PNG")
        bio.seek(0)

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ I'VE PAID", callback_data="paid"))

        bot.send_photo(
            call.message.chat.id,
            bio,
            caption=f"💰 Amount: ₹{amount}\n\nUPI: {UPI_ID}",
            reply_markup=markup
        )

    elif call.data == "paid":

        bot.send_message(
            call.message.chat.id,
            "✅ Payment request received"
        )

print("Bot running...")

bot.infinity_polling()
