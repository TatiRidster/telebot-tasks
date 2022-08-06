import csv


def read_file(filename: str) -> dict:
    """
    Выгружает в память словарь с данными из CSV файла.

    :param filename: имя файла.
    :return: словарь.
    """
    result = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                result[int(row[0])] = {
                    'task': str(row[1]),
                    'is_done': int(row[2])
                }
    except FileNotFoundError:
        print('Файл не найден. Проверьте имя файла и/или путь к файлу.')
    return result


all_task = read_file('todo.csv')


def add_task(todo: dict, arg: str):
    todo_new = arg
    if todo_new:
        id_new = max(list(x for x in todo.keys())) + 1
        result_new = {
            'task': todo_new,
            'is_done': 0
        }
        todo[id_new] = result_new
        return f"Ваша задача < {todo_new} > добавлена."
    else:
        return 'Название не может быть пустым'


def edit_task(todo: dict):
    print('Список дел:')
    for key, value in todo.items():
        # Вывод ID, названия дела, статус выполнения
        print("\033[7m {} \033[0m".format(
            f'ID {key} >>> {value["task"]} >>> {"Выполнено" if value["is_done"] else "Не выполнено"}'))
    try:  # Проверка ввода
        n = abs(int(input('Введите ID задачи которую хотите изменить: ')))
    except ValueError:
        print('Wrong input')
    if n in todo.keys():
        for k, v in todo.items():
            if k == n:
                while True:
                    try:  # Проверка ввода
                        new_status = int(input('Введите статус задачи\n'
                                               '1 - выполнено, 0 - не выполнено\n'
                                               'любое другое число - не менять статус\n'
                                               '>>> '))
                        break
                    except ValueError:
                        print('Wrong input!')
                if new_status in (0, 1):
                    v['is_done'] = new_status
                new_task = input('Введите новое название задачи\n'
                                 'Enter - не менять название\n'
                                 '>>> ')
                if new_task:
                    v['task'] = new_task
    else:
        print(f'ID {n} не найден')
    print(f'Операция завершена.')


def del_task(todo: dict):
    print('Список дел:')
    for key, value in todo.items():
        # Вывод ID, названия дела
        print("\033[7m {} \033[0m".format(f'ID {key} >>> {value["task"]}'))
    while True:  # Проверка ввода
        try:
            del_id = abs(int(input('Введите id задачи для удаления: ')))
        except ValueError:
            print('Wrong input')
        if del_id in todo.keys():
            del todo[del_id]
            break
        else:
            print(f'ID {del_id} не найден')
    print(f'Задача {del_id} удалена')


def save_data(todo: dict):
    with open('todo.csv', 'w', encoding='utf-8', newline='') as file:
        todo_save = csv.writer(file, delimiter=',')
        for k, v in todo.items():
            new_line = [k, v['task'], v['is_done']]
            todo_save.writerow(new_line)
    print('Данные успешно сохранены!')



def print_todo(to_do: dict, done: int) -> None:
    """
    Вывод в консоль списка дел на основе переданного значения 'done'.

    :param to_do: словарь с данными.
    :param done: параметр match для печати соответствующих данных.
    :return: None.
    """
    tmp_list = []
    match done:
        case 1:
            for key, value in to_do.items():
                # Вывод ID и названия дела
                tmp_list.append(f'ID {key} >>> {value["task"]} >>> {"Выполнено" if value["is_done"] else "Не выполнено"}')
            return '\n'.join(tmp_list)
        case 2:
            for value in to_do.values():
                for k, v in value.items():
                    if k == 'is_done' and v:
                        # Вывод названия выполненных дел
                        print("\033[36m {} \033[0m".format(value['task']))
        case 3:
            for value in to_do.values():
                for k, v in value.items():
                    if k == 'is_done' and not v:
                        # Вывод невыполненных дел
                        print("\033[31m {} \033[0m".format(value['task']))


get_tasks = print_todo(all_task, 1)