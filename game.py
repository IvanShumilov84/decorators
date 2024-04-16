from datetime import datetime as dt
from random import randint

from constants import ADMIN_USERNAME, UNKNOWN_COMMAND


class Game:
    start_time = dt.now()
    username = ''
    total_games = 0
    number = 0
    guess = -1

    def __init__(self) -> None:
        pass

    @staticmethod
    def __access_control(func):
        def wrapper(self):
            if self.username == ADMIN_USERNAME:
                result = func(self)
                return result
            else:
                print(UNKNOWN_COMMAND)
        return wrapper

    @__access_control
    def __get_statistics(self) -> None:
        game_time = dt.now() - self.start_time
        print(f'Общее время игры: {game_time}, текущая игра - №{self.total_games}')

    @__access_control
    def __get_right_answer(self) -> None:
        print(f'Правильный ответ: {self.number}')

    def __get_username(self):
        username = input('Представьтесь, пожалуйста, как Вас зовут?\n').strip()
        if username == ADMIN_USERNAME:
            print(
                '\nДобро пожаловать, создатель! '
                'Во время игры вам доступны команды "stat", "answer"'
            )
        else:
            print(f'\n{username}, добро пожаловать в игру!')
        self.username = username

    def __check_number(self) -> bool:
        # Если число угадано...
        if self.guess == self.number:
            print(f'Отличная интуиция, {self.username}! Вы угадали число :)')
            # ...возвращаем True
            return True

        if self.guess < self.number:
            print('Ваше число меньше того, что загадано.')
        else:
            print('Ваше число больше того, что загадано.')
        return False

    def __game(self) -> None:
        # Получаем случайное число в диапазоне от 1 до 100.
        self.number = randint(1, 100)
        print(
            '\nУгадайте число от 1 до 100.\n'
            'Для выхода из текущей игры введите команду "stop"'
        )
        while True:
            # Получаем пользовательский ввод,
            # отрезаем лишние пробелы и переводим в нижний регистр.
            user_input = input('Введите число или команду: ').strip().lower()

            match user_input:
                case 'stop':
                    break
                case 'stat':
                    self.__get_statistics()
                case 'answer':
                    self.__get_right_answer()
                case _:
                    try:
                        self.guess = int(user_input)
                    except ValueError:
                        print(UNKNOWN_COMMAND)
                        continue

                    if self.__check_number():
                        break

    def guess_number(self) -> None:
        self.__get_username()
        # Счётчик игр в текущей сессии.
        while True:
            self.total_games += 1
            self.__game()
            play_again = input('\nХотите сыграть ещё? (yes/no) ')
            if play_again.strip().lower() not in ('y', 'yes'):
                break
