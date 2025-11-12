import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === BOT SETTINGS ===
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # 🔹 Replace with your bot token
ADMIN_ID = 123456789  # 🔹 Replace with your Telegram user ID

# === API LINKS ===
API1 = "http://osintapi.anshapi.workers.dev"
API2 = "https://veerulookup.onrender.com/search_phone?number="

# === USER CREDIT DATA ===
user_credits = {}  # Example: {user_id: credits}

# === COMMANDS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_credits:
        user_credits[user_id] = 5  # default credits = 5

    await update.message.reply_text(
        "👑🥂 WELCOME TO ARES INFO BOT 👑🥂\n\n"
        "Use /lookup <phone_number> to get details.\n"
        f"💰 Credits: {'∞' if user_id == ADMIN_ID else user_credits[user_id]}"
    )

async def lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Admin has unlimited credits
    if user_id != ADMIN_ID:
        if user_id not in user_credits:
            user_credits[user_id] = 5
        if user_credits[user_id] <= 0:
            await update.message.reply_text("❌ You have no credits left. Please contact admin.")
            return

    if not context.args:
        await update.message.reply_text("❌ Please provide a phone number.\nExample: /lookup +919876543210")
        return

    number = context.args[0]
    await update.message.reply_text("🔍 Searching, please wait...")

    results = []

    try:
        r1 = requests.get(f"{API1}?number={number}", timeout=10)
        if r1.ok:
            results.append(r1.text)
    except Exception:
        pass

    try:
        r2 = requests.get(f"{API2}{number}", timeout=10)
        if r2.ok:
            results.append(r2.text)
    except Exception:
        pass

    if results:
        await update.message.reply_text("\n\n".join(results))
        if user_id != ADMIN_ID:
            user_credits[user_id] -= 1
    else:
        await update.message.reply_text("❌ No data found or APIs not responding.")

    if user_id != ADMIN_ID:
        await update.message.reply_text(f"💰 Remaining credits: {user_credits[user_id]}")

async def credit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    credits = "∞" if user_id == ADMIN_ID else user_credits.get(user_id, 5)
    await update.message.reply_text(f"💰 You have {credits} credits remaining.")

async def add_credit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("Usage: /addcredit <user_id> <amount>")
        return

    try:
        target_id = int(context.args[0])
        amount = int(context.args[1])
        user_credits[target_id] = user_credits.get(target_id, 5) + amount
        await update.message.reply_text(f"✅ Added {amount} credits to user {target_id}.")
    except ValueError:
        await update.message.reply_text("❌ Invalid input. Use numbers only.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("lookup", lookup))
    app.add_handler(CommandHandler("credit", credit))
    app.add_handler(CommandHandler("addcredit", add_credit))
    print("✅ ARES INFO BOT started...")
    app.run_polling()

if __name__ == "__main__":
    main()
