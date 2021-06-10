from tkinter import *
from tkinter import messagebox
from random import choice, randrange
from copy import deepcopy
import time
# Операция присваивания не копирует объект, он лишь создаёт ссылку на объект. Для изменяемых коллекций,
# или для коллекций,
# содержащих изменяемые элементы, часто необходима такая копия, чтобы её можно было изменить,
# не изменяя оригинал.
# copy.copy(x) - возвращает поверхностную копию x.
#
# copy.deepcopy(x) - возвращает полную копию x.

W, H = 10, 20  # количество квадратов по оси х и оси у
size_sqr = 40  # размер квадрата
size_game = W * size_sqr, H * size_sqr  # размер контейнера тетриса
window = 700, 850
FPS = 60

def on_closing():
    global app_running
    if messagebox.askokcancel("Выход из приложения", "Хотите выйти из приложения?"):
        app_running = False

tk = Tk()
app_running = True
tk.protocol("WM_DELETE_WINDOW", on_closing)
tk.title("Тетрис")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
# tk.iconbitmap("bomb-3175208_640.ico")

canvas = Canvas(tk, width=window[0], height=window[1], bg="black", highlightthickness=0)  # размеры по 0 и 1 индексу
canvas.pack()

def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')
        return "0"


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))

# создаем 2 область
game = Canvas(tk, width=W * size_sqr, height=H * size_sqr, bg='yellow', highlightthickness=0)
game.place(x=0, y=0, anchor=NW)


img_obj1 = PhotoImage(file="img/fon2.png")  # фон тетриса
canvas.create_image(0, 0, anchor=NW, image=img_obj1)  # 0,0 - координаты, anchor = NordWest( верхний левый угол)

grid = [game.create_rectangle(x * size_sqr, y * size_sqr, x * size_sqr + size_sqr, y * size_sqr + size_sqr) for x in
        range(W) for y in range(H)]

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],  # создадим список позиций
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[[x + W // 2, y + 1, 1, 1] for x, y in fig_pos] for fig_pos in figures_pos]
# создаем виртуальный список элементов
# для создания одного квадрата (0,0, window - 2, window -2)
field = [[0 for i in range(W)] for j in range(H)]  # логическая область игрового поля
# Метод grid позволяет поместить элемент в конкретную ячейку условной сетки

anim_count, anim_speed, anim_limit = 0, 60, 2000

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
record = "0"

canvas.create_text(505, 30, text="Тетрис", font=("Arial", 30), fill='dark blue', anchor=NW)
canvas.create_text(500, 645, text="Рекорд", font=("Arial", 30), fill='orange', anchor=NW)
_record=canvas.create_text(500, 600, text = record, font=("Arial", 30), fill='gold', anchor=NW)
canvas.create_text(500, 745, text="Ваш счет", font=("Arial", 30), fill='orange', anchor=NW)
_score =canvas.create_text(500, 700, font=("Arial", 30), fill='violet', anchor=NW)
# Создание эффекта финиша
get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))  # используем функцию лямбда
figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
# выбираем случайную фигуру и следующую фигуру
color, next_color = get_color(), get_color()  # выбираем цвета


def rgb_to_hex(rgb):  # преобразуем из rgb в 16-чный код цвета
    return '#%02x%02x%02x' % rgb


print(rgb_to_hex(get_color()))  # проверим формат кода

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
# выбираем случайную фигуру и следующую фигуру
color, next_color = get_color(), get_color()  # выбираем цвета

def check_borders():
    if figure[i][0] < 0 or figure[i][0] > W - 1:
        return False
    elif figure[i][1] > H - 1 or field[figure[i][1]][figure[i][0]]:
        return False
    return True


def move_obj(event):
    global rotate, anim_limit, dx
    if event.keysym == 'Up':
        rotate = True
    elif event.keysym == 'Down':
        anim_limit = 100
    elif event.keysym == 'Left':
        dx = -1
    elif event.keysym == 'Right':
        dx = 1

game.bind_all("<KeyPress-Up>",move_obj)
game.bind_all("<KeyPress-Down>",move_obj)
game.bind_all("<KeyPress-Left>",move_obj)
game.bind_all("<KeyPress-Right>",move_obj)

dx, rotate = 0, False
while app_running:
    if app_running:
        record = get_record()
        # move x
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i][0] += dx
            if not check_borders():
                figure = deepcopy(figure_old)
                break
        # move y
        anim_count += anim_speed
        if anim_count > anim_limit:
            anim_count = 0
            figure_old = deepcopy(figure)
            for i in range(4):
                figure[i][1] += 1
                if not check_borders():
                    for i in range(4):
                        field[figure_old[i][1]][figure_old[i][0]] = color
                    figure, color = next_figure, next_color
                    next_figure, next_color = deepcopy(choice(figures)), get_color()
                    anim_limit = 2000
                    break
        # rotate
        center = figure[0]
        figure_old = deepcopy(figure)
        if rotate:
            for i in range(4):
                x = figure[i][1] - center[1]
                y = figure[i][0] - center[0]
                figure[i][0] = center[0] - x
                figure[i][1] = center[1] + y
                if not check_borders():
                    figure = deepcopy(figure_old)
                    break
        # check lines
        line, lines = H - 1, 0
        for row in range(H - 1, -1, -1):
            count = 0
            for i in range(W):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < W:
                line -= 1
            else:
                anim_speed += 3
                lines += 1
        # compute score
        score += scores[lines]

        fig = []
        # draw figure
        for i in range(4):
            figure_rect_x = figure[i][0] * size_sqr
            figure_rect_y = figure[i][1] * size_sqr
            fig.append(game.create_rectangle(figure_rect_x, figure_rect_y, figure_rect_x + size_sqr, figure_rect_y + size_sqr, fill=rgb_to_hex(color)))

        # draw field
        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect_x, figure_rect_y = x * size_sqr, y * size_sqr
                    fig.append(game.create_rectangle(figure_rect_x, figure_rect_y, figure_rect_x + size_sqr,
                                                        figure_rect_y + size_sqr, fill=rgb_to_hex(col)))

        figure2 = []
        # draw next figure
        for i in range(4):
            figure_rect_x = next_figure[i][0] * size_sqr + 380
            figure_rect_y = next_figure[i][1] * size_sqr + 185
            figure2.append(canvas.create_rectangle(figure_rect_x, figure_rect_y, figure_rect_x + size_sqr, figure_rect_y + size_sqr,
                                fill=rgb_to_hex(next_color)))
        # draw titles
        canvas.itemconfigure(_score, text=str(score))
        canvas.itemconfigure(_record, text=record)

        # game over
        for i in range(W):
            if field[0][i]:
                set_record(record, score)
                field = [[0 for i in range(W)] for i in range(H)]
                anim_count, anim_speed, anim_limit = 0, 60, 2000
                score = 0
                for item in grid:
                    game.itemconfigure(item, fill=rgb_to_hex(get_color()))
                    time.sleep(0.005)
                    tk.update_idletasks()
                    tk.update()

                for item in grid:
                    game.itemconfigure(item, fill="")


        dx, rotate = 0, False
        tk.update_idletasks()
        tk.update()
        for id_fig in fig: game.delete(id_fig)
        for id_fig in figure2: canvas.delete(id_fig)
    time.sleep(0.005)

tk.destroy()
#tk.mainloop()