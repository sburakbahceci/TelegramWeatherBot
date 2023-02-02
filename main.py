import requests
import telebot

API_KEY = "a71fb9e3a4b5c63ff9ee97c33070c610"
bot = telebot.TeleBot("5814091483:AAE4GDkOC49Bmn79rqpwV_n6CMLDGR_kpGk")

cities = ["Istanbul", "Ankara", "Izmir", "Adana", "Antalya"]


def generate_keyboard(cities):
  keyboard = [[telebot.types.InlineKeyboardButton(city, callback_data=city)]
              for city in cities]
  return keyboard


def get_turkish_weather_description(description):
  if description == "clear sky":
    return "Açık Hava"
  elif description == "few clouds":
    return "Az Bulutlu"
  elif description == "scattered clouds":
    return "Parçalı Bulutlu"
  elif description == "broken clouds":
    return "Çok Bulutlu"
  elif description == "shower rain":
    return "Sağanak Yağışlı"
  elif description == "rain":
    return "Yağmurlu"
  elif description == "thunderstorm":
    return "Fırtınalı"
  elif description == "snow":
    return "Karlı"
  elif description == "mist":
    return "Sisli"
  else:
    return description


@bot.callback_query_handler(func=lambda call: call.data in cities)
def callback_handler(call):
  weather_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(
    call.data, API_KEY)
  weather_data = requests.get(weather_url).json()
  temp = weather_data["main"]["temp"]
  humidity = weather_data["main"]["humidity"]
  description = weather_data["weather"][0]["description"]
  turkish_description = get_turkish_weather_description(description)
  result = "Şehir: {}\nSıcaklık: {}°C\nNem: {}%\nHava Durumu: {}".format(
    call.data, temp, humidity, turkish_description)
  bot.send_message(chat_id=call.message.chat.id, text=result)


@bot.message_handler(commands=['weather'])
def weather(message):
  keyboard = generate_keyboard(cities)
  markup = telebot.types.InlineKeyboardMarkup(keyboard=keyboard)
  bot.send_message(chat_id=message.chat.id,
                   text="Lütfen bir şehir seçin:",
                   reply_markup=markup)


bot.polling()
