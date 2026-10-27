import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile

from config import BOT_TOKEN
from database import init_db, get_user, update_user, reset_car
from keyboards import get_main_menu, get_car_menu

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_car_image_path(user_data):
    fixed_count = user_data["engine"] + user_data["body"] + user_data["wheels"]
    if fixed_count == 0: level_img = 1
    elif fixed_count == 1: level_img = 2
    elif fixed_count == 2: level_img = 3
    else: level_img = 4
    
    return f"images/vaz2106_{level_img}.png"

@dp.message(CommandStart())
async def cmd_start(message: Message):
    get_user(message.from_user.id)
    await message.answer(
        "Привет! Ты — начинающий механик. У тебя есть ржавая «шестёрка», которую нужно восстановить и выгодно продать.\n"
        "Зарабатывай монеты на подработке и покупай запчасти!",
        reply_markup=get_main_menu()
    )

@dp.callback_query(F.data == "view_car")
async def show_car(callback: CallbackQuery):
    user_data = get_user(callback.from_user.id)
    photo_path = get_car_image_path(user_data)
    
    text = (f"🚗 **ВАЗ 2106**\n"
            f"💰 Баланс: {user_data['coins']} монет\n\n"
            f"Состояние:\n"
            f"Двигатель: {'✅' if user_data['engine'] else '❌'}\n"
            f"Кузов: {'✅' if user_data['body'] else '❌'}\n"
            f"Колёса: {'✅' if user_data['wheels'] else '❌'}")
            
    await callback.message.delete()
    
    try:
        photo = FSInputFile(photo_path)
        await callback.message.answer_photo(
            photo=photo, caption=text, parse_mode="Markdown", reply_markup=get_car_menu(user_data)
        )
    except Exception as e:
        # Если картинку не нашли, присылаем текст (чтобы бот не падал)
        await callback.message.answer(
            text + f"\n\n⚠️ *Картинка не найдена ({photo_path})*", 
            parse_mode="Markdown", reply_markup=get_car_menu(user_data)
        )
    await callback.answer()

@dp.callback_query(F.data == "work")
async def do_work(callback: CallbackQuery):
    user_data = get_user(callback.from_user.id)
    update_user(callback.from_user.id, coins=user_data["coins"] + 30)
    await callback.message.edit_text(
        "💼 Ты отработал смену в сервисе и заработал **30 монет**!",
        reply_markup=get_main_menu(), parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "fix_wheels")
async def fix_wheels(callback: CallbackQuery):
    user_data = get_user(callback.from_user.id)
    if user_data["coins"] >= 100:
        update_user(callback.from_user.id, coins=user_data["coins"] - 100, wheels_fixed=1)
        await callback.answer("Машина поставлена на ход!", show_alert=True)
        await show_car(callback)
    else:
        await callback.answer("Недостаточно монет!", show_alert=True)

@dp.callback_query(F.data == "fix_engine")
async def fix_engine(callback: CallbackQuery):
    user_data = get_user(callback.from_user.id)
    if user_data["coins"] >= 200:
        update_user(callback.from_user.id, coins=user_data["coins"] - 200, engine_fixed=1)
        await callback.answer("Двигатель отремонтирован!", show_alert=True)
        await show_car(callback)
    else:
        await callback.answer("Недостаточно монет!", show_alert=True)

@dp.callback_query(F.data == "fix_body")
async def fix_body(callback: CallbackQuery):
    user_data = get_user(callback.from_user.id)
    if user_data["coins"] >= 150:
        update_user(callback.from_user.id, coins=user_data["coins"] - 150, body_fixed=1)
        await callback.answer("Кузов покрашен!", show_alert=True)
        await show_car(callback)
    else:
        await callback.answer("Недостаточно монет!", show_alert=True)

@dp.callback_query(F.data == "sell_car")
async def sell_car(callback: CallbackQuery):
    user_data = get_user(callback.from_user.id)
    fixed_count = user_data["engine"] + user_data["body"] + user_data["wheels"]
    
    if fixed_count == 1: sell_price = 250
    elif fixed_count == 2: sell_price = 450
    else: sell_price = 700
    
    update_user(callback.from_user.id, coins=user_data["coins"] + sell_price)
    reset_car(callback.from_user.id)
    
    await callback.message.delete()
    await callback.message.answer(
        f"💰 Ты продал машину за **{sell_price} монет**!\n"
        f"Твой баланс: {get_user(callback.from_user.id)['coins']} монет.\n\n"
        f"В гараж заехала следующая ржавая «шестёрка». Крути гайки дальше!",
        reply_markup=get_main_menu(), parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "main_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Главное меню:", reply_markup=get_main_menu())
    await callback.answer()

async def main():
    init_db()
    print("Бот запущен! Иди в Telegram и проверяй.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())