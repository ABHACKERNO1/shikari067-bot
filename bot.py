import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ENV VARIABLES
TOKEN = os.getenv("TOKEN")
UPI_ID = os.getenv("UPI_ID")

PRICE = {
    "1d": "100",
    "7d": "300",
    "30d": "800"
}

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚡ ENTER STORE", callback_data="store")],
        [InlineKeyboardButton("📞 SUPPORT", callback_data="support")]
    ]

    await update.message.reply_text(
        "⚔️ SHIKARI SYSTEM ONLINE\n\nSelect option:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# STORE
async def store(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("⚡ 1 DAY", callback_data="1d"),
            InlineKeyboardButton("🔥 7 DAYS", callback_data="7d"),
            InlineKeyboardButton("💎 30 DAYS", callback_data="30d")
        ]
    ]

    await query.edit_message_text("🛒 Select Plan:", reply_markup=InlineKeyboardMarkup(keyboard))

# PLAN SELECT
async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    plan = query.data
    context.user_data["plan"] = plan
    price = PRICE[plan]

    keyboard = [
        [InlineKeyboardButton("✅ I'VE PAID", callback_data="paid")]
    ]

    await query.edit_message_text(
        f"📦 Plan: {plan}\n💰 Price: ₹{price}\n\n💳 UPI: {UPI_ID}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# FAKE KEY (later automation yaha lagega)
def generate_key():
    return "TEST-KEY-1234"

# PAYMENT CONFIRM
async def paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text("⏳ Processing...")

    await asyncio.sleep(2)

    key = generate_key()

    await query.edit_message_text(
        f"🎉 SUCCESS\n\n🔑 KEY:\n`{key}`",
        parse_mode="Markdown"
    )

# SUPPORT
async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📞 Contact: @SHIKARI067")

# MAIN
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(store, pattern="store"))
app.add_handler(CallbackQueryHandler(plan, pattern="^(1d|7d|30d)$"))
app.add_handler(CallbackQueryHandler(paid, pattern="paid"))
app.add_handler(CallbackQueryHandler(support, pattern="support"))

app.run_polling()