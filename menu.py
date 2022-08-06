import sys
from controllers import *


def menu() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Добро пожаловать!')
    while True:
        print('1 - Показать все задачи\n'
              '2 - Показать выполненные \n'
              '3 - Показать не выполненные\n'
              '4 - Добавить задачу\n'
              '5 - Изменить задачу\n'
              '6 - Удалить задачу\n'
              '9 - Сохранить изменения\n'
              '0 - Выход')
        while True:
            try:
                num = abs(int(input('Для продолжения работы введите цифру: ')))
                if num in (0, 1, 2, 3, 4, 5, 6, 9):
                    break
                else:
                    print("\033[32m {} \033[0m".format('Нет такого пункта меню! Повнимательнее=)'))
            except ValueError:
                print('Wrong input! Try again...')

        match num:
            case 1:
                print_todo(all_task, 1)
            case 2:
                print_todo(all_task, 2)
            case 3:
                print_todo(all_task, 3)
            case 4:
                add_task(all_task)
            case 5:
                edit_task(all_task)
            case 6:
                del_task(all_task)
            case 9:
                save_data(all_task)
            case 0:
                os.system('cls' if os.name == 'nt' else 'clear')
                sys.exit()
