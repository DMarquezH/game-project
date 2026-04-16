# Documento de Diseño de Juego (GDD)

## Información general

- Nombre: --rellenar--
- Género: Survivor
- Plataforma: PC (Mínimo Windows y Linux)
- Tecnologías: Python + Arcade
- Versión GDD: 0.1

## Glosario

- Incremental: ...

## Concepto

Ideas principales resumidas de forma breve.

- Resumen del juego: Un juego de oleadas incremental con extracción de recursos con partidas de
  duración ilimitada.
- Objetivos del jugador: Sobrevivir el máximo tiempo posible, derrotando enemigos y mejorando
  progresivamente la partida.
- Inspiración / Referencias: Vampire Survivors, Megabonk.

## Características principales

- Dimensionalidad: 2D
- Perspectiva de cámara: Superior (isométrica, lateral, superior, etc)
- Tipo de cámara: seguimiento del jugador
- Modo de juego: un jugador
- Progresión: Por niveles/escenarios
- Dificultad y escalado: Por oleadas + progresión del jugador
- Ritmo de juego: A tiempo real
- Tipo de mapa: procedural
- Duración media de partida promedio: 20 min

## Gameplay (Jugabilidad)

Especificación de elementos de jugabilidad.

### Mecánicas principales

1) Extracción de recursos:
   - Descripción: El jugador puede recolectar recursos generados en el mapa.
   - Activación: El jugador interactua con las entidades de recursos extraíbles.
   - Resultado: El jugador obtiene una cantidad variable de un tipo de recurso.
   </br></br>

2) Fabricación:
   - Descripción: El jugador puede consumir recursos en la elaboración de objetos que mejoran
     las estadísticas de jugador/armas.
   - Activación: Mediante un menú de creación.
   - Resultado: El jugador obtiene una mejora de estadísticas o de arma.
   </br></br>

3) Tienda:
   - Descripción: Cada cierto número de oleadas aparece un menú de una tienda que permite al
     jugador adquirir objetos que otorgan hablidades/mejoras pasivas y/o activas.
   - Activación: Se abre un menú y el jugador adquiere un artículo usando una moneda.
   - Resultado: El jugador adquiere uno o varios objetos de mejora.

4) Dash:
   - ...

### Sistemas de juego

Definición de los sistemas que estarán en funcionamiento a lo largo de la ejecución juego.

1) Oleadas:
   - Descripción: Cada cierto tiempo se inicia una oleada en la que aparece una cantidad de
     enemigos que persiguen y atacan al jugador. La siguiente oleada se inicia pasado cireto
     tiempo si el jugador no consigue eliminar a todos los enemigos a tiempo. Cada x oleadas
     aparece un enemigo más poderoso (jefe), acompañado de un número reducido de enemigos normales.

   - Características: El tiempo entre oleadas (excepto la anterior a la tienda, la del jefe)
     escala en función del número de oleada, mediante una función logarítmica.
   
2) Recursos:
   - Descripción: El jugador puede almacenar una cantidad ilimitada (de momento) de recursos
     de cada tipo, obtenidos mediante la recolección de recursos, o la eliminación de enemigos.
   
   - Recursos de entidades: Moneda, experiencia, recursos exclusivos con baja probabilidad de drop,
     materiales de entidades pasivas.

   - Recursos naturales: Metal (sin especificar), Materia orgánica (sin especificar).

3) Experiencia:
   - Descripción: El jugador posee una barra de experiencia que se rellena al derrotar enemigos. Cuando
     la barra se completa el jugador recibe un punto de nivel (acumulables) que puede usar en un menú
     contiguo al de fabricación para adquirir una mejora de estadísticas/pasivas a elegir. 
   
4) Salud:
   - Descripción: Las entidades tienen una cantidad de salud. Cuando se agota, la entidad es derrotada.
     La salud se va regenerando con el tiempo y mediante

### Controles

Asignación de controles de dispositivos externos a eventos de input del juego.

1) Movimiento del jugador:
   - Teclas WASD del teclado
   - Joystick izquierdo del gamepad
   </br></br>

2) Ataque
3) Dash
4) Menús
5) Interacción

### Cámara

Descripción de comportamientos de la cámara de juego.

- Offset de seguimiento al jugador -> Cuando el jugador se aleja lo suficiente del centro de la vista, la
  cámara actualiza su posición respecto al jugador.

### Reglas de juego

Descripción de las reglas principales de juego.

- Condiciones de derrota: El jugador pierde todos los puntos de salud.
- Condiciones de superación de nivel: --rellenar--
- ...

## Jugador

Especificación de aspectos, atributos y comportamientos del personaje principal.

### Estadísticas

- Ejemplo 1: --rellenar--
- Ejemplo 2: --rellenar--
- ...

### Comportamiento

- Ejemplo 1: --rellenar--
- Ejemplo 2: --rellenar--
- ...

### Habilidades

- Ejemplo 1: --rellenar--
- Ejemplo 2: --rellenar--
- ...

## Enemigos y NPCs

Especificación de aspectos, atributos y comportamientos de los NPCs y enemigos del juego.

### NPC 1

- Descripción: --rellenar--
- Comportamiento: --rellenar--
- ...

### Enemigo 1

- Descripción: --rellenar--
- Estadísticas: --rellenar--
- Comportamiento: --rellenar--
- Ataques / Habilidades: --rellenar--
- Drops / Loot: --rellenar--
- ...

## Niveles (Mundo)

Descripción de los escenarios disponibles de juego: Temática, ambientación, elementos del escenario, mecánicas,
ideas, etc.

1) Ejemplo 1:
   - Descripción: --rellenar--
   - ...

## Estilo visual

Especificaciones gráficas y visuales del juego: Bocetos de personajes, escenarios, interfaz, etc.

- Estilo artístico: --rellenar-- (pixel art, cartoon, realista, etc)
- Paleta de colores: --rellenar--
- Temática principal: --rellenar--
- Efectos gráficos: --rellenar-- (partículas, etc)
- ...

## Música y sonido

Especificación de la música y el sonido del juego.

- Estilo musical: --rellenar--
- Efectos de sonido: --rellenar-- (sonidos de menú, ataques, habilidades, etc)
- ...

## Interfaz de usuario (UI)

Descripción de los elementos, atributos y comportamientos de las interfaces gráficas de usuario (GUI) del juego.

### Menú principal

...

### Submenús de juego

...

### HUD de la partida

...

### Pantallas de victoria / derrota

...

## Juego mínimo funcional (MVP)

Definición de la versión de juego mínima jugable (primer objetivo a lograr).

Lista inicial de funcionalidades:
- Movimiento del jugador
- Ataque del jugador
- Mapa vacío con alguna entidad (recurso/obstaculo)
- Enemigo que persiga y ataque al jugador
- Estadísticas del jugador: Vida, daño, velocidad de movimiento, velocidad de ataque.
- Armas (distancia y melee) con atributos propios: Melee[alcance, daño], Distancia[velocidad proyectil,
  tamaño proyectil, daño proyectil, alcance]


## Ideas y sugerencias

Lista de ideas y sugerencias:
- ...
- ...



## Borrador (primera sesión de clase):

- Nombre: survivor-project
- Genero: Survivor/Idler/resource-fetch
- Objetivos/Historia: Muchos
- Personajes: Jugador/Enemigos
- Estetica: Cartoony
- Gimmicks: Estadisticas, habilidades, tienda, recoleccion de recursor, y mas (ya se vera)
- Escenarios: Escenarios alien (borrador)