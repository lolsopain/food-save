import os
import telebot
from telebot import types
import requests

# ENV orqali olish
BOT_TOKEN = os.getenv("8692490877:AAHvz4SOORQlxDoK16nY3XgJctzmgDlU5yA")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN topilmadi!")

bot = telebot.TeleBot(BOT_TOKEN)

# Render API URL
API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://food-save.onrender.com/api"
)

user_steps = {}

# =========================
# START
# =========================

@bot.message_handler(commands=['start'])
def send_welcome(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn_foods = types.KeyboardButton("🛒 Taomlar vitrinasi")
    btn_help = types.KeyboardButton("ℹ️ Loyiha haqida")

    markup.add(btn_foods, btn_help)

    bot.send_message(
        message.chat.id,
        f"Salom {message.from_user.first_name} 👋\n\n"
        f"FoodSave botiga xush kelibsiz!",
        reply_markup=markup
    )

# =========================
# SHOW FOODS
# =========================

@bot.message_handler(func=lambda message: message.text == "🛒 Taomlar vitrinasi")
def show_foods(message):

    bot.send_message(
        message.chat.id,
        "🔄 Taomlar yuklanmoqda..."
    )

    try:

        response = requests.get(
            f"{API_BASE_URL}/foods/",
            timeout=15
        )

        if response.status_code != 200:
            bot.send_message(
                message.chat.id,
                "❌ API bilan bog‘lanib bo‘lmadi."
            )
            return

        data = response.json()

        # pagination support
        foods = data["results"] if isinstance(data, dict) and "results" in data else data

        if not foods:
            bot.send_message(
                message.chat.id,
                "📭 Hozircha taomlar yo‘q."
            )
            return

        for food in foods:

            if food.get("is_booked"):
                continue

            food_type = (
                "🔥 Yangi"
                if food.get("food_type") == "new"
                else "🍃 Qolgan"
            )

            price = food.get("price", "Noma'lum")

            caption = (
                f"🍔 Taom: {food.get('name')}\n"
                f"📝 {food.get('description', 'Tavsif yo‘q')}\n"
                f"💰 Narx: {price}\n"
                f"📌 Turi: {food_type}"
            )

            markup = types.InlineKeyboardMarkup()

            buy_btn = types.InlineKeyboardButton(
                "🛍️ Buyurtma qilish",
                callback_data=f"buy_{food['id']}"
            )

            markup.add(buy_btn)

            image = food.get("image")

            # Rasm bo‘lsa photo yuboradi
            if image:
                try:
                    bot.send_photo(
                        message.chat.id,
                        image,
                        caption=caption,
                        reply_markup=markup
                    )
                except:
                    bot.send_message(
                        message.chat.id,
                        caption,
                        reply_markup=markup
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    caption,
                    reply_markup=markup
                )

    except Exception as e:

        print(e)

        bot.send_message(
            message.chat.id,
            "❌ Serverda xatolik yuz berdi."
        )

# =========================
# ABOUT
# =========================

@bot.message_handler(func=lambda message: message.text == "ℹ️ Loyiha haqida")
def about_project(message):

    text = (
        "FoodSave — oziq-ovqat isrofini kamaytirishga "
        "qaratilgan platforma."
    )

    bot.send_message(message.chat.id, text)

# =========================
# BUY BUTTON
# =========================

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def handle_buy_callback(call):

    food_id = int(call.data.split("_")[1])

    chat_id = call.message.chat.id

    user_steps[chat_id] = {
        "food_id": food_id
    }

    msg = bot.send_message(
        chat_id,
        "👤 Ismingizni kiriting:"
    )

    bot.register_next_step_handler(
        msg,
        process_name_step
    )

# =========================
# NAME STEP
# =========================

def process_name_step(message):

    chat_id = message.chat.id

    if chat_id not in user_steps:
        return

    user_steps[chat_id]["client_name"] = message.text

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    btn_phone = types.KeyboardButton(
        "📱 Telefon yuborish",
        request_contact=True
    )

    markup.add(btn_phone)

    msg = bot.send_message(
        chat_id,
        "📞 Telefon raqamingizni yuboring:",
        reply_markup=markup
    )

    bot.register_next_step_handler(
        msg,
        process_phone_step
    )

# =========================
# PHONE STEP
# =========================

def process_phone_step(message):

    chat_id = message.chat.id

    if chat_id not in user_steps:
        return

    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text

    user_steps[chat_id]["client_phone"] = phone

    order_data = {
        "food": user_steps[chat_id]["food_id"],
        "client_name": user_steps[chat_id]["client_name"],
        "client_phone": phone,
        "delivery_type": "pickup",
        "payment_method": "cash"
    }

    bot.send_message(
        chat_id,
        "⏳ Buyurtma yuborilmoqda..."
    )

    try:

        res = requests.post(
            f"{API_BASE_URL}/reservations/",
            json=order_data,
            timeout=15
        )

        main_markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True
        )

        main_markup.add(
            types.KeyboardButton("🛒 Taomlar vitrinasi"),
            types.KeyboardButton("ℹ️ Loyiha haqida")
        )

        if res.status_code in [200, 201]:

            bot.send_message(
                chat_id,
                "✅ Buyurtmangiz qabul qilindi!",
                reply_markup=main_markup
            )

        else:

            print(res.text)

            bot.send_message(
                chat_id,
                "❌ Buyurtma yuborilmadi.",
                reply_markup=main_markup
            )

    except Exception as e:

        print(e)

        bot.send_message(
            chat_id,
            "❌ Server bilan bog‘lanishda xatolik."
        )

    del user_steps[chat_id]

# =========================
# RUN
# =========================

if __name__ == "__main__":

    print("🤖 Bot ishga tushdi...")

    bot.infinity_polling(
        skip_pending=True
    )