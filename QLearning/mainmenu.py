import pygame, sys
import threading
from pygame.locals import *
from run import *

WHITE = (255, 255, 255)
GRAY = (155, 155, 155)
BLACK = (0, 0, 0)
MAINBACKCOLOR = (128, 64, 64)

WINW = 1024
WINW_CENTER = WINW/2
WINH = 768
WINH_CENTER = WINH/2 + 50

mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Q-Learning')
screen = pygame.display.set_mode((WINW, WINH))
font = pygame.font.SysFont('Segoe UI', 24)

color_active = WHITE
color_passive = GRAY

click = False

def set_box_color(value, color_input):
    if value == True:
        color_input = color_active
        return color_input
    else:
        color_input = color_passive
        return color_input

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():

    start_x = ''
    sx_rect = pygame.Rect(WINW_CENTER + 100, WINH_CENTER - 200, 40, 30)
    active_sx = False
    color_input_sx = color_passive

    start_y = ''
    sy_rect = pygame.Rect(WINW_CENTER + 100, WINH_CENTER - 150, 40, 30)
    active_sy = False
    color_input_sy = color_passive

    end_x = ''
    ex_rect = pygame.Rect(WINW_CENTER + 100, WINH_CENTER - 50, 40, 30)
    active_ex = False
    color_input_ex = color_passive

    end_y = ''
    ey_rect = pygame.Rect(WINW_CENTER + 100, WINH_CENTER, 40, 30)
    active_ey = False
    color_input_ey = color_passive
    
    button_go_text = 'SOLVE'
    button_go = pygame.Rect(WINW_CENTER - 50, WINH_CENTER + 100, 100, 40)
    color_button_go = WHITE

    while True:
        screen.fill(MAINBACKCOLOR)
        draw_text('# Setting up Start & End Points (50 x 50) #', font, WHITE, screen, WINW_CENTER - 220, WINH_CENTER - 300)

        draw_text('Start Point X Position : ', font, WHITE, screen, WINW_CENTER - 150, WINH_CENTER - 200)
        color_input_sx = set_box_color(active_sx, color_input_sx)
        pygame.draw.rect(screen, color_input_sx, sx_rect, 2)
        draw_text(start_x, font, WHITE, screen, sx_rect.x + 8, sx_rect.y - 2)

        draw_text('Start Point Y Position : ', font, WHITE, screen, WINW_CENTER - 150, WINH_CENTER - 150)
        color_input_sy = set_box_color(active_sy, color_input_sy)
        pygame.draw.rect(screen, color_input_sy, sy_rect, 2)
        draw_text(start_y, font, WHITE, screen, sy_rect.x + 8, sy_rect.y - 2)

        draw_text('End Point X Position  : ', font, WHITE, screen, WINW_CENTER - 150, WINH_CENTER - 50)
        color_input_ex = set_box_color(active_ex, color_input_ex)
        pygame.draw.rect(screen, color_input_ex, ex_rect, 2)
        draw_text(end_x, font, WHITE, screen, ex_rect.x + 8, ex_rect.y - 2)

        draw_text('End Point Y Position  : ', font, WHITE, screen, WINW_CENTER - 150, WINH_CENTER)
        color_input_ey = set_box_color(active_ey, color_input_ey)
        pygame.draw.rect(screen, color_input_ey, ey_rect, 2)
        draw_text(end_y, font, WHITE, screen, ey_rect.x + 8, ey_rect.y - 2)

        pygame.draw.rect(screen, GRAY, button_go)
        draw_text(button_go_text, font, MAINBACKCOLOR, screen, button_go.x + 16, button_go.y + 2)
        
        mx, my = pygame.mouse.get_pos()
        if button_go.collidepoint(mx, my):
            if click:
                game(start_x, start_y, end_x, end_y)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if sx_rect.collidepoint(event.pos):
                    active_sx = True
                else:
                    active_sx = False
                if sy_rect.collidepoint(event.pos):
                    active_sy = True
                else:
                    active_sy = False
                if ex_rect.collidepoint(event.pos):
                    active_ex = True
                else:
                    active_ex = False
                if ey_rect.collidepoint(event.pos):
                    active_ey = True
                else:
                    active_ey = False
                
                if event.button == 1:
                    click = True

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if active_sx == True:
                    if event.key == K_BACKSPACE:
                        start_x = ''
                    else:
                        key = str(event.unicode)
                        if key.isdecimal() and len(start_x)<2:
                            start_x += event.unicode
                if active_sy == True:
                    if event.key == K_BACKSPACE:
                        start_y = ''
                    else:
                        key = str(event.unicode)
                        if key.isdecimal() and len(start_y)<2:
                            start_y += event.unicode
                if active_ex == True:
                    if event.key == K_BACKSPACE:
                        end_x = ''
                    else:
                        key = str(event.unicode)
                        if key.isdecimal() and len(end_x)<2:
                            end_x += event.unicode
                if active_ey == True:
                    if event.key == K_BACKSPACE:
                        end_y = ''
                    else:
                        key = str(event.unicode)
                        if key.isdecimal() and len(end_y)<2:
                            end_y += event.unicode

        pygame.display.update()
        mainClock.tick(60)


def game(start_x, start_y, end_x, end_y):
    running = True

    if start_x == '':
        start_x = 0
    if start_y == '':
        start_y = 0
    if end_x == '':
        end_x = 49
    if end_y == '':
        end_y = 49

    app = Run(int(start_x),int(start_y),int(end_x),int(end_y))

    t1 = threading.Thread(target=app.train)
    t1.daemon = True
    t1.start()
    
    while running:
        screen.fill(MAINBACKCOLOR)
        statex = app.getState()
        k=0
        for i in range(50):
            for j in range(50):
                pygame.draw.rect(screen, (app.game_board[k].color_r, app.game_board[k].color_g, app.game_board[k].color_b), (j * 15 + 135, i * 15 + 10, 14, 14))
                pygame.draw.circle(screen, MAINBACKCOLOR, (statex[1] * 15 + 142, statex[0] * 15 + 17), 7, 0)
                k+=1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        mainClock.tick(60)

main_menu()