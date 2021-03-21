from telebot import types


def country_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    usa = types.KeyboardButton('United States')
    russia = types.KeyboardButton('Russia')
    germany = types.KeyboardButton('Germany')
    uk = types.KeyboardButton('United Kingdom')
    poland = types.KeyboardButton('Poland')
    ua = types.KeyboardButton('Ukraine')
    italy = types.KeyboardButton('Italy')
    thailand = types.KeyboardButton('Thailand')
    litva = types.KeyboardButton('Republic of Lithuania')
    esp = types.KeyboardButton('Spain')
    sa = types.KeyboardButton('South Africa')
    romania = types.KeyboardButton('Romania')
    czech = types.KeyboardButton('Czech Republic')
    estonia = types.KeyboardButton('Estonia')
    kz = types.KeyboardButton('Kazakhstan')
    philip = types.KeyboardButton('Philippines')
    belarus = types.KeyboardButton('Belarus')
    france = types.KeyboardButton('France')
    ireland = types.KeyboardButton('Ireland')
    serbia = types.KeyboardButton('Serbia')
    switzerland = types.KeyboardButton('Switzerland')
    keyboard.add(
        belarus, czech, estonia, france, germany, ireland, italy,
        kz, philip, poland, litva, romania, russia, serbia, sa,
        esp, switzerland, thailand, ua, uk, usa
    )
    return keyboard