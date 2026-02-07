import pygame
import os
import random
 
# Change Directory # Random Error 01
os.chdir(os.path.dirname(os.path.abspath(__file__)))

run = True
FPS = 60

# Board Config
RADIUS = 40
GAP = 10
BOARD_Y = 200
BOARD_X = 0
ROWS = 6
COLUMN = 7 
BOARD_WIDTH = 7*(GAP + 2*RADIUS) + GAP
BOARD_HEIGHT = 6*(GAP + 2*RADIUS) + GAP
YELLOW = '#fcec35'
RED = '#d91e17'

player_color = random.choice((RED, YELLOW))
click_delay_count = 0
check_win = False
is_won = None
checkers_pos = []
vertical_count = [0,0]

for _ in range(COLUMN): checkers_pos.append([])

SCREEN_WIDTH = BOARD_WIDTH
SCREEN_HEIGHT = BOARD_HEIGHT + BOARD_Y
CHECKERS_CENTER_X = []

pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Connect Four")

ICON = pygame.image.load('icon.png')
pygame.display.set_icon(ICON)

# Checker
class Checker():
    def __init__(self, column, row, hex_color):
        self.column = column
        self.row = row
        self.hex_color = hex_color
        self.checker_instance = None

    def update(self):
        pygame.draw.circle(screen, self.hex_color, (GAP*self.column + RADIUS*((2*self.column)-1) + BOARD_X, GAP*(self.row+1)//2 + RADIUS*self.row + BOARD_Y), RADIUS)

    def __repr__(self):
        if self.hex_color == RED: 
            self.color = 'R'
            return 'R'
        else: 
            self.color = 'Y'
            return 'Y'

def draw_board():
    global BOARD_HEIGHT, BOARD_WIDTH
    pygame.draw.rect(screen, (21, 86, 166), (BOARD_X,BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT))

    for col_n in range(1,COLUMN+1): # 7 -> x addition checkers
        for row_n in range(1,ROWS+1):
            pygame.draw.circle(screen, 'black', (GAP*col_n + RADIUS*(col_n+(col_n-1)) + BOARD_X, GAP*row_n + RADIUS*(row_n+(row_n-1)) + BOARD_Y), RADIUS)        

        if len(CHECKERS_CENTER_X) < 7:
            CHECKERS_CENTER_X.append(int(GAP*col_n + RADIUS*(col_n+(col_n-1)) + BOARD_X))

# (x, y) = (column, row)
def add_checkers():
    global click_delay_count, player_color, check_win
    mouse_pos = pygame.mouse.get_pos()

    # Checker follows cursor
    if not is_won:
        if mouse_pos[1] < BOARD_Y - RADIUS:
            if player_color == YELLOW: pygame.draw.circle(screen, RED, (mouse_pos[0], mouse_pos[1]), RADIUS)   
            else: pygame.draw.circle(screen, YELLOW, (mouse_pos[0], mouse_pos[1]), RADIUS)   

        if pygame.mouse.get_pressed()[0]:
            if click_delay_count < 500 and click_delay_count != 0:
                click_delay_count += 1

            else:
                for checker_x in enumerate(CHECKERS_CENTER_X): # (index, value)
                    if mouse_pos[0] > checker_x[-1] - RADIUS and mouse_pos[0] < checker_x[-1] + RADIUS:
                        # Check for max verical column for x
                        coln_length = len(checkers_pos[checker_x[0]])
                        checker_row = 2*(ROWS-coln_length) - 1

                        if coln_length < ROWS:
                            if player_color == YELLOW: player_color = RED
                            else: player_color = YELLOW
                            checkers_pos[checker_x[0]].append(Checker(checker_x[0]+1, checker_row, player_color))

                        check_win = True
                # Reset Click Delay
                click_delay_count = 1
        else:
            click_delay_count = 0             

def check_connect_four(vertical_count, eng_color):
    global is_won
    horizontal_pos = []
    total_checkers = 0
    for col_data in checkers_pos:
        for row_data in col_data:
            # Vertical Scan
            if row_data.hex_color == player_color:
                vertical_count += 1
                if vertical_count >= 4:
                    is_won = eng_color  
                    break
                # Horizontal Scan
                horizontal_pos.append((row_data.row, row_data.column))
            else:
                vertical_count = 0
            total_checkers += 1
        # Reset Vertical
        vertical_count = 0        

    if total_checkers >= (ROWS*COLUMN):
        is_won = 'DRAW'

    # Horizontal Scan
    horizontal_pos.sort()
    temp = horizontal_pos[0]
    horizontal_count = 0
    for pos in horizontal_pos[1:]:
        if temp[0] == pos[0] and (pos[1]-temp[1] == 1):
            horizontal_count += 1
            if horizontal_count >= 3:
                is_won = eng_color  
                break
        else:
            horizontal_count = 0
        temp = pos    

    # Diagonal Lost my SANITY
    horizontal_pos = sorted(horizontal_pos, key=lambda x: x[1])
    for data in horizontal_pos:
        if (data[0]+2,data[1]+1) in horizontal_pos:
            if (data[0]+4,data[1]+2) in horizontal_pos:
                if (data[0]+6,data[1]+3) in horizontal_pos:
                    is_won = eng_color
                    break

        if (data[0]-2, data[1]+1) in horizontal_pos:
            if (data[0]-4, data[1]+2) in horizontal_pos:
                if (data[0]-6, data[1]+3) in horizontal_pos:
                    is_won = eng_color      
                    break

def reset():
    global player_color,click_delay_count,check_win, is_won, checkers_pos, vertical_count
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        print(1)
        player_color = random.choice((RED, YELLOW))
        click_delay_count = 0
        check_win = False
        is_won = None
        checkers_pos = []
        vertical_count = [0,0]

        for _ in range(COLUMN): checkers_pos.append([])

def update_checkers():
    global is_player_red, check_win
    
    # Updating Checker for list of <Checker>
    for column in checkers_pos:
        for row in column:
            row.update()

    # Check Connect 4
    if check_win and not is_won:
        if player_color == RED:
            check_connect_four(vertical_count[0], 'RED')
        else:
            check_connect_four(vertical_count[1], 'YELLOW')

    # Check for win
    if is_won:
        text_2 = font_2.render('Press Enter to Restart',True, 'white')
        if is_won == 'RED':
            text_1 = font_1.render(f"{is_won} Won",True, RED)
            screen.blit(text_1,(SCREEN_WIDTH//2.9,30))
            screen.blit(text_2,(SCREEN_WIDTH//4.4,100))
            reset()
        elif is_won == 'YELLOW':
            text_1 = font_1.render(f"{is_won} Won",True, YELLOW)
            screen.blit(text_1,(SCREEN_WIDTH//3.4,30))
            screen.blit(text_2,(SCREEN_WIDTH//4.5,100))
            reset()

        else:
            text_1 = font_1.render("DRAW",True, 'white')
            screen.blit(text_1,(SCREEN_WIDTH//2.5,30))
            screen.blit(text_2,(SCREEN_WIDTH//4.5,100))
            reset()

font_1 = pygame.font.SysFont('LCD', 60)
font_2 = pygame.font.SysFont('Courier New', 30)
while run:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False        

    check_win = False
    screen.fill((0,0,0))
    draw_board()
    add_checkers()
    update_checkers()

    pygame.display.update()
    clock.tick(FPS)
