import pygame as pg
import sys
import random
import time

def nivel3(screen, clock):
    WIDTH, HEIGHT = 800, 600

    # Lista de las imágenes de la barra de vida
    vidas_img = [
        pg.image.load("Kangaroo-Escape/assets/barra-6.png"),
        pg.image.load("Kangaroo-Escape/assets/barra-5.png"),
        pg.image.load("Kangaroo-Escape/assets/barra-4.png"),
        pg.image.load("Kangaroo-Escape/assets/barra-3.png"),
        pg.image.load("Kangaroo-Escape/assets/barra-2.png"),
        pg.image.load("Kangaroo-Escape/assets/barra-1.png")
    ]
    vidas_img = [pg.transform.scale(img, (160, 80)) for img in vidas_img]

    # Añadir imagen de fondo
    try:
        fondo_nivel = pg.image.load("Kangaroo-Escape/image/fondo_nivel3.png").convert()
        fondo_nivel = pg.transform.scale(fondo_nivel, (WIDTH, HEIGHT))
    except:
        fondo_nivel = None
    
    player = pg.Rect(100, HEIGHT - 90, 40, 40)
    speed = 5
    vel_y = 0
    gravity = 0.8
    jump = -14

    vida = 5
    ultimo_golpe = 0
    tiempo_de_parpadeo = 0
    parpadear = False

    platforms = [
        pg.Rect(50, 500, 120, 20),
        pg.Rect(250, 430, 120, 20),
        pg.Rect(500, 460, 120, 20),
        pg.Rect(650, 350, 120, 20),
        pg.Rect(400, 300, 120, 20),
        pg.Rect(150, 260, 120, 20),
        pg.Rect(350, 170, 120, 20),
        pg.Rect(600, 120, 120, 20),
        pg.Rect(0, HEIGHT - 40, WIDTH, 40)  # piso
    ]

    enemy_platforms = platforms[:-1].copy()
    random.shuffle(enemy_platforms)

    plat_enemy1 = enemy_platforms.pop()
    plat_enemy2 = enemy_platforms.pop()
    plat_shooter = enemy_platforms.pop()

    enemies = []
    enemy_size = 30

    ex = plat_enemy1.x + random.randint(0, plat_enemy1.width - enemy_size)
    ey = plat_enemy1.y - enemy_size
    enemies.append({
        "rect": pg.Rect(ex, ey, enemy_size, enemy_size),
        "dir": random.choice([-1,1]),
        "speed": 2,
        "plat": plat_enemy1
    })

    ex = plat_enemy2.x + random.randint(0, plat_enemy2.width - enemy_size)
    ey = plat_enemy2.y - enemy_size
    enemies.append({
        "rect": pg.Rect(ex, ey, enemy_size, enemy_size),
        "dir": random.choice([-1,1]),
        "speed": 2,
        "plat": plat_enemy2
    })
  
    shooter_size = 30
    sp = plat_shooter

    shooter = pg.Rect(
        sp.x + sp.width//2 - shooter_size//2,
        sp.y - shooter_size,
        shooter_size,
        shooter_size
    )

    shooter_dir = 1
    shooter_min = sp.x
    shooter_max = sp.x + sp.width - shooter.width

    bullet_interval = 90  # 1.5 seg
    shoot_timer = 0
    bullets = []
    
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
   
        for e in enemies[:]:
            plat = e["plat"]
            e["rect"].x += e["dir"] * e["speed"]

            if e["rect"].left < plat.left:
                e["rect"].left = plat.left
                e["dir"] = 1
            if e["rect"].right > plat.right:
                e["rect"].right = plat.right
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

        if shooter:
            shooter.x += shooter_dir * 2
            if shooter.x <= shooter_min:
                shooter.x = shooter_min
                shooter_dir = 1
            if shooter.x >= shooter_max:
                shooter.x = shooter_max
                shooter_dir = -1
          
            if player.colliderect(shooter):
                tiempo_actual = time.time()
                # ¿Pisado?
                if vel_y > 0 and player.bottom <= shooter.centery:
                    shooter = None  
                    vel_y = -12     
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
      
        if shooter:
            shoot_timer += 1
            if shoot_timer >= bullet_interval:
                shoot_timer = 0

                dx = player.centerx - shooter.centerx
                dy = player.centery - shooter.centery
                dist = max(1, (dx*dx + dy*dy)**0.5)

                vx = dx/dist * 2
                vy = dy/dist * 2

                bullets.append({
                    "rect": pg.Rect(shooter.centerx, shooter.centery, 10, 10),
                    "vx": vx,
                    "vy": vy
                })
     
        for b in bullets[:]:
            b["rect"].x += b["vx"]
            b["rect"].y += b["vy"]

            if not (0 <= b["rect"].x <= WIDTH and 0 <= b["rect"].y <= HEIGHT):
                bullets.remove(b)
                continue

            if player.colliderect(b["rect"]):
                tiempo_actual = time.time()
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

        if player.top <= 0:
            return "nivel4"

        screen.fill((60, 20, 90))

        for p in platforms:
            pg.draw.rect(screen, (170, 120, 70), p)

        # Dibuja el fondo agregando para probar
        if fondo_nivel:
            screen.blit(fondo_nivel, (0, 0))
        else:
            screen.fill((120, 190, 255)) # Rellena la pantalla con un color celeste
        for p in platforms:
            pg.draw.rect(screen, (150, 80, 40), p)

        jugador_visible = True
        if parpadear:
            if time.time() - tiempo_de_parpadeo < 0.5:
                if int((time.time() - tiempo_de_parpadeo) * 10) % 2 == 0:
                    jugador_visible = False
                else:
                    parpadear = False
                    
        if jugador_visible:
            pg.draw.rect(screen, (255, 255, 255), player)

        for e in enemies:
            pg.draw.rect(screen, (255,60,60), e["rect"])

        if shooter:
            pg.draw.rect(screen, (160,40,160), shooter)

        for b in bullets:
            pg.draw.rect(screen, (200,100,200), b["rect"])
        
        screen.blit(vidas_img[vida], (20, 20))

        pg.display.update()
        clock.tick(60)