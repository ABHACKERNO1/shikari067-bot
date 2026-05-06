import os
import qrcode
from io import BytesIO
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
UPI_ID = os.getenv("UPI_ID")

if not TOKEN:
    raise Exception("TOKEN missing in environment")
if not UPI_ID:
    raise Exception("UPI_ID missing in environment")

PRICE = {
    "1d": 120,
    "7d": 300,
    "30d": 800
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 1 Day - ₹120", callback_data="1d")],
        [InlineKeyboardButton("⚡ 7 Days - ₹300", callback_data="7d")],
        [InlineKeyboardButton("💀 30 Days - ₹800", callback_data="30d")]
    ]

    await update.message.reply_text(
        "💀 Welcome to Shikari Store\n\nSelect your plan:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    plan = query.data
    amount = PRICE.get(plan)

    user_id = update.effective_user.id
    order_id = f"{user_id}_{plan}"

    upi_link = f"upi://pay?pa={UPI_ID}&pn=Shikari&am={amount}&tn={order_id}"

    qr = qrcode.make(upi_link)
    bio = BytesIO()
    bio.name = "qr.png"
    qr.save(bio, "PNG")
    bio.seek(0)

    keyboard = [
        [InlineKeyboardButton("✅ I'VE PAID", callback_data="paid")]
    ]

    await query.message.reply_photo(
        photo=bio,
        caption=f"💰 Amount: ₹{amount}\n\n📲 Scan & Pay\n\nUPI: {UPI_ID}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "✅ Payment received request!\n\n⏳ We will verify shortly."
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(plan, pattern="^(1d|7d|30d)$"))
app.add_handler(CallbackQueryHandler(paid, pattern="^paid$"))

print("Bot running...")
app.run_polling()
