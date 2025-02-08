import time
import telebot
from flask import Flask, request

import os
TOKEN = os.environ.get("BOT_TOKEN")

WEBHOOK_URL = "https://diamodgiftbot-production.up.railway.app"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# حذف و تنظیم مجدد Webhook
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

# سوالات و پاسخ‌ها، همراه با پیام خاص بعد از جواب درست
questions = [
    {"type": "text", "question": "نام عامیانه فرمول شیمیایی ریحانه چیست؟🧪", "answer": "اکسیژن",
     "correct_message": "همونجور که من«اکسیژن» شمام شما هم الماس منی!😍💎"},
    
    {"type": "image", "question": "به این تصویر نگاه کن و بگو به جای علامت سوال چی باید باشه؟!👀", 
     "image": "https://i.ibb.co/6cL9TqzF/photo-2025-02-08-18-37-37.jpg", "answer": "24",
     "correct_message": "البته میدونم که برای شما سوال خیلی آسونی بود! «24» بهمن سالگردمون مبارک عشق جان🥹❤️"},
    
    {"type": "text", "question": "نام صفتی که تو داری و ایجاد شدن رابطمونو بهش مدیونیم چیست؟!😇", "answer": "شریف",
     "correct_message": "شما «شریف» ترین انسانی هستی که میشناسم و بله ما رابطمونو به دانشگاه شریف بسیار مدیونیم!🤭"},

    {"type": "image", "question": "به این تصویر نگاه کن و بگو به جای علامت سوال چی باید باشه؟!👀", 
     "image": "https://i.ibb.co/4wbVxcxT/photo-2025-02-08-18-38-06.jpg", "answer": "سالگرد",
     "correct_message": "آفرین «سالگرد» کاملا درسته! این اولین سالگردمونه و من خوشحال ترین و شکرگزار ترینم که خدا تو رو به من داد زندگی جان💋❤️"},

    {"type": "text", "question": "نام علمی در مهندسی که نقطه ی وصل ما بود؟!🤓", "answer": "شیمی",
     "correct_message": "بله «شیمی»! در اصل توی میم شیمی اولین بار همو بوسیدیم💋(منحرف!)"},

    {"type": "text", "question": "خب ریحانه برات پانتومیم بازی میکنه و باید حدس بزنی!😈", "answer": "آزمون آزمایشی",
     "correct_message": "آخه تو چقدر خفنی که باهات همه چی انقدر خوش میگذره😭 آفرین «آزمون آزمایشی» که میشه اولین جایی که همو دیدیم!😍"},

    {"type": "text", "question": "√(-1) 2³ ∑ π...and it was delicious! خب وجه اشتراک این جمله و چیزی که شما میخوری و دوست داری چیه؟🙊", "answer": "پای",
     "correct_message": "اگر به اون میگی cream pie پس خودش میشه «پای»!باهوش خودمی و عاشقتم خب؟!❤️"},

    {"type": "text", "question": "این سوالو جواب بدی میتونی به کادوت دست پیدا کنی! با این حروف کلمه مد نظر رو بساز: ی س چ ی و🎁", "answer": "سوییچ",
     "correct_message": "خب فکر کنم فهمیدی که کجا باید دنبال کادوت بگردی! امیدوارم خوشت بیاد اویس جانم هر چند قابل شمارو نداره💃"},
]

user_states = {}

# --- توابع کمکی برای ارسال ایمن پیام و عکس ---
def safe_send_message(chat_id, text):
    tries = 3  # تعداد تلاش‌ها
    for i in range(tries):
        try:
            bot.send_message(chat_id, text)
            time.sleep(2)  # جلوگیری از بلاک شدن
            return
        except telebot.apihelper.ApiTelegramException as e:
            if e.error_code == 429:
                retry_after = int(e.result["parameters"]["retry_after"])
                time.sleep(retry_after)
            else:
                print(f"خطا در ارسال پیام: {e}")
                time.sleep(3)

def safe_send_photo(chat_id, photo_url, caption=""):
    tries = 3
    for i in range(tries):
        try:
            bot.send_photo(chat_id, photo_url, caption=caption)
            time.sleep(2)  # جلوگیری از بلاک شدن
            return
        except telebot.apihelper.ApiTelegramException as e:
            if e.error_code == 429:
                retry_after = int(e.result["parameters"]["retry_after"])
                time.sleep(retry_after)
            else:
                print(f"خطا در ارسال عکس: {e}")
                time.sleep(3)

# --- هندلر استارت ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    
    # اگر کاربر تازه وارد شده، از اول شروع کن
    user_states[user_id] = 0
    
    safe_send_message(user_id, "😃بزن بریم")
    send_question(user_id)

# --- هندلر ریست ---
@bot.message_handler(commands=['reset'])
def reset(message):
    user_id = message.chat.id
    
    # ریست کردن وضعیت کاربر
    user_states[user_id] = 0
    safe_send_message(user_id, "وضعیتت ریست شد کیوت جونی میتونی از اول خاطره بازی کنی☺️")
    send_question(user_id)

# --- ارسال سوال بعدی ---
def send_question(user_id):
    index = user_states.get(user_id, 0)
    
    if index >= len(questions):
        safe_send_message(user_id, "🎉سالگردمون مبارک")
        return
    
    question = questions[index]
    if question["type"] == "text":
        safe_send_message(user_id, question["question"])
    elif question["type"] == "image":
        safe_send_photo(user_id, question["image"], caption=question["question"])
    
    print(f"📩 ارسال سوال {index+1} برای کاربر {user_id}")

# --- بررسی پاسخ کاربر ---
@bot.message_handler(func=lambda message: True)
def check_answer(message):
    user_id = message.chat.id
    index = user_states.get(user_id, 0)
    
    if index >= len(questions):
        safe_send_message(user_id, "✅ تو قبلاً همه سوالات رو جواب دادی.")
        return
    
    question = questions[index]
    correct_answer = question["answer"]

    # حذف فاصله‌های اضافی و کوچک کردن حروف برای مقایسه راحت‌تر
    user_answer = message.text.strip().lower().replace(" ", "")
    correct_answer = correct_answer.strip().lower().replace(" ", "")

    if user_answer == correct_answer:
        # ارسال پیام خاص بعد از جواب درست
        safe_send_message(user_id, question["correct_message"])
        
        user_states[user_id] += 1  # برو سوال بعدی
        
        print(f"✅ کاربر {user_id} جواب درست داد، رفت به سوال {user_states[user_id] + 1}")
        
        if user_states[user_id] < len(questions):  # اگر سوالات تموم نشده، سوال بعدی رو بپرس
            send_question(user_id)
        else:
            safe_send_message(user_id, "🎉سالگردمون مبارک")
    else:
        safe_send_message(user_id, "❌اشتباه گفتی کیوت جان، دوباره امتحان کن.")

# --- تنظیم Webhook برای دریافت پیام‌های تلگرام ---
@app.route("/", methods=["POST"])
def webhook():
    update = request.get_json()
    if update:
        bot.process_new_updates([telebot.types.Update.de_json(update)])
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
