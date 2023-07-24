import telebot           # для бота
import pickle            # для открытия файла с цветами поля
from pathlib import Path # для удаления неугодного файла
from PIL import Image    # для отправки холста пользователю
import time              # для высчитывания времени межу изменениями цвета

st = time.time() - 100 # переменная измерения времени и его ограничения
l = 100                # ширина и высота поля
h = 7                  # размер пикселя на изображении

data = []
try:
    with open("data.pickle", "rb") as f:
        data = pickle.load(f)
except Exception as ex:
    print("Error during unpickling object (Possibly unsupported):", ex)

bot = telebot.TeleBot('токен')

@bot.message_handler(commands=['start']) # отслеживание команды
def start(message):
    # пояснения:
    bot.send_message(message.chat.id, text="Вы находитесь в боте для группового рисования картины. В этом боте вы можете внести свой вклад в сетевой холст, на котором рисуют и другие люди. Вы можете изменить цвет одного из пикселей раз в 10 секунд. Так вы можете рисовать свои шедеврыы, но учтите, что их могут изменять другие люди.")
    bot.send_message(message.chat.id, text = "Чтобы провести все вышеописанные операции, необходимо отправить мне цвет пикселя в формате: x, y, красный, зелёный, синий (через запятую, без пробелов). Причём ширина поля 0-99, длина 0-99, максимальное значение каждого из цветов 255, минимальное 0. Например:")
    bot.send_message(message.chat.id, text = "0,0,255,255,255")
    bot.send_message(message.chat.id, text = "Отправь 'к' чтобы увидеть полученное изображение.")

    # берём данные из файла
    try:
        with open("data.pickle", "rb") as f:
            data = pickle.load(f)
    except Exception as ex:
        print("Error during unpickling object (Possibly unsupported):", ex)

    # создаём изображение с pillow
    img = Image.new("RGB", (l*h, l*h), 'black')
    for i in range(l):      # для каждого пикселя поля
        for j in range(l):
            # если data[i*l + j] является не нулём
            try:
                # рисуем квадрат hхh
                for i1 in range(h):
                    for j1 in range(h):
                        img.putpixel((i*h +i1, j*h +j1), tuple(data[i*l + j]))

            # иначе ничего не делаем (имитация бурной деятельности):
            except TypeError:
                if j // 2000 == 3:
                    print("0")

    bot.send_photo(message.chat.id, img) # отправляем полученное изображение

@bot.message_handler(content_types=['text']) # отслеживаем текст
def func(message):
    # если пользователь просит изображение поля
    if message.text == "к" or message.text == "k" or message.text == "К":
        # берём данные из файла (обновляем)
        try:
            with open("data.pickle", "rb") as f:
                data = pickle.load(f)
        except Exception as ex:
            print("Error during unpickling object (Possibly unsupported):", ex)
    
        # создаём изображение с pillow
        img = Image.new("RGB", (l*h, l*h), 'black')
        for i in range(l):      # для каждого пикселя поля
            for j in range(l):
                # если data[i*l + j] является не нулём (изменялся хоть раз)
                try:
                    # рисуем квадрат hхh
                    for i1 in range(h):
                        for j1 in range(h):
                            img.putpixel((i*h +i1, j*h +j1), tuple(data[i*l + j]))
    
                # иначе ничего не делаем (имитация бурной деятельности):
                except TypeError:
                    if j // 2000 == 3:
                        print("0")
    
        bot.send_photo(message.chat.id, img) # отправляем полученное изображение

  
    else:
        # если длиннее минимального
        if len(message.text) >= 9:
            # переменная таймера - глобальная
            global st

            # Если с прошлого изменения пикселя прошло не меньше 20 секунд
            if time.time() - st < 20:
                bot.send_message(message.chat.id, text = "слишком часто. Промежуток между сообщениями - 20 секунд")
            else:
                # преобразуем текст сообщения в массив с координатами и цветом
                t = message.text
                x = []
                n = ""
                
                # с учётом разделителей
                for i in t:
                    if i != ",":
                        n += i
                    else:
                        x.append(n)
                        n = ""

                x.append(n)
                n = ""

                # просматриваем корректность цветов и координат: 
                # не вышли ли за край поля, и т.п.
                a = 0
                n = 0
                # в случае нарушений n = 1 (флаг)
                while a <= len(x)-1:
                    try:
                        x[a] = int(x[a])
                        if a < 2:
                            if x[a] > l:
                                n = 1
                        else:
                            if x[a] > 255 or x[a] < 0:
                                n = 1

                    except Exception:
                        n = 1
                        
                    a += 1
                # если нашёл ошибку
                if n == 1:
                    bot.send_message(message.chat.id, text = "Неверный формат запроса! Необходимо отправить цвет пикселя в формате: x, y, красный, зелёный, синий (через запятую, без пробелов). Причём ширина поля 100, длина 100, максимальное значение каждого из цветов 255, минимальное 0.")

                # если запрос корректный
                else:
                    # обновляем значение цветов пикселей поля
                    # (его могли изменить другие пользователи)
                    try:
                        with open("data.pickle", "rb") as f:
                            data = pickle.load(f)
                    except Exception as ex:
                        print("Error during unpickling object (Possibly unsupported):", ex)

                    # записываем в список новый цвет
                    data[(l*x[0]) + x[1]] = x[2:5]
                    
                    # отправляем пользователю оповещение
                    bot.send_message(message.chat.id, text = "корректно!")
                    
                    # удаляем файл с устаревшими данными
                    file= Path("data.pickle")
                    file.unlink()

                    # обновляем файл
                    try:
                        with open("data.pickle", "wb") as f:
                            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
                    except Exception as ex:
                        print("Error during pickling object (Possibly unsupported):", ex)

                    # обновляем таймер
                    st = time.time()                  
bot.polling(none_stop=True)
