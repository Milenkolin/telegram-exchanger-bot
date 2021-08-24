import tokenfile
from banks_data import OschadBank, PrivatBank, NationalBankOfUkraine
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(tokenfile.TOKEN)
dp = Dispatcher(bot)
Ob = OschadBank()
Pb = PrivatBank()
NboU = NationalBankOfUkraine()


@dp.message_handler(commands=["start"])
async def start(message):
    await bot.send_message(message.chat.id,
                           "*Привіт, це тестовий бот обміну валют.\nВикористай команду /help для інструкції.*",
                           parse_mode="Markdown")
    await message.answer_sticker(r"CAACAgIAAxkBAAEClnlg8ZrUJ3TdyfreKZDh6JJnzRJ6IAACsAEAAlbLZxHmvuuk_wzIKiAE")


@dp.message_handler(commands=["help"])
async def help(message):
    await bot.send_message(message.chat.id, "Цей бот підтримує 3 українські банки:"
                                            "\n*Приватбанк, Ощадбанк та Національний Банк України.*"
                                            "\nДля того, щоб вибрати банк використовуй такі команди:"
                                            "\n/privat          /oschad         /nbu."
                                            "\nЩоб вивести список доступних валют НБУ - /allcurrency ."
                                            "\nТи можеш в будь-який момент отримати курс валюти НБУ, вписавши її код.",
                           parse_mode="Markdown")


@dp.message_handler(commands=['allcurrency'])
async def list_currency(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="*Список доступних валют:\n*", parse_mode="Markdown")
    await bot.send_message(chat_id=message.chat.id,
                           text="*AUD 🇦🇺  Австралійський долар\nCAD 🇨🇦  Канадський долар\nCNY 🇨🇳  Юань Женьміньбі"
                                "\nHRK 🇭🇷  Куна\nCZK 🇨🇿  Чеська крона\nDKK 🇩🇰  Данська крона\nHKD 🇭🇰  Гонконгівський долар\nHUF 🇭🇺  Форинт"
                                "\nINR 🇮🇳  Індійська рупія"
                                "\nIDR 🇮🇩  Рупія\nILS 🇮🇱  Новий ізраїльський шекель\nJPY 🇯🇵  Єна\nKZT 🇰🇿  Теньге\nKRW 🇰🇷  Вона"
                                "\nMXN 🇲🇽  Мексиканське песо\nMDL 🇲🇩  Молдовський лей\nNZD 🇳🇿  Новозеландський долар\nNOK 🇳🇴  Норвезька крона\n"
                                "RUB 🇷🇺  Російський рубль\nSAR 🇸🇦  Саудівський ріял\nSGD 🇸🇬  Сінгапурський долар\nZAR 🇿🇦  Ренд"
                                "\nSEK 🇸🇪  Шведська крона\nCHF 🇨🇭  Швейцарський франк\nEGP 🇪🇬  Єгипетський фунт\nGBP 🇬🇧  Фунт стерлінгів"
                                "\nUSD 🇺🇸  Долар США\nBYN 🇧🇾  Білоруський рубль"
                                "\nRON 🇷🇴  Румунський  лей\nTRY 🇹🇷  Турецька ліра\nBGN 🇧🇬  Болгарський лев\nEUR 🇪🇺  Євро\nPLN 🇵🇱  Злотий"
                                "\nDZD 🇩🇿  Алжирський динар\nBDT 🇧🇩  Така\nAMD 🇦🇲  Вірменський драм\nIRR 🇮🇷  Іранський ріал\nIQD 🇮🇶  Іракський динар"
                                "\nKGS 🇰🇬  Сом\nLBP 🇱🇧  Ліванський фунт\nLYD 🇱🇾  Лівійський динар\nMYR 🇲🇾  Малайзійський ринггіт"
                                "\nMAD 🇲🇦  Марокканський дирхам\nPKR 🇵🇰  Пакистанська рупія\nVND 🇻🇳  Донг\nTHB 🇹🇭  Бат\nAED 🇦🇪  Дирхам ОАЕ\n"
                                "TND 🇹🇳  Туніський динар"
                                "\nUZS 🇺🇿  Узбецький сум\nTMT 🇹🇲  Туркменський новий манат\nRSD 🇷🇸  Сербський динар\nAZN 🇦🇿  Азербайджанський манат"
                                "\nTJS 🇹🇯  Сомоні\nGEL🇬🇪  Ларі\nBRL 🇧🇷  Бразильський реал*",
                           parse_mode="Markdown")


@dp.message_handler(commands=['privat'])
async def mainmenu_pb(message: types.Message):
    but_eur = types.InlineKeyboardButton(text="EUR🇪🇺", callback_data="privat-EUR")
    but_usd = types.InlineKeyboardButton(text="USD🇺🇸", callback_data="privat-USD")
    but_rub = types.InlineKeyboardButton(text="RUB🇷🇺", callback_data="privat-RUB")
    but_btc = types.InlineKeyboardButton(text="BTC💰", callback_data="privat-BTC")
    key = types.InlineKeyboardMarkup(row_width=2).add(but_eur, but_usd, but_rub, but_btc)
    await bot.send_message(message.chat.id, "*Виберіть валюту*", parse_mode="Markdown", reply_markup=key)


@dp.callback_query_handler(lambda call: call.data.split("-")[0] == "privat")
async def pb_func(call):
    data = call.data.split("-")[1]
    if data == "RUB": data = "RUR"
    await bot.send_chat_action(call.message.chat.id, 'typing')
    Pb_answer = Pb.pretify_data(Pb.get_data(data))
    await bot.send_message(call.message.chat.id, f"*{Pb_answer}*", parse_mode="Markdown")
    await call.answer()


@dp.message_handler(commands=['oschad'])
async def mainmenu_ob(message: types.Message):
    but_eur = types.InlineKeyboardButton(text="EUR🇪🇺", callback_data="oschad-EUR")
    but_usd = types.InlineKeyboardButton(text="USD🇺🇸", callback_data="oschad-USD")
    but_rub = types.InlineKeyboardButton(text="RUB🇷🇺", callback_data="oschad-RUB")
    key = types.InlineKeyboardMarkup().add(but_eur, but_usd, but_rub)
    await bot.send_message(message.chat.id, "*Виберіть валюту*", parse_mode="Markdown", reply_markup=key)


@dp.callback_query_handler(lambda call: call.data.split("-")[0] == "oschad")
async def ob_func(call):
    data = call.data.split("-")[1]
    await bot.send_chat_action(call.message.chat.id, 'typing')
    Ob_answer = Ob.pretify_data(Ob.get_data(Ob.get_code(), Ob.buy_currency(), Ob.sell_currency()), data)
    await bot.send_message(call.message.chat.id, f"*{Ob_answer}*", parse_mode="Markdown")
    await call.answer()


@dp.message_handler(commands=['nbu'])
async def mainmenu_nbu(message):
    but_eur = types.InlineKeyboardButton(text="EUR🇪🇺", callback_data="nbu-EUR")
    but_usd = types.InlineKeyboardButton(text="USD🇺🇸", callback_data="nbu-USD")
    but_rub = types.InlineKeyboardButton(text="RUB🇷🇺", callback_data="nbu-RUB")
    but_btc = types.InlineKeyboardButton(text="Інші🏳️‍🌈", callback_data="nbu-others")
    key = types.InlineKeyboardMarkup(row_width=2).add(but_eur, but_usd, but_rub, but_btc)
    await bot.send_message(message.chat.id, "*Виберіть валюту*", parse_mode="Markdown", reply_markup=key)


@dp.callback_query_handler(lambda call: call.data.split("-")[0] == "nbu")
async def nbu_func(call):
    data = call.data.split("-")[1]
    if data == "others":
        await others(message=call.message)
        await call.answer()
    else:
        await bot.send_chat_action(call.message.chat.id, 'typing')
        NboU_answer = NboU.pretify_data(NboU.get_data(data))
        await bot.send_message(call.message.chat.id, f"*{NboU_answer}*", parse_mode="Markdown")
        await call.answer()


async def others(message):
    await bot.send_message(message.chat.id, f"*Введіть, будь-ласка, код валюти верхнім регістром"
                                            "\nНаприклад, для отримання курсу Австралійського долару:* _AUD_"
                                            "\n*Для того, щоб отримати список всіх доступних валют, використовуйте команду /allcurrency*",parse_mode="Markdown")


@dp.message_handler(content_types=['text'])
async def list_currency(message: types.Message):
    country_dict = {'AUD': "🇦🇺", "CAD": "🇨🇦", "CNY": "🇨🇳", "HRK": "🇭🇷", "CZK": "🇨🇿", "DKK": "🇩🇰",
                    "HKD": "🇭🇰",
                    "HUF": "🇭🇺", "INR": "🇮🇳", "IDR": "🇮🇩", "ILS": "🇮🇱", "JPY": "🇯🇵", "KZT": "🇰🇿",
                    "KRW": "🇰🇷", "MXN": "🇲🇽",
                    "MDL": "🇲🇩", "NZD": "🇳🇿", "NOK": "🇳🇴", "RUB": "🇷🇺", "SAR": "🇸🇦", "SGD": "🇸🇬",
                    "ZAR": "🇿🇦", "SEK": "🇸🇪",
                    "CHF": "🇨🇭", "EGP": "🇪🇬", "GBP": "🇬🇧", "USD": "🇺🇸", "BYN": "🇧🇾", "RON": "🇷🇴",
                    "TRY": "🇹🇷", "BGN": "🇧🇬",
                    "EUR": "🇪🇺", "PLN": "🇵🇱", "DZD": "🇩🇿", "BDT": "🇧🇩", "AMD": "🇦🇲", "IRR": "🇮🇷",
                    "IQD": "🇮🇶", "KGS": "🇰🇬", "LBP": "🇱🇧", "LYD": "🇱🇾", "MYR": "🇲🇾", "MAD": "🇲🇦",
                    "PKR": "🇵🇰", "VND": "🇻🇳",
                    "THB": "🇹🇭", "AED": "🇦🇪", "TND": "🇹🇳", "UZS": "🇺🇿", "TMT": "🇹🇲", "RSD": "🇷🇸",
                    "AZN": "🇦🇿", "TJS": "🇹🇯", "GEL": "🇬🇪", "BRL": "🇧🇷"}
    if message.text in country_dict:
        await nbu_func2(message, message.text)
    else:
        await bot.send_message(chat_id=message.chat.id, text="*Я незнаю такої валюти!*", parse_mode="Markdown")


async def nbu_func2(message, data):
    await bot.send_chat_action(message.chat.id, 'typing')
    NboU_answer = NboU.pretify_data(NboU.get_data(data))
    await bot.send_message(message.chat.id, f"*{NboU_answer}*", parse_mode="Markdown")


if __name__ == '__main__':
    executor.start_polling(dp)
