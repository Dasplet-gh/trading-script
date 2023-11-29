import threading
import keyboard
import signal
import mouse
import time
import os


# Константы
FULLHD_X = 1920
FULLHD_Y = 1080

HOTKEY_EXIT = "Shift+Esc"
HOTKEY_START_OR_STOP = "Shift+b"
HOTKEY_STOP_CYCLE = "Shift+v"

CORDS_TRADE_BUTTON_X = 680
CORDS_TRADE_BUTTON_Y = 380

BUTTONS_CORDS_DIFF = 60

CORDS_TRADE_CONFIRMATION_CELL_X = 1230
CORDS_TRADE_CONFIRMATION_CELL_Y = 420

REPO_URL = "https://github.com/Duriatt/Trading-Script"


"""
  * ================================================ Класс Параметров ==================================================
"""


class Parameters(object):
    # Инициализация
    def __init__(self):
        # Номер монитора пользователя
        self.MonitorNumber = 1
        self.MonitorNumberDescription = "номер монитора на котором запущен minecraft"
        # Размер интерфейса пользователя в Minecraft
        self.InterfaceSize = 3
        self.InterfaceSizeDescription = "размер интерфейса в minecraft"
        # Номер торгового слота
        self.TradeButtonNumber = 1
        self.TradeButtonNumberDescription = "номер торгового слота жителя"
        # Количество покупок
        self.TradeCount = -1
        self.TradeCountDescription = "количество покупок"
        # Пауза между покупками
        self.DelayBetweenTrading = 2
        self.DelayBetweenTradingDescription = "паузa между покупками"

    # Функция получающая число из ввода, при заданом условии
    def get_number_from_input(self, condition, error_msg):
        number = -10
        # Пока введённое значение не число или не подходит
        while condition(number):
            try:
                number = float(input())
                if condition(number):
                    raise ValueError
            except ValueError:
                print(error_msg, end="")
        return number

    # Функция выводящая значения всех параметров
    def print_parameters(self):
        # Вывод значений всех параметров
        print(
            f"- {self.MonitorNumberDescription.capitalize()} = {self.MonitorNumber}\n"
            f"- {self.InterfaceSizeDescription.capitalize()} = {self.InterfaceSize}\n"
            f"- {self.TradeButtonNumberDescription.capitalize()} = {self.TradeButtonNumber}\n"
            f"- {self.TradeCountDescription.capitalize()} = {self.TradeCount}\n"
            f"- {self.DelayBetweenTradingDescription.capitalize()} = {self.DelayBetweenTrading}"
        )

    # Функция считывающая команды и меняющая параметры
    def changing_parameters(self):
        # Инструкция
        print(
            f"\nВведите число:\n"
            f"-1 - Вывод значений всех параметров.\n"
            f"0 - Завершить изменение параметров.\n"
            f"1 - Изменить {self.MonitorNumberDescription}.\n"
            f"2 - Изменить {self.InterfaceSizeDescription}.\n"
            f"3 - Изменить {self.TradeButtonNumberDescription}.\n"
            f"4 - Изменить {self.TradeCountDescription}.\n"
            f"5 - Изменить {self.DelayBetweenTradingDescription}.\n"
        )
        # Считывание команд
        command = input("Введите команду: ")
        while command != "0":
            if command == "-1":
                # Вывод значений всех параметров
                print()
                self.print_parameters()
                print()
            elif command == "1":
                # Получение номера монитора пользователя
                print(f"Введите {self.MonitorNumberDescription}: ", end="")
                error_msg = "Требуется ввести целое число от еденицы: "
                self.MonitorNumber = int(self.get_number_from_input((lambda x: x < 1), error_msg))
            elif command == "2":
                # Получение размера интерфейса пользователя в Minecraft
                print(f"Введите {self.InterfaceSizeDescription}: ", end="")
                error_msg = "Требуется ввести целое число от еденицы до четырёх включительно: "
                self.InterfaceSize = int(self.get_number_from_input((lambda x: not (1 <= x <= 4)), error_msg))
            elif command == "3":
                # Получение номера торгового слота
                print(f"Введите {self.TradeButtonNumberDescription}: ", end="")
                error_msg = "Требуется ввести целое число от еденицы до семи включительно:"
                self.TradeButtonNumber = int(self.get_number_from_input((lambda x: not (1 <= x <= 7)), error_msg))
            elif command == "4":
                # Получение количества покупок
                print(f"Введите {self.TradeCountDescription}, введите -1 для бесконечной торговли: ", end="")
                error_msg = "Требуется ввести целое число от еденицы, введите -1 для бесконечной торговли: "
                self.TradeCount = int(self.get_number_from_input((lambda x: x < -1 or x == 0), error_msg))
            elif command == "5":
                # Получение паузы между покупками
                print(f"Введите {self.DelayBetweenTradingDescription}, задаётся в секундах: ", end="")
                error_msg = "Требуется ввести не отрицательное число: "
                self.DelayBetweenTrading = float(self.get_number_from_input((lambda x: x < 0), error_msg))
            else:
                print("Неизвестная команда.")
            # Считывание команды
            command = input("Введите команду: ")
        print()


"""
  * ================================================= Класс Действий ===================================================
"""


class Actions(object):
    # Инициализация
    def __init__(self):
        # Координаты кнопкок трейда на экране
        self.cordsTradeButtons = {}
        # Координаты ячейки с подтверждением сделки на экране
        self.cordsTradeConfirmation = []

    # Функция записывающащя координаты
    def set_cords(self, parameters):
        # Координата монитора x
        start_x = (parameters.MonitorNumber - 1) * FULLHD_X
        # Координаты кнопкок трейда на экране
        self.cordsTradeButtons = {}
        for i in range(7):
            diff_cell = BUTTONS_CORDS_DIFF * i
            self.cordsTradeButtons[i + 1] = [start_x + CORDS_TRADE_BUTTON_X, CORDS_TRADE_BUTTON_Y + diff_cell]
        # Координаты ячейки с подтверждением сделки на экране
        self.cordsTradeConfirmation = [start_x + CORDS_TRADE_CONFIRMATION_CELL_X, CORDS_TRADE_CONFIRMATION_CELL_Y]

    # Функция производящая покупку у жителя
    def trade(self, parameters):
        # Вход в сундук-ловушку
        mouse.click('right')
        time.sleep(1.8)
        # Продвижение по воде мимо портала, к жителю
        keyboard.press('w')
        time.sleep(1.2)
        keyboard.release('w')
        time.sleep(0.2)
        # Вход в меню жителя
        mouse.click('right')
        time.sleep(2)
        # Зажатие Shift для автоматических действий
        keyboard.press('Shift')
        time.sleep(0.1)
        # Перемещение мыши и нажатие на кнопку нужного трейда
        mouse.move(
            self.cordsTradeButtons[parameters.TradeButtonNumber][0],
            self.cordsTradeButtons[parameters.TradeButtonNumber][1]
        )
        time.sleep(0.1)
        mouse.click('left')
        time.sleep(0.1)
        # Перемещение мыши и нажатие на кнопку подтверждения трейда
        mouse.move(
            self.cordsTradeConfirmation[0],
            self.cordsTradeConfirmation[1]
        )
        time.sleep(0.1)
        mouse.click('left')
        time.sleep(0.1)
        # Отжатие Shift
        keyboard.release('Shift')
        time.sleep(0.1)
        # Выход из меню жителя
        keyboard.send('Esc')
        time.sleep(0.1)


"""
  * ================================================= Прочие Функции ===================================================
"""


# ======== Функция ожидающая остановки скрипта
def script_exit():
    keyboard.wait(HOTKEY_EXIT)
    print("- Остановка скрипта")
    os.kill(os.getpid(), signal.SIGINT)


#  ======== Функция ожидающая нажатие клавиш(и) определённое количество секунд
def wait_for_key(hotkey, timeout_seconds):
    start_time = time.time()
    # Проверка нажат ли хоткей в течении определённого времени
    while time.time() - start_time < timeout_seconds:
        if keyboard.is_pressed(hotkey):
            return True
    return False


"""
  * =================================================== Основной Код ===================================================
"""


if __name__ == "__main__":
    # Начало -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- 0

    # Предупреждение
    print(f"Предупреждение:\n"
          f"Перед использованием, пожалуйста, прочитайте инструкцию в README.md в репозитории по ссыле:\n"
          f"{REPO_URL}\n")

    # Создание возможности закрыть скрипт  -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- 1

    # Создание потока для функции script_exit
    thread_exit = threading.Thread(target=script_exit)
    # Запуск потока
    thread_exit.start()
    # Объявление
    print(f"Нажмите {HOTKEY_EXIT} для остановки работы скрипта.\n")

    # Создание класса параметров и действий  -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- 2

    # Создание параметров
    parameters = Parameters()
    print("-=- Измените параметры. Или оставьте значения по умолчанию, для этого завершите редактирование параметров.")
    # Включение редактора параметров
    parameters.changing_parameters()

    # Создание действий
    actions = Actions()
    # Запись координат
    actions.set_cords(parameters)

    # Предупреждение и декоративная загрузка -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- 3

    # Предупреждение
    print("Перед тем как начать торговать, вы должны прицелиться в середину нижней половины сундука-ловушки!\n"
          "Остановить торговлю можно только в паузе между циклами торговли (после выхода из меню жителя).\n")
    # Декоративная загрузка
    for _ in range(3):
        print(".", end="")
        time.sleep(0.4)
    print("\n")

    # Основной цикл работы скрипта -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- 4
    print(f"Готово к работе! Нажмите {HOTKEY_START_OR_STOP}, чтобы начать/остановить торговлю.")

    while True:
        # Статус
        is_works = False

        # Количество циклов трейда
        count = parameters.TradeCount
        while count != 0:
            # Основной алгоритм если скрипт включен  -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- 5
            if is_works:
                # Торговля
                actions.trade(parameters)
                # Запись номера и объявление
                count -= 1
                print(f"- Покупка {parameters.TradeCount - count} выполнена.")

            # Запуск или остановка торговли  -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- 6
            if not is_works or wait_for_key(HOTKEY_START_OR_STOP, parameters.DelayBetweenTrading):
                # Если торговля остановлена, то ожидание её возобновления или остановки цикла
                print(f"- Ожидание возобновления торговли. Для остановки цикла торговли нажмите {HOTKEY_STOP_CYCLE}.")
                # Ожидание нажатия горячих клавиш
                while True:
                    event = keyboard.read_event()
                    if event.event_type == keyboard.KEY_DOWN:
                        if keyboard.is_pressed(HOTKEY_START_OR_STOP):
                            break
                        elif keyboard.is_pressed(HOTKEY_STOP_CYCLE):
                            count = 0
                            break
                # Изменение статуса
                is_works = True
                time.sleep(0.5)

        # Подготовка к новому циклу торговли -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- 7

        # Объявление
        print("-=- Требуемое количество покупок было сделано. Измените параметры, или оставьте прежние, "
              "для этого завершите редактирование параметров.")
        # Включение редактора параметров
        parameters.changing_parameters()
        # Обновление координат
        actions.set_cords(parameters)
