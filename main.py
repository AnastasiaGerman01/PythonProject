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

SIZE_OF_FIELD = 24

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
        if (self.xcor(), self.ycor() + SIZE_OF_FIELD) not in walls:
            self.goto(self.xcor(), self.ycor() + SIZE_OF_FIELD)

    def go_down(self):
        if (self.xcor(), self.ycor() - SIZE_OF_FIELD) not in walls:
            self.goto(self.xcor(), self.ycor() - SIZE_OF_FIELD)

    def go_left(self):
        if (self.xcor() - SIZE_OF_FIELD, self.ycor()) not in walls:
            self.goto(self.xcor() - SIZE_OF_FIELD, self.ycor())

    def go_right(self):
        if (self.xcor() + SIZE_OF_FIELD, self.ycor()) not in walls:
            self.goto(self.xcor() + SIZE_OF_FIELD, self.ycor())

#Функция,проверяющая находится ли игрок в одной клетке с каким-либо другим объектом

    def check_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))
        if distance == 0:
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
    def go(self):
        if self.direction == "up":
            dx = 0
            dy = SIZE_OF_FIELD
        elif self.direction == "down":
            dx = 0
            dy = -SIZE_OF_FIELD
        elif self.direction == "left":
            dx = -SIZE_OF_FIELD
            dy = 0
        else:
            dx = SIZE_OF_FIELD
            dy = 0

        if (self.xcor() + dx, self.ycor() + dy) not in walls:
            self.goto(self.xcor() + dx, self.ycor() + dy)
        else:
            self.direction = random.choice(["up", "down", "left", "right"])
        turtle.ontimer(self.go, t=random.randint(100, 300))

# Функция удаления врага
    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()


#Метод генерации лабиринта

def Generate_level():

    #Метод для подсчёта пустых клеток вокург обрабатываемой клетки
    def Count(wall):
        count = 0
        if maze[wall[0] - 1][wall[1]] == ' ':
            count += 1
        if maze[wall[0]][wall[1] - 1] == ' ':
            count += 1
        if maze[wall[0] + 1][wall[1]] == ' ':
            count += 1
        if maze[wall[0]][wall[1] + 1] == ' ':
            count += 1
        return count

    #Создание лабиринта
    maze = []
    for i in range(25):
        stroka = ['u'] * 25
        maze.append(stroka)

    #Определение начальной точки лабиринта
    begin_x = int(random.random() * 25)
    begin_y = int(random.random() * 25)
    if begin_x == 0:
        begin_x += 1
    if begin_x == SIZE_OF_FIELD:
        begin_x -= 1
    if begin_y == 0:
        begin_y += 1
    if begin_y == SIZE_OF_FIELD:
        begin_y -= 1

    maze[begin_x][begin_y] = ' '

    #Добавление в массив стен вокруг обрабатываемой клетки
    walls = []
    walls.append([begin_x + 1, begin_y])
    walls.append([begin_x, begin_y + 1])
    walls.append([begin_x - 1, begin_y])
    walls.append([begin_x, begin_y - 1])

    while (len(walls)):
        #Выбор случайной клетки из ещё не обработанных
        element = walls[int(random.random() * len(walls)) - 1]
        #Проверка на то, что клетка не является крайней
        if element[0] == 0 or element[0] == SIZE_OF_FIELD or element[1] == 0 or element[1] == SIZE_OF_FIELD:
            maze[element[0]][element[1]] = 'X'
            for i in range(len(walls)):
                if walls[i] == element:
                    walls.pop(i)
                    break
        else:
            #Подсчёт количества пустых клеток вокруг обрабатываемой клетки, если количество клеток меньше 2,
            # то делаем данную клетку проходом лабиринта, иначе - стеной
            count = Count(element)
            if count < 2:
                maze[element[0]][element[1]] = ' '
                walls.append([element[0] - 1, element[1]])
                walls.append([element[0], element[1] - 1])
                walls.append([element[0] + 1, element[1]])
                walls.append([element[0], element[1] + 1])
            for i in range(len(walls)):
                if walls[i] == element:
                    walls.pop(i)
                    break
    # Обрабатываем оставшиеся элементы
    for i in range(25):
        for j in range(25):
            if maze[i][j] == 'u':
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

#Выбор уровня игры
level_of_difficulty = turtle.textinput("Уровень сложности", "1, 2, 3")

# Массив сокровищ
treasures = []

# Массив врагов
enemies = []

# Создание объекта класса поля
pen = Pen()

# Создание объекта класса игрок
player1 = Player()
player1.hideturtle()

# Координаты стен
walls = []

player2 = Player()
player2.hideturtle()

#Проверка на количество игроков, если check == False, то количество игроков - 1, иначе - 2
check = False
quantity_of_players = turtle.textinput("Количество игроков", "1 или 2")


class gameApp():

     def Run(self):
         # Заполнение массива стен и проходов лабиринта
         for i in range(25):
             for j in range(25):
                 if level_1[i][j] == ' ':
                     spaces.append([i, j])
                 elif i != 0 and i != SIZE_OF_FIELD and j != 0 and j != SIZE_OF_FIELD:
                     walls1.append([i, j])

         # Определение координат врагов

         for i in range(5 * int(level_of_difficulty)):
             coordinate_enemy = spaces[int(random.random() * (len(spaces) - 1))]
             level_1[coordinate_enemy[0]][coordinate_enemy[1]] = 'E'
             spaces.remove(coordinate_enemy)

             # Определение координат сокровищ

         for i in range(3 * int(level_of_difficulty)):
             coordinate_box = spaces[int(random.random() * (len(spaces) - 1))]
             level_1[coordinate_box[0]][coordinate_box[1]] = 'T'
             spaces.remove(coordinate_box)

         list_of_levels.append(level_1)

         # Определение начальной координаты персонажа
         while True:
             coordinate_person = spaces[int(random.random() * len(spaces)) - 1]
             if level_1[coordinate_person[0]][coordinate_person[1]] == 'X':
                 continue
             if level_1[coordinate_person[0] + 1][coordinate_person[1]] == 'E':
                 continue
             if level_1[coordinate_person[0]][coordinate_person[1] + 1] == 'E':
                 continue
             if level_1[coordinate_person[0] - 1][coordinate_person[1]] == 'E':
                 continue
             if level_1[coordinate_person[0]][coordinate_person[1] - 1] == 'E':
                 continue
             break
         spaces.remove(coordinate_person)
         level_1[coordinate_person[0]][coordinate_person[1]] = 'P'

         # Создание второго игрока
         if int(quantity_of_players) == 2:
             check = True
             while True:
                 coordinate_person = spaces[int(random.random() * len(spaces)) - 1]
                 if level_1[coordinate_person[0]][coordinate_person[1]] == 'X':
                     continue
                 if level_1[coordinate_person[0] + 1][coordinate_person[1]] == 'E':
                     continue
                 if level_1[coordinate_person[0]][coordinate_person[1] + 1] == 'E':
                     continue
                 if level_1[coordinate_person[0] - 1][coordinate_person[1]] == 'E':
                     continue
                 if level_1[coordinate_person[0]][coordinate_person[1] - 1] == 'E':
                     continue
                 break
             spaces.remove(coordinate_person)
             level_1[coordinate_person[0]][coordinate_person[1]] = 'P2'
             screen_x = -288 + (coordinate_person[0] * SIZE_OF_FIELD)
             screen_y = 288 - (coordinate_person[1] * SIZE_OF_FIELD)
             player2.hideturtle()

game = gameApp()
game.Run()

#Функция создание лабиринта и вывода его на экран

def create_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            object = level[y][x]

            # Подсчёт координат расположения на экране

            screen_x = -288 + (x * SIZE_OF_FIELD)
            screen_y = 288 - (y * SIZE_OF_FIELD)

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
            if object == 'P2':
                player2.shape("hero.gif")
                player2.goto(screen_x, screen_y)
                player2.showturtle()



create_maze(level_1)

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
    turtle.ontimer(enemy.go, t=250)

# Главный цикл игры

while True:
    # Проверка на то, что персонаж 1 дошёл до сокровища
    for t in treasures:
        if player1.check_collision(t):
            player1.gold += t.gold
            t.destroy()
            treasures.remove(t)

    # Проверка на то, что персонаж 2 дошёл до сокровища
    for t in treasures:
        if player2.check_collision(t):
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
        if player1.check_collision(enemy):
            player1.health -= enemy.health
        if player2.check_collision(enemy):
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
