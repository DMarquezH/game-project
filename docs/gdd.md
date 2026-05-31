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

- Resumen del juego: Juego de oleadas con elementos roguelite en el que el jugador debe sobrevivir el máximo tiempo posible. Entre oleadas, el jugador puede mejorar a su personaje comprando objetos en la tienda usando monedas obtenidas al derrotar enemigos. El juego no tiene condición de victoria definida: el objetivo es sobrevivir y progresar indefinidamente.
- Objetivos del jugador: Sobrevivir el máximo tiempo posible, derrotando enemigos y mejorando progresivamente la partida.  Acumular monedas para comprar mejoras en la tienda.	Optimizar las estadísticas del personaje para aguantar oleadas cada vez más difíciles.
- Inspiración / Referencias: Vampire Survivors, Megabonk.

## Características principales

- Dimensionalidad: 2D
- Perspectiva de cámara: Superior (top-down)
- Tipo de cámara: seguimiento del jugador con clamp al límite del mapa
- Modo de juego: un jugador
- Progresión: Por oledas dentro de niveles/escenarios
- Dificultad y escalado: Escalado por oleada (más enemigos, mayor velocidad de spawn)
- Ritmo de juego: A tiempo real
- Tipo de mapa: Escenarios fijos 
- Duración media de partida promedio: 20 min

## Gameplay (Jugabilidad)

Especificación de elementos de jugabilidad.

### Mecánicas principales

1) Combate Cuerpo a Cuerpo (Melee):
    -	Activación: Clic izquierdo del ratón.
    -	Descripción: El jugador lanza un arco de golpe (MeleeSwipeEntity) en la dirección del cursor.
    -	Parámetros: alcance, amplitud del arco, daño, knockback, duración del swipe.
    -	Sistema de parry: si el swipe del jugador colisiona con el de un enemigo, ambos se cancelan y reciben un stun breve.
    -	Redirección de proyectiles: el swipe puede interceptar proyectiles enemigos y redirigirlos hacia los enemigos.

2) Combate a Distancia (Ranged):
    -	Activación: Clic derecho del ratón.
    -	Descripción: El jugador dispara un proyectil (ProjectileEntity) hacia la posición del cursor.
    -	Parámetros: velocidad del proyectil, daño, knockback, distancia Maxima, penetración (pierce).
    -	Ambos modos (melee y ranged) comparten el mismo temporizador de velocidad de ataque.   

3) Tienda:
    -	Activacion: Automatica cada 5 oleadas completadas (con un retraso de 1.5s tras la oleada). Tambien accesible manualmente pulsando P (modo debug).
    -	Descripción: Se presenta un menú con 3 objetos aleatorios que el jugador puede comprar gastando monedas.
    -	Reroll: el jugador puede cambiar los objetos disponibles pagando un coste (empieza en 0 monedas e incrementa con cada reroll).
    -	La compra se confirma con suficientes monedas; se aplica la mejora de estadistica inmediatamente.

4) Recogida de Pickups:
    -	Al morir un enemigo, suelta entre 3 y 8 monedas (CoinPickupEntity) con físicas de impulso.
    -	Con un 10% de probabilidad, suelta además un corazón (HeartPickupEntity) que recupera vida.
    -	Los pickups se recogen al contacto físico con el jugador.


### Sistemas de juego

Definición de los sistemas que estarán en funcionamiento a lo largo de la ejecución juego.

1) Oleadas:
   - El juego genera 10 oleadas por nivel. Cada oleada define una lista de enemigos a spawnear y un intervalo de spawn.
   - Spawn position: fuera del viewport del jugador (margen de 80px extra), con validación de límites del mapa.
   - Los enemigos usan pathfinding A* (arcade.astar_calculate_path) recalculado cada 0.5s.
   - Al completar las 10 oleadas, las 10 siguientes tendran enemigos de elite y mayor nivel (con estadisticas aumentadas).

   
2) Sistema de Combate (CombatSystem):
   - 	Gestiona colisiones entre Hitboxes (ataques) y Hurtboxes (entidades).
   -	Fuego amigo desactivado: jugador no se daño a si mismo ni a otros jugadores; enemigos no se dañan entre si.
   -	Invulnerabilidad temporal (iframes): 0.5s tras recibir un golpe.
   -	Cálculo de daño: Daño final = max(1, (dañó * (1 - armadura)) - defensa). Armadura máxima al 80%.
   -	Knockback: se inyecta vía EntityMoveEvent pausando primero todas las demás ordenes de movimiento de la entidad con intensidad proporcional al knockback / velocidad_movimiento.

3) Sistema de Movimiento (MovementSystem):
   -	Las entidades se desplazan mediante eventos EntityMoveEvent.
   -	El jugador usa PhysicsEngineSimple con colisión contra las capas de obstáculos del tilemap.
   -	Los enemigos tienen física propia (PhysicsEngineSimple individual) para colisión con paredes.
   -	Stun: si el invulnerable_timer > 0.3, la entidad no puede moverse voluntariamente.
 
   
4) Sistema de Estadísticas (EntityStats):
   Cada entidad tiene un conjunto de estadísticas (StatDefinition). Las mejoras de la tienda llaman a stats.increase(), que aplica logica diferente según la estadística:
    - ATTACK_SPEED, MOVEMENT_SPEED: incremento porcentual multiplicativo.
    -	ATTACK_KNOCKBACK: multiplicador directo.
    -	Resto de estadísticas: incremento aditivo.
    -	HEALTH tiene un tope máximo en MAX_HEALTH al incrementarse.


### Controles

Asignación de controles de dispositivos externos a eventos de input del juego.

1) Movimiento del jugador:
    - Teclas WASD del teclado / Teclas de flecha 
    - Joystick izquierdo del gamepad
   </br></br>

2) Ataque melee:
    - Clic izquierdo del ratón 

3) Ataque a distancia:
    - Clic derecho del ratón

4) Pausar / Reanudar:
    - Escape

5) Activar tienda (debug):
    - P

6) Modo debug (hitboxes):
    - F3

7) Pantalla completa:
    - F11


### Cámara

Descripción de comportamientos de la cámara de juego.

- Camara de seguimiento al jugador con suavizado.
-	Clamp al rectángulo de límites del nivel actual (no se ve fuera del mapa).
-	Se recrea al cambiar de nivel para ajustar los nuevos límites.


### Reglas de juego

Descripción de las reglas principales de juego.

- Condición de derrota: el jugador pierde toda la salud (HEALTH <= 0). Se muestra GAME OVER.
-	Condición de progresión: completar las 10 oleadas del nivel actual carga el siguiente nivel.
-	Las estadísticas del jugador y las monedas se conservan entre niveles.


## Jugador

Especificación de aspectos, atributos y comportamientos del personaje principal.

### Estadísticas

- MAX_HEALTH: Salud maxima.
- HEALTH: Salud actual.
- MOVEMENT_SPEED: Velocidad de movimiento.
- ATTACK_DAMAGE: Daño base de todos los ataques.
- ATTACK_SPEED: Ataques por segundo.
- SHOT_SPEED: Velocidad de proyectiles.
- ATTACK_RANGE: Alcance del ataque melee / distancia máxima del proyectil (x6).
- SWING_AMPLITUDE: Amplitud en grados del arco de golpe melee.
- ATTACK_KNOCKBACK: Fuerza de retroceso aplicada a los enemigos.
- DEFENSE: Reducción aditiva de daño recibido.
- ARMOR: Reducción porcentual de daño recibido (max 80%).
- CRIT_CHANCE: Probabilidad de golpe critico (0.0 - 1.0).
- CRIT_DAMAGE_MULTI: Multiplicador de daño en golpe critico.
- SHOT_PIERCE: Enemigos adicionales que puede atravesar un proyectil.
- SHOT_SPREAD:Dispersión de disparos (negativo = más precisión).


### Comportamiento

-	Animación de movimiento con 4 direcciones (arriba, abajo, izquierda, derecha), 4 frames cada una, a 6 fps.
-	Evento de pisada (EntityFootstepEvent) en los frames 0 y 2 del ciclo de caminar.
-	En reposo muestra un frame estático.
-	Stun momentáneo al recibir un golpe fuerte (invulnerable_timer > 0.3 bloquea el movimiento voluntario).


### Habilidades

-	Ataque melee: arco de golpe con MeleeSwipeEntity (visible y con hitbox).
-	Ataque ranged: proyectil con ProjectileEntity (físicas, distancia máxima, pierce).
-	Parry: cancelar el ataque cuerpo a cuerpo de un enemigo golpeando simultaneamente su swipe.
-	Redirección de proyectiles: golpear un proyectil enemigo con el swipe del jugador lo redirige hacia los enemigos.
-

## Enemigos y NPCs

Especificación de aspectos, atributos y comportamientos de los NPCs y enemigos del juego.

### Enemigo Melee (MeleeEnemy)

-	Comportamiento: persigue al jugador mediante A*. Cuando está a <= 50px, se detiene y ataca.
-	Ataque: EntityAttackedMeleeEvent con amplitud de 90 grados.
-	Animación: 4 direcciones x 4 frames, a 8 fps.
- Estadísticas: HEALTH, ATTACK_DAMAGE, MOVEMENT_SPEED, ATTACK_SPEED, ATTACK_KNOCKBACK, ATTACK_DISTANCE


### Enemigo Ranged (RangedEnemy)

-	Comportamiento: persigue al jugador mediante A* hasta estar dentro de 250px. Luego se detiene y dispara.
-	Ataque: EntityAttackedRangedEvent disparando un proyectil hacia el jugador.
-	Animación: misma estructura que el enemigo melee.
- Estadísticas: HEALTH ATTACK_DAMAGE, MOVEMENT_SPEED, ATTACK_SPEED, ATTACK_RANGE, SHOT_SPEED, ATTACK_KNOCKBACK.


### Enemigo Rapido (FastEnemy)

-	Comportamiento: persigue al jugador rapidamente mediante A*.  Cuando está a <= 50px, se detiene y ataca.
-	Ataque: EntityAttackedMeleeEvent con amplitud de 90 grados y ATTACK_SPEED aumentada.
-	Animación: misma estructura que el enemigo melee.
- Estadísticas: HEALTH ATTACK_DAMAGE, MOVEMENT_SPEED, ATTACK_SPEED, ATTACK_RANGE, SHOT_SPEED, ATTACK_KNOCKBACK.


### Jefe (BossEnemy)

-	Comportamiento: persigue al jugador.  Cuando está a >=50px, se detiene y ataca en area.
-	Ataque: EntityAttackedMeleeEvent con amplitud de 144 grados.
-	Animación: 4 direcciones y un ataque en area.
- Estadísticas: HEALTH ATTACK_DAMAGE, MOVEMENT_SPEED, ATTACK_SPEED, ATTACK_RANGE, SHOT_SPEED, ATTACK_KNOCKBACK.


### Drops

-	Al morir cualquier enemigo: 3-8 monedas con físicas de impulso (vel. aleatoria), cada una otorga 10-25 monedas de tienda.
-	10% de probabilidad de soltar un HeartPickupEntity que recupera vida al ser recogido.

## Niveles (Mundo)

Descripción de los escenarios disponibles de juego: Temática, ambientación, elementos del escenario, mecánicas,
ideas, etc.

1) Nivel 1 - Cementerio (Cementery):
  - Archivo de mapa: assets/levels/level_2/LV2_1.0.tmj (formato Tiled).
  -	Tilesets: cementerio.tsx, Cementerio2.tsx, tileset_mod.tsx.
  -	Elementos visuales: lapidas, arboles, troncos, vallas, postes (apagados/encendidos), piedras.
  -	Capas de colisión definidas en el tilemap para el pathfinding y las físicas.
  -	Temática: noche de cementerio, ambiente oscuro y gótico.


## Estilo visual

-	Estilo artístico: Pixel art con resolución de sprites relativamente alta (spritesheet de alta resolución).
-	Perspectiva: vista superior (top-down).
-	Escala de sprites: jugador y enemigos al 30-35% del tamaño original del spritesheet.
-	Temática principal: survival en escenarios oscuros (cementerio, ambientes de terror/fantasia).
-	Efectos de ataque: MeleeSwipeEntity visible como arco animado; proyectiles visibles con sprite propio.
-	Fuente de texto: Black Ops One (BlackOpsOne-Regular.ttf) para la UI.


## Música y sonido

Especificación de la música y el sonido del juego.
-   La gestion de sonidos se aprovecha del gran uso de eventos para la mayoria de acciones en el juego,
    hay 3 maneras de reproducir los sonidos siendo 2 para los audios cortos (si hay variaciones, al azar) y 1 para los audios largos
    que se cargan desde la MP.
-	Música de gameplay: soundtrack3-edit.mp3 (se inicia al entrar en GameView).
-	Música de menu principal: soundtrack1.mp3.


## Interfaz de usuario (UI)

Descripción de los elementos, atributos y comportamientos de las interfaces gráficas de usuario (GUI) del juego.

### Menú principal

-	Fondo: main_menu_background.png.
-	Botones: Jugar, Opciones, Salir (con spritesheets animados para los estados normal/hover/pressed).

### Menú de pausa

-	Se activa con Escape durante la partida.
-	Botones: Reanudar, Menú Principal, Salir.
-	El juego se congela mientras esta activo.

### HUD de la partida

-	Esquina superior izquierda: icono de corazón + texto 'HP_actual/HP_maximo', icono de moneda + cantidad de monedas.
-	Esquina superior derecha: widget de oleada con spritesheet animado (30 frames) que avanza al completar cada oleada.


### Tienda

-	Se activa automáticamente tras completar oleadas múltiplo de 5 (con 1.5s de retraso).
-	Muestra hasta 3 objetos con icono, nombre, descripción, coste y botón de compra.
-	Botón de Reroll para cambiar los objetos (coste incremental).
-	Fondo: shop_background.png.
-	El juego se congela mientras esta activo.


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