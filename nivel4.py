import pygame as pg
import sys
import random
import time

def nivel4(screen, clock):
    WIDTH, HEIGHT = 800, 600

    # --- JUGADOR ---
    player_size = 40
    player_rect = pg.Rect(100, HEIGHT - player_size - 50, player_size, player_size)
    player_speed = 5
    player_y_vel = 0
    gravity = 0.5
    jump_force = -10
    on_ground = False

    # --- PLATAFORMAS ---
    platforms = [
        pg.Rect(0, HEIGHT - 40, WIDTH, 40), # Suelo
        pg.Rect(150, 480, 150, 20),
        pg.Rect(450, 380, 150, 20),

        # Plataformas que se mueven
        pg.Rect(200, 260, 150, 20),
        pg.Rect(500, 150, 150, 20),
    ]

    # Velocidades para las plataformas móviles
    moving_speeds = {
        3: 2,   # plataforma 3 se mueve
        4: -2,  # plataforma 4 se mueve
    }

    # --- ENEMIGOS ROJOS ---
    enemies = []
    enemy_platforms = [platforms[1], platforms[2], platforms[3], platforms[4]]

    for plat in enemy_platforms:
        ex = plat.x + random.randint(0, plat.width - 40)
        ey = plat.y - 40
        enemies.append({
            "rect": pg.Rect(ex, ey, 40, 40),
            "dir": random.choice([-1, 1]),
            "speed": 2,
            "plat": plat
        })

    # --- LOOP PRINCIPAL ---
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # Movimiento jugador
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pg.K_RIGHT]:
            player_rect.x += player_speed
        if keys[pg.K_SPACE] and on_ground:
            player_y_vel = jump_force
            on_ground = False

        # Gravedad
        player_y_vel += gravity
        player_rect.y += player_y_vel

        # --- MOVER PLATAFORMAS MÓVILES ---
        for idx, vel in moving_speeds.items():
            plat = platforms[idx]
            plat.x += vel

            # límites
            if plat.x < 100:
                plat.x = 100
                moving_speeds[idx] *= -1

            if plat.x + plat.width > WIDTH - 100:
                plat.x = WIDTH - 100 - plat.width
                moving_speeds[idx] *= -1

        # --- COLISIONES CON PLATAFORMAS ---
        on_ground = False
        for plat in platforms:
            if player_rect.colliderect(plat):
                if player_y_vel > 0:
                    player_rect.bottom = plat.top
                    player_y_vel = 0
                    on_ground = True

        # --- ENEMIGOS ROJOS ---
        for e in enemies:
            p = e["plat"]
            e["rect"].x += e["dir"] * e["speed"]

            if e["rect"].left < p.left:
                e["rect"].left = p.left
                e["dir"] = 1

            if e["rect"].right > p.right:
                e["rect"].right = p.right
                e["dir"] = -1

            if player_rect.colliderect(e["rect"]):
                return "menu"

        # --- PASAR AL NIVEL 5 ---
        if player_rect.top <= 0 and player_y_vel < 0:
            return "nivel5"

        # --- DIBUJAR ---
        screen.fill((120, 200, 255))

        for plat in platforms:
            pg.draw.rect(screen, (160, 90, 50), plat)

        pg.draw.rect(screen, (255, 255, 255), player_rect)

        for e in enemies:
            pg.draw.rect(screen, (255, 40, 40), e["rect"])

        pg.display.update()
        clock.tick(60)