import keyboard
import threading
import signal
import os
import mouse
import time


# Константы
FULLHD_X = 1920
FULLHD_Y = 1080

HOTKEY_EXIT = "Shift+Esc"
HOTKEY_START_OR_STOP = "Shift+b"

CORDS_TRADE_BUTTON_X = 680
CORDS_TRADE_BUTTON_Y = 380

BUTTONS_CORDS_DIFF = 70

CORDS_TRADE_CONFIRMATION_CELL_X = 1230
CORDS_TRADE_CONFIRMATION_CELL_Y = 420


"""
  * ===================================================== Функции ======================================================
"""


# ======== Функция ожидающая остановки скрипта
def script_exit():
    keyboard.wait(HOTKEY_EXIT)
    print("- Остановка скрипта")
    os.kill(os.getpid(), signal.SIGINT)


# ======== Функция получающая число из ввода, при заданом условии
def get_number_from_input(condition, error_msg):
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


#  ======== Функция ожидающая нажатие клавиш(и) определённое количество секунд
def wait_for_key(hotkey, timeout_seconds):
    start_time = time.time()
    # Проверка нажат ли хоткей в течении определённого времени
    while time.time() - start_time < timeout_seconds:
        if keyboard.is_pressed(hotkey):
            return True
    return False


"""
  * =================================================== Основной код ===================================================
"""


if __name__ == "__main__":
    # Предупреждение
    print("Предупреждение:\n"
          "Перед использованием, пожалуйста, прочитайте инструкцию в README.md в репозитории по ссыле:\n"
          "https://github.com/Duriatt/Trading-Script\n")

    # Создание возможности закрыть скрипт  -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- 1

    # Создание потока для функции script_exit
    thread_exit = threading.Thread(target=script_exit)
    # Запуск потока
    thread_exit.start()

    # Объявление
    print(f"Нажмите {HOTKEY_EXIT} для остановки работы скрипта.\n")

    # Получение номера монитора пользователя -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- 2
    print("Введите номер монитора на котором запущен Minecraft: ", end="")

    mn_error_msg = "Требуется ввести целое число от еденицы: "
    mn_lambda = (lambda x: x < 1)
    monitor_number = get_number_from_input(mn_lambda, mn_error_msg)

    # Получение размера интерфейса пользователя в Minecraft  -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- 3
    # print("Введите размер интерфейса в Minecraft: ")
    # error_msg = "Требуется ввести целое число от еденицы до четырёх включительно: "
    # INTERFACE_SIZE = get_number_from_input((lambda x: not (1 <= x <= 7)), error_msg)

    # Получение номера торгового слота -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- 4
    print("Введите номер торгового слота жителя: ", end="")

    tcn_error_msg = "Требуется ввести целое число от еденицы до семи включительно:"
    tcn_lambda = (lambda x: not (1 <= x <= 7))
    trade_button_number = get_number_from_input(tcn_lambda, tcn_error_msg)

    # Получение количество покупок -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- 5
    print("Введите количество покупок, то сколько раз вы поторгуете, введите -1 для бесконечной торговли: ", end="")

    tc_error_msg = "Требуется ввести целое число от еденицы, введите -1 для бесконечной торговли: "
    tc_lambda = (lambda x: x < -1 or x == 0)
    trade_count = get_number_from_input(tc_lambda, tc_error_msg)

    # Получение паузы между покупками  -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- 6
    print("Введите паузу между покупками, задаётся в секундах: ", end="")

    dbt_error_msg = "Требуется ввести не отрицательное число: "
    dbt_lambda = (lambda x: x < 0)
    delay_between_trading = get_number_from_input(dbt_lambda, dbt_error_msg)

    # Координаты -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- 7
    start_x = (monitor_number - 1) * FULLHD_X

    # Координаты кнопкок трейда на экране
    cords_trade_buttons = {}
    for i in range(7):
        diff_cell = BUTTONS_CORDS_DIFF * i
        cords_trade_buttons[i + 1] = [start_x + CORDS_TRADE_BUTTON_X, CORDS_TRADE_BUTTON_Y + diff_cell]

    # Координаты ячейки с подтверждением сделки на экране
    cords_trade_confirmation_button = [start_x + CORDS_TRADE_CONFIRMATION_CELL_X, CORDS_TRADE_CONFIRMATION_CELL_Y]

    # Предупреждение и декоративная загрузка -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- 8
    print("\nПеред тем как начать торговать, вы должны прицелиться в середину нижней половины сундука-ловушки!\n"
          "Остановить торговлю можно только в паузе между циклами торговли (после выхода из меню жителя).\n")

    for _ in range(3):
        print(".", end="")
        time.sleep(0.4)
    print("\n")

    # Основной цикл работы скрипта -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- 9
    print(f"Готово к работе! Нажмите {HOTKEY_START_OR_STOP}, чтобы начать/остановить торговлю.")
    while True:
        # Статус
        is_works = False
        # Количество циклов трейда
        trade_count = int(trade_count)
        count = trade_count
        while count != 0:
            # Основной алгоритм если скрипт включен -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- 10
            if is_works:
                # Поочерёдное нажатие необходимых кнопок

                mouse.click('right')
                time.sleep(1.8)

                keyboard.press('w')
                time.sleep(1.2)
                keyboard.release('w')
                time.sleep(0.2)

                mouse.click('right')
                time.sleep(2)

                keyboard.press('Shift')
                time.sleep(0.1)

                mouse.move(cords_trade_buttons[trade_button_number][0], cords_trade_buttons[trade_button_number][1])
                time.sleep(0.1)
                mouse.click('left')
                time.sleep(0.1)

                mouse.move(cords_trade_confirmation_button[0], cords_trade_confirmation_button[1])
                time.sleep(0.1)
                mouse.click('left')
                time.sleep(0.1)

                keyboard.release('Shift')
                time.sleep(0.1)

                keyboard.send('Esc')
                time.sleep(0.1)

                count -= 1
                print(f"- Покупка {trade_count - count} выполнена.")

            # Запуск или остановка торговли -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- 11
            if not is_works or wait_for_key(HOTKEY_START_OR_STOP, delay_between_trading):
                # Если торговля остановлена, то ожидание её возобновления
                print("- Ожидание возобновления торговли.")
                keyboard.wait(HOTKEY_START_OR_STOP)
                is_works = True
                time.sleep(0.5)

        # Получение количество покупок  -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- 12
        print("Требуемое количество покупок было сделано. Требуются новые данные.")

        msg = "Введите 1 если желаете оставить предыдущие настройки, иначе введите что угодно другое: "
        if input(msg) != "1":
            print("Введите количество покупок: ", end="")
            trade_count = get_number_from_input(tc_lambda, tc_error_msg)

            print("Введите номер торгового слота: ", end="")
            trade_button_number = get_number_from_input(tcn_lambda, tcn_error_msg)

            print("Введите паузу между покупками: ", end="")
            delay_between_trading = get_number_from_input(dbt_lambda, dbt_error_msg)
