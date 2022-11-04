import logging
from aiogram import Bot, Dispatcher, executor, types
import inline_keyboard
# import messages
from data_accessor import DataAccessor

logging.basicConfig(level=logging.INFO)

token='5795263448:AAG3elMgSX6lJJGDZ0LEwLjqHDSuRIhB6gE'

bot = Bot(token=token)
dp = Dispatcher(bot)

data_accessor = DataAccessor("database.sqlite3")
income_type = None
expend_type = None


@dp.message_handler(commands=['start'])
async def show_weather(message: types.Message):
    await message.answer(text="Выберите, что Вам нужно",
                         reply_markup=inline_keyboard.MAIN_MENU)


@dp.callback_query_handler(text='income')
async def process_callback_wind(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await bot.send_message(
        callback_query.from_user.id,
        text="Выберите тип дохода",
        reply_markup=inline_keyboard.INCOMES
    )


@dp.callback_query_handler(text='expend')
async def process_callback_wind(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await bot.send_message(
        callback_query.from_user.id,
        text="Выберите тип расхода",
        reply_markup=inline_keyboard.EXPENDS
    )


@dp.callback_query_handler(text='income_salary')
async def process_callback_wind(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    global income_type
    income_type = 1
    global expend_type
    expend_type = None

    await bot.send_message(
        callback_query.from_user.id,
        text="Введите величину дохода",
    )


@dp.callback_query_handler(text='income_gift')
async def process_callback_wind(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    global income_type
    income_type = 2
    global expend_type
    expend_type = None

    await bot.send_message(
        callback_query.from_user.id,
        text="Введите величину дохода",
    )


@dp.callback_query_handler(text='income_other')
async def process_callback_wind(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    global income_type
    income_type = 3
    global expend_type
    expend_type = None

    await bot.send_message(
        callback_query.from_user.id,
        text="Введите величину дохода",
    )


@dp.callback_query_handler(text='expend_odezhda')
async def process_callback_wind(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    global expend_type
    expend_type = 1
    global income_type
    income_type = None

    await bot.send_message(
        callback_query.from_user.id,
        text="Введите величину расхода"
    )


@dp.message_handler()
async def add_expenditure(message: types.Message):
    global income_type
    global expend_type

    successfully = 0
    if expend_type != None:
        successfully = data_accessor.add_expend(expend_type, message.text)
    else:
        successfully = data_accessor.add_income(income_type, message.text)

    if successfully != 0:
        await message.answer(text="Отлично\nВыберите действие",
                            reply_markup=inline_keyboard.MAIN_MENU)
    else:
        await message.answer(text="Произошла ошибка\nВыберите действие",
                            reply_markup=inline_keyboard.MAIN_MENU)


@dp.callback_query_handler(text='expend_dom')
async def process_callback_wind(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    global expend_type
    expend_type = 2
    global income_type
    income_type = None

    await bot.send_message(
        callback_query.from_user.id,
        text="Введите величину дохода",
    )


@dp.callback_query_handler(text='expend_zdorovie')
async def process_callback_wind(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    global expend_type
    expend_type = 3
    global income_type
    income_type = None

    await bot.send_message(
        callback_query.from_user.id,
        text="Введите величину дохода",
    )


@dp.callback_query_handler(text='expend_avtomobil')
async def process_callback_wind(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    global expend_type
    expend_type = 4
    global income_type
    income_type = None

    await bot.send_message(
        callback_query.from_user.id,
        text="Введите величину дохода",
    )


@dp.callback_query_handler(text='expend_domashnie_zhiv')
async def process_callback_wind(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    global expend_type
    expend_type = 5
    global income_type
    income_type = None

    await bot.send_message(
        callback_query.from_user.id,
        text="Введите величину дохода",
    )

@dp.callback_query_handler(text='stat')
async def process_callback_wind(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await bot.send_message(
        callback_query.from_user.id,
        text="Выберите период",
        reply_markup=inline_keyboard.PERIODS
    )


@dp.callback_query_handler(text='stat_month')
async def process_callback_wind(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    expenditures, incomes = data_accessor.get_incomes_expenditures()
    total_expenditure = expenditures[0][1]
    total_income = incomes[0][1]
    difference = total_income - total_expenditure

    await bot.send_message(
        callback_query.from_user.id,
        text="Отчет о доходах и расходах за текущий месяц: \nДоходы: %s Расходы: %s \nРазница: %s"%(total_income, total_expenditure, difference),
        reply_markup=inline_keyboard.MAIN_MENU
    )


@dp.callback_query_handler(text='stat_half_year')
async def process_callback_wind(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    expenditures, incomes = data_accessor.get_incomes_expenditures(where="2")

    total_expenditure = expenditures[0][1]
    total_income = incomes[0][1]
    difference = total_income - total_expenditure

    await bot.send_message(
        callback_query.from_user.id,
        text="Отчет о доходах и расходах за текущее полугодие: \nДоходы: %s Расходы: %s \nРазница: %s"%(total_income, total_expenditure, difference),
        reply_markup=inline_keyboard.MAIN_MENU
    )


@dp.callback_query_handler(text='stat_year')
async def process_callback_wind(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    expenditures, incomes = data_accessor.get_incomes_expenditures(where="3")

    total_expenditure = expenditures[0][1]
    total_income = incomes[0][1]

    difference = total_income - total_expenditure

    await bot.send_message(
        callback_query.from_user.id,
        text="Отчет о доходах и расходах за текущий год: \nДоходы: %s Расходы: %s \nРазница: %s"%(total_income, total_expenditure, difference),
        reply_markup=inline_keyboard.MAIN_MENU
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
