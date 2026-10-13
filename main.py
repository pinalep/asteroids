import pygame, sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, LINE_WIDTH, PLAYER_RADIUS
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from circleshape import CircleShape
from shot import Shot

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    clock = pygame.time.Clock()
    dt = 0.0
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    player = Player(x, y)
    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()
    shots = pygame.sprite.Group()
    Shot.containers = (shots, updatable, drawable)
    font = pygame.font.Font(None, 36)
    score = 0
    highest_score = 0
    game_over = False
    timer = 0

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_over:
                if game_over == True:
                    for asteroid in asteroids:
                        asteroid.kill()

                    for shot in shots:
                        shot.kill()

                    asteroid_field.spawn_timer = 0
                    player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    player.velocity = pygame.Vector2(0, 0)

                    score = 0
                    timer = 0
                    game_over = False

            
        screen.fill("black")

        if game_over == False:
            for item in drawable:
                item.draw(screen)
            updatable.update(dt)
            for item in asteroids:
                if player.collides_with(item) == True:
                    log_event("player_hit")
                    game_over = True
            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.collides_with(shot):
                        log_event("asteroid_shot")
                        asteroid.split()
                        shot.kill()
                        if asteroid.radius == 20:
                            score += 10
                        elif asteroid.radius == 40:
                            score += 25
                        elif asteroid.radius == 60:
                            score += 50
                        if score > highest_score:
                            highest_score = score
            score_text = font.render(f"Score: {score}", True, "white")
            screen.blit(score_text, (10, 10))
            highest_score_text = font.render(f"Highest score: {highest_score}", True, "white")
            screen.blit(highest_score_text, (10, 50))
            timer = timer + dt
            timer_text = font.render(f"Time: {int(timer)}", True, "white")
            screen.blit(timer_text, (SCREEN_WIDTH - timer_text.get_width() - 10, 10))


        if game_over == True:
            game_over_text = font.render("Game Over", True, "white")
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 180))
            score_text = font.render(f"Score: {score}", True, "white")
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 240))
            highest_score_text = font.render(f"Highest score: {highest_score}", True, "white")
            screen.blit(highest_score_text, (SCREEN_WIDTH // 2 - highest_score_text.get_width() // 2, 290))
            play_again_text = font.render("Press SPACE to play again", True, "white")
            screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, 350))
            
        

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
