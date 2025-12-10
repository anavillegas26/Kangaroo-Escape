import pygame as pg
import sys

# Importar niveles
from nivel1 import nivel1
from nivel2 import nivel2
from nivel3 import nivel3
from nivel4 import nivel4

# Inicia todos los modulos pygame
pg.init()

# Resolución de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
# Poner título de la ventana
pg.display.set_caption("Kangaroo Escape")

# Carga portada si existe (si no, seguirá sin fondo)
try:
    fondo = pg.image.load("Kangaroo-Escape/image/portada.png")
    fondo = pg.transform.scale(fondo, (WIDTH, HEIGHT))
except:
    fondo = None

# Agregar icono del juego si existe
try:
    icono = pg.image.load("Kangaroo-Escape/icon/icono.png")
except:
    icono = None
if icono:
    pg.display.set_icon(icono)

# Fuente de letras
font = pg.font.SysFont("Arial", 48, bold=True)
small = pg.font.SysFont("Arial", 32)

menu_abierto = False
volumen = 5

# Botónes de jugar y opciones
jugar_x, jugar_y = WIDTH // 2, 380
opciones_x, opciones_y = WIDTH // 2, 450

def texto_boton(texto, x, y):
    mouse = pg.mouse.get_pos()
    tx = font.render(texto, True, (255, 255, 255))
    rect = tx.get_rect(center=(x, y))
    if rect.collidepoint(mouse):
        tx = font.render(texto, True, (255, 220, 100))
    screen.blit(tx, rect)
    return rect

def dibujar_menu_transparente():
    overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    titulo = font.render("Opciones", True, (255, 255, 255))
    screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 120))
    txt = small.render("Sonido:", True, (255, 255, 255))
    screen.blit(txt, (260, 240))
    flecha_izq = small.render("<", True, (255, 255, 0))
    screen.blit(flecha_izq, (360, 235))
    val = small.render(str(volumen), True, (255, 255, 255))
    screen.blit(val, (400, 237))
    flecha_der = small.render(">", True, (255, 255, 0))
    screen.blit(flecha_der, (440, 235))
    for i in range(10):
        color = (0, 255, 0) if i < volumen else (80, 80, 80)
        pg.draw.rect(screen, color, (260 + i * 28, 300, 22, 28), border_radius=4)
clock = pg.time.Clock()

def run_chain():
    """
    Ejecuta la cadena de niveles de forma segura.
    Cada nivel devuelve:
     - "menu" para volver al menú
     - "nivel2" para pedir cargar nivel2
     - "nivel3" para pedir cargar nivel3
    """
    # r1 expected: "menu" or "nivel2"
    # Actualiza el título de ventana "Nivel 1"
    pg.display.set_caption("Kangaroo Escape - Nivel 1")
    r1 = nivel1(screen, clock)

    if r1 == "nivel2":
        # Actualiza el título de ventana "Nivel 2"
        pg.display.set_caption("Kangaroo Escape - Nivel 2")
        r2 = nivel2(screen, clock)

        if r2 == "nivel3":
            # Actualiza el título de ventana "Nivel 3"
            pg.display.set_caption("Kangaroo Escape - Nivel 3")
            r3 = nivel3(screen, clock)

            if r3 == "nivel4":
                # Actualiza el título de ventana "Nivel 4"
                pg.display.set_caption("Kangaroo Escape - Nivel 4")
                r4 = nivel4(screen, clock)

    # Vuelve al título original
    pg.display.set_caption("Kangaroo Escape")
        # si r2 == "menu" vuelve al menú
    # si r1 == "menu" vuelve al menú

# Loop del menú
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN and menu_abierto:
            if event.key == pg.K_LEFT:
                volumen = max(0, volumen - 1)
            if event.key == pg.K_RIGHT:
                volumen = min(10, volumen + 1)
            if event.key == pg.K_ESCAPE:
                menu_abierto = False

        if event.type == pg.MOUSEBUTTONDOWN:
            mx, my = pg.mouse.get_pos()
            if not menu_abierto:
                if 'jugar_rect' in globals() and jugar_rect.collidepoint(mx, my):
                    run_chain()
                    menu_abierto = False
                if 'opciones_rect' in globals() and opciones_rect.collidepoint(mx, my):
                    menu_abierto = True
            else:
                if 360 < mx < 380 and 235 < my < 270:
                    volumen = max(0, volumen - 1)
                if 440 < mx < 460 and 235 < my < 270:
                    volumen = min(10, volumen + 1)

    if fondo:
        screen.blit(fondo, (0, 0))
    else:
        screen.fill((40, 100, 180))

    if not menu_abierto:
        jugar_rect = texto_boton("Jugar", jugar_x, jugar_y)
        opciones_rect = texto_boton("Opciones", opciones_x, opciones_y)
    else:
        dibujar_menu_transparente()

    pg.display.update()
    clock.tick(60)