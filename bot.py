import telebot

TOKEN = "7542381540:AAFoF9_X4yq34r-JYkBQIPtISPykAc9mSfU"
bot = telebot.TeleBot(TOKEN)

questions = [
    {"type": "text", "question": "1+1 چند میشه؟", "answer": "2"},
    {"type": "image", "question": "به این تصویر نگاه کن و بگو چی می‌بینی", "image": "https://ibb.co/gb0RCGCT", "answer": "درخت"},
    {"type": "text", "question": "پایتخت ایران کجاست؟", "answer": "تهران"},
]

user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_states[user_id] = 0
    send_question(user_id)

def send_question(user_id):
    index = user_states.get(user_id, 0)
    if index < len(questions):
        question = questions[index]
        if question["type"] == "text":
            bot.send_message(user_id, question["question"])
        elif question["type"] == "image":
            if question["image"].startswith("http"):  # اگر لینک اینترنتی بود
                bot.send_photo(user_id, question["image"], caption=question["question"])
            else:  # اگر file_id از تلگرام بود
                bot.send_photo(user_id, photo=question["image"], caption=question["question"])
    else:
        bot.send_message(user_id, "✅ تبریک! شما همه سوالات را پاسخ دادید.")

@bot.message_handler(func=lambda message: True)
def check_answer(message):
    user_id = message.chat.id
    index = user_states.get(user_id, 0)
    
    if index < len(questions):
        question = questions[index]
        correct_answer = question["answer"]
        
        if message.text.strip().lower() == correct_answer.lower():
            user_states[user_id] += 1  # سوال بعدی
            
            bot.send_message(user_id, "✅ درست گفتی!")
            send_question(user_id)  # سوال بعدی رو ارسال کن
            
            return  # **اضافه شد تا مطمئن بشیم کد جای دیگه گیر نمیکنه**

        else:
            bot.send_message(user_id, "❌ اشتباهه، دوباره امتحان کن.")

bot.polling()
