import turtle
import math
import random
import time

# Инициализация окошка игры

window = turtle.Screen()
window.bgcolor("black")
window.title("Dungeon game")
window.setup(700, 700)

turtle.register_shape("wall.gif")
turtle.register_shape("ghost.gif")
turtle.register_shape("wizard.gif")
turtle.register_shape("box.gif")
turtle.register_shape("hero.gif")

# Класс поля

class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.color("blue")
        self.shape("square")
        self.speed(0)


# Класс персонажа

class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.shape("wizard.gif")
        self.speed(0)
        self.color("purple")
        self.gold = 0
        self.health = 1000

# Функции для перемещения игрока по полю
    def go_up(self):
        if (self.xcor(), self.ycor() + 24) not in walls:
            self.goto(self.xcor(), self.ycor() + 24)

    def go_down(self):
        if (self.xcor(), self.ycor() - 24) not in walls:
            self.goto(self.xcor(), self.ycor() - 24)

    def go_left(self):
        if (self.xcor() - 24, self.ycor()) not in walls:
            self.goto(self.xcor() - 24, self.ycor())

    def go_right(self):
        if (self.xcor() + 24, self.ycor()) not in walls:
            self.goto(self.xcor() + 24, self.ycor())

#Функция,проверяющая находится ли игрок в одной клетке с каким-либо другим объектом

    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))
        if distance == 0:
            print(distance)
            return True
        else:
            return False

#Класс сокровищ

class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.shape("box.gif")
        self.color("gold")
        self.gold = 50
        self.goto(x, y)

# Операция удаления сокровищ, используется, когда герой доходит до сокровища
    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

#Класс врагов

class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.shape("ghost.gif")
        self.goto(x, y)
        self.health = 10
        self.direction = random.choice(["up", "down", "left", "right"])

# Фукнции перемещения врагов
    def move(self):
        if self.direction == "up":
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx = 0
            dy = -24
        elif self.direction == "left":
            dx = -24
            dy = 0
        else:
            dx = 24
            dy = 0

        if (self.xcor() + dx, self.ycor() + dy) not in walls:
            self.goto(self.xcor() + dx, self.ycor() + dy)
        else:
            self.direction = random.choice(["up", "down", "left", "right"])
        turtle.ontimer(self.move, t=random.randint(100, 300))

# Функция удаления врага
    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()


def Generate_level():

    # Метод для подсчёта количества пустых клеток вокруг данной клетки
    def countCells(wall1):
        count = 0
        if (maze[wall1[0] - 1][wall1[1]] == ' '):
            count += 1
        if (maze[wall1[0] + 1][wall1[1]] == ' '):
            count += 1
        if (maze[wall1[0]][wall1[1] - 1] == ' '):
            count += 1
        if (maze[wall1[0]][wall1[1] + 1] == ' '):
            count += 1

        return count

    # Создание масссива лабиринта
    maze = []

# Сначала помечаем все клетки непосещёнными
    for i in range(0, 25):
        stroka = ['u']*25
        maze.append(stroka)

# Задаём координаты начальной точки, причём делаем это так, чтобы точка оказалась внутри поля, а не с краю
    begin_x = int(random.random() * 25)
    begin_y = int(random.random() * 25)
    if (begin_x == 0):
        begin_x += 1
    if (begin_x == 24):
        begin_x -= 1
    if (begin_y == 0):
        begin_y += 1
    if (begin_y == 24):
        begin_y -= 1

# Помечаем выбранную начальную точку и добавляем
    maze[begin_x][begin_y] = ' '
# Cоздаём массив стен
    walls = []
    walls.append([begin_x - 1, begin_y])
    walls.append([begin_x, begin_y - 1])
    walls.append([begin_x, begin_y + 1])
    walls.append([begin_x + 1, begin_y])

    # Обозначаем стены в лабиринте
    maze[begin_x - 1][begin_y] = 'X'
    maze[begin_x][begin_y - 1] = 'X'
    maze[begin_x][begin_y + 1] = 'X'
    maze[begin_x + 1][begin_y] = 'X'

    while (walls):
        # Выбираем случайный элемет в массиве стен
        wall1 = walls[int(random.random() * len(walls)) - 1]

        # Проверяем не находится ли элемент на левом краю
        if (wall1[1] != 0):
            if (maze[wall1[0]][wall1[1] - 1] == 'u' and maze[wall1[0]][wall1[1] + 1] == ' '):
                # Находим количество уже помеченных ячеек вокруг рассматриваемого элемента
                count = countCells(wall1)

                if (count < 2):
                    # Обозначаем рассматриваемый элемент, как проход в лабиринте
                    maze[wall1[0]][wall1[1]] = ' '

                    # Добавляем новые стены
                    if (wall1[0] != 0):
                        if (maze[wall1[0] - 1][wall1[1]] != ' '):
                            maze[wall1[0] - 1][wall1[1]] = 'X'
                        if ([wall1[0] - 1, wall1[1]] not in walls):
                            walls.append([wall1[0] - 1, wall1[1]])

                    if (wall1[0] != 25 - 1):
                        if (maze[wall1[0] + 1][wall1[1]] != ' '):
                            maze[wall1[0] + 1][wall1[1]] = 'X'
                        if ([wall1[0] + 1, wall1[1]] not in walls):
                            walls.append([wall1[0] + 1, wall1[1]])

                    if (wall1[1] != 0):
                        if (maze[wall1[0]][wall1[1] - 1] != ' '):
                            maze[wall1[0]][wall1[1] - 1] = 'X'
                        if ([wall1[0], wall1[1] - 1] not in walls):
                            walls.append([wall1[0], wall1[1] - 1])

                # Удаляем стену из массива рассматриваемых элементов(стен)
                for wall in walls:
                    if (wall[0] == wall1[0] and wall[1] == wall1[1]):
                        walls.remove(wall)

                continue

        # Проверяем не находится ли элемент в верхней строке
        if (wall1[0] != 0):
            if (maze[wall1[0] - 1][wall1[1]] == 'u' and maze[wall1[0] + 1][wall1[1]] == ' '):

                count = countCells(wall1)
                if (count < 2):
                    # Обозначаем рассматриваемый элемент, как проход в лабиринте
                    maze[wall1[0]][wall1[1]] = ' '

                    # Добавляем новые стены
                    if (wall1[0] != 0):
                        if (maze[wall1[0] - 1][wall1[1]] != ' '):
                            maze[wall1[0] - 1][wall1[1]] = 'X'
                        if ([wall1[0] - 1, wall1[1]] not in walls):
                            walls.append([wall1[0] - 1, wall1[1]])

                    if (wall1[1] != 0):
                        if (maze[wall1[0]][wall1[1] - 1] != ' '):
                            maze[wall1[0]][wall1[1] - 1] = 'X'
                        if ([wall1[0], wall1[1] - 1] not in walls):
                            walls.append([wall1[0], wall1[1] - 1])

                    if (wall1[1] != 25 - 1):
                        if (maze[wall1[0]][wall1[1] + 1] != ' '):
                            maze[wall1[0]][wall1[1] + 1] = 'X'
                        if ([wall1[0], wall1[1] + 1] not in walls):
                            walls.append([wall1[0], wall1[1] + 1])

                #Удаляем стену из массива рассматриваемых элементов(стен)
                for wall in walls:
                    if (wall[0] == wall1[0] and wall[1] == wall1[1]):
                        walls.remove(wall)

                continue

        # Проверяем не находится ли элемент в нижней строке
        if (wall1[0] != 25 - 1):
            if (maze[wall1[0] + 1][wall1[1]] == 'u' and maze[wall1[0] - 1][wall1[1]] == ' '):

                count = countCells(wall1)
                if (count < 2):
                    # Обозначаем текущий элемент, как проход в лабиринте
                    maze[wall1[0]][wall1[1]] = ' '

                    # Добавляем новые стены
                    if (wall1[0] != 25 - 1):
                        if (maze[wall1[0] + 1][wall1[1]] != ' '):
                            maze[wall1[0] + 1][wall1[1]] = 'X'
                        if ([wall1[0] + 1, wall1[1]] not in walls):
                            walls.append([wall1[0] + 1, wall1[1]])
                    if (wall1[1] != 0):
                        if (maze[wall1[0]][wall1[1] - 1] != ' '):
                            maze[wall1[0]][wall1[1] - 1] = 'X'
                        if ([wall1[0], wall1[1] - 1] not in walls):
                            walls.append([wall1[0], wall1[1] - 1])
                    if (wall1[1] != 25 - 1):
                        if (maze[wall1[0]][wall1[1] + 1] != ' '):
                            maze[wall1[0]][wall1[1] + 1] = 'X'
                        if ([wall1[0], wall1[1] + 1] not in walls):
                            walls.append([wall1[0], wall1[1] + 1])

                #Удаляем стену из массива рассматриваемых элементов(стен)
                for wall in walls:
                    if (wall[0] == wall1[0] and wall[1] == wall1[1]):
                        walls.remove(wall)

                continue

        #Проверяем не находится ли элемент в самом правом столбце
        if (wall1[1] != 25 - 1):
            if (maze[wall1[0]][wall1[1] + 1] == 'u' and maze[wall1[0]][wall1[1] - 1] == ' '):

                count = countCells(wall1)
                if (count < 2):
                    # Обозначаем текущий элемент, как проход в лабиринте
                    maze[wall1[0]][wall1[1]] = ' '

                    # Добавляем новые стены
                    if (wall1[1] != 25 - 1):
                        if (maze[wall1[0]][wall1[1] + 1] != ' '):
                            maze[wall1[0]][wall1[1] + 1] = 'X'
                        if ([wall1[0], wall1[1] + 1] not in walls):
                            walls.append([wall1[0], wall1[1] + 1])
                    if (wall1[0] != 25 - 1):
                        if (maze[wall1[0] + 1][wall1[1]] != ' '):
                            maze[wall1[0] + 1][wall1[1]] = 'X'
                        if ([wall1[0] + 1, wall1[1]] not in walls):
                            walls.append([wall1[0] + 1, wall1[1]])
                    if (wall1[0] != 0):
                        if (maze[wall1[0] - 1][wall1[1]] != ' '):
                            maze[wall1[0] - 1][wall1[1]] = 'X'
                        if ([wall1[0] - 1, wall1[1]] not in walls):
                            walls.append([wall1[0] - 1, wall1[1]])

                #Удаляем стену из массива рассматриваемых элементов(стен)
                for wall in walls:
                    if (wall[0] == wall1[0] and wall[1] == wall1[1]):
                        walls.remove(wall)

                continue

        #Удаляем стену из массива рассматриваемых элементов(стен) - случай, когда мы не удалили рассматриваемый элемент ранее
        for wall in walls:
            if (wall[0] == wall1[0] and wall[1] == wall1[1]):
                walls.remove(wall)

    # Оставшиеся не посещёнными клетки помечаем, как стены
    for i in range(0, 25):
        for j in range(0, 25):
            if (maze[i][j] == 'u'):
                maze[i][j] = 'X'
    return maze


# Уровни игры
list_of_levels = [""]

#Генерация лабиринта
level_1 = Generate_level()
#Массив, в котором хранятся координаты прохода лабиринта
spaces = []
#Массив, в котором хранятся координаты стен лабиринта
walls1 = []

#Заполнение массива стен и проходов лабиринта
for i in range(25):
    for j in range(25):
        if level_1[i][j] == ' ':
            spaces.append([i, j])
        elif i != 0 and i != 24 and j != 0 and j != 24:
            walls1.append([i, j])

#Определение начальной координаты персонажа
coordinate_person = spaces[int(random.random() * len(spaces)) - 1]
spaces.remove(coordinate_person)
level_1[coordinate_person[0]][coordinate_person[1]] = 'P'

#Добавление дополнительных проходов в лабиринт
for i in range(70):
    coordinate_path = walls1[int(random.random() * (len(walls1) - 1))]
    left = [coordinate_path[0] - 1, coordinate_path[1]]
    right = [coordinate_path[0] + 1, coordinate_path[1]]
    up = [coordinate_path[0], coordinate_path[1] - 1]
    down = [coordinate_path[0], coordinate_path[1] + 1]
    count_free_cells = 0
    if left[0] > -1 and level_1[left[0]][left[1]] == ' ':
        count_free_cells += 1
    if right[0] < 25 and level_1[right[0]][right[1]] == ' ':
        count_free_cells += 1
    if up[1] > -1 and level_1[up[0]][up[1]] == ' ':
        count_free_cells += 1
    if down[1] < 25 and level_1[down[0]][down[1]] == ' ':
        count_free_cells += 1
    if count_free_cells >= 2:
        level_1[coordinate_path[0]][coordinate_path[1]] = ' '
        spaces.append(coordinate_path)
        walls1.remove(coordinate_path)

#Определение координат врагов

for i in range(7):
    coordinate_enemy = spaces[int(random.random() * (len(spaces) - 1))]
    level_1[coordinate_enemy[0]][coordinate_enemy[1]] = 'E'
    spaces.remove(coordinate_enemy)

#Определение координат сокровищ

for i in range(3):
    coordinate_box = spaces[int(random.random() * (len(spaces) - 1))]
    level_1[coordinate_box[0]][coordinate_box[1]] = 'T'
    spaces.remove(coordinate_box)

list_of_levels.append(level_1)

# Массив сокровищ
treasures = []

# Массив врагов

enemies = []

#Функция создание лабиринта и вывода его на экран

def create_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            object = level[y][x]

            # Подсчёт координат расположения на экране

            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            if object == "X":
                pen.goto(screen_x, screen_y)
                pen.shape("wall.gif")
                pen.stamp()
                walls.append((screen_x, screen_y))
            if object == "P":
                player1.showturtle()
                player1.goto(screen_x, screen_y)
            if object == "T":
                treasures.append(Treasure(screen_x, screen_y))
            if object == "E":
                enemies.append(Enemy(screen_x, screen_y))


# Создание объекта класса поля
pen = Pen()

# Создание объекта класса игрок
player1 = Player()
player1.hideturtle()

# Координаты стен
walls = []

create_maze(list_of_levels[1])

player2 = Player()
player2.hideturtle()

#Проверка на количество игроков, если check == False, то количество игроков - 1, иначе - 2
check = False
x = turtle.textinput("Количество игроков", "1 или 2")

#Создание второго игрока
if int(x) == 2:
    check = True
    coordinate_person = spaces[int(random.random() * len(spaces)) - 1]
    spaces.remove(coordinate_person)
    level_1[coordinate_person[0]][coordinate_person[1]] = 'P'
    screen_x = -288 + (coordinate_person[0] * 24)
    screen_y = 288 - (coordinate_person[1] * 24)
    player2.shape("hero.gif")
    player2.goto(screen_x, screen_y)
    player2.showturtle()


# Связывание клавиатуры и экрана

turtle.listen()
turtle.onkey(player1.go_up, "Up")
turtle.onkey(player1.go_down, "Down")
turtle.onkey(player1.go_left, "Left")
turtle.onkey(player1.go_right, "Right")
turtle.onkey(player2.go_up, "w")
turtle.onkey(player2.go_down, "s")
turtle.onkey(player2.go_left, "a")
turtle.onkey(player2.go_right, "d")

window.tracer(0)

for enemy in enemies:
    turtle.ontimer(enemy.move, t=250)

# Главный цикл игры

while True:
    # Проверка на то, что персонаж 1 дошёл до сокровища
    for t in treasures:
        if player1.is_collision(t):
            player1.gold += t.gold
            t.destroy()
            treasures.remove(t)

    # Проверка на то, что персонаж 2 дошёл до сокровища
    for t in treasures:
        if player2.is_collision(t):
            player2.gold += t.gold
            t.destroy()
            treasures.remove(t)

    # Проверка на то, что персонаж собрал все сундуки
    if not (len(treasures)):
        window.update()
        pen.goto(0, 0)
        if check:
            if player1.gold > player2.gold:
                pen.write("The winner is\n      player1", move=False, align="center", font=("Arial", 50, "normal"))
            else:
                pen.write("The winner is\n      player2", move=False, align="center", font=("Arial", 50, "normal"))
        else:
            pen.write("You have won", move=False, align="center", font=("Arial", 80, "normal"))
        time.sleep(3)
        break

    # Проверка на то, что персонаж столкнулся с врагом
    for enemy in enemies:
        if player1.is_collision(enemy):
            player1.health -= enemy.health
        if player2.is_collision(enemy):
            player2.health -= enemy.health

    # Проверка на количество здоровья персонажа в случае режима игры 2 героев

    if check and (player1.health <=0 or player2.health <= 0):
        window.update()
        pen.goto(0, 0)
        if player1.health <=0:
            pen.write("The winner is\n      player2", move=False, align="center", font=("Arial", 50, "normal"))
        else:
            pen.write("The winner is\n      player1", move=False, align="center", font=("Arial", 50, "normal"))
        time.sleep(3)
        break

    # Проверка на количество здоровья персонажа, если количество здоровья меньше 0, то игра завершается
    if player1.health <= 0:
        window.update()
        player1.hideturtle()
        pen.goto(0, 0)
        pen.write("Game Over", move=False, align="center", font=("Arial", 80, "normal"))
        time.sleep(3)
        pen.clear()
        player1.clear()
        break
    window.update()
