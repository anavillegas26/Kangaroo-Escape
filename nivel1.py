import pygame as pg
import sys
import random

def nivel1(screen, clock):
    WIDTH, HEIGHT = 800, 600

    player = pg.Rect(100, HEIGHT - 90, 40, 40)
    speed = 5
    vel_y = 0
    gravity = 0.8
    jump = -14

    platforms = [
        pg.Rect(0, HEIGHT - 40, WIDTH, 40),
        pg.Rect(120, 460, 200, 20),
        pg.Rect(360, 370, 200, 20),
        pg.Rect(200, 280, 200, 20),
        pg.Rect(460, 180, 200, 20)  # última plataforma (arriba)
    ]

    # Enemigo en plataforma baja/med
    plat_e = platforms[1]
    enemy = {
        "rect": pg.Rect(plat_e.x + 30, plat_e.y - 30, 30, 30),
        "dir": 1,
        "speed": 2,
        "plat": plat_e
    }

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            player.x -= speed
        if keys[pg.K_RIGHT]:
            player.x += speed
        if keys[pg.K_SPACE] and vel_y == 0:
            vel_y = jump

        vel_y += gravity
        player.y += vel_y

        # Plataformas
        on_ground = False
        for p in platforms:
            if player.colliderect(p) and vel_y > 0:
                player.bottom = p.top
                vel_y = 0
                on_ground = True

        e = enemy
        e["rect"].x += e["dir"] * e["speed"]
        p = e["plat"]
        if e["rect"].left < p.left:
            e["rect"].left = p.left
            e["dir"] = 1
        if e["rect"].right > p.right:
            e["rect"].right = p.right
            e["dir"] = -1

        if player.colliderect(e["rect"]):
            return "menu"
        
        if player.left < 0:
            player.left = 0
        if player.right > WIDTH:
            player.right = WIDTH
    
        last = platforms[-1]
        encima_last = (player.bottom <= last.top + 5 and last.x <= player.centerx <= last.x + last.width)
        if encima_last and vel_y < 0 and player.top <= last.y - 100:
            return "nivel2"
        
        screen.fill((120, 190, 255))
        for p in platforms:
            pg.draw.rect(screen, (150, 80, 40), p)
        pg.draw.rect(screen, (255, 255, 255), player)
        pg.draw.rect(screen, (200, 30, 30), e["rect"])

        pg.display.update()
        clock.tick(60)