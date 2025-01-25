from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


def main_menu_button(have_bought_course: bool):
    if have_bought_course:
        buttons = [
            [InlineKeyboardButton(text="📖 Гайд 📖", callback_data='viewing_guide')],
            [InlineKeyboardButton(text="💰 Баланс 💰", callback_data='balance')],
            [InlineKeyboardButton(text="🏷️ Промокод 🏷️", callback_data='viewing_promo')]
        ]
    else:
        buttons = [
            [InlineKeyboardButton(text="💳 Купить гайд 💳", callback_data='by_course')],
        ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup

def check_promo_code():
    button = [[types.InlineKeyboardButton(text="Есть промокод 😁", callback_data='check_promo')],
              [types.InlineKeyboardButton(text="Нет промокода 🫠", callback_data='no_promo')]]
    markup = InlineKeyboardMarkup(inline_keyboard=button)
    return markup

def payment_keyboard(amount):
    buttons = [[types.InlineKeyboardButton(text=f"Оплатить {amount} RUB" , pay=True)], ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup

def balance_out_money():
    buttons = [[types.InlineKeyboardButton(text=f"Вывести деньги" , callback_data='out_money')], ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup

def out_money_get_card():
    web_app = WebAppInfo(url="https://olezhkaa.github.io/YooCassaWidget/")  # URL на ваш хостинг с HTML
    button = [[types.KeyboardButton(text="💸 Вывод средств 💸", web_app=web_app)], ]
    markup = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True, one_time_keyboard=True)
    return markup

def create_promo():
    buttons = [[types.InlineKeyboardButton(text=f"Создать промокод" , callback_data='create_promo')], ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup