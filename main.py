import pygame
import sys
import random


# Ініціалізація Pygame
pygame.init()

# Завантаження музики та звуків
music_bg = "yumoristicheskiy-multyashnyiy-ritm-mg-short-music-38034 (1).ogg"
crash_sound = pygame.mixer.Sound("avtomobil-popal-v-avariyu.ogg")
fail = pygame.mixer.Sound("fail.ogg")
win = pygame.mixer.Sound("win.ogg")
pygame.mixer.music.load(music_bg)
pygame.mixer.music.play()


# Налаштування екрану
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Гонки")

# Завантаження зображень
def load_and_scale(image_path, size):
    image = pygame.image.load(image_path)
    return pygame.transform.scale(image, size)

player_car_image = load_and_scale("my_car.png", (90, 100))
enemy_pictures = [
    load_and_scale("enemy_car.png", (110, 100)),
    load_and_scale("enemy_car2.png", (110, 100)),
    load_and_scale("enemy_car3.png", (110, 100))
]

# Шрифт для відображення тексту
font = pygame.font.Font(None, 36)

# Клас гри
class Game:
    def __init__(self):
        self.car = Car(WIDTH // 2, HEIGHT - 120, player_car_image)
        self.enemies = [EnemyCar(random.randint(50, WIDTH - 150), random.randint(-500, -100), random.choice(enemy_pictures)) for _ in range(7)]
        self.running = True
        self.lifes = 10
        self.point = 0

    def run(self):
        while self.running:
            screen.fill((50, 50, 50))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            keys = pygame.key.get_pressed()
            self.car.move(keys)
            self.car.draw(screen)
            
            for enemy_car in self.enemies:
                enemy_car.move()
                enemy_car.draw(screen)
                if self.car.collides_with(enemy_car):
                    crash_sound.play()
                    self.lifes -= 1
                    enemy_car.reset_position()
                if self.lifes <= 0:
                    pygame.mixer.music.stop()
                    fail.play()
                    self.show_game_over()
                    self.running = False
                if self.lifes > 0 and self.point >= 150:
                    pygame.mixer.music.stop()
                    win.play()
                    self.show_game_won()
                    self.running = False
            
            # Відображення життів та рахунку
            lifes_text = font.render(f"Життя: {self.lifes}", True, (255, 255, 255))
            screen.blit(lifes_text, (10, 10))
            point_text = font.render(f"Рахунок: {self.point}", True, (255, 255, 255))
            screen.blit(point_text, (WIDTH - 150, 10))
            
            pygame.display.update()
            pygame.time.delay(30)
        
        pygame.quit()
        sys.exit()
    
    def show_game_over(self):
        screen.fill((0, 0, 0))
        game_over_text = font.render("ГРА ЗАКІНЧЕНА", True, (255, 255, 255))
        score_text = font.render(f"Ваш рахунок: {self.point}", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.update()
        pygame.time.delay(3000)


    def show_game_won(self):
        screen.fill((0, 255, 0))
        game_over_text = font.render("Ви пройшли цю надскладну гру", True, (0, 0, 0))
        score_text = font.render(f"Ваш рахунок: {self.point}", True, (0, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.update()
        pygame.time.delay(3000)

# Клас машини
class Car:
    def __init__(self, x, y, image):
        self.image = image
        self.x = x
        self.y = y
        self.speed = 6
    
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - 100:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - 100:
            self.y += self.speed
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def collides_with(self, enemy):
        car_rect = self.image.get_rect(topleft=(self.x, self.y))
        enemy_rect = enemy.image.get_rect(topleft=(enemy.x, enemy.y))
        return car_rect.colliderect(enemy_rect)

# Клас машини противника
class EnemyCar:
    def __init__(self, x, y, image):
        self.image = image
        self.x = x
        self.y = y
        self.speed = random.randint(5, 10)
    
    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.reset_position()
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def reset_position(self):
        self.y = random.randint(-500, -100)
        self.x = random.randint(50, WIDTH - 150)
        self.speed = random.randint(5, 10)
        game.point += 1  # Додаємо очко при респавні

# Запуск гри
if __name__ == "__main__":
    game = Game()
    game.run()
