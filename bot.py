import telebot

TOKEN = "7542381540:AAFoF9_X4yq34r-JYkBQIPtISPykAc9mSfU"
bot = telebot.TeleBot(TOKEN)

questions = [
    {"type": "text", "question": "1+1 چند میشه؟", "answer": "2"},
    {"type": "image", "question": "به این تصویر نگاه کن و بگو چی می‌بینی", "image": "https://i.ibb.co/4wbVxcxT/photo-2025-02-08-18-38-06.jpg", "answer": "درخت"},
    {"type": "text", "question": "پایتخت ایران کجاست؟", "answer": "تهران"},
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
        bot.send_message(user_id, "✅ درست گفتی!")
        user_states[user_id] += 1  # برو سوال بعدی
        
        print(f"✅ کاربر {user_id} جواب درست داد، رفت به سوال {user_states[user_id] + 1}")
        
        if user_states[user_id] < len(questions):  # اگر سوالات تموم نشده، سوال بعدی رو بپرس
            send_question(user_id)
        else:
            bot.send_message(user_id, "🎉 تبریک! تو به همه سوالات پاسخ دادی.")
    else:
        bot.send_message(user_id, "❌ اشتباهه، دوباره امتحان کن.")

bot.polling()
