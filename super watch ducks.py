from ursina import *
from ursina import Audio
from time import perf_counter
import random
import threading
import time
import os
app = Ursina()
window.fullscreen = True
textures = ['pixil-frame-0 (1).png', 'pixil-frame-0.png']
layer = Entity(model='quad', texture='pixil-frame-0 (3).png', scale=8.6, position=Vec3(0,0,1))
goldduck = Entity(model='quad', texture='pixil-frame-0 (2).png', position=Vec3(-3.5, -3.5, 0))
cube = Entity(model='quad', texture=textures[0], scale=2, position=Vec3(3,0,0))
timer_text = Text(text='0000', origin=(0,0), scale=2, position=Vec2(0,0.30))
score_text = Text(text='0', origin=(-0.5,-0.5), scale=1, position=Vec2(-0.35,-0.4))
tex_index = 0
running = False
start_time = 0.0
accumulated = 0.0
score = 0
last_whole_second = -1
def format_no_dot(t: float) -> str:
    value = int(t * 100)
    return f'{value:04d}'
def update():
    global timer_text, running, start_time, accumulated, score, last_whole_second
    if running:
        elapsed = perf_counter() - start_time + accumulated
    else:
        elapsed = accumulated
    timer_text.text = format_no_dot(elapsed)
    whole_second = int(elapsed)
    if whole_second != last_whole_second:
        last_whole_second = whole_second
        if random.random() < 0.1:
            try:
                play_short.play()
            except Exception as e:
                print('Failed to play short sound:', e)
        if random.random() < 0.01:
            score += 1
            score_text.text = str(score)
def input(key):
    global running, start_time, accumulated, tex_index, last_whole_second
    if key == 'space':
        tex_index = 1 - tex_index
        cube.texture = textures[tex_index]
        if not running:
            start_time = perf_counter()
            running = True
            last_whole_second = int(accumulated)
        else:
            accumulated += perf_counter() - start_time
            running = False
    elif key == 'escape':
        application.quit()
AUDIO_PATH = 'forest-lark-and-european-robin.mp3'
SHORT_PATH = 'cartoon-quacking.mp3'
if AUDIO_PATH and os.path.isfile(AUDIO_PATH):
    music = Audio(AUDIO_PATH, autoplay=True, loop=True, volume=0.6)
else:
    print('Background audio not found:', AUDIO_PATH)
    music = None
if SHORT_PATH and os.path.isfile(SHORT_PATH):
    play_short = Audio(SHORT_PATH, autoplay=False, loop=False, volume=1.0)
else:
    if music is not None:
        play_short = music
    else:
        class Silent:
            def play(self): pass
        play_short = Silent()
    print('Short audio not found, using fallback:', SHORT_PATH)
app.run()