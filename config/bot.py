import os
import telebot
from telebot import types
import requests

# Bot Tokeningizni @BotFather'dan olib shu yerga qo'ying
BOT_TOKEN = "8692490877:AAHvz4SOORQlxDoK16nY3XgJctzmgDlU5yA" 
bot = telebot.TeleBot(BOT_TOKEN)

# Django API manzili (Mahalliyda http://127.0.0.1:8000, Render'da o'zingizning havolangiz)
# Render havolangiz: 'https://food-save.onrender.com/api'
API_BASE_URL = 'http://127.0.0.1:8000/api'

# Foydalanuvchi buyurtma berish jarayonidagi vaqtinchalik ma'lumotlarni saqlash uchun
user_steps = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_foods = types.KeyboardButton("🛒 Taomlar vitrinasi")
    btn_help = types.KeyboardButton("ℹ️ Loyiha haqida")
    markup.add(btn_foods, btn_help)
    
    bot.send_message(
        message.chat.id, 
        f"Xush kelibsiz, {message.from_user.first_name}!\nFoodSave botiga xush kelibsiz. Bu yerda siz restoranlardagi eng arzon va mazali aksiya taomlarini buyurtma qilishingiz mumkin.", 
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "🛒 Taomlar vitrinasi")
def show_foods(message):
    bot.send_message(message.chat.id, "🔄 Taomlar ro'yxati bazadan yuklanmoqda...")
    
    try:
        # Django API'dan taomlarni olish
        response = requests.get(f"{API_BASE_URL}/foods/")
        if response.status_code == 200:
            foods = response.json()
            
            if not foods:
                bot.send_message(message.chat.id, "Hozircha vitrinada taomlar mavjud emas.")
                return
                
            for food in foods:
                food_type = "Aksiya 🔥" if food['food_type'] == 'new' else "Ortib qolgan (Isrofga qarshi) 🍃"
                caption = (
                    f"🍏 Taom: {food['name']}\n"
                    f"📝 Tavsif: {food.get('description', 'Mavjud emas')}\n"
                    f"💰 Narxi: {int(food['price']):,} SO'M\n"
                    f"📌 Turi: {food_type}"
                )
                
                # Inline tugma (Buyurtma berish uchun)
                inline_markup = types.InlineKeyboardMarkup()
                buy_btn = types.InlineKeyboardButton("🛍️ Buyurtma qilish", callback_data=f"buy_{food['id']}_{food['name'][:15]}")
                inline_markup.add(buy_btn)
                
                bot.send_message(message.chat.id, caption, reply_markup=inline_markup)
        else:
            bot.send_message(message.chat.id, "Xatolik yuz berdi. API bilan bog'lanib bo'lmadi.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Tizimda texnik xatolik: {str(e)}")

@bot.message_handler(func=lambda message: message.text == "ℹ️ Loyiha haqida")
def about_project(message):
    text = "FoodSave — Oziq-ovqat isrofini (Food Waste) kamaytirish va tadbirkorlar hamda xalq uchun manfaatli platforma yaratish maqsadida ishlab chiqilgan MVP loyihadir."
    bot.send_message(message.chat.id, text)

# Inline tugma bosilganda (Buyurtma jarayoni boshlanishi)
@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def handle_buy_callback(call):
    # call.data dan food_id ni ajratib olish
    data_parts = call.data.split('_')
    food_id = int(data_parts[1])
    food_name = data_parts[2]
    
    chat_id = call.message.chat.id
    user_steps[chat_id] = {
        'food_id': food_id,
        'food_name': food_name
    }
    
    # Ismni so'rash
    msg = bot.send_message(chat_id, f"✨ {food_name} uchun buyurtma rasmiylashtirilmoqda.\nIltimos, ismingizni kiriting:")
    bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    chat_id = message.chat.id
    if chat_id not in user_steps:
        return
        
    user_steps[chat_id]['client_name'] = message.text
    
    # Telefon raqamni so'rash (Tugma orqali yuborish imkoniyati bilan)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_phone = types.KeyboardButton("📱 Telefon raqamni ulashish", request_contact=True)
    markup.add(btn_phone)
    
    msg = bot.send_message(chat_id, "Rahmat! Endi telefon raqamingizni kiriting yoki quyidagi tugma orqali ulashing:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_phone_step)

def process_phone_step(message):
    chat_id = message.chat.id
    if chat_id not in user_steps:
        return
        
    # Agar tugma orqali kontakt yuborilgan bo'lsa yoki qo'lda yozilgan bo'lsa
    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text
        
    user_steps[chat_id]['client_phone'] = phone
    
    # Ma'lumotlarni Django API'ga POST so'rov orqali yuborish
    order_data = {
        "food": user_steps[chat_id]['food_id'],
        "client_name": user_steps[chat_id]['client_name'],
        "client_phone": user_steps[chat_id]['client_phone'],
        "delivery_type": "pickup",     # Standart qiymat
        "payment_method": "cash",      # Standart qiymat
        "status": "pending"
    }
    
    bot.send_message(chat_id, "⏳ Buyurtma tizimga yuborilmoqda...")
    
    try:
        # Django'dagi reservations endpointiga yuboramiz
        res = requests.post(f"{API_BASE_URL}/reservations/", json=order_data)
        
        # Boshlang'ich tugmalarni qaytarish
        main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        main_markup.add(types.KeyboardButton("🛒 Taomlar vitrinasi"), types.KeyboardButton("ℹ️ Loyiha haqida"))
        
        if res.status_code == 201 or res.status_code == 200:
            bot.send_message(
                chat_id, 
                f"🎉 Tabriklaymiz! {user_steps[chat_id]['food_name']} uchun buyurtmangiz muvaffaqiyatli qabul qilindi.\nRestoran tez orada siz bilan bog'lanadi.",
                reply_markup=main_markup
            )
        else:
            bot.send_message(chat_id, "Xatolik! Buyurtma qabul qilinmadi. API xatosi.", reply_markup=main_markup)
            
    except Exception as e:
        bot.send_message(chat_id, f"Xatolik yuz berdi: {str(e)}")
        
    # Vaqtinchalik xotirani tozalash
    del user_steps[chat_id]

if __name__ == '__main__':
    print("Bot ishga tushdi...")
    bot.infinity_polling()