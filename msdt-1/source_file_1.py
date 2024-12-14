from random import randint

# Функция вывода информации по лабораторной работе
def task():
    print("Лабораторная работа №2")
    print("Вариант №3. Выполнил студент группы 6102-020302D Васильев А.Л.")
    print("Задание:")
    print("1. В списке целочисленных элементов найти минимальный")
    print("     элемент, некратный заданному числу")
    print("2. С использованием цикла while найти в списке индекс")
    print("     первого нечётного ненулевого элемента")
    print("3. Отсортировать список (без использования стандартных функций сортировки")
    print("     по убыванию (сортировка выбором)")
    print("")


# Функция для ручного ввода списка в одну строку
def manual_entry_list(int_list):
    int_list = list(map(int, input().split()))
    return int_list


# Функция для автоматического формирования списка из n чисел в диапазоне от b до c
def automatic_list_entry(int_list, n, b, c):
    for i in range(n):
        int_list.append(randint(b, c))
    return int_list


# Функция для поиска минимального элемента, некратного заданному числу, в списке целочисленных элементов
def finding_min_elem(int_list, x):
    min_elem = 10 ** 10
    for i in range(len(int_list)):
        if (int_list[i] % x != 0) and (int_list[i] < min_elem):
            min_elem = int_list[i]
    return min_elem


# Функция для поиска в списке индекса первого нечетного ненулевого элемента с использованием цикла while
def index_search(int_list):
    index_elem = 0
    while (index_elem < len(int_list)) and (int_list[index_elem] % 2 == 0):
        index_elem += 1
    return index_elem


# Функция для сортировки списка по убыванию, используя сортировку выбором
def selection_sort(int_list):
    for j in range(len(int_list) - 1):
        max_el = int_list[j]                    # Запоминаем j элемент списка в переменной max_el
        ind_max = j                             # Запоминаем индекс j элемента списка
        for i in range(j + 1, len(int_list)):   # Запускаем цикл для просмотра последующих элементов и поиска наибольшего
            if int_list[i] > max_el:            # Если элемент из списка больше текущего max_el
                max_el = int_list[i]            # Присваиваем элементу max_el новое значение
                ind_max = i                     # Запоминаем индекс нового элемента max_el
        int_list[ind_max] = int_list[j]         # Меняем фиксированный элемент
        int_list[j] = max_el                    # с наибольшим найденным элементом
    return int_list


# Функция main

task()

v = int
flag = True
while flag:
    print("Выберите способ заполнения списка и введите нужную цифру:")
    print("1 - ручной ввод элементов списка в одну строку через пробел;")
    print("0 - автоматический формаирования списка из n элементов в диапазоне от b до c.\n")
    v = int(input("Ваш выбор: "))
    print("")
    if (v == 1) or (v == 0):
        flag = False
    else:
        print("Ошибка ввода! Попробуйте снова!\n")

# Создание списка
int_list = []
if v == 1:
    print("Введите элементы списка в строку через пробел: ")
    int_list = manual_entry_list(int_list)
else:
    n = int(input("Введите количество элементов списка: "))
    b, c = map(int, input("Введите диапазон элементов b и c через пробел: ").split())
    int_list = automatic_list_entry(int_list, n, b, c)
    print(int_list)
print("")

# Нахождение минимального элемента, некратного заданному числу x, из целочисленного списка
x = int(input("Введите число, кратность которому нужно проверить, x = "))
min_elem = finding_min_elem(int_list, x)
if min_elem != 10 ** 10:
    print("Минимальный элемент, некратный заданному числу x = {0}, равен: {1}".format(x, min_elem))
else:
    print("Минимальный элемент, некратный заданному числу x = {0}, отсутствует!".format(x))
print("")

# Нахождение индекса первого нечётного ненулевого элемента в целочисленном списке с помощью цикла while
index_elem = index_search(int_list)
if index_elem < len(int_list):
    print("Индекс первого нечётного ненулевого элемента равен: ", index_elem)
else:
    print("В списке отсутствуют нечётные ненулевые элементы!")
print("")

# Сортировка списка по убыванию, используя сортировку выбором
print("Исходный список:")
print(int_list)
selection_sort(int_list)
print("\nСписок после сортировки выбором по убыванию:")
print(int_list)
print("")