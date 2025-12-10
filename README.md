# Kangaroo Escape





![Kanguroo_Escape](https://github.com/user-attachments/assets/8b7ac5a9-5c75-4fd4-b21f-05624d05c9d1)


Juego de plataformas 2D desarrollado con Pygame basado en la película "Kangaroo Jack", donde el jugador controla a Kangaroo Jack, un canguro aventurero que debe recuperar monedas de oro robadas mientras evita enemigos y trampas en el desierto australiano.

# Descripción del juego
Kangaroo Escape es un juego de plataformas en 2D donde:
- Controlas a Kangaroo Jack, un canguro con habilidades especiales.
- Debes recorrer diferentes escenarios, saltar obstáculos y esquivar enemigos.
- El objetivo es recolectar todas las monedas de cada nivel y llegar a la meta sin perder todas las vidas.
- El juego incluye power-ups, enemigos variados y niveles diseñados progresivamente.

# Jugabilidad
Controles de movimiento:
- ⬅️ Izquierda: moverse a la izquierda
- ➡️ Derecha: moverse a la derecha
- ⬆️ Espacio/Barra espaciadora: saltar
- ⬆️ Mantener salto: súper salto

# Objetivo
Recolectar todas las monedas del nivel y llegar al final sin perder todas las vidas.

# Enemigos
- Serpientes
- Dingos
- Trampas del desierto

# Power-Ups
- Zanahorias → restauran salud
- Boomerangs → permiten atacar enemigos a distancia

# Niveles
1. Desierto del Outback – Nivel tutorial
2. Cañón Rojo – Plataformas móviles y enemigos en movimiento
3. Mina Perdida – Túneles oscuros con trampas
4. Templo del Tesoro – Nivel final con jefe cazador furtivo

# Estilo visual y sonido
- Gráficos coloridos con estética caricaturesca
- Fondos inspirados en el desierto australiano
- Música con tambores, sonidos de fauna
- Animaciones simples pero expresivas

# Arquitectura del proyecto (POO)
El juego está construido con Programación Orientada a Objetos, aplicando:
- Jugador: movimiento, salto y física
- Enemigo (clase base): Serpiente, Dingo
- PowerUp: Zanahoria, Boomerang
- Nivel: gestiona colisiones, plataformas y entidad del jugador
- Moneda: coleccionable del nivel

# Conceptos POO usados
1. Concepto POO: Aplicación en el juego
2. Clase: Representa entidades del juego (Jugador, Enemigo, Moneda)
3. Objeto: Instancias concretas (serpiente1, moneda3, kangaroo_jack)
4. Herencia: Serpiente y Dingo heredan de Enemigo
5. Polimorfismo: El método atacar() funciona distinto en Jugador y Enemigo
6. Encapsulamiento: Vida del jugador con getters/setters
7. Abstracción: Métodos como saltar() ocultan física interna

# Instalación
1. Clonar el repositorio
git clone https://github.com/usuario/kangaroo-escape.git
2. Instalar dependencias
pip install pygame
3. Ejecutar el juego
python main.py

# Estructura del proyecto
```bash
kangaroo-escape/
│── assets/
│   ├── sprites/
│   ├── sonidos/
│   └── fondos/
│── src/
│   ├── player.py
│   ├── enemy.py
│   ├── level.py
│   ├── powerups.py
│   └── main.py
│── README.md
│── requirements.txt

# Estado del proyecto
🟡 En desarrollo (versión prototipo).

# Próximas mejoras
- Menú principal
- Sistema de guardado
- Más animaciones del jugador
- Nuevos enemigos

# Colaboradores
Colaborador 1 – Matthew Olmedo: Programación y diseño de niveles
Colaborador 2 – Bryan Carcamo: Arte y sprites
Colaborador 3 – Ana Villegas: Redacción e investigación
