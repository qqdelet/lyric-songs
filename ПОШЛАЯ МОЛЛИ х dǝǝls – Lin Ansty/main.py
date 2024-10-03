import pyglet
import random
import os
import sys

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # Путь, когда приложение запущено из .exe
else:
    base_path = os.path.dirname(__file__)  # Путь, когда приложение запущено из исходного кода

# Полные пути к ресурсам
mp3_path = os.path.join(base_path, "pm.mp3")
bg_gif_path = os.path.join(base_path, "BG.gif")
# Создание окна
window = pyglet.window.Window(820, 740)
batch = pyglet.graphics.Batch()
lyrics_labels = []
current_line = 0
line_height = 30  # Высота строки

hearts = []
MAX_HEARTS = 11  # Максимальное количество сердечек

# Загрузка музыки
music = pyglet.media.load(mp3_path)
music.play()
background_image = pyglet.image.load(bg_gif_path)
# Лирика с задержками
lyrics = [
    ("Настя, Настя", 3.0),
    ("Дай мне руку, чтобы не упасть мне", 4.0),
    ("Руку, чтобы не у—", 2.0),
    ("Мрачный и такой невкусный город смерти", 4.3),
    ("Там, где порох и вода грязнее черни", 5.2),
    ("Но даже здесь я слышу этот запах сирени", 5.2),
    ("Который тебя сделал красным небом весенним", 5.3),
    ("Даже здесь я слышу этот запах сирени", 5.3),
    ("Который тебя сделал красным небом весенним", 5.4),
    ("Даже здесь я слы-слышу этот запах сирени", 5.5),
    ("Который тебя сделал красным небом весенним", 5.4),
    ("Даже здесь я слышу этот запах сирени", 5.3),
    ("Который тебя сделал красным небом весенним", 12.3),
    ("Дай мне руку, чтобы не упасть мне", 3.5),
    ("Руку, чтобы не у—", 6.7),
    ("Дай мне руку, чтобы не упасть мне", 3.7),
    ("Руку, чтобы не у—", 3.7),
    ("Настя, Настя", 2.9),
    ("Дай мне руку, чтобы не упасть мне в этот", 4.4),
    ("Мрачный и такой невкусный город смерти", 5.1),
    ("Там, где порох и вода грязнее черни", 4.7),
    ("Но даже здесь я слышу этот запах сирени", 5.2),
    ("Который тебя сделал красным небом весенним", 5.5),
    ("Даже здесь я слышу этот запах сирени", 5.3),
    ("Который тебя сделал красным небом весенним", 5.5),
    ("Даже здесь я слышу этот запах сирени", 5.3),
    ("Который тебя сделал красным небом весенним", 5.5)]

def update(dt):
    global current_line
    if current_line < len(lyrics):
        text, delay = lyrics[current_line]
        label = pyglet.text.Label(text,
                                  font_name='Times New Roman',
                                  font_size=24,
                                  x=window.width // 2,
                                  y=window.height // 2 + (len(lyrics_labels) * line_height),
                                  anchor_x='center',
                                  anchor_y='center')
        lyrics_labels.append(label)
        
        # Убираем первую строку после каждых трех строк
        if len(lyrics_labels) > 3:
            lyrics_labels.pop(0)  # Удаляем первую строку
            # Поднимаем оставшиеся строки
            for i in range(len(lyrics_labels)):
                lyrics_labels[i].y -= line_height
        
        current_line += 1
        # Устанавливаем таймер для следующей строки
        pyglet.clock.schedule_once(update, delay)
    else:
        pyglet.app.exit()

def update_hearts(dt):
    for heart in hearts:
        heart.y -= random.randint(1, 7)  # Скорость падения сердечек
    hearts[:] = [heart for heart in hearts if heart.y > 0]  # Убираем сердечки, которые упали за экран

def add_heart(dt):
    if len(hearts) < MAX_HEARTS:  # Проверяем количество сердечек
        x = random.randint(0, window.width - 20)
        heart = pyglet.text.Label("♥", color=(255, 20, 147, 255), font_name='Arial', font_size=32, x=x, y=window.height, batch=batch)
        hearts.append(heart)

@window.event
def on_draw():
    window.clear()
    background_image.blit(0, 0, width=window.width, height=window.height)
    batch.draw()
    for label in lyrics_labels:
        label.draw()

# Начинаем обновление с первой строки
pyglet.clock.schedule_once(update, 0)
pyglet.clock.schedule_interval(add_heart, 0.5)      # Добавление сердечек каждые 0.5 секунды
pyglet.clock.schedule_interval(update_hearts, 0.05) # Обновление сердечек каждые 0.05 секунды

pyglet.app.run()