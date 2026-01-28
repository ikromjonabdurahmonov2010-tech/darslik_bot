import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = "8545245862:AAE5ylq1zFcG2lQOK8omEjYJHlhqZi_nI3c"
ADMIN_ID = 7650759032

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

MOVIES = {}
movie_id = 1
ADD_MODE = set()   # kim kino qo‘shyapti


# ================= START =================

@dp.message(Command("start"))
async def start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        keyboards = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="darslik qoshish ➕"), KeyboardButton(text="darslik qidirish 🔎")]
            ],
            resize_keyboard=True,
            input_field_placeholder="Menyudan tanlang..."
        )
    else:
        keyboards = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="darslik qidirish 🔎")]],
            resize_keyboard=True,
            input_field_placeholder="Menyudan tanlang..."
        )

    await message.answer(
        f"Assalomu alaykum {message.from_user.first_name}\n\n"
        "🎥 darslik botga xush kelibsiz!",
        reply_markup=keyboards
    )


# ================= ADD MOVIE =================

@dp.message(F.text == "darslik qoshish ➕")
async def ask_video(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        ADD_MODE.add(message.from_user.id)
        await message.answer("Iltimos, darslik video ko‘rinishida yuboring 🎬")
    else:
        await message.answer("Sizga ruxsat yo‘q ❌")


@dp.message(F.video)
async def add_video(message: types.Message):
    global movie_id

    if message.from_user.id in ADD_MODE:
        MOVIES[movie_id] = {
            "title": f"darslik#{movie_id}",
            "film_id": message.video.file_id
        }
        movie_id += 1
        ADD_MODE.remove(message.from_user.id)

        await message.answer("✅ darslik botga qoshildi!")
    else:
        await message.answer("Avval 'darslik qoshish ➕' tugmasini bosing.")


# ================= SEARCH MOVIE =================

@dp.message(F.text == "darslik qidirish 🔎")
async def ask_number(message: types.Message):
    await message.answer("darslik raqamini kiriting 🔢")


@dp.message(F.text.regexp(r'^\d+$'))
async def send_movie(message: types.Message):
    raqam = int(message.text)
    movie = MOVIES.get(raqam)

    if movie:
        await message.answer_video(
            video=movie["film_id"],
            caption=f"🎬 {movie['title']}"
        )
    else:
        await message.answer("❌ Bunday raqamli darslik yoq")


# ================= OTHER TEXT =================

@dp.message(F.text)
async def other_text(message: types.Message):
    await message.answer("Iltimos, menyudan foydalaning yoki darslik raqamini kiriting 🙂")


# ================= RUN =================

async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


