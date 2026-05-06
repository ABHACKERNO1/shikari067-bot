import os
import qrcode
from io import BytesIO
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
UPI_ID = os.getenv("UPI_ID")

PRICE = {
    "1d": 120,
    "7d": 300,
    "30d": 800
}

# START COMMAND
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

# PLAN SELECT
async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    plan = query.data
    amount = PRICE[plan]

    user_id = update.effective_user.id
    order_id = f"{user_id}_{plan}"

    # UPI deep link (auto amount)
    upi_link = f"upi://pay?pa={UPI_ID}&pn=Shikari&am={amount}&tn={order_id}"

    # Generate QR
    qr = qrcode.make(upi_link)
    bio = BytesIO()
    bio.name = "qr.png"
    qr.save(bio, "PNG")
    bio.seek(0)

    keyboard = [
        [InlineKeyboardButton("✅ I'VE PAID", callback_data=f"paid_{plan}")]
    ]

    await query.message.reply_photo(
        photo=bio,
        caption=f"💰 Amount: ₹{amount}\n\n📲 Scan & Pay\n\nUPI: {UPI_ID}\n\n⏳ Valid for 5 minutes",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# PAYMENT BUTTON
async def paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "✅ Payment request received!\n\n⏳ Please wait, we are verifying your payment..."
    )

    # yaha baad me tu admin verify ya auto system laga sakta hai

# MAIN
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(plan, pattern="^(1d|7d|30d)$"))
app.add_handler(CallbackQueryHandler(paid, pattern="^paid_"))

print("Bot running...")
app.run_polling()            InlineKeyboardButton("💎 30 DAYS", callback_data="30d")
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
