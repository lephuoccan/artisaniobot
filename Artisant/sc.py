import threading
import time
import requests
import telebot
import queue

TOKEN = '6228427174:AAGnO6UxecRK_f1dcPmFn8QLDtLKaUDlez4'
CHAT_ID = '-1001936854118'
# CHAT_ID = '-1001832667683'
API_URL = 'https://collect.artisant.io/api/products'

bot = telebot.TeleBot(TOKEN)

def get_data():
    while True:
        try:
            response = requests.get(API_URL)
            data = response.json()
            # Gửi dữ liệu vào hàng đợi cho thread khác xử lý
            message_queue.put(data)
            time.sleep(5)  # Chờ 2 giây để lấy dữ liệu tiếp theo
        except:
            # Xử lý lỗi khi không thể lấy dữ liệu
            pass

def send_message():
    preID = 140
    count = 0
    while True:
        # Lấy dữ liệu từ hàng đợi
        data = message_queue.get()
        if len(data) > 0:
            newData = data[0]
            if newData['id'] > preID:
                for item in data:
                    if item['id'] > preID:
                        text = f"Artisant: Có Item mới phẩm chất {item['rarity']}:{item['id']}: {item['name']}: {item['publishedAt']} @lephuoccan"
                        bot.send_message(chat_id=CHAT_ID, text=text)
                        
                        count += 1
                        if count >= 5:
                            preID = item['id']
                            count = 0
                            

        time.sleep(5)  # Chờ 1 giây để kiểm tra dữ liệu tiếp theo

if __name__ == '__main__':
    message_queue = queue.Queue()
    
    # Tạo thread để lấy dữ liệu
    t1 = threading.Thread(target=get_data)
    t1.start()
    
    # Tạo thread để gửi tin nhắn
    t2 = threading.Thread(target=send_message)
    t2.start()

    # Chờ cho tất cả các thread kết thúc
    t1.join()
    t2.join()
