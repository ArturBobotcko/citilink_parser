from telegram_bot import dp
from aiogram import executor


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()

# TODO: Добавить сортировку по чипсету (создать список словарей и отсортировать)
