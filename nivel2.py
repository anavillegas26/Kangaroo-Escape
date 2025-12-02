import pygame as pg
import sys
import time

def nivel2(screen, clock):
    WIDTH, HEIGHT = 800, 600

    vidas_img = [
        pg.image.load("Kangaroo-Escape/assets/barra-6.png"),
        pg.image.load("Kangaroo-Escape/assets/barra-5.png"),
        pg.image.load("Kangaroo-Escape/assets/barra-4.png"),
        pg.image.load("Kangaroo-Escape/assets/barra-3.png"),
        pg.image.load("Kangaroo-Escape/assets/barra-2.png"),
        pg.image.load("Kangaroo-Escape/assets/barra-1.png")
    ]

    vidas_img = [pg.transform.scale(img, (160, 80)) for img in vidas_img]

    player = pg.Rect(40, HEIGHT - 90, 40, 40)
    speed = 5
    vel_y = 0
    gravity = 0.8
    jump = -14

    vida = 5
    ultimo_golpe = 0
    tiempo_de_parpadeo = 0
    parpadear = False

    platforms = [
        pg.Rect(0, HEIGHT - 40, WIDTH, 40),       # piso
        pg.Rect(100, 450, 150, 20),               # plataforma media 1
        pg.Rect(350, 350, 150, 20),               # plataforma media 2
        pg.Rect(600, 250, 150, 20),               # plataforma derecha
        pg.Rect(320, 150, 150, 20),               # única plataforma superior (subida leve)
    ]

    enemies = []

    p1 = platforms[1]
    enemies.append({
        "rect": pg.Rect(p1.x + 20, p1.y - 40, 40, 40),
        "dir": 1,
        "speed": 2,
        "plat": p1
    })

    p2 = platforms[2]
    enemies.append({
        "rect": pg.Rect(p2.x + 20, p2.y - 40, 40, 40),
        "dir": -1,
        "speed": 2,
        "plat": p2
    })

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

        for p in platforms:
            if player.colliderect(p) and vel_y > 0:
                player.bottom = p.top
                vel_y = 0
        
        for e in enemies:
            p = e["plat"]
            e["rect"].x += e["dir"] * e["speed"]

            if e["rect"].left < p.left:
                e["rect"].left = p.left
                e["dir"] = 1

            if e["rect"].right > p.right:
                e["rect"].right = p.right
                e["dir"] = -1

            tiempo_actual = time.time()
            if player.colliderect(e["rect"]):
                # ¿Pisado?
                if vel_y > 0 and player.bottom <= e["rect"].centery:
                    enemies.remove(e)
                    vel_y = -10  # rebote
                else:

                    if tiempo_actual - ultimo_golpe > 1:
                        vida -= 1
                        ultimo_golpe = tiempo_actual

                        parpadear = True
                        tiempo_de_parpadeo = tiempo_actual

                        if vida <= 0:
                            desaparecer = time.time()
                            while time.time() - desaparecer < 1.5:
                                screen.fill((0, 0, 0))
                                pg.display.update()
                                clock.tick(60)

                            font = pg.font.SysFont("Century  Gothic", 90, bold=True)
                            text = font.render("Fin del Juego", True, (255, 0, 0))
                            start = time.time()

                            while time.time() - start < 4:
                                screen.fill((0, 0, 0))
                                screen.blit(text, (WIDTH // 2 - 270, HEIGHT // 2 - 50))
                                pg.display.update()
                                clock.tick(60)
                            return "menu"
            
        if player.left < 0:
            player.left = 0
        if player.right > WIDTH:
            player.right = WIDTH

        upper = platforms[4]  
        sobre_ella = (
            player.bottom <= upper.top + 5 and
            upper.x <= player.centerx <= upper.x + upper.width
        )

        if sobre_ella and vel_y < 0 and player.top <= 40:
            return "nivel3"

        screen.fill((100, 180, 255))

        for p in platforms:
            pg.draw.rect(screen, (160, 90, 50), p)

        jugador_visible = True
        if parpadear:
            if time.time() - tiempo_de_parpadeo < 0.5:
                if int((time.time() - tiempo_de_parpadeo) * 10) % 2 == 0:
                    jugador_visible = False
                else:
                    parpadear = False
        if jugador_visible:
            pg.draw.rect(screen, (255, 255, 255), player)
        pg.draw.rect(screen, (255, 255, 255), player)

        for e in enemies:
            pg.draw.rect(screen, (255, 30, 30), e["rect"])
        
        screen.blit(vidas_img[vida], (20, 20))
        
        pg.display.update()
        clock.tick(60)