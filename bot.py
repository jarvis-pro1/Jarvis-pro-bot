import asyncio
import nest_asyncio
from together import Together
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

nest_asyncio.apply()

TELEGRAM_TOKEN = "7873028623:AAH0t1JgwHNU3w4XqgdanJNj09nwAW-3Pjk"
TOGETHER_API_KEY = "76b10b1000663fc947ea89714cd62bbdc8a2f7b8"

client = Together(api_key=TOGETHER_API_KEY)

def ask_gpt(prompt):
    response = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.7
    )
    return response.choices[0].message.content

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    reply = ask_gpt(user_msg)
    await update.message.reply_text(reply)

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Jarvis PRO запущен!")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())