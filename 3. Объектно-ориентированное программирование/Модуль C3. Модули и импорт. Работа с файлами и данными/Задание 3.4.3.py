# Сделайте функцию, которая принимает от пользователя путь и выводит всю информацию о содержимом этой папки.
# Для реализации используйте функцию встроенного модуля os.walk().
# Если путь не указан, то сравнение начинается с текущей директории.

# это писал не я.
# я просто скопировал из образца. дело в том, что из тех объяснений которые предоставляет курс понять что-то и чему-то
# научится невозможно. так что, мне придётся подрудится, чтобы понять этот модуль. или, как я надеюсь, на
# моём парллельном курсе будет подробно изложен этот матерал.
import os


def walk_desc(path=None):
    start_path = path if path is not None else os.getcwd()

    for root, dirs, files in os.walk(start_path):
        print("Текущая директория", root)
        print("---")

        if dirs:
            print("Список папок", dirs)
        else:
            print("Папок нет")
        print("---")

        if files:
            print("Список файлов", files)
        else:
            print("Файлов нет")
        print("---")

        if files and dirs:
            print("Все пути:")
        for f in files:
            print("Файл ", os.path.join(root, f))
        for d in dirs:
            print("Папка ", os.path.join(root, d))
        print("===")


if __name__ == '__main__':
    walk_desc("../..")
