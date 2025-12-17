import pygame as pg
import sys
import time
import random

def nivel5(screen, clock):
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
        fondo_nivel = pg.image.load("Kangaroo-Escape/image/fondo_nivel2.png").convert()
        fondo_nivel = pg.transform.scale(fondo_nivel, (WIDTH, HEIGHT))
    except:
        fondo_nivel = None

    # Características del jugador
    player = pg.Rect(100, HEIGHT - 90, 40, 40)
    speed = 5
    vel_y = 0
    gravity = 0.8
    jump = -14
    on_ground = False

    # Características de la vida
    vida = 5
    ultimo_golpe = 0
    tiempo_de_parpadeo = 0
    parpadear = False

    # Añadir un código para el sprite del canguro
    try:
        canguro_img_original = pg.image.load("Kangaroo-Escape/assets/canguro.png").convert_alpha()
        canguro_img_original = pg.transform.scale(canguro_img_original, (60, 60))
        # Cambia la imagen a transparente
        canguro_img_original.set_colorkey((0, 0, 0))
    except:
        canguro_img_original = None
    mirando_derecha = True

    # Efectos de sonido
    pg.mixer.init() # Inicializar el mixer
    try:
        sonido_saltar = pg.mixer.Sound("Kangaroo-Escape/audio/saltar.wav")
        sonido_aplastar = pg.mixer.Sound("Kangaroo-Escape/audio/aplastar.wav")
    except:
        sonido_saltar = None
        sonido_aplastar = None

    # --- PLATAFORMAS ---
    platforms = [
        pg.Rect(0, HEIGHT - 40, WIDTH, 40), # Suelo
        pg.Rect(100, 500, 150, 20),
        pg.Rect(200, 450, 200, 20),
        pg.Rect(500, 320, 150, 20),
        pg.Rect(350, 120, 120, 20),
        pg.Rect(300, 220, 150, 20),
        pg.Rect(600, 120, 150, 20)
    ]

    # Enemigos
    enemies = []
    bullets = []
    bullet_interval = 90  # 1.5 seg
    shoot_timer = 0
    enemy_size = 30

    for plat in platforms[1:]:
        ex = plat.x + random.randint(0, plat.width - enemy_size)
        ey = plat.y - enemy_size
        enemies.append({
            "rect": pg.Rect(ex, ey, enemy_size, enemy_size),
            "dir": random.choice([-1, 1]),
            "speed": 2,
            "plat": plat
        })

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            player.x -= speed
            mirando_derecha = False # Cambia de linea
        if keys[pg.K_RIGHT]:
            player.x += speed
            mirando_derecha = True # Cambia de linea
        if keys[pg.K_SPACE] and vel_y == 0:
            vel_y = jump
            if sonido_saltar:
                sonido_saltar.play() # Reproduce el sonido al saltar

        vel_y += gravity
        player.y += vel_y

        on_ground = False
        for p in platforms:
            if player.colliderect(p) and vel_y > 0:
                player.bottom = p.top
                vel_y = 0
                on_ground = True

        for e in enemies[:]:
            plat = e["plat"]
            e["rect"].x += e["dir"] * e["speed"]

            if e["rect"].left < plat.left:
                e["rect"].left = plat.left
                e["dir"] = 1
            if e["rect"].right > plat.right:
                e["rect"].right = plat.right
                e["dir"] = -1

        shoot_timer += 1
        if shoot_timer >= bullet_interval:
            shoot_timer = 0

            for e in enemies:
                dx = player.centerx - e["rect"].centerx
                dy = player.centery - e["rect"].centery
                dist = max(1, (dx*dx + dy*dy)**0.5)

                vx = dx/dist * 2
                vy = dy/dist * 2

                bullets.append({
                    "rect": pg.Rect(e["rect"].centerx, e["rect"].centery, 10, 10),
                    "vx": vx,
                    "vy": vy
                })

        for e in enemies[:]:
            if player.colliderect(e["rect"]):
                tiempo_actual = time.time()
                # ¿Pisado?
                if vel_y > 0 and player.bottom <= e["rect"].centery:
                    if sonido_aplastar:
                        sonido_aplastar.play() # Reproduce el sonido al eliminar un enemigo
                    enemies.remove(e)  
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
                    
        if player.left < 0:
            player.left = 0
        if player.right > WIDTH:
            player.right = WIDTH

        if player.top <= 0:
            return "menu"
        
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

        # Verificar la visibilidad del jugador y el parpadeo al recibir daño
        jugador_visible = True
        if parpadear:
            if time.time() - tiempo_de_parpadeo < 0.5:
                if int((time.time() - tiempo_de_parpadeo) * 10) % 2 == 0:
                    jugador_visible = False
            else:
                parpadear = False

        # Dibuja el canguro con el sprite
        if canguro_img_original:
            if jugador_visible:
                if mirando_derecha:
                    canguro_img = canguro_img_original
                else:
                    canguro_img = pg.transform.flip(canguro_img_original, True, False)
                
                sprite_rect = canguro_img.get_rect()
                sprite_rect.midbottom = player.midbottom

                screen.blit(canguro_img, sprite_rect.topleft)
            else:
                if jugador_visible:
                    pg.draw.rect(screen, (255, 255, 255), player)

        for e in enemies:
            pg.draw.rect(screen, (160,40,160), e["rect"])

        for b in bullets:
            pg.draw.rect(screen, (200,100,200), b["rect"])
        
        screen.blit(vidas_img[vida], (20, 20))

        pg.display.update()
        clock.tick(60)