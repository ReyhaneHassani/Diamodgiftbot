import telebot

TOKEN = "7542381540:AAFoF9_X4yq34r-JYkBQIPtISPykAc9mSfU"
bot = telebot.TeleBot(TOKEN)

questions = [
    {"type": "text", "question": "1+1 چند میشه؟", "answer": "2"},
    {"type": "image", "question": "به این تصویر نگاه کن و بگو چی می‌بینی", "image": "https://ibb.co/gb0RCGCT", "answer": "سالگرد"},
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
            bot.send_photo(user_id, question["image"], caption=question["question"])
    else:
        bot.send_message(user_id, "✅ تبریک! شما همه سوالات را پاسخ دادید.")

@bot.message_handler(func=lambda message: True)
def check_answer(message):
    user_id = message.chat.id
    index = user_states.get(user_id, 0)
    
    if index < len(questions):
        question = questions[index]
        correct_answer = question["answer"]

        # حذف فاصله‌های اول و آخر، کوچک کردن حروف، و حذف فاصله‌های میانی
        user_answer = message.text.strip().lower().replace(" ", "")
        correct_answer = correct_answer.strip().lower().replace(" ", "")

        if user_answer == correct_answer:
            user_states[user_id] += 1
            bot.send_message(user_id, "✅ درست گفتی!")
            send_question(user_id)
            return  
        else:
            bot.send_message(user_id, "❌ اشتباهه، دوباره امتحان کن.")

bot.polling()
