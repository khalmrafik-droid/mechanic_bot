import time
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu(user_data=None): 
    builder = InlineKeyboardBuilder()
    builder.button(text="🚗 Моя машина", callback_data="view_car")
    
    if user_data:
        current_time = time.time()
        time_passed = current_time - user_data.get("last_work", 0)
        
        if time_passed < 900: 
            builder.button(text="⏳ Подработка (Перерыв)", callback_data="work")
        else:
            builder.button(text="💼 Подработка (+30 монет)", callback_data="work")
    else:
        builder.button(text="💼 Подработка (+30 монет)", callback_data="work")
        
    builder.adjust(1)
    return builder.as_markup()

def get_car_menu(user_data):
    builder = InlineKeyboardBuilder()
    
    if not user_data["wheels"]:
        builder.button(text="🛞 Поставить на ход (100 монет)", callback_data="fix_wheels")
    if not user_data["engine"]:
        builder.button(text="🔧 Починить двигатель (200 монет)", callback_data="fix_engine")
    if not user_data["body"]:
        builder.button(text="🎨 Покрасить кузов (150 монет)", callback_data="fix_body")
        
    if user_data["wheels"]: 
        builder.button(text="💰 Продать машину", callback_data="sell_car")
        
    builder.button(text="⬅️ Назад", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()
