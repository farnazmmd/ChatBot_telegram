from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
# conversation
NAME, PHONE, GRADE = range(3)
# start bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لطفا اسمت رو وارد کن:")
    return NAME

#input name
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("شماره تماس را وارد کن:")
    return PHONE

#input number
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("پایه تحصیلی را وارد کن:")
    return GRADE

#input grade
async def get_grade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["grade"] = update.message.text

    name = context.user_data["name"]
    phone = context.user_data["phone"]
    grade = context.user_data["grade"]


    message = f"ثبت نام جدید:\n\nنام: {name}\nشماره: {phone}\nپایه: {grade}"
    admin_id = 1157193692

    await context.bot.send_message(chat_id=admin_id, text=message)
    await update.message.reply_text("اطلاعات ثبت شد. ممنون!")
    return ConversationHandler.END

#cancele conversation
async def cancele(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لغو شد.")
    return ConversationHandler.END

#start bot
if __name__== "__main__":
    import os
    from telegram.ext import Application

    TOKEN = "7288625978:AAH_elZKFf1IMMUhnowI0TYlIRQsTaUipVs"
    
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start",start)],
        states={
            NAME:[MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE:[MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            GRADE:[MessageHandler(filters.TEXT & ~filters.COMMAND, get_grade)]
        },
        fallbacks=[CommandHandler("cancele",cancele)],
    )
    app.add_handler(conv_handler)
    print("ربات در حال اجراست...")
    app.run_polling()