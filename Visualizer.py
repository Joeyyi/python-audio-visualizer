# -*- coding: utf-8 -*-
#reference:
#http://www.cnblogs.com/xiaowuyi/category/426566.html
#http://eyehere.net/2011/python-pygame-novice-professional-2/
#https://www.bilibili.com/video/av9615162/
#http://1029975378-qq-com.iteye.com/blog/1981053
#http://www.pygame.org/docs/ref/music.html
#https://docs.python.org/3/library/wave.html
#http://blog.csdn.net/daiyinger/article/details/48289575


import sys, math, wave, numpy, pygame
from pygame.locals import *
from scipy.fftpack import dct

N = 30 # num of bars
HEIGHT = 100 # height of a bar
WIDTH = 10 # width of a bar
FPS = 10

file_name = sys.argv[1]
status = 'stopped'
fpsclock = pygame.time.Clock()

# screen init, music playback
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode([N * WIDTH, 50 + HEIGHT]) 
pygame.display.set_caption('Audio Visulizer')
my_font = pygame.font.SysFont('consolas', 16)
pygame.mixer.music.load(file_name)
pygame.mixer.music.play()
pygame.mixer.music.set_endevent()
status = "playing"

# process wave data
f = wave.open(file_name, 'rb')
params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]
str_data  = f.readframes(nframes)  
f.close()  
wave_data = numpy.fromstring(str_data, dtype = numpy.short)  
wave_data.shape = -1,2  
wave_data = wave_data.T  


num = nframes

def visualizer(num):
    num = int(num)
    h = abs(dct(wave_data[0][nframes - num:nframes - num + N]))
    h = [min(HEIGHT,int(i **(1 / 2.5) * HEIGHT / 100)) for i in h]
    draw_bars(h)

def vis(status):
    global num
    if status == "stopped":
        num = nframes
        return
    elif status == "paused":
        visualizer(num)
    else:
        num -= framerate/FPS
        if num > 0:
            visualizer(num)

def get_time(): 
    seconds = max(0, pygame.mixer.music.get_pos()/1000)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    hms = ('%02d:%02d:%02d' % (h, m, s))
    return hms

def controller(key):
    global status
    if status == 'stopped':
        if key == K_RETURN:
            pygame.mixer.music.play()
            status = 'playing'
    elif status == 'paused':
        if key == K_RETURN:
            pygame.mixer.music.stop()
            status = 'stopped'
        elif key == K_SPACE:
            pygame.mixer.music.unpause()
            status = 'playing'
    elif status == 'playing':
        if key == K_RETURN:
            pygame.mixer.music.stop()
            status = 'stopped'
        elif key == K_SPACE:
            pygame.mixer.music.pause()
            status = 'paused'



def draw_bars(h):
    bars = []
    for i in h:
        bars.append([len(bars) * WIDTH,50 + HEIGHT-i,WIDTH - 1,i])
    for i in bars:
        pygame.draw.rect(screen,[255,255,255],i,0)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            controller(event.key)

    if num <= 0:
        status = 'stopped'

    name = my_font.render(file_name, True, (255,255,255))
    info = my_font.render(status.upper() + ' ' + get_time(), True, (255,255,255))
    screen.fill((0,0,0))
    screen.blit(name,(0, 0))
    screen.blit(info,(0, 18))
    fpsclock.tick(FPS)
    vis(status)

    pygame.display.update()


