import sys
from random import randint
import pygame as pg
import pygame_widgets
from pygame.sprite import Group
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import time
pg.init()
pg.display.set_caption('PyGame')
screen = pg.display.set_mode((800, 600), pg.RESIZABLE)
clock = pg.time.Clock()
FONT_head = pg.font.Font(None, 35)
FONT_head.set_bold(True)
FONT_head.set_italic(True)
FONT_vol = pg.font.Font(None, 28)
FONT_score = pg.font.Font(None, 30)
FONT_back = pg.font.Font(None, 50)
FONT_score2 = pg.font.Font(None, 55)
FONT_back1 = pg.font.Font(None, 54)
FONT_button = pg.font.Font(None, 40)
FONT_button1 = pg.font.Font(None, 55)
FONT_OK = pg.font.Font(None, 55)
FONT_setting = pg.font.Font(None, 50)
FONT_exit = pg.font.Font(None, 50)
FONT_scoreboard = pg.font.Font(None, 50)
FONT_ARESTED = pg.font.Font(None, 85)
SCORE = 0
particles = []
particles1 = []
particle_image = pg.image.load("Sprite/apple.png")
NIGHT_COLOR = (20, 20, 20)
fog = pg.Surface((800, 600))
static_light_mask = pg.image.load("Lights/Vector_Smar33t_Objec.png").convert_alpha()
static_light_mask = pg.transform.scale(static_light_mask, (100, 100))
static_light_mask_rect = static_light_mask.get_rect()
start_time_static = 0
dinamic_light_mask = pg.image.load("Lights/light_350_hard.png").convert_alpha()
dinamic_light_mask = pg.transform.scale(dinamic_light_mask, (150, 150))
dinamic_light_mask_rect = dinamic_light_mask.get_rect()
dinamic_light_speed_y = 2
dinamic_light_speed_x = 2
dinamic_light_direction = [dinamic_light_speed_x, dinamic_light_speed_y]
slider = Slider(screen, 408, 216, 100, 10)
output = TextBox(screen, 375, 210, 20, 20, fontSize=16)
output.disable()
animation_right = [pg.transform.scale(pg.image.load(f'animations/r{i}.png'), (60, 100)) for i in range(1, 7)]
animation_left = [pg.transform.scale(pg.image.load(f'animations/l{i}.png'), (60, 100)) for i in range(1, 7)]
map = pg.image.load('animations/map.png')
map = pg.transform.scale(map, (800, 600))
menu_esc = pg.image.load('Sprite/menu_esc.png')
menu_esc = pg.transform.scale(menu_esc, (400, 400))
menu_esc_rect = menu_esc.get_rect(center=(400, 300))
base_menu = pg.image.load('Sprite/base_menu.png')
base_menu = pg.transform.scale(base_menu, (350, 350))
base_menu_rect = base_menu.get_rect(center=(395, 300))
base_menu1 = pg.image.load('Sprite/base_menu.png')
base_menu1 = pg.transform.scale(base_menu1, (350, 350))
base_menu_rect1 = base_menu.get_rect(center=(395, 300))
stand = pg.image.load('animations/0.png')
stand = pg.transform.scale(stand, (60, 100))
stand_rect = stand.get_rect(center=(100, 100))
start_pic = pg.image.load("Sprite/map1.jpg")
start_pic = pg.transform.scale(start_pic, (800, 600))
start_pic_rect = base_menu.get_rect()
sound1 = pg.mixer.Sound('Sprite/gamesound.wav')
sound1.set_volume(0.3)
sound2 = pg.mixer.Sound('Sprite/cowboy.wav')
sound2.set_volume(0.3)
sound3 = pg.mixer.Sound('Sprite/happy.wav')
sound3.set_volume(0.3)
sound4 = pg.mixer.Sound('Sprite/sample.wav')
sound4.set_volume(0.3)
point = pg.mixer.Sound('Sprite/point.wav')
soundSirena = pg.mixer.Sound('Sprite/sirena.mp3')
soundSirena.set_volume(0.3)
lose = pg.mixer.Sound("Sprite/lose.wav")
apple_group = Group()
spikes_group = Group()
slider_value = slider.getValue()
names = {}
def emit_particle(x, y, x_vel, y_vel, radius):
    particles.append([[x, y], [x_vel, y_vel], radius])

def update_draw_particle():
    for i, particle in reversed(list(enumerate(particles))):
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.8
        if particle[2] <= 0:
            particles.pop(i)
        if len(particles) == 0:
            break
        reverse_particle = particles[len(particles) - i - 1]
        image_copy = pg.transform.scale(particle_image, (reverse_particle[2], reverse_particle[2]))
        screen.blit(image_copy, (reverse_particle[0][0], reverse_particle[0][1]))


def update_dinamic_light_mask():
    global dinamic_light_speed_x, dinamic_light_speed_y, dinamic_light_direction
    if dinamic_light_mask_rect.right > 820:
        dinamic_light_speed_x *= -1
    if dinamic_light_mask_rect.left < -20:
        dinamic_light_speed_x *= -1
    if dinamic_light_mask_rect.top < -20:
        dinamic_light_speed_y *= -1
    if dinamic_light_mask_rect.bottom > 620:
        dinamic_light_speed_y *= -1
    dinamic_light_direction = [dinamic_light_speed_x, dinamic_light_speed_y]
    dinamic_light_mask_rect.move_ip(dinamic_light_direction)
    collision = pg.Rect.colliderect(stand_rect, dinamic_light_mask_rect)
    if collision:
        dinamic_light_mask_rect.center = stand_rect.center
    return collision


def emit_particle1(x, y, x_vel, y_vel, radius, color):
    particles1.append([[x, y], [x_vel, y_vel], radius, color])


def update_draw_particle1():
    for i, particle in reversed(list(enumerate(particles1))):
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 1
        pg.draw.circle(screen, particle[3], (particle[0][0], particle[0][1]), particle[2])
        if particle[2] == 0:
            particles1.pop(i)


def render_fog(chek):
    fog.fill(NIGHT_COLOR)
    fog.blit(dinamic_light_mask, dinamic_light_mask_rect)
    if chek and time.time() % 1 > 0.5:
        fog.blit(static_light_mask, (5, 5))
        fog.blit(static_light_mask, (720, 25))
        fog.blit(static_light_mask, (5, 520))
        fog.blit(static_light_mask, (700, 500))
    screen.blit(fog, (0, 0), special_flags=pg.BLEND_MULT)


def start_window_registration():
    global SCORE
    text = ""
    color = (200, 200, 200)
    color_active = (50, 50, 200)
    color_inactive = (200, 200, 200)
    active = False
    input_box = pg.Rect(325, 273, 150, 55)
    text_menu = FONT_head.render("Menu", True, (0, 0, 0))
    text_menu_rect = text_menu.get_rect(center=(395, 180))
    text_name = FONT_button.render("Input your name", True, (0, 0, 0))
    text_name_rect = text_name.get_rect(center=(400, 240))
    OK = FONT_OK.render('Ok', True, (0, 0, 0), (255, 255, 255))
    OK_rect = OK.get_rect(center=(395, 360))
    screen.blit(start_pic, start_pic_rect)
    screen.blit(base_menu, base_menu_rect)
    screen.blit(text_menu, text_menu_rect)
    screen.blit(text_name, text_name_rect)
    screen.blit(OK, OK_rect)
    pg.display.update()
    play = True
    while play:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 365 < event.pos[0] < 425 and 339 < event.pos[1] < 380 and text != '':
                        play = False
                        start_window_menu()
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN and active:
                if event.key == pg.K_RETURN:
                    names[text] = SCORE
                    text = ''
                    play = False
                    start_window_menu()
                elif event.key == pg.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        text_img = FONT_button.render(text, True, color)
        width = max(input_box.width, text_img.get_width() + 10)
        input_box.width = width
        screen.blit(text_img, (input_box.x + 5, input_box.y + 10))
        pg.draw.rect(screen, color, input_box, 2)
        pg.display.update()


def start_window_menu():
    text_menu = FONT_head.render("Menu", True, (0, 0, 0))
    text_menu_rect = text_menu.get_rect(center=(395, 180))
    text_start = FONT_button1.render("Start", True, (0, 0, 0), (255, 255, 255))
    text_start_rect = text_start.get_rect(center=(400, 240))
    text_setting = FONT_setting.render('Setting', True, (0, 0, 0), (255, 255, 255))
    text_setting_rect = text_setting.get_rect(center=(400, 295))
    text_scoreboard = FONT_exit.render('Scoreboard', True, (0, 0, 0), (255, 255, 255))
    text_scoreboard_rect = text_scoreboard.get_rect(center=(400, 350))
    text_exit = FONT_exit.render('Exit', True, (0, 0, 0), (255, 255, 255))
    text_exit_rect = text_exit.get_rect(center=(400, 405))
    screen.blit(map, (0, 0))
    screen.blit(base_menu, base_menu_rect)
    screen.blit(text_menu, text_menu_rect)
    screen.blit(text_start, text_start_rect)
    screen.blit(text_setting, text_setting_rect)
    screen.blit(text_scoreboard, text_scoreboard_rect)
    screen.blit(text_exit, text_exit_rect)
    play = True
    while play:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 335 < event.pos[0] < 465 and 265 < event.pos[1] < 325:
                        play = False
                        draw_setting1()
                    if 365 < event.pos[0] < 435 and 380 < event.pos[1] < 430:
                        sys.exit()
                if text_start_rect.collidepoint(event.pos):
                    play = False
        pg.display.update()


def draw_setting1():
    global slider_value
    screen.blit(base_menu, base_menu_rect)
    text_head = FONT_head.render('Settings', True, (0, 0, 0))
    text_rect_head = text_head.get_rect(center=(395, 180))
    screen.blit(text_head, text_rect_head)
    text_vol = FONT_vol.render('Volume: ', True, (0, 0, 0))
    text_rect_vol = text_vol.get_rect(center=(320, 220))
    screen.blit(text_vol, text_rect_vol)
    back_text = FONT_back.render('Back', True, (0, 0, 0), (255, 255, 255))
    back_text_rect = back_text.get_rect(center=(395, 400))
    screen.blit(back_text, back_text_rect)
    play = True
    while play:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    play = False
                    start_window_menu()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 351 < event.pos[0] < 438 and 380 < event.pos[1] < 420:
                        play = False
                        start_window_menu()
        output.setText(slider.getValue())
        pygame_widgets.update(events)
        slider_value = slider.getValue()
        sound1.set_volume(slider_value / 100)
        sound2.set_volume(slider_value / 100)
        sound3.set_volume(slider_value / 100)
        sound4.set_volume(slider_value / 100)
        pg.display.update(base_menu_rect)

def draw_setting():
    global slider_value
    screen.blit(base_menu, base_menu_rect)
    text_head = FONT_head.render('Settings', True, (0, 0, 0))
    text_rect_head = text_head.get_rect(center=(395, 180))
    screen.blit(text_head, text_rect_head)
    text_vol = FONT_vol.render('Volume: ', True, (0, 0, 0))
    text_rect_vol = text_vol.get_rect(center=(320, 220))
    screen.blit(text_vol, text_rect_vol)
    back_text = FONT_back.render('Back', True, (0, 0, 0), (255, 255, 255))
    back_text_rect = back_text.get_rect(center=(395, 400))
    screen.blit(back_text, back_text_rect)
    play = True
    while play:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    play = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 351 < event.pos[0] < 438 and 380 < event.pos[1] < 420:
                        play = False
        output.setText(slider.getValue())
        pygame_widgets.update(events)
        slider_value = slider.getValue()
        sound1.set_volume(slider_value / 100)
        sound2.set_volume(slider_value / 100)
        sound3.set_volume(slider_value / 100)
        sound4.set_volume(slider_value / 100)
        pg.display.update(base_menu_rect)

def draw_menu():
    play = True
    while play:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 340 < event.pos[0] < 465 and 250 < event.pos[1] < 280:
                        play = False
                    if 340 < event.pos[0] < 465 and 306 < event.pos[1] < 336:
                        draw_setting()
                    if 340 < event.pos[0] < 470 and 365 < event.pos[1] < 402:
                        sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    play = False
        screen.blit(map, (0, 0))
        screen.blit(menu_esc, menu_esc_rect)
        pg.display.update(menu_esc_rect)

def update(keys, person):
    if keys[pg.K_d]:
        person.centerx += 5
    if keys[pg.K_w]:
        person.centery -= 5
    if keys[pg.K_s]:
        person.centery += 5
    if keys[pg.K_a]:
        person.centerx -= 5
    if person.top < 0:
        person.bottom = 600
    if person.bottom > 600:
        person.top = 0
    if person.right > 800:
        person.left = 0
    if person.left < 0:
        person.right = 800


class Apple(pg.sprite.Sprite):
    def __init__(self, screen, x, y):
        super(Apple, self).__init__()
        self.screen = screen
        self.image = pg.image.load('Sprite/apple.png')
        self.image = pg.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(center=(x, y))
    def draw(self):
        self.screen.blit(self.image, self.rect)

for i in range(randint(15, 30)):
    apple = Apple(screen, randint(20, 780), randint(20, 580))
    apple_group.add(apple)

class Spikes(pg.sprite.Sprite):
    def __init__(self, screen, x, y):
        super(Spikes, self).__init__()
        self.screen = screen
        self.image = pg.image.load("Sprite/shipi.png")
        self.image = pg.transform.scale(self.image, (45, 65))
        self.rect = self.image.get_rect(center=(x, y))
    def draw(self):
        self.screen.blit(self.image, self.rect)

for i in range(6):
    spike = Spikes(screen, randint(75, 725), randint(45, 555))
    spikes_group.add(spike)


def draw(screen, keys):
    global index
    if keys[pg.K_d]:
        screen.blit(animation_right[index // 10], stand_rect)
    elif keys[pg.K_a]:
        screen.blit(animation_left[index // 10], stand_rect)
    elif keys[pg.K_w]:
        screen.blit(animation_right[index // 10], stand_rect)
    elif keys[pg.K_s]:
        screen.blit(animation_left[index // 10], stand_rect)
    else:
        screen.blit(stand, stand_rect)
    index += 2
    if index == 60:
        index = 0

    apple_group.draw(screen)
    spikes_group.draw(screen)

def draw1(stand_rect, keys):
    global index
    if keys[pg.K_d]:
        screen.blit(animation_right[index // 10], stand_rect)
    elif keys[pg.K_a]:
        screen.blit(animation_left[index // 10], stand_rect)
    elif keys[pg.K_w]:
        screen.blit(animation_right[index // 10], stand_rect)
    elif keys[pg.K_s]:
        screen.blit(animation_left[index // 10], stand_rect)
    else:
        screen.blit(stand, stand_rect)
    index += 2
    if index == 60:
        index = 0

red = False
night = False
play_music = True
index = 0
play = True
screen.blit(map, (0, 0))
pg.display.update()
start_window_registration()
color = (255, 0, 0)
while play:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                if red:
                    red = False
                else:
                    red = True
            if event.key == pg.K_n:
                if night:
                    night = False
                else:
                    night = True
            if event.key == pg.K_ESCAPE:
                draw_menu()
            if event.key == pg.K_p:
                if play_music == True:
                    sound1.stop()
                    sound2.stop()
                    sound3.stop()
                    sound4.stop()
                    play_music = False
                else:
                    sound1.play()
                    sound2.stop()
                    sound3.stop()
                    sound4.stop()
                    play_music = True
            if event.key == pg.K_0:
                sound1.stop()
                sound2.stop()
                sound3.stop()
                sound4.stop()
            if event.key == pg.K_1:
                sound1.stop()
                sound1.play()
            if event.key == pg.K_KP1:
                sound1.play()
                sound2.stop()
                sound3.stop()
                sound4.stop()
            if event.key == pg.K_KP2:
                sound1.stop()
                sound2.play()
                sound3.stop()
                sound4.stop()
            if event.key == pg.K_KP3:
                sound1.stop()
                sound2.stop()
                sound3.play()
                sound4.stop()
            if event.key == pg.K_KP4:
                sound1.stop()
                sound2.stop()
                sound3.stop()
                sound4.play()
    screen.blit(map, (0, 0))
    keys = pg.key.get_pressed()
    draw(screen, keys)
    update(keys, stand_rect)
    for sprite in apple_group:
        collision = pg.Rect.colliderect(stand_rect, sprite.rect)
        if collision:
            emit_particle(sprite.rect.centerx, sprite.rect.centery, randint(-2, 2), randint(-2, 2), 40)
            sprite.kill()
            SCORE += 1
            point.play()
    for sprite in spikes_group:
        collision = pg.Rect.colliderect(stand_rect, sprite.rect)
        if collision:
            emit_particle(stand_rect.centerx, sprite.rect.centery, -2, 0, 40)
            emit_particle(stand_rect.centerx, sprite.rect.centery, -1, -1, 40)
            emit_particle(stand_rect.centerx, sprite.rect.centery, 0, -1, 40)
            emit_particle(stand_rect.centerx, sprite.rect.centery, 1, -1, 40)
            emit_particle(stand_rect.centerx, sprite.rect.centery, 2, 0, 40)
            sprite.kill()
            SCORE -= 5
            lose.play()
    update_draw_particle()
    score_text = FONT_score.render(f'Score: {SCORE}', True, (0, 0, 0))
    score_text_rect = score_text.get_rect(center=(750, 20))
    screen.blit(score_text, score_text_rect)
    score_text1 = FONT_score.render(f'Score: {SCORE}', True, (255, 255, 255))
    score_text_rect1 = score_text1.get_rect(center=(750, 20))
    arested_text = FONT_ARESTED.render('YOU ARE UNDER ARREST', True, (255, 255, 255))
    arested_text_rect = arested_text.get_rect(center=(400, 250))
    if night:
        check = update_dinamic_light_mask()
        render_fog(check)
        screen.blit(score_text1, score_text_rect1)
        if check and time.time() % 1 > 0.5:
            screen.blit(score_text1, score_text_rect1)
            screen.blit(arested_text, arested_text_rect)
        if check:
            soundSirena.play(-1)
            SCORE = 0
            emit_particle1(stand_rect.centerx, stand_rect.centery, randint(-2, 2), randint(-2, 2), 40, color)
            update_draw_particle1()
            draw1(stand_rect, keys)
        else:
            soundSirena.stop()
    pg.display.update()
    clock.tick(60)