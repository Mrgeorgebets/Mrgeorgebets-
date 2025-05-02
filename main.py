
import logging
from telegram import Update, LabeledPrice
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, PreCheckoutQueryHandler

# Replace with your bot token and private channel ID
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_USERNAME = "@yourprivatechannel"
PAYMENT_PROVIDER_TOKEN = "STARS_PAYMENT_PROVIDER_TOKEN"

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PRICE = [LabeledPrice("Access to Premium Group", 300000)]  # 3000 Stars = 300000 in subunits

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Type /pay to get access to the premium content.")

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_invoice(
        chat_id=update.effective_chat.id,
        title="Premium Access",
        description="Pay 3000 Stars to access the private group",
        payload="paywall-access",
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency="XTR",
        prices=PRICE,
        start_parameter="paywall-start"
    )

async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    if query.invoice_payload != "paywall-access":
        await query.answer(ok=False, error_message="Something went wrong.")
    else:
        await query.answer(ok=True)

async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Payment received! Here's your access link:")
    await update.message.reply_text(f"https://t.me/{CHANNEL_USERNAME[1:]}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pay", pay))
    app.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))
    
    app.run_polling()
