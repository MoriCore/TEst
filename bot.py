from aiogram import Bot, Dispatcher
from aiogram.types import Message
import asyncio
import os

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# команда /start
@dp.message(lambda message: message.text == "/start")
async def start_cmd(message: Message):
    text = (
        "<b>Привет! 🪽</b>\n\n"
        "Это официальный бот <a href='https://t.me/moricoreuz'>@moricoreuz</a> для обратной связи и предложений! ୭ 🌙 "
        "<i>Просьба не отправлять оффтоп, мэмы и другое</i>\n"
        "────── ✧.°୭. ──────\n"
        "<b>Здесь ты можешь отправить нам свои:</b>\n\n"
        "✧ Идеи для обновления ассортимента\n\n"
        "✧ Предложения по добавлению нового мерча, украшений или товаров — даже если они не связаны с фандомами\n\n"
        "✧ Предложения украшений или брелков в определённой тематике, или с определённым дизайном "
        "(например, из Pinterest или в определённой палитре)\n\n"
        "✧ Можете отправлять фото желаемого дизайна или примера\n\n"
        "<i>Или просто написать нам сообщение с пожеланиями! ✨</i>\n"
        "────── ✧.°୭. ──────\n"
        "Мы читаем все сообщения и обязательно ответим тебе прямо здесь, в боте 💌\n\n"
        "Если вы обнаружите ошибку в работе бота, просьба написать сюда "
        "<a href='https://t.me/KommoriRawr'>@KommoriRawr</a> — Спасибо!"
    )

    await message.answer(text, parse_mode="HTML")

# обработчик любых сообщений
@dp.message()
async def forward_to_admin(message: Message):
    print(f"[{message.from_user.full_name}] написал(а): {message.text or 'не текстовое сообщение'}")

    if message.from_user.id != ADMIN_ID:
        username = f"@{message.from_user.username}" if message.from_user.username else "—"
        try:
            header = (
                f"📩 О, НОВОЕ СООБЩЕНИЕ В БОТЕ\n\n"
                f"👤 Имя: {message.from_user.full_name}\n"
                f"🆔 ID: {message.from_user.id}\n"
                f"🔗 Username: {username}\n\n"
            )

            # если это текст
            if message.text:
                await bot.send_message(ADMIN_ID, header + f"💬 Текст: {message.text}")
            else:
                # если фото, видео, документ и т.п.
                file_id = None
                caption = message.caption or ""
                if message.photo:
                    file_id = message.photo[-1].file_id
                    await bot.send_photo(ADMIN_ID, file_id, caption=header + caption)
                elif message.video:
                    file_id = message.video.file_id
                    await bot.send_video(ADMIN_ID, file_id, caption=header + caption)
                elif message.voice:
                    file_id = message.voice.file_id
                    await bot.send_voice(ADMIN_ID, file_id, caption=header + caption)
                elif message.document:
                    file_id = message.document.file_id
                    await bot.send_document(ADMIN_ID, file_id, caption=header + caption)
                else:
                    await bot.send_message(ADMIN_ID, header + "📎 (неподдерживаемый тип файла)")

            await message.answer("✅ Ваше сообщение отправлено! Совсем скоро прилетит ответ.")
        except Exception as e:
            print("Ошибка при пересылке:", e)

    else:
        # админ отвечает пользователю
        if message.reply_to_message:
            original = message.reply_to_message.text or message.reply_to_message.caption
            if not original:
                await message.answer("⚠️ Невозможно определить ID пользователя. Ответьте на сообщение с текстом, где указан ID.")
                return

            lines = original.split("\n")
            user_id_line = next((line for line in lines if line.startswith("🆔 ID: ")), None)
            if user_id_line:
                user_id = int(user_id_line.replace("🆔 ID: ", ""))
                try:
                    if message.text:
                        await bot.send_message(user_id, f"📬 Прилетел ответ!:\n{message.text}")
                    elif message.photo:
                        await bot.send_photo(user_id, message.photo[-1].file_id, caption="📬 Ответ от администратора:")
                    elif message.video:
                        await bot.send_video(user_id, message.video.file_id, caption="📬 Ответ от администратора:")
                    elif message.voice:
                        await bot.send_voice(user_id, message.voice.file_id, caption="📬 Ответ от администратора:")
                    await message.answer("✅ Ответ отправлен пользователю.")
                except Exception as e:
                    await message.answer(f"⚠️ Не удалось отправить сообщение: {e}")
            else:
                await message.answer("⚠️ Не удалось найти ID пользователя в сообщении.")
async def main():
    print("🚀 Бот запущен и работает...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())