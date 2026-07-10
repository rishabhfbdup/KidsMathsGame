import pygame
import random
import sys

try:
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    ANDROID = True
except ImportError:
    ANDROID = False

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kids Maths Game")

WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (255, 50, 50)
GREEN = (50, 205, 50)
YELLOW = (255, 215, 0)
BLACK = (0, 0, 0)
DARK_BLUE = (20, 70, 160)
ORANGE = (255, 165, 0)

game_state = "MENU" 

basket_width = 150
basket_height = 35
basket_x = (SCREEN_WIDTH - basket_width) // 2
basket_y = SCREEN_HEIGHT - basket_height - 40
basket_speed = 15

score = 0
level = 1
lives = 3
base_speed = 4
item_speed = base_speed

correct_x = 200
wrong_x = 600
item_y = 0

BANNER_AD_ID = "ca-app-pub-1777482814323307/9602018225" 
INTERSTITIAL_AD_ID = "ca-app-pub-1777482814323307/2015971000"

def show_banner_ad():
    if ANDROID:
        print("Android Native Banner Active")

def show_interstitial_ad():
    if ANDROID:
        print("Android Native Interstitial Active")

def generate_question(current_level):
    if current_level == 1:
        num1 = random.randint(1, 6)
        num2 = random.randint(1, 6)
        correct_ans = num1 + num2
        q_text = f"{num1} + {num2} = ?"
    elif current_level == 2:
        mode = random.choice(["add", "sub"])
        if mode == "add":
            num1 = random.randint(5, 10)
            num2 = random.randint(3, 9)
            correct_ans = num1 + num2
            q_text = f"{num1} + {num2} = ?"
        else:
            num1 = random.randint(6, 12)
            num2 = random.randint(1, 5)
            correct_ans = num1 - num2
            q_text = f"{num1} - {num2} = ?"
    else:
        mode = random.choice(["add", "sub"])
        max_num = 10 + (current_level * 2)
        if mode == "add":
            num1 = random.randint(10, max_num)
            num2 = random.randint(5, 15)
            correct_ans = num1 + num2
            q_text = f"{num1} + {num2} = ?"
        else:
            num1 = random.randint(15, max_num)
            num2 = random.randint(5, 12)
            correct_ans = num1 - num2
            q_text = f"{num1} - {num2} = ?"

    wrong_ans = correct_ans + random.choice([-3, -2, -1, 1, 2, 3])
    if wrong_ans == correct_ans or wrong_ans < 0:
        wrong_ans = correct_ans + 4
        
    return q_text, correct_ans, wrong_ans

def reset_ball_position():
    global correct_x, wrong_x, item_y
    item_y = 0
    ball_layout = random.choice(["correct_left", "correct_right"])
    if ball_layout == "correct_left":
        correct_x = random.randint(100, 300)
        wrong_x = random.randint(500, 700)
    else:
        wrong_x = random.randint(100, 300)
        correct_x = random.randint(500, 700)

question_text, correct_answer, wrong_answer = generate_question(level)
reset_ball_position()

font_title = pygame.font.SysFont("Arial", 50, bold=True)
font_large = pygame.font.SysFont("Arial", 45, bold=True)
font_medium = pygame.font.SysFont("Arial", 35, bold=True)
font_small = pygame.font.SysFont("Arial", 25, bold=True)

clock = pygame.time.Clock()
show_banner_ad()

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "MENU":
                if 250 <= mouse_pos[0] <= 550 and 220 <= mouse_pos[1] <= 290:
                    score, level, lives = 0, 1, 3
                    item_speed = base_speed
                    game_state = "CLASSIC"
                    question_text, correct_answer, wrong_answer = generate_question(level)
                    reset_ball_position()
                
                if 250 <= mouse_pos[0] <= 550 and 330 <= mouse_pos[1] <= 400:
                    score, level, lives = 0, 1, 3
                    item_speed = base_speed
                    game_state = "GRAPHIC"
                    question_text, correct_answer, wrong_answer = generate_question(level)
                    reset_ball_position()

            elif game_state == "GAME_OVER":
                game_state = "MENU"

    if game_state in ["CLASSIC", "GRAPHIC"]:
        if pygame.mouse.get_pressed()[0]: 
            if mouse_pos[0] < basket_x + (basket_width//2):
                basket_x -= basket_speed
            elif mouse_pos[0] > basket_x + (basket_width//2):
                basket_x += basket_speed
            
            if basket_x < 0: basket_x = 0
            if basket_x > SCREEN_WIDTH - basket_width: basket_x = SCREEN_WIDTH - basket_width

        item_y += item_speed

        if item_y > SCREEN_HEIGHT:
            lives -= 1
            if lives <= 0: 
                game_state = "GAME_OVER"
                show_interstitial_ad()
            else:
                question_text, correct_answer, wrong_answer = generate_question(level)
                reset_ball_position()

        if (item_y + 25 >= basket_y) and (basket_x <= correct_x <= basket_x + basket_width):
            score += 1
            if score <= 5: level = 1; item_speed = base_speed
            elif score <= 12: level = 2; item_speed = base_speed + 1.5
            elif score <= 20: level = 3; item_speed = base_speed + 3
            else:
                level = 3 + (score - 20) // 7
                item_speed = base_speed + 3 + (level - 3) * 0.6
            question_text, correct_answer, wrong_answer = generate_question(level)
            reset_ball_position()

        elif (item_y + 25 >= basket_y) and (basket_x <= wrong_x <= basket_x + basket_width):
            lives -= 1
            if lives <= 0: 
                game_state = "GAME_OVER"
                show_interstitial_ad()
            else:
                question_text, correct_answer, wrong_answer = generate_question(level)
                reset_ball_position()

    screen.fill(BLUE)

    if game_state == "MENU":
        title_txt = font_title.render("Maths Game Menu", True, WHITE)
        screen.blit(title_txt, (SCREEN_WIDTH//2 - title_txt.get_width()//2, 80))
        pygame.draw.rect(screen, YELLOW, (255, 220, 290, 70), border_radius=10)
        btn1_txt = font_medium.render("1. Classic Mode", True, BLACK)
        screen.blit(btn1_txt, (SCREEN_WIDTH//2 - btn1_txt.get_width()//2, 235))
        pygame.draw.rect(screen, ORANGE, (255, 330, 290, 70), border_radius=10)
        btn2_txt = font_medium.render("2. Graphic Mode", True, WHITE)
        screen.blit(btn2_txt, (SCREEN_WIDTH//2 - btn2_txt.get_width()//2, 345))

    elif game_state == "CLASSIC":
        pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, 85))
        q_surface = font_large.render(question_text, True, BLACK)
        screen.blit(q_surface, (SCREEN_WIDTH // 2 - q_surface.get_width() // 2, 15))

        pygame.draw.rect(screen, YELLOW, (basket_x, basket_y, basket_width, basket_height))
        pygame.draw.circle(screen, GREEN, (correct_x, int(item_y)), 25)
        pygame.draw.circle(screen, RED, (wrong_x, int(item_y)), 25)

        correct_txt = font_small.render(str(correct_answer), True, WHITE)
        wrong_txt = font_small.render(str(wrong_answer), True, WHITE)
        screen.blit(correct_txt, (correct_x - correct_txt.get_width() // 2, int(item_y) - 12))
        screen.blit(wrong_txt, (wrong_x - wrong_txt.get_width() // 2, int(item_y) - 12))

        screen.blit(font_small.render(f"Score: {score}", True, BLACK), (20, 15))
        screen.blit(font_small.render(f"Level: {level}", True, BLACK), (20, 45))
        screen.blit(font_small.render(f"Lives: {lives}", True, RED), (SCREEN_WIDTH - 120, 30))

    elif game_state == "GRAPHIC":
        screen.fill((230, 245, 255)) 

        pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, 90))
        pygame.draw.line(screen, DARK_BLUE, (0, 90), (SCREEN_WIDTH, 90), 3)
        q_surface = font_large.render(f"Question: {question_text}", True, DARK_BLUE)
        screen.blit(q_surface, (SCREEN_WIDTH // 2 - q_surface.get_width() // 2, 18))

        BROWN = (139, 69, 19)
        LIGHT_BROWN = (205, 133, 63)
        pygame.draw.rect(screen, BROWN, (basket_x, basket_y, basket_width, basket_height), border_radius=10)
        pygame.draw.rect(screen, LIGHT_BROWN, (basket_x - 5, basket_y, basket_width + 10, 8), border_radius=4)

        pygame.draw.circle(screen, GREEN, (correct_x, int(item_y)), 26)
        pygame.draw.ellipse(screen, (34, 139, 34), (correct_x - 5, int(item_y) - 38, 12, 10))
        correct_txt = font_small.render(str(correct_answer), True, WHITE)
        screen.blit(correct_txt, (correct_x - correct_txt.get_width() // 2, int(item_y) - 13))

        pygame.draw.circle(screen, RED, (wrong_x, int(item_y)), 26)
        pygame.draw.ellipse(screen, (34, 139, 34), (wrong_x - 5, int(item_y) - 38, 12, 10))
        wrong_txt = font_small.render(str(wrong_answer), True, WHITE)
        screen.blit(wrong_txt, (wrong_x - wrong_txt.get_width() // 2, int(item_y) - 13))

        score_text = font_small.render(f"Score: {score}", True, BLACK)
        level_text = font_small.render(f"Level: {level}", True, BLACK)
        lives_text = font_small.render(f"Lives: {lives}", True, RED)
        
        screen.blit(score_text, (20, 15))
        screen.blit(level_text, (20, 50))
        screen.blit(lives_text, (SCREEN_WIDTH - 140, 30))
        
    elif game_state == "GAME_OVER":
        pygame.draw.rect(screen, DARK_BLUE, (150, 150, 500, 300), border_radius=15)
        go_txt = font_large.render("GAME OVER", True, RED)
        fs_txt = font_medium.render(f"Final Score: {score}", True, WHITE)
        ml_txt = font_small.render(f"Reached Level: {level}", True, YELLOW)
        restart_txt = font_small.render("Tap anywhere to return to Menu", True, WHITE)
        
        screen.blit(go_txt, (SCREEN_WIDTH // 2 - go_txt.get_width() // 2, 180))
        screen.blit(fs_txt, (SCREEN_WIDTH // 2 - fs_txt.get_width() // 2, 250))
        screen.blit(ml_txt, (SCREEN_WIDTH // 2 - ml_txt.get_width() // 2, 310))
        screen.blit(restart_txt, (SCREEN_WIDTH // 2 - restart_txt.get_width() // 2, 380))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()