import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ==========================
#  BOT SETTINGS
# ==========================
BOT_TOKEN = "8573740591:AAFcvHHLyp9S9JoQMM3Em6vPsXoG_ZB4Cd0"  # Replace with your bot token
ADMIN_ID = 6430768414                  # Replace with your Telegram user ID

# API LINK
API = "https://veerulookup.onrender.com/search_phone?number="

# USER CREDIT DATA
user_credits = {}  # {user_id: credits}


# ==========================
#  COMMANDS
# ==========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_credits:
        user_credits[user_id] = 5

    await update.message.reply_text(
        "👑🥂 WELCOME TO ARES INFO BOT - PREMIUM 👑🥂\n\n"
        "Use /lookup <phone_number> to get details.\n"
        f"💰 Credits: {'∞' if user_id == ADMIN_ID else user_credits[user_id]}"
    )


async def lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check credits
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

    try:
        r = requests.get(f"{API}{number}", timeout=15)
        if r.ok:
            data = r.json()
            
            # Replace 'anshapi' with 'Ares'
            if 'credit' in data and data['credit'].lower() == 'anshapi':
                data['credit'] = 'Ares'

            # Premium formatting
            results = data.get("result", [])
            msg = f"💎 **ARES INFO BOT - PREMIUM RESULT** 💎\n\n"
            msg += f"⚡ Credit: {data.get('credit','Ares')}\n"
            msg += f"✅ Success: {data.get('success', True)}\n\n"

            if not results:
                msg += "❌ No results found.\n"
            else:
                for idx, entry in enumerate(results, 1):
                    msg += f"🔹 Result {idx} 🔹\n"
                    msg += f"Name       : {entry.get('name','N/A')}\n"
                    msg += f"Mobile     : {entry.get('mobile','N/A')}\n"
                    msg += f"Alt Mobile : {entry.get('alt_mobile','N/A')}\n"
                    msg += f"Father Name: {entry.get('father_name','N/A')}\n"
                    msg += f"Address    : {entry.get('address','N/A')}\n"
                    msg += f"Circle     : {entry.get('circle','N/A')}\n"
                    msg += f"Email      : {entry.get('email','N/A')}\n"
                    msg += "-"*30 + "\n"

            await update.message.reply_text(msg)
        else:
            await update.message.reply_text("❌ No data found or API not responding.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error connecting to the API.\n{str(e)}")

    # Deduct credits if not admin
    if user_id != ADMIN_ID:
        user_credits[user_id] -= 1
        await update.message.reply_text(f"💰 Credits used: 1 | Remaining: {user_credits[user_id]}")


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


# ==========================
# HELP / COMMANDS LIST
# ==========================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    msg = "📜 **ARES INFO BOT - COMMANDS LIST** 📜\n\n"
    msg += "🔹 /start - Start the bot and see your credits\n"
    msg += "🔹 /lookup <phone_number> - Lookup info for a phone number (uses 1 credit)\n"
    msg += "🔹 /credit - Check your remaining credits\n"
    if user_id == ADMIN_ID:
        msg += "🔹 /addcredit <user_id> <amount> - Add credits to a user (Admin only)\n"
    msg += "🔹 /help - Show this command list\n"
    await update.message.reply_text(msg)


# ==========================
#  MAIN
# ==========================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("lookup", lookup))
    app.add_handler(CommandHandler("credit", credit))
    app.add_handler(CommandHandler("addcredit", add_credit))
    app.add_handler(CommandHandler("help", help_command))  # Added /help command
    print("✅ PREMIUM ARES INFO BOT started...")
    app.run_polling()


if __name__ == "__main__":
    main()