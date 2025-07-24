from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)

# مراحل گفتگو
NAME, PHONE, GRADE = range(3)

# شروع گفتگو
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لطفا اسمت رو وارد کن:")
    return NAME

# گرفتن اسم
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("شماره تماس رو وارد کن:")
    return PHONE

# گرفتن شماره
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("پایه تحصیلی رو وارد کن:")
    return GRADE

# گرفتن پایه و ارسال به ادمین
async def get_grade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["grade"] = update.message.text

    name = context.user_data["name"]
    phone = context.user_data["phone"]
    grade = context.user_data["grade"]

    message = f"📥 فرم ثبت‌نام:\n\n👤 نام: {name}\n📞 شماره: {phone}\n🎓 پایه: {grade}"
    admin_id = 1157193692

    await context.bot.send_message(chat_id=admin_id, text=message)
    await update.message.reply_text("✅ اطلاعات ثبت شد. ممنون!")

    return ConversationHandler.END

# لغو
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ لغو شد.")
    return ConversationHandler.END

# اجرای برنامه
import asyncio

TOKEN = "7288625978:AAH_elZKFf1IMMUhnowI0TYlIRQsTaUipVs"

app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            GRADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_grade)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

app.add_handler(conv_handler)
async def main():
    await app.initialize()
    print("ربات در حال اجرا است.....")
    await  app.start()
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
