# Модули
import keyboard
import itertools
import sys
import mouse
import time


# Предупреждение
print("Warning:\nThe script only works for FullHD monitors!\nThe operation of the script depends on the correctness of the data you entered!")

# Получение номера монитора пользователя
monitor_number = int(input("Enter the number of the monitor on which Minecraft is running, counting from one, from left to right:\n"))
# Получение размера интерфейса пользователя в Minecraft
interface_size = 3 # int(input(""))

# Координаты кнопки трейда на экране
cords_trade_button = [680 + (monitor_number - 1) * 1920, 370]
# Координаты ячейки с подтверждением сделки на экране
cords_trade_confirmation_cell = [680 + (monitor_number - 1) * 1920, 370]

# Объявление
print("Ready to go! Press Shift + B to start/stop trading, and Shift + Esc to exit.")
# Предупреждение
print("Before you start trading, you should aim at the middle of the lower half of the trap chest!")

# Статус скрипта
is_works = False

# Главный алгоритм
while (not (keyboard.is_pressed("Shift") and keyboard.is_pressed("Esc"))):
	# Запуск или остановки торговли
	if keyboard.is_pressed("Shift") and keyboard.is_pressed("b"):
		is_works = not is_works

	# Основной цикл если скрипт включен
	if (is_works):
		print(mouse.get_position())



# # Начало кода, активация АРК-а
# time.sleep(1)
# mouse.move(cord_num["1"][0] - 200, cord_num["1"][1])
# mouse.click('left')
# time.sleep(1)
# # Все ПИН-коды
# all_pin = list(itertools.product("0123456789", repeat=4))
# # ПИН-код с которого начинаеться подбор
# pin_start = ("1", "4", "9", "9")
# index_pin_start = all_pin.index(pin_start)
# # Подбор ПИН-кода
# for elem in all_pin:
# 	# Когда цикл дошёл до нужного ПИН-кода, подбор начинается
# 	if all_pin.index(elem) >= index_pin_start:
# 		# Текущий ПИН-код
# 		print(elem)
# 		# Открытие окна ввода ПИН-кода
# 		keyboard.send('e')
# 		# Ожидание анимации
# 		time.sleep(0.3)
# 		# Нажатие каждой цифры
# 		for i in elem:
# 			# Перемещение курсора и нажатие на цифру
# 			mouse.move(cord_num[i][0], cord_num[i][1])
# 			mouse.click('left')
# 			# Задержка
# 			time.sleep(0.01)
# 			# Закрытие программы если ...
# 			if keyboard.is_pressed("Esc"):
# 				sys.exit()
# 		# Ожидание анимации
# 		time.sleep(0.7)
# # Конец
