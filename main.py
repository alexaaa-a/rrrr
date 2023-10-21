import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6123423775:AAHSZjR70wGFw1l-T6re0vu94pRIhnEVzHY",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Регистрация в моем боте"  # Можно менять текст
text_button_1 = "Купить бургер"  # Можно менять текст
text_button_2 = "Посмотреть полезные напитки"  # Можно менять текст
text_button_3 = "Посмотреть полезные блюда"  # Можно менять текст


menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Если ты зашел в этот бот, значит ты везунчик :)',  # Можно менять текст
        reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Супер! Введите ваше *имя:*')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Супер! Ваш [индекс массы тела](https://calc.by/weight-and-calories/body-mass-index-calculator.html)?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Спасибо за регистрацию! Надеемся, что вы сделаете правильный выбор', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "К сожалению бургеры для вас закончились. Тело само спортом не займется. Пора начать заниматься спортом и начать есть здоровую еде. Я верю в тебя✊", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Вы тоже первым делом подумали о воде? Даже если нет, то знайте: вода — один из самых полезных для здоровья в рейтинге напитков мира. Она не содержит калорий, важна для пищеварения, и необходима для усвоения витаминов В и С. Кроме того, вода помогает в детоксикации организма и является очень важным компонентом крови. Другие полезные напитки смотри [здесь](https://dzen.ru/a/Xz9F2piRMH2O11rp)", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Паста с тунцом. Тебе понадобится: 200 г макарон, 1 помидор, 100 г томатного соуса, 1 банка тунца, специи, чеснок, зелень. <b>Приготовление:</b> Отвари макароны до готовности. Обжарь тунец с чесноком буквально минуту. Добавь рубленый помидор и томатный соус, и туши все вместе 7 минут. Добавь зелень и специи, и перемешай соус с макаронами.", parse_mode="HTML", reply_markup=menu_keyboard)  # Можно менять текст


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()