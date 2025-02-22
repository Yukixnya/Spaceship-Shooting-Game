import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Shooting Game")

player_image = pygame.image.load("main.png").convert_alpha() 
target_image = pygame.image.load("enemy.png").convert_alpha() 
bullet_image = pygame.image.load("bullet.png").convert_alpha() 

player_image = pygame.transform.scale(player_image, (50, 50))  
target_image = pygame.transform.scale(target_image, (50, 50)) 
bullet_image = pygame.transform.scale(bullet_image, (50, 50))    

class Player:
    def __init__(self):
        self.rect = player_image.get_rect(center=(WIDTH // 2, HEIGHT - 50))

    def move(self, dx):
        self.rect.x += dx
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width

class Bullet:
    def __init__(self, x, y):
        self.rect = bullet_image.get_rect(center=(x, y))  

    def update(self):
        self.rect.y -= 10
        return self.rect.bottom < 0 

class Target:
    def __init__(self):
        self.rect = target_image.get_rect(center=(random.randint(0, WIDTH - 50), 0))

    def update(self):
        self.rect.y += 3                # Speed of enemy
        return self.rect.top > HEIGHT  

def main():
    clock = pygame.time.Clock()
    player = Player()
    bullet = None  # Track the current bullet
    targets = []
    score = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-5)
        if keys[pygame.K_RIGHT]:
            player.move(5)
        if keys[pygame.K_SPACE] and bullet is None:  # Only fire if there's no bullet
            bullet = Bullet(player.rect.centerx, player.rect.top) 

        if not game_over:
            if bullet is not None:
                if bullet.update():  # Update the bullet and check if it's off-screen
                    bullet = None  # Reset bullet if it's off-screen

            if random.randint(1, 30) == 1:          # Rate of enemy
                targets.append(Target())

            for target in targets[:]:
                if target.update():
                    targets.remove(target)
                
                if target.rect.bottom > HEIGHT - 50:
                    # score += 1
                    game_over = True  # Stop the game

            if bullet is not None:  # Check for collisions only if bullet exists
                for target in targets[:]:
                    if bullet.rect.colliderect(target.rect):
                        targets.remove(target)
                        bullet = None  # Reset bullet after collision
                        score += 1
                        break

            screen.fill((0, 0, 0)) 
            screen.blit(player_image, player.rect)
            if bullet is not None:  # Draw the bullet if it exists
                screen.blit(bullet_image, bullet.rect)
            for target in targets:
                screen.blit(target_image, target.rect)

            # Display score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Score: {score}', True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

        else:
            # Game over display
            font = pygame.font.Font(None, 74)
            game_over_text = font.render('Game Over', True, (255, 255, 255))
            final_score_text = font.render(f'Final Score: {score}', True, (255, 255, 255))
            screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
            screen.blit(final_score_text, (WIDTH // 2 - 150, HEIGHT // 2 + 10))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
