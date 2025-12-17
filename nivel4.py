import pygame as pg
import sys
import time
import random

def nivel4(screen, clock):
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
        fondo_nivel = pg.image.load("Kangaroo-Escape/image/fondo_nivel1.png").convert()
        fondo_nivel = pg.transform.scale(fondo_nivel, (WIDTH, HEIGHT))
    except:
        fondo_nivel = None

    # Características del jugador
    player_size = 40
    player_rect = pg.Rect(100, HEIGHT - player_size - 50, player_size, player_size)
    player_speed = 5
    player_y_vel = 0
    gravity = 0.8
    jump_force = -14
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

    # Añadir un código para el sprite del enemigo
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

    # --- PLATAFORMAS ---
    platforms = [
        pg.Rect(0, HEIGHT - 40, WIDTH, 40), # Suelo
        pg.Rect(150, 480, 150, 20),
        pg.Rect(450, 380, 150, 20),

        # Plataformas que se mueven
        pg.Rect(200, 260, 150, 20),
        pg.Rect(500, 150, 150, 20)
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
        ex = plat.x + random.randint(0, plat.width - 30)
        ey = plat.y - 48
        enemies.append({
            "rect": pg.Rect(ex, ey, 60, 60),
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
            mirando_derecha = False # Cambia de linea
        if keys[pg.K_RIGHT]:
            player_rect.x += player_speed
            mirando_derecha = True # Cambia de linea
        if keys[pg.K_SPACE] and on_ground:
            player_y_vel = jump_force
            on_ground = False
            if sonido_saltar:
                sonido_saltar.play() # Reproduce el sonido al saltar

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

            tiempo_actual = time.time()
            if player_rect.colliderect(e["rect"]):
                # ¿Pisado?
                if player_y_vel > 0 and player_rect.bottom <= e["rect"].centery:
                    if sonido_aplastar:
                        sonido_aplastar.play() # Reproduce el sonido al eliminar un enemigo
                    enemies.remove(e)
                    player_y_vel = -10  # rebote
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
            
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > WIDTH:
            player_rect.right = WIDTH

        # --- PASAR AL NIVEL 5 ---
        if player_rect.top <= 0 and player_y_vel < 0:
            return "nivel5"

        # --- DIBUJAR ---
        screen.fill((120, 200, 255))

        for plat in platforms:
            pg.draw.rect(screen, (160, 90, 50), plat)

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
                sprite_rect.midbottom = player_rect.midbottom

                screen.blit(canguro_img, sprite_rect.topleft)
            else:
                if jugador_visible:
                    pg.draw.rect(screen, (255, 255, 255), player_rect)

        for e in enemies:
            if enemy_img_original:
                if e["dir"] == 1:
                    enemy_img = enemy_img_right
                else:
                    enemy_img = enemy_img_left
                screen.blit(enemy_img, e["rect"])
            else:
                pg.draw.rect(screen, (255, 60, 60), e["rect"])

        screen.blit(vidas_img[vida], (20, 20))

        pg.display.update()
        clock.tick(60)