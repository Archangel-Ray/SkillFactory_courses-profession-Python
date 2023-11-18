# ещё раз... я скопировал готовое решение. потому, что понять что либо из этих объяснений не возможно.
# так что сохранил пример как памятку и пошёл искать развёрнутые объяснения темы.


class OpenFile:
    def __init__(self, path, in_type):
        self.file = open(path, in_type)

    def __enter__(self):
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()


with OpenFile('hello.txt', 'wt') as f:
    f.write('Мой контекстный менеджер делает то же самое!')
