# Напишите программу, которая принимает на вход 2 числа. Задайте список из N элементов,
# заполненных числами из промежутка [-N, N].
# Найдите произведение элементов на указанных позициях(не индексах).
# Position one: 1
# Position two: 3
# Number of elements: 5
# -> [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
# -> 15

from random import randint
import sys

print('Введите позиции двух элементов списка, и я выведу на экран их произведение')
N = int(input('Для начала определите количество элементов списка N \n'))
print('Я составлю список из {} случайных элементов в диапазоне от {} до {}'.format(N, -N, N))
num_list = []
for i in range(N):
    num_list.append(randint(-N, N))
print('У нас есть такой список: \n', num_list)
print('Теперь введите позиции элементов, произведение которых нужно найти')
position_one = int(input('Позиция элемента № 1: '))
position_two = int(input('Позиция элемента № 2: '))
if 0 < position_one <= N and 0 < position_two <= N:
    element_one = num_list[position_one-1]
    element_two = num_list[position_two-1]
    print(' Элемент № 1 = {}, \n \
Элемент № 2 = {}, \n    \
Произведение элементов равно: {}'.format
          (element_one, element_two, element_one*element_two))
else:
    print('Вы ввели неверное значение позиций. Попробуйте в следующий раз!')
print('Для выхода введите exit()')
