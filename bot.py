import asyncio
import nest_asyncio
from together import Together
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    ContextTypes, MessageHandler, filters
)

# Активация совместимости с Colab и другими async-средами
nest_asyncio.apply()

# КЛЮЧИ
TELEGRAM_TOKEN = "7873028623:AAH0t1JgwHNU3w4XqgdanJNj09nwAW-3Pjk"
TOGETHER_API_KEY = "76b10b1000663fc947ea89c0c271b7785e3187bfa95c61ee9ebff2950b556b1a"

client = Together(api_key=TOGETHER_API_KEY)

# Обработка сообщений
async def ask_gpt(prompt):
    try:
        response = client.chat.completions.create(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка: {e}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = await ask_gpt(user_message)
    await update.message.reply_text(response)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я Jarvis PRO. Просто напиши мне что-нибудь.")

# Запуск бота
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Jarvis PRO запущен!")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())