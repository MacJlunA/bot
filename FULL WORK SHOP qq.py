import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import aiohttp
import time
import datetime
from aiogram.fsm.storage.memory import MemoryStorage
import random

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if TOKEN is None:
    raise ValueError("Token error")

BLOCKCYPHER_TOKEN = os.getenv("BLOCKCYPHER_TOKEN")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
MONOBANK_API_KEY = os.getenv("MONOBANK_API_KEY")

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

users = [7053825090]

def add_user(user_id):
    if user_id not in users:
        users.append(user_id)

products = {
    "product_1": {"name": "🤍 Мефедрон Rolex 2g", "price": 900, "description": "Кристаллический мефедрон янтарного цвета, он же Шампань! Звонкий хруст стекла под картой гарантирует уникальное произведение искусства, наслаждаясь которым невозможно остановиться.", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/mefedron.jpg"},
    "product_2": {"name": "💎 Alpha-PvP VHQ 0.5g", "price": 300, "description": "Чистейшие кристаллы, приготовленные руками настоящего доктора Хайзенберг в мире Альфы-PVP ", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/alphapvp.jpg"},
    "product_3": {"name": "❌ Alpha-PvP VHQ 1g", "price": 550, "description": "Чистейшие кристаллы, приготовленные руками настоящего доктора Хайзенберг в мире Альфы-PVP ", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/alphapvp.jpg"},
    "product_4": {"name": "💎 Alpha-PvP VHQ 2g", "price": 850, "description": "Чистейшие кристаллы, приготовленные руками настоящего доктора Хайзенберг в мире Альфы-PVP ", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/alphapvp.jpg"},
    "product_5": {"name": "❌ Грибы Pink Buffalo 2g", "price": 600, "description": "Галлюциногенное действие, влияние на нервную систему, приятное ощущение расслабления. Рекомендуемая доза 1-2г.", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/mushrooms.jpg"},
    "product_6": {"name": "❌ Грибы Pink Buffalo 3g", "price": 850, "description": "Галлюциногенное действие, влияние на нервную систему, приятное ощущение расслабления. Рекомендуемая доза 1-2г.", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/mushrooms.jpg"},
    "product_7": {"name": "🌿 Шишки White Widow 2g", "price": 500, "description": "Сильные сативные шишки 19-20% THC", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/trava.jpg"},
    "product_8": {"name": "🌿 Шишки White Widow 5g", "price": 1150, "description": "Сильные сативные шишки 19-20% THC", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/trava.jpg"},
    "product_9": {"name": "🌿 Шишки White Widow 10g", "price": 2200, "description": "Сильные сативные шишки 19-20% THC", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/trava.jpg"},
    "product_10": {"name": "🌿 Шишки White Widow 20g", "price": 4600, "description": "Сильные сативные шишки 19-20% THC", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/trava.jpg"},
    "product_11": {"name": "❌ MDA Adam 1g - 1400 грн", "price": 1400, "description": "Кристаллический тенамфетамин. Дарит длинную эмпатию, стимуляцию и эйфорию с нотами психоделии. Рекомендуемая оральная доза 60-150мг", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/mda.jpeg"},
    "product_12": {"name": "🤍 Amphetamine White Power 2g", "price": 550, "description": "Стимулятор центральной нервной системы. Рекомендуемая доза 50-100мг", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/Amphetamine.jpg"},
    "product_13": {"name": "❌ Amphetamine White Power 5g", "price": 1300, "description": "Стимулятор центральной нервной системы. Рекомендуемая доза 50-100мг", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/Amphetamine.jpg"},
    "product_14": {"name": "🤍 Amphetamine White Power 10g", "price": 2600, "description": "Стимулятор центральной нервной системы. Рекомендуемая доза 50-100мг", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/Amphetamine.jpg"},
    "product_15": {"name": "❌ LSD-25 Acid 175 MG 🗂 1pcx", "price": 400, "description": "Реальность тает, краски взрываются, сознание расширяется, переплетая фантазии с бесконечностью. Мир вокруг – живое полотно, где каждая мысль становится искусством! Дозировка 150-300 мг", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/lsd.jpg"},
    "product_16": {"name": "🗂 LSD-25 Acid 175 MG 🗂 3pcx", "price": 1000, "description": "Реальность тает, краски взрываются, сознание расширяется, переплетая фантазии с бесконечностью. Мир вокруг – живое полотно, где каждая мысль становится искусством! Дозировка 150-300 мг", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/lsd.jpg"},
    "product_17": {"name": "🌿 Шишки 🌿 AK-47 5g", "price": 1200, "description": "Тепличные сативные шишки. 21-22% THC", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/trava2.jpg"},
    "product_18": {"name": "🌿 Шишки 🌿 AK-47 10g", "price": 2150, "description": "Тепличные сативные шишки. 21-22% THC", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/trava2.jpg"},
    "product_19": {"name": "🎁 1 x 300mg MDMA Punisher", "price": 350, "description": "Экстази из Амстердама. Двойная доза, новичкам начинать с половинки. Цвет таблеток может отличаться от партии к партии.", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/extazy.jpg"},
    "product_20": {"name": "💊 1 x Xanax", "price": 450, "description": "Гасит тревогу, как тёплый плед в холодный вечер. Внутренний штиль, лёгкость и спокойствие – просто расслабься и дыши ровно.", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/xanax.jpg"},
    "product_21": {"name": "💊 3 x Xanax", "price": 1300, "description": "Гасит тревогу, как тёплый плед в холодный вечер. Внутренний штиль, лёгкость и спокойствие – просто расслабься и дыши ровно.", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/xanax.jpg"},
    "product_22": {"name": "💊 14 x Lirika", "price": 2500, "description": "Мягкая волна расслабления накрывает с головой, растворяя тревоги и напряжение. Легкость, умиротворение и капля блаженства – наслаждайся моментом!", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/lirika.jpg"},
    "product_23": {"name": "💊 28 x Lirika", "price": 4700, "description": "Мягкая волна расслабления накрывает с головой, растворяя тревоги и напряжение. Легкость, умиротворение и капля блаженства – наслаждайся моментом!", "photo": "https://raw.githubusercontent.com/MacJlunA/123123q/main/lirika.jpg"}
}

districts = {
    "kiev": [
        "🌃 Теремки ✅ (Прикоп)",
        "🌃 Академгородок 🌃 (Магнит)",
        "🌃 Осокорки ❌",
        "🌃 Позняки ✅ (Магнит)",
        "🌃 Иподром ❌",
        "🌃 Соломенский ✅ (Магнит)",
        "🌃 Шулявка ✅ (Магнит)",
        "🌃 Кадетский Гай ✅ (Прикоп)",
        "🌃 Борщаговка ❌",
        "🌃 Вокзальная ✅ (Прикоп)",
        "🌃 Чоколовка ✅ (Магнит)",
        "🌃 Палац спорта ✅ (Магнит)",
        "🌃 Лесовой ❌",
        "🌃 Голосеевская ✅ (Магнит)",
        "🌃 Выдубичи ✅ (Магнит)",
        "🌃 Левобережная ✅ (Магнит)",
        "🌃 Нивки ✅ (Магнит)",
        "🌃 Индустриальный ✅ (Магнит)",
        "🌃 Красный Хутор ❌",
        "🌃 Демеевская ✅ (Магнит)",
    ],
    "lviv": [
        "🌃 Центр ✅ (Магнит)",
        "🌃 Сихов ✅ (Прикоп)",
        "🌃 Железнодорожный ❌ (Прикоп)",
        "🌃 Шевченковский ✅ (Прикоп)",
        "🌃 Франковский ✅ (Магнит)",

    ],
    "odesa": [
        "🌃 Центр ✅ (Магнит)",
        "🌃 Аркадия ✅ (Магнит)",
        "🌃 Таирово ❌",
        "🌃 Черноморск ✅ (Магнит)",
        "🌃 Аркадия ✅ (Прикоп)",
        "🌃 Хаджибей ❌",
        "🌃 Лиманка ✅ (Прикоп)",
        "🌃 Киевский ✅ (Прикоп)",
    ],
    "zaporizhzhia": [
        "🌃 Центр ✅ (Магнит)",
        "🌃 Хортица ✅ (Прикоп)",
        "🌃 Вознесеновский ❌",
        "🌃 Кичкас ✅ (Прикоп)",
        "🌃 Заводской ✅ (Магнит)",
        "🌃 Александровский  ❌",
        "🌃 Шевченковский ❌",
        "🌃 Днепровский ✅ (Магнит)",
    ],
    "sumy": [
        "🌃 Химки ✅ (Прикоп)",
        "🌃 Автовокзал (Аэропорт) ✅ (Прикоп)",
        "🌃 Кирово ✅ (Прикоп)",
        "🌃 Заречный ✅ (Прикоп)",

        ]
}

@dp.message(Command("help"))
async def send_help(message: types.Message):
    help_text = """🙋 Привет Бро 🙋
Это бот 🥇 KYIV THC BOT 🥇
────────────────────────────

❓ /help - помощь по боту ❓

────────────────────────────
⠀⠀⠀⠀⬇️⬇️⬇️ КОНТАКТЫ ⬇️⬇️⬇️

❤️ОПЕРАТОР ПОЧТОВЫХ ЗАКАЗОВ - @operator_thc ❤️

❤️ОПЕРАТОР ПО НЕНАХОДАМ - @operator_thc ❤️

❤️!ВНИМАНИЕ, по ненаходам и проблемным ситуациям с кладами обращаться только к @operator_thc , ЗАСОРЯЯ ЛС ДРУГИХ СОТРУДНИКОВ НЕ ПО ЕГО СПЕЦИАЛИЗАЦИИ - БАН!

❤️Чтобы вернуться в меню и начать сначала нажмите 👉 /start ❤️
"""
    await message.answer(help_text)

@dp.message(Command("start"))
async def start_command(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏛 Киев 🏛", callback_data="city_kiev")],
        [InlineKeyboardButton(text="🏢 Львов 🏢", callback_data="city_lviv")],
        [InlineKeyboardButton(text="🌊 Одесса 🌊", callback_data="city_odesa")],
        [InlineKeyboardButton(text="🏭 Запорожье 🏭", callback_data="city_zaporizhzhia")],
        [InlineKeyboardButton(text="🌁 Сумы 🌁", callback_data="city_sumy")],
    ])
    start_text = """🙋 Привет Бро 🙋
Это бот 🥇 KYIV THC BOT 🥇
Выбирай город и погнали 🥇
────────────────────────────

❓ /help - помощь по боту ❓

────────────────────────────
"""
    await message.answer(start_text + "\n Выберите город", reply_markup=keyboard)

@dp.message(Command("broadcast"))
async def broadcast_command(message: types.Message):
    if message.from_user.id not in [600790285]:  # Замените на ID админа
        await message.answer("У вас нет прав для использования этой команды.")
        return

    broadcast_text = message.text.replace("/broadcast ", "")
    for user_id in users:
        try:
            await bot.send_message(chat_id=user_id, text=broadcast_text)
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

    await message.answer("Сообщение отправлено всем пользователям.")

@dp.callback_query(lambda c: c.data.startswith("city_"))
async def city_selected(callback_query: types.CallbackQuery, state: FSMContext):
    city_code = callback_query.data.split("_")[1]
    city_names = {
        "kiev": "Киев",
        "lviv": "Львов",
        "odesa": "Одесса",
        "zaporizhzhia": "Запорожье",
        "sumy": "Сумы",
    }

    city_name = city_names.get(city_code, "Неизвестный город")

    await state.update_data(city=city_code)

    product_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🤍 Мефедрон 🤍 Rolex 2g - 900 грн", callback_data="product_1"),
        InlineKeyboardButton(text="💎 Alpha-PvP 💎 VHQ 0.5g - 300 грн", callback_data="product_2")
    ],
    [
        InlineKeyboardButton(text="❌ Alpha-PvP 💎 VHQ 1g - 450 грн ", callback_data="product_3"),
        InlineKeyboardButton(text="💎 Alpha-PvP 💎 VHQ 2g - 850 грн", callback_data="product_4")
    ],
    [
        InlineKeyboardButton(text="❌ Грибы 🍄 Pink Buffalo 2g - 600 грн", callback_data="product_5"),
        InlineKeyboardButton(text="❌ Грибы 🍄 Pink Buffalo 3g - 850 грн", callback_data="product_6"),
    ],
    [
        InlineKeyboardButton(text="🌿 Шишки 🌿 White Widow 2g - 500 грн", callback_data="product_7"),
        InlineKeyboardButton(text="🌿 Шишки 🌿 White Widow 5g - 1150 грн", callback_data="product_8"),
    ],
    [
        InlineKeyboardButton(text="🌿 Шишки 🌿 White Widow 10g - 2200 грн", callback_data="product_9"),
        InlineKeyboardButton(text="🌿 Шишки 🌿 White Widow 20g - 4000 грн", callback_data="product_10"),
    ],
    [
        InlineKeyboardButton(text="❌ MDA 🤍 Adam 1g - 1400 грн", callback_data="product_11"),
        InlineKeyboardButton(text="🤍 Amphetamine 🤍 White Power 2g - 550 грн", callback_data="product_12"),
    ],
    [
        InlineKeyboardButton(text="❌ Amphetamine 🤍 White Power 5g - 1300 грн", callback_data="product_13"),
        InlineKeyboardButton(text="🤍 Amphetamine 🤍 White Power 10g - 2600 грн", callback_data="product_14"),
    ],
    [
        InlineKeyboardButton(text="❌ LSD-25 Acid 175 MG 🗂 1pcx - 400 грн", callback_data="product_15"),
        InlineKeyboardButton(text="🗂 LSD-25 Acid 175 MG 🗂 3pcx - 1000 грн", callback_data="product_16"),
    ],
    [
        InlineKeyboardButton(text="🌿 Шишки 🌿 AK-47 5g - 1200 грн", callback_data="product_17"),
        InlineKeyboardButton(text="🌿 Шишки 🌿 AK-47 10g - 2150 грн", callback_data="product_18"),
    ],
    [
        InlineKeyboardButton(text="🎁 1 x 300mg MDMA Punisher - 350 грн", callback_data="product_19"),
        InlineKeyboardButton(text="💊 1 x Xanax - 450 грн", callback_data="product_20"),
    ],
    [
        InlineKeyboardButton(text="💊 3 x Xanax - 1300 грн", callback_data="product_21"),
        InlineKeyboardButton(text="💊 14 x Лирика - 2500 грн", callback_data="product_22"),
    ],
    [
        InlineKeyboardButton(text="💊 28 x Лирика - 4700 грн", callback_data="product_23"),
        InlineKeyboardButton(text="◀️ Назад ◀️", callback_data="back_to_city")
    ]
])

    await callback_query.message.answer(f"Выбран город: 🏛 {city_name} 🏛\nВыберите товар", reply_markup=product_keyboard)
    await callback_query.answer()


@dp.callback_query(lambda c: c.data.startswith("product_"))
async def product_selected(callback_query: types.CallbackQuery, state: FSMContext):
    product_code = callback_query.data.split("_")[1]
    product = products.get(f"product_{product_code}")
    product_name = product["name"]
    product_price = product["price"]
    product_description = product["description"]
    product_photo = product["photo"]

    if "❌" in product_name:
        await callback_query.message.answer("❌ Товара нет в наличии, зайдите позже ❌")
        return

    await state.update_data(product=product_name, price=product_price, description=product_description)

    user_data = await state.get_data()
    city_name = user_data.get("city", "kiev")

    city_districts = districts.get(city_name, [])

    if not city_districts:
        await callback_query.message.answer(f"Извините, для города {city_name.get(city_name, 'Неизвестный город')} районы недоступны.")
        return

    district_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=district, callback_data=f"district_{i+1}")]
        for i, district in enumerate(city_districts)
    ] + [[InlineKeyboardButton(text="◀️ Назад ◀️", callback_data=f"city_{city_name}")]])

    await callback_query.message.answer_photo(product_photo, caption=f"Выбран товар: {product_name}\n ➖➖➖➖➖➖➖➖➖➖➖➖ \n Теперь выберите район", reply_markup=district_keyboard)
    await callback_query.answer()

@dp.callback_query(lambda c: c.data == "back_to_city")
async def back_to_city(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏛 Киев 🏛", callback_data="city_kiev")],
        [InlineKeyboardButton(text="🏢 Львов 🏢", callback_data="city_lviv")],
        [InlineKeyboardButton(text="🌊 Одесса 🌊", callback_data="city_odesa")],
        [InlineKeyboardButton(text="🏭 Запорожье 🏭", callback_data="city_zaporizhzhia")],
        [InlineKeyboardButton(text="🌁 Сумы 🌁", callback_data="city_sumy")],
    ])
    await callback_query.message.answer("Пожалуйста, выберите город:", reply_markup=keyboard)
    await callback_query.answer()


@dp.callback_query(lambda c: c.data.startswith("district_"))
async def district_selected(callback_query: types.CallbackQuery, state: FSMContext):
    district_index = int(callback_query.data.split("_")[1]) - 1
    user_data = await state.get_data()
    city_name = user_data.get("city", "Киев")

    city_districts = districts.get(city_name.lower(), [])

    if district_index < 0 or district_index >= len(city_districts):
        district_name = "Неизвестный район"
    else:
        district_name = city_districts[district_index]

    await state.update_data(district=district_name)

    product_name = user_data.get("product", "Неизвестный товар")
    product_price = user_data.get("price", 0)
    product_description = user_data.get("description", "Описание отсутствует")

    payment_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💸 Bitcoin 💸", callback_data="payment_bitcoin")],
        [InlineKeyboardButton(text="💲 USDT TRC20 💲", callback_data="payment_usdt")],
        [InlineKeyboardButton(text="💳 Перевод на карту | БЕЗ % 💳", callback_data="payment_card")],
        [InlineKeyboardButton(text="◀️ Назад ◀️", callback_data="back_to_city")]
    ])

    await callback_query.message.answer(
        f"🏠 Город: {city_name}\n"
        f"🎁 Товар: {product_name}\n"
        f"📜 Описание: {product_description}\n"
        f"💰 Стоимость: {product_price}₴\n"
        f"🏃 Район: {district_name}\n"
        "────────────────────────────\n"
        "💰 Выберите метод оплаты: 💰\n"
        "────────────────────────────\n"
        "👉 Чтобы вернуться в меню и начать сначала нажмите 👉 /start",
        reply_markup=payment_keyboard
    )
    await callback_query.answer()

async def get_btc_to_uah_rate():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=uah"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data['bitcoin']['uah']
            else:
                return None

async def check_bitcoin_payment(address, expected_amount):
    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance"
    headers = {
        "Authorization": f"Bearer {BLOCKCYPHER_TOKEN}"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                total_received = data['total_received']

                if total_received >= expected_amount:
                    return True
                else:
                    return False
            else:
                raise Exception("Ошибка при запросе к BlockCypher API")

def generate_order_id():
    return str(random.randint(100000, 999999))

@dp.callback_query(lambda c: c.data == "payment_bitcoin")
async def payment_bitcoin(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    city_name = user_data.get("city", "Неизвестный город")
    product_name = user_data.get("product", "Неизвестный товар")
    product_price = user_data.get("price", 0)
    district_name = user_data.get("district", "Неизвестный район")
    btc_to_uah_rate = await get_btc_to_uah_rate()

    if btc_to_uah_rate is None:
        await callback_query.message.answer("❌ Не удалось получить актуальный курс биткоина, попробуйте позже ❌")
        return

    btc_amount = product_price / btc_to_uah_rate
    time.sleep(2)
    message_text = (
        "🏃 Заказ создан, адрес забронирован!\n"
        "💱 Время брони 90 минут!\n"
        "⠀⠀⠀\n"
        f"🏠 Город:🏛 {city_name} 🏛\n"
        f"🎁 Товар: {product_name}\n"
        f"💰 Стоимость: {product_price}₴\n"
        f"🏃 Район: {district_name}\n"
        f"💱 Метод оплаты: Bitcoin\n"
        "────────────────────────────\n"
        "❓ /help - помощь по боту ❓\n"
        "────────────────────────────\n"
        f"💳 Переведите {btc_amount:.8f} BTC на кошелек 💳\n"
        "⠀⠀⠀⠀⠀⠀\n"
        "💰 <code>127cXY4Lqk4847FQXps7WM16Zxh9KHNaA7</code> 💰\n"
        "⠀⠀⠀⠀⠀⠀\n"
        "❗️ После перевода нажмите ПРОВЕРИТЬ ОПЛАТУ ❗️\n"
        "❗️ ВНИМАТЕЛЬНО проверяйте платежные реквизиты ❗️\n"
        "❗️ Чтобы скопировать реквизиты просто нажмите на них ❗️\n"
        "❗️ Если вы перевели не ту сумму которую выдал бот, свяжитесь с оператором @operator_thc ❗️\n"
        "❗️ Перед нажатием ПРОВЕРИТЬ ОПЛАТУ подождите 5-10 минут ❗️\n"
        "────────────────────────────\n\n"
        "Чтобы вернуться в меню и начать сначала нажмите 👉 /start"
    )

    payment_keyboard2 = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Проверить оплату 💰", callback_data="check_payment")],
        [InlineKeyboardButton(text="❌ Отменить оплату ❌", callback_data="confirm_cancel_payment")]
    ])

    await callback_query.message.answer(message_text, reply_markup=payment_keyboard2, parse_mode="HTML")
    await callback_query.answer()

@dp.callback_query(lambda c: c.data == "confirm_cancel_payment")
async def confirm_cancel_payment(callback_query: types.CallbackQuery):
    confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Да, отменить ❌", callback_data="cancel_payment")],
        [InlineKeyboardButton(text="💰 Нет, вернуться 💰", callback_data="payment_bitcoin")]
    ])

    await callback_query.message.answer("❓ Вы точно хотите отменить оплату? ❓", reply_markup=confirm_keyboard)
    await callback_query.answer()

@dp.callback_query(lambda c: c.data == "cancel_payment")
async def cancel_payment(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("✅ Заказ был отменен ✅")
    await state.clear()
    await callback_query.answer()

@dp.callback_query(lambda c: c.data == "payment_bitcoin")
async def back_to_payment(callback_query: types.CallbackQuery):
    await callback_query.message.answer("💰 Возвращаемся к оплате 💰")
    await callback_query.answer()


@dp.callback_query(lambda c: c.data == "check_payment")
async def check_payment_callback(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    order_id = user_data.get("order_id")
    target_amount = user_data.get("price", 0)
    payment_method = user_data.get("payment_method", "")

    if not order_id or not target_amount:
        await callback_query.message.answer("❌ Данные заказа не найдены ❌")
        return

    success, message = await check_payment(order_id, target_amount, payment_method)

    if success:
        await callback_query.message.answer(f"✅ Оплата подтверждена! {message}")
    else:
        await callback_query.message.answer(f"❌ Оплата не найдена для заказа {order_id}. {message}")

    await callback_query.answer()

async def get_usdt_to_uah_rate():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=uah"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data['tether']['uah']
            else:
                return None


@dp.callback_query(lambda c: c.data == "payment_usdt")
async def payment_usdt(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    city_name = user_data.get("city", "Неизвестный город")
    product_name = user_data.get("product", "Неизвестный товар")
    product_price = user_data.get("price", 0)
    district_name = user_data.get("district", "Неизвестный район")

    usdt_to_uah_rate = await get_usdt_to_uah_rate()

    if usdt_to_uah_rate is None:
        await callback_query.message.answer("❌ Не удалось получить актуальный курс usdt, напишите в лс @operator_thc ❌")
        return

    usdt_amount = product_price / usdt_to_uah_rate
    time.sleep(2)
    message_text = (
        "🏃 Заказ создан, адрес забронирован!\n"
        "💱 Время брони 90 минут!\n"
        "⠀⠀⠀⠀⠀⠀\n"
        f"🏠 Город: 🏛 {city_name} 🏛\n"
        f"🎁 Товар: {product_name}\n"
        f"💰 Стоимость: {product_price}₴\n"
        f"🏃 Район: {district_name}\n"
        f"💱 Метод оплаты: USDT TRC20\n\n"
        "────────────────────────────\n"
        "❓ /help - помощь по боту ❓\n"
        "────────────────────────────\n"
        f"💳 Переведите {usdt_amount:.8f} USDT на кошелек 💳\n"
        "⠀⠀⠀⠀⠀⠀\n"
        "💰 <code>TDhhazay3wD5eN1E42udFF1JqdLn2ygE1f</code> 💰\n"
        "⠀⠀⠀⠀⠀⠀\n"
        "❗️ После перевода нажмите ПРОВЕРИТЬ ОПЛАТУ ❗️\n"
        "❗️ ВНИМАТЕЛЬНО проверяйте платежные реквизиты ❗️\n"
        "❗️ Чтобы скопировать реквизиты просто нажмите на них ❗️\n"
        "❗️ Если вы перевели не ту сумму которую выдал бот, свяжитесь с оператором @operator_thc ❗️\n"
        "❗️ Перед нажатием ПРОВЕРИТЬ ОПЛАТУ подождите 5-10 минут ❗️\n"
        "────────────────────────────\n\n"
        "Чтобы вернуться в меню и начать сначала нажмите 👉 /start"
    )

    payment_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Проверить оплату 💰", callback_data="check_payment")],
        [InlineKeyboardButton(text="❌ Отменить оплату❌ ", callback_data="city_kiev")]
    ])

    await callback_query.message.answer(message_text, reply_markup=payment_keyboard, parse_mode="HTML")
    await callback_query.answer()

async def get_transactions():
    headers = {"X-Token": MONOBANK_API_KEY}
    url = "https://api.monobank.ua/personal/statement/0/"

    now = int(datetime.datetime.now().timestamp())
    since = now - 3 * 60 * 60

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{url}{since}/{now}", headers=headers, timeout=10) as response:
                if response.status == 200:
                    transactions = await response.json()
                    return transactions
                else:
                    print(f"❌ Не удалось получить транзакции, статус: {response.status} ❌")
                    return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

async def check_payment(order_id: str, target_amount: float, payment_method: str):
    transactions = await get_transactions()

    if not transactions:
        return False, "❌ Не удалось получить транзакции ❌"

    unique_transactions = {tx['id']: tx for tx in transactions}.values()

    for tx in unique_transactions:
        amount = tx.get("amount", 0) / 100
        comment = tx.get("comment", "").strip()

        print(f"Checking transaction: {tx}, Amount: {amount}, Comment: {comment}")

        if abs(amount) == target_amount and comment == order_id:
            return True, f"✅ Оплата найдена! ID заказа: {comment} ✅"

        if comment == order_id:
            return False, f"❌ Оплата не найдена: сумма {amount} не совпадает с ожидаемой ❌"

    return False, "Оплата не найдена!"


def generate_order_id():
    return str(random.randint(100000, 999999))

@dp.callback_query(lambda c: c.data == "payment_card")
async def payment_card(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    city_name = user_data.get("city", "Неизвестный город")
    product_name = user_data.get("product", "Неизвестный товар")
    product_price = user_data.get("price", 0)
    district_name = user_data.get("district", "Неизвестный район")

    order_id = generate_order_id()

    await state.update_data(order_id=order_id)

    message_text = (
        "🏃 Заказ создан, адрес забронирован!\n"
        "💱 Время брони 90 минут!\n"
        f"🏠 Город:🏛 {city_name} 🏛\n"
        f"🎁 Товар: {product_name}\n"
        f"💰 Стоимость: {product_price:.2f}₴\n"
        f"🏃 Район: {district_name}\n"
        f"💱 Метод оплаты: Перевод на карту\n"
        "────────────────────────────\n"
        f"💰 Переведите сумму {product_price:.2f}₴ на карту и укажите ID заказа в комментарии!\n"
        f"💳 Номер карты: <code>5355 2800 2980 0776</code>\n"
        f"🆔 ID заказа (укажите в комментарии к платежу): <code>{order_id}</code>\n"
        "────────────────────────────\n"
        "❗️ После перевода нажмите ПРОВЕРИТЬ ОПЛАТУ ❗️\n"
        "❗️ Если перевели не ту сумму, свяжитесь с @operator_thc ❗️\n"
        "────────────────────────────\n\n"
        "Чтобы вернуться в меню нажмите 👉 /start"
    )

    payment_keyboard2 = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Проверить оплату 💰", callback_data="check_payment")],
        [InlineKeyboardButton(text="❌ Отменить оплату ❌", callback_data="confirm_cancel_payment")]
    ])

    await callback_query.message.answer(message_text, reply_markup=payment_keyboard2, parse_mode="HTML")
    await callback_query.answer()
    await asyncio.sleep(1)

@dp.callback_query(lambda c: c.data == "confirm_cancel_payment")
async def confirm_cancel_payment(callback_query: types.CallbackQuery):
    confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Да, отменить ❌", callback_data="cancel_payment")],
        [InlineKeyboardButton(text="💰 Нет, вернуться 💰", callback_data="back_to_payment")]
    ])

    await callback_query.message.answer("❓ Вы точно хотите отменить оплату? ❓", reply_markup=confirm_keyboard)
    await callback_query.answer()

@dp.callback_query(lambda c: c.data == "cancel_payment")
async def cancel_payment(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("✅ Заказ был отменен ✅")
    await state.clear()
    await callback_query.answer()

@dp.callback_query(lambda c: c.data == "back_to_payment")
async def back_to_payment(callback_query: types.CallbackQuery):
    await callback_query.message.answer("💰 Возвращаемся к оплате 💰")
    await callback_query.answer()


async def main():
    print("Магазин включен..")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())