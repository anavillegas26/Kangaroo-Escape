import pygame as pg
import sys
import time
import random

def nivel2(screen, clock):
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
    player = pg.Rect(40, HEIGHT - 90, 40, 40)
    speed = 5
    vel_y = 0
    gravity = 0.8
    jump = -14

    # Características de la vida
    vida = 5
    ultimo_golpe = 0
    tiempo_de_parpadeo = 0
    parpadear = False
    
    # Carga el sprite del canguro
    try:
        canguro_img_original = pg.image.load("Kangaroo-Escape/assets/canguro.png").convert_alpha()
        canguro_img_original = pg.transform.scale(canguro_img_original, (60, 60))
        # Cambia la imagen a transparente
        canguro_img_original.set_colorkey((0, 0, 0))
    except:
        canguro_img_original = None
    mirando_derecha = True

    # Carga el sprite del enemigo
    try:
        enemy_img_original = pg.image.load("Kangaroo-Escape/assets/serpiente.png")
        enemy_img_original = pg.transform.scale(enemy_img_original, (60, 60))
        enemy_img_right = enemy_img_original
        enemy_img_left = pg.transform.flip(enemy_img_original, True, False)
    except:
        enemy_img_original = None
        enemy_img_right = None
        enemy_img_left = None

    # Efectos de sonido
    pg.mixer.init() # Inicializar el mixer
    try:
        sonido_saltar = pg.mixer.Sound("Kangaroo-Escape/audio/saltar.wav")
        sonido_aplastar = pg.mixer.Sound("Kangaroo-Escape/audio/aplastar.wav")
    except:
        sonido_saltar = None
        sonido_aplastar = None

    platforms = [
        pg.Rect(0, HEIGHT - 40, WIDTH, 40),       # piso
        pg.Rect(100, 450, 150, 20),               # plataforma media 1
        pg.Rect(350, 350, 150, 20),               # plataforma media 2
        pg.Rect(600, 250, 150, 20),               # plataforma derecha
        pg.Rect(320, 150, 150, 20),               # única plataforma superior (subida leve)
    ]

    enemy_platforms = platforms[:-1].copy()
    random.shuffle(enemy_platforms)

    plat_enemy1 = enemy_platforms.pop()
    plat_enemy2 = enemy_platforms.pop()

    enemies = []
    enemy_size = 48

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
                    if sonido_aplastar:
                        sonido_aplastar.play() # Reproduce el sonido al eliminar un enemigo
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
            if enemy_img_original:
                if e["dir"] == 1:
                    enemy_img = enemy_img_right
                else:
                    enemy_img = enemy_img_left    
                screen.blit(enemy_img, e["rect"])
            else:
                pg.draw.rect(screen, (200, 30, 30), e["rect"])
        
        screen.blit(vidas_img[vida], (20, 20))
        
        pg.display.update()
        clock.tick(60)