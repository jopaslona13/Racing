import pygame
import sys
import random

# Ініціалізація Pygame
pygame.init()

music_bg = "yumoristicheskiy-multyashnyiy-ritm-mg-short-music-38034 (1).ogg"
crash_sound = "avtomobil-popal-v-avariyu.ogg"
pygame.mixer.music.load(music_bg)
pygame.mixer.music.play(-1)

# Налаштування екрану
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Гонки")

# Завантаження зображень
player_car_image = pygame.image.load("my_car.png")  # Гравець
player_car_image = pygame.transform.scale(player_car_image, (90, 100))

enemy_car_image = pygame.image.load("enemy_car.png")  # Противник
enemy_car_image = pygame.transform.scale(enemy_car_image, (110, 100))

enemy_car_image_2 = pygame.image.load("enemy_car2.png")  # Противник
enemy_car_image_2 = pygame.transform.scale(enemy_car_image_2, (110, 100))

enemy_car_image_3 = pygame.image.load("enemy_car3.png")  # Противник
enemy_car_image_3 = pygame.transform.scale(enemy_car_image_3, (110, 100))

enemy_pictures = [enemy_car_image, enemy_car_image_2, enemy_car_image_3]

# Шрифт для відображення тексту
font = pygame.font.Font(None, 36)

# Клас гри
class Game:
    def __init__(self):
        self.car = Car(WIDTH // 2, HEIGHT - 120, player_car_image)
        self.enemies = [
            EnemyCar(random.randint(50, WIDTH - 150),
            random.randint(-500, -100), 
            random.choice(enemy_pictures)) for _ in range(7)
        ]
        self.running = True
        self.lifes = 10  # Кількість життів
        self.point = 0

    def run(self):
        while self.running:
            screen.fill((50, 50, 50))  # Колір фону
            
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
                    self.lifes -= 1
                    enemy_car.reset_position()
                if self.lifes <= 0:
                    self.running = False
                if enemy_car.y > 792:

                    self.point += 1
            
            # Відображення життів
            lifes_text = font.render(f"Життя: {self.lifes}", True, (255, 255, 255))
            screen.blit(lifes_text, (10, 10))
            
            # Відображення рахунку
            point_text = font.render(f"Рахунок: {self.point}", True, (255, 255, 255))
            screen.blit(point_text, (WIDTH - 150, 10))
            
            pygame.display.update()
            pygame.time.delay(30)
        
        pygame.quit()
        sys.exit()
        

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
        car_rect = pygame.Rect(self.x, self.y, 100, 100)
        enemy_rect = pygame.Rect(enemy.x, enemy.y, 100, 100)
        #pygame.mixer.music.load(crash_sound)
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

# Запуск гри
if __name__ == "__main__":
    game = Game()
    game.run()
