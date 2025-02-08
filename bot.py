import telebot

TOKEN = "7542381540:AAFoF9_X4yq34r-JYkBQIPtISPykAc9mSfU"
bot = telebot.TeleBot(TOKEN)
# حذف webhook قبلی
bot.remove_webhook()

# تنظیم webhook جدید
bot.set_webhook(url="diamodgiftbot-production.up.railway.app")  # اینجا آدرس webhook جدید خودت رو بذار

# سوالات و پاسخ‌ها، همراه با پیام خاص بعد از جواب درست
questions = [
    {"type": "text", "question": "نام عامیانه فرمول شیمیایی ریحانه چیست؟", "answer": "اکسیژن", "correct_message": "همونجور که من«اکسیژن» شمام شما هم الماس منی!😍💎"},  # پیام بعد از جواب درست
    {"type": "image", "question": "به این تصویر نگاه کن و بگو به جای علامت سوال چی باید باشه؟!", "image": "https://i.ibb.co/4wbVxcxT/photo-2025-02-08-18-38-06.jpg", "answer": "سالگرد", "correct_message": "آفرین «سالگرد» کاملا درسته! این اولین سالگردمونه و من خوشحال ترین و شکرگزار ترینم که خدا تو رو به من داد زندگی جان💋❤️"},  # پیام بعد از جواب درست
    {"type": "text", "question": "نام صفتی که تو داری و ایجاد شدن رابطمونو بهش مدیونیم چیست؟!", "answer": "شریف", "correct_message": "شما «شریف» ترین انسانی هستی که میشناسم و بله ما رابطمونو به دانشگاه شریف بسیار مدیونیم!🤭"},  # پیام بعد از جواب درست
]

user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    
    # بررسی می‌کنیم که کاربر قبلاً وارد نشده باشه
    if user_id not in user_states:
        user_states[user_id] = 0  # شروع از سوال اول
    
    bot.send_message(user_id, "👋 سلام! بریم سراغ سوال اول...")
    send_question(user_id)

@bot.message_handler(commands=['reset'])
def reset(message):
    user_id = message.chat.id
    
    # ریست کردن وضعیت کاربر
    user_states[user_id] = 0
    bot.send_message(user_id, "وضعیت شما ریست شد. بیاید دوباره شروع کنیم!")
    send_question(user_id)

def send_question(user_id):
    index = user_states.get(user_id, 0)
    
    if index >= len(questions):
        bot.send_message(user_id, "🎉 تبریک! تو به همه سوالات پاسخ دادی.")
        return
    
    question = questions[index]
    if question["type"] == "text":
        bot.send_message(user_id, question["question"])
    elif question["type"] == "image":
        bot.send_photo(user_id, question["image"], caption=question["question"])
    
    print(f"📩 ارسال سوال {index+1} برای کاربر {user_id}")

@bot.message_handler(func=lambda message: True)
def check_answer(message):
    user_id = message.chat.id
    index = user_states.get(user_id, 0)
    
    if index >= len(questions):
        bot.send_message(user_id, "✅ تو قبلاً همه سوالات رو جواب دادی.")
        return
    
    question = questions[index]
    correct_answer = question["answer"]

    # حذف فاصله‌های اضافی و کوچک کردن حروف برای مقایسه راحت‌تر
    user_answer = message.text.strip().lower().replace(" ", "")
    correct_answer = correct_answer.strip().lower().replace(" ", "")

    if user_answer == correct_answer:
        # ارسال پیام خاص بعد از جواب درست
        bot.send_message(user_id, question["correct_message"])
        
        user_states[user_id] += 1  # برو سوال بعدی
        
        print(f"✅ کاربر {user_id} جواب درست داد، رفت به سوال {user_states[user_id] + 1}")
        
        if user_states[user_id] < len(questions):  # اگر سوالات تموم نشده، سوال بعدی رو بپرس
            send_question(user_id)
        else:
            bot.send_message(user_id, "🎉 تبریک! تو به همه سوالات پاسخ دادی.")
    else:
        bot.send_message(user_id, "❌ اشتباهه، دوباره امتحان کن.")

bot.remove_webhook()  # حذف webhook اگر قبلاً تنظیم شده
bot.set_webhook(url='URL_OF_YOUR_WEBHOOK')  # تنظیم مجدد webhook

bot.polling()
