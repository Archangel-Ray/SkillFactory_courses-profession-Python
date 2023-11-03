from random import choice


# создаёт объект корабль
class Ship:
    def __init__(self, bow_of_the_ship_coordinates, ship_decks, ship_direction):
        # координаты корабля
        self.coordinates = [(bow_of_the_ship_coordinates[0] + num_deck, bow_of_the_ship_coordinates[1])
                            if ship_direction
                            else (bow_of_the_ship_coordinates[0], bow_of_the_ship_coordinates[1] + num_deck)
                            for num_deck in range(ship_decks)]
        # координаты примыкающие к кораблю
        self.around = set(filter(lambda x: type(x) is tuple,
                                 {(d[0] + dx, d[1] + dy)
                                  if 0 <= d[0] + dx < 6 and 0 <= d[1] + dy < 6 else None
                                  for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0),
                                                 (0, 1), (1, -1), (1, 0), (1, 1)]
                                  for d in self.coordinates}))


# поле боя
class Battlefield:
    def __init__(self, size=6):
        # размер поля для масштабирования, но я не доделал пока масштабирование. оставил на будущее
        self.size = size
        # поле боя
        self.field = {(line, column): " " for line in range(size) for column in range(size)}
        # обозначения столбцов. предполагалось использовать при масштабировании.
        # пока используется только на отображении самого поля
        self.battlefield_header = [chr(1072 + index) for index in range(self.size)]
        # список расставленых кораблей на поле
        self.ships = []

    # определяет наличие кораблей на поле. если кораблей нет конец игры
    def ending(self):
        return "П" in {x for x in self.field.values()}

    # возвращает множество из свободных клеток на поле
    def free_cells(self):
        cells = set()
        for key, value in self.field.items():
            if value == " ":
                cells.add(key)
        return cells

    # возвращает список свободных клеток с учётом края поля и примыкания всех кораблей
    def docking(self, num_dock, direction, check=True):
        free = set()
        if check:
            if direction:
                free = free.union(set(filter(lambda x: x[0] <= self.size - num_dock, self.free_cells())))
            else:
                free = free.union(set(filter(lambda x: x[1] <= self.size - num_dock, self.free_cells())))
        else:
            free = free.union(self.free_cells())
        for ship_in in self.ships:
            free = free.difference(ship_in.around)
        return list(free)

    # ставит созданный корабль на поле
    def adding_ship_to_the_field(self, ship):
        free_cells = self.docking(num_dock=1, direction=False, check=False)
        for coord in ship.coordinates:
            if coord not in free_cells:
                return False
        for coord in ship.coordinates:
            self.field[coord] = "П"
        self.ships.append(ship)
        return True

    # создаёт корабли случайно
    def random_placement_of_ships(self):
        decks = [3, 2, 2, 1, 1, 1, 1]
        for number in decks:
            while True:
                vertical = choice([True, False])
                list_free_cells = self.docking(number, vertical)
                if list_free_cells:
                    ship = Ship(choice(list_free_cells), number, vertical)
                    if self.adding_ship_to_the_field(ship):
                        break
                else:
                    return False
        return True

    # создание кораблей вручную
    def manual_placement_of_ships(self, coord, number, direction):
        ship = Ship(coord, number, direction)
        set_free_cells = self.free_cells()
        for coord_ship in ship.coordinates:
            if coord_ship not in set_free_cells:
                print("корабль на поле не встал.\nучитывай что корабль не должен выходить за границы поля\n"
                      "справа и снизу должно быть место для остальных палуб\nдавай ещё раз...")
                return False
        list_free_cells = self.docking(number, direction, check=False)
        if list_free_cells:
            for coord_ship in ship.coordinates:
                if coord_ship not in list_free_cells:
                    print("не могу сюда поставить.\nучти, что корабли не должны соприкасаться\nдавай ещё раз...")
                    return False
        self.adding_ship_to_the_field(ship)
        if len(self.ships) < 7:
            if self.docking(number, direction, check=False):
                return True
            else:
                print("вот незадачка... корабли не помещаются\n"
                      "давай как-то по компактней!\nначинаем расставлять заного!")
                return "reiterative"
        else:
            return True


# созаёт игрока
class AllGamers:
    def __init__(self):
        self.my_battlefield = None

    # запрос координаты
    def request_for_shot(self, field):
        raise NotImplementedError()


# создаёт компьютерного играка
class Computer(AllGamers):
    def request_for_shot(self, field):
        free = [key for key, value in field.items() if value == " " or value == "П"]
        shot_coord = choice(free)
        print(f"компьютер стрелял в -> {'абвгде'[shot_coord[1]]}{shot_coord[0] + 1}")
        return shot_coord


# создаёт игрока пользователя
class Gamer(AllGamers):
    def request_for_shot(self, field):
        shot_coord = list()
        input_shot = list(input("куда?"))
        while not shot_coord:
            if len(input_shot) < 2:
                print("с одним символом я пересечения не найду")
                input_shot = list(input("в координате должно быть два символа! куда?"))
                continue
            else:
                if len(input_shot) > 2:
                    print("координат должно быть две (пробел не нужен)")
                    input_shot = list(input("ещё раз, куда?"))
                    continue
                else:
                    if input_shot[0] in "123456":
                        shot_coord.append(int(input_shot[0]) - 1)
                        input_shot.pop(0)
                    else:
                        if input_shot[1] in "123456":
                            shot_coord.append(int(input_shot[1]) - 1)
                            input_shot.pop(1)
                        else:
                            print("строки нумеруются от 1 до 6. а где цифра в координатах?")
                            input_shot = list(input("введи координату. только уже с нужной цифрой"))
                            continue
                    if input_shot[0].isdigit():
                        print("а буква где? в координате должна быть буква")
                        input_shot = list(input("введи координату. и букву не забудь. (из обозначений столбиков)"))
                        shot_coord.clear()
                        continue
                    else:
                        letter = input_shot[0].lower()
                        if letter in "f<,dult":
                            if letter == "<":
                                letter = ","
                            shot_coord.append("f,dult".find(letter))
                        else:
                            if letter in "абвгде":
                                shot_coord.append("абвгде".find(letter))
                            else:
                                print("столбцы обозначены буквами от а до е. правильно называй столбцы")
                                input_shot = list(input("мы куда-то попадём?"))
                                shot_coord.clear()
                                continue
            return tuple(shot_coord)


# процесс игры
class GameProcess:
    def __init__(self):
        self.computer = Computer()
        self.gamer = Gamer()

    # создаёт поле боя и запускает расстановку кораблей
    def placement_of_ships(self, player, itself=False):
        the_ships_are_positioned = False
        while not the_ships_are_positioned:
            player.my_battlefield = Battlefield()
            if itself:
                the_ships_are_positioned = self.manual(player)
            else:
                the_ships_are_positioned = player.my_battlefield.random_placement_of_ships()

    # перебирает корабли игрока и запрашивает координату для установки на поле
    def manual(self, player):
        decks = [3, 2, 2, 1, 1, 1, 1]
        ship_name = {3: "трёхпалубный", 2: "двухпалубный", 1: "однопалубный"}
        for number in decks:
            while True:
                self.field_demonstration()
                print(f"ставим {ship_name[number]} корабль")
                if number != 1:
                    direction = True if input('нажми пробел если корабль надо ставить вертикально\n'
                                              'или куда-нибудь ещё нажми если горизонтально') == " " else False
                    print("_" * 10,
                          choice(["ладно", "хорошо", "принял", "и так сойдёт", "пусть будет так", "понял"]),
                          "_" * 10)
                    print("если считать слева на право и сверху в низ то\nнос корабля встанет", end=" ")
                else:
                    direction = choice([True, False])
                bow_of_the_ship = player.request_for_shot(player.my_battlefield.field)
                print(f"{'_' * 40}\n{'_' * 40}\n\n")
                reiterative = player.my_battlefield.manual_placement_of_ships(bow_of_the_ship, number, direction)
                if reiterative == "reiterative":
                    return False
                elif reiterative:
                    break
        return True

    # выводит состояние полей
    def field_demonstration(self):
        print(f"     твоё поле{' ' * 10}поле компьютера")
        print(f"  | {' '.join(self.gamer.my_battlefield.battlefield_header)} |", end=" " * 5)
        print(f"  | {' '.join(self.computer.my_battlefield.battlefield_header)} |")
        print("-" * 18 + " " * 4 + "-" * 18)
        for i in range(6):
            print(i + 1, end=" | ")
            for j in range(6):
                print(self.gamer.my_battlefield.field[(i, j)], end=" ")
            print("|", end=" " * 5)
            print(i + 1, end=" | ")
            for j in range(6):
                mark = self.computer.my_battlefield.field[(i, j)]
                if mark == "П":
                    print(" ", end=" ")
                else:
                    print(mark, end=" ")
            print("|")
        print("-" * 18 + " " * 4 + "-" * 18)

    # фиксирует результат выстрела
    @staticmethod
    def mark_shot_on_field(player, coord):
        field = player.field
        list_ship = player.ships
        if field[coord] == " ":
            print(f"{'_' * 40}\n{'_' * 17} мимо {'_' * 17}\n")
            field[coord] = "."
        elif field[coord] == ".":
            print(f"{' ' * 8}{'-' * 21}\n{' ' * 7}| сюда ты уже стрелял |\n{' ' * 8}{'-' * 21}")
            return 0
        elif field[coord] == "Х":
            print(f"{' ' * 4}{'-' * 29}\n{' ' * 3}| в этот корабль уже попадали |\n{' ' * 4}{'-' * 29}")
            return 0
        elif field[coord] == "П":
            for ship in list_ship:
                if coord in ship.coordinates:
                    if len(ship.coordinates) > 1:
                        ship.coordinates.remove(coord)
                        field[coord] = "Х"
                        print(f"{'_' * 40}\n{'_' * 17} попал {'_' * 16}\n")
                        return 0
                    else:
                        field[coord] = "Х"
                        for x in ship.around:
                            if field[x] == " ":
                                field[x] = "."
                        print(f"{'_' * 40}\n{'_' * 15} ПОТОПИЛ {'_' * 16}\n")
                        print("")
                        return 1
        return 1

    # собственно процесс игры здесь
    def movement(self):
        self.placement_of_ships(self.computer)
        it_self = True if input('\nвведи один пробел если хочешь расставить корабли сам\n'
                                'или что-нибудь другое нажми и они встанут сами как попало\n') == " " else False
        self.placement_of_ships(self.gamer, itself=it_self)
        whose_next = 0
        while self.computer.my_battlefield.ending() and self.gamer.my_battlefield.ending():
            if whose_next % 2 == 0:
                self.field_demonstration()
                print("твой выстрел")
                shot_coord = self.gamer.request_for_shot(self.computer.my_battlefield.field)
                whose_next += self.mark_shot_on_field(self.computer.my_battlefield, shot_coord)
            else:
                shot_coord = self.computer.request_for_shot(self.gamer.my_battlefield.field)
                whose_next += self.mark_shot_on_field(self.gamer.my_battlefield, shot_coord)
        if whose_next % 2 != 0:
            print(f"{'~' * 40}\n{'~' * 7}|{' ' * 7}ТЫ ВЫИГРАЛ!{' ' * 6}|{'~' * 7}\n"
                  f"{'~' * 7}| ФЛОТ ПРОТИВНИКА НА ДНЕ |{'~' * 7}\n{'~' * 40}")
        else:
            print(f"{'~' * 40}\n{'~' * 6}|{' ' * 6}комп выиграл.{' ' * 6}|{'~' * 7}\n"
                  f"{'~' * 6}| весь твой флот потоплен |{'~' * 7}\n{'~' * 40}")

    def start(self):
        print(f"{'~' * 40}\n{'~' * 13} МОРСКОЙ БОЙ {'~' * 14}\n{'~' * 40}")
        self.movement()
        self.field_demonstration()


g = GameProcess()
g.start()
