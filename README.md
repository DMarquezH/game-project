Survivor Project

Juego de oleadas con elementos roguelite desarrollado con Python + Arcade para la asignatura de Tecnología de Videojuegos (UAH). El objetivo es sobrevivir el mayor tiempo posible, derrotando enemigos y mejorando a tu personaje entre oleadas.

Controles:
    - Mover al jugador:W A S D o flechas o Joystick izquierdo
    - Ataque melee: Clic izquierdo
    - Ataque a distancia: Clic derecho
    - Pausar / Reanudar: Escape
    - Pantalla completa: F11
    - Ver hitboxes: (debug) F3

Mecánicas de combate:

- Ataque melee (clic izquierdo):
    El jugador lanza un arco de golpe en la dirección del cursor. Tiene parámetros de alcance, amplitud, daño y knockback.
        - Parry: si el swipe del jugador colisiona con el ataque melee de un enemigo al mismo tiempo, ambos se cancelan y el enemigo queda brevemente aturdido.
        - Redirección de proyectiles: golpear un proyectil enemigo con el swipe lo redirige hacia los propios enemigos.
- Ataque a distancia (clic derecho):
    Dispara un proyectil hacia la posición del cursor. Ambos modos de ataque comparten el mismo temporizador de velocidad de ataque, así que no se pueden encadenar sin cooldown.
    Con el ítem Shot Pierce, los proyectiles pueden atravesar varios enemigos antes de desaparecer.
- Recepción de daño e invulnerabilidad:
    Tras recibir un golpe, el jugador tiene 0.5 segundos de invulnerabilidad. Si el golpe es fuerte, queda momentáneamente aturdido e incapaz de moverse.

Oleadas y progresión:
e divide en niveles de 10 oleadas cada uno.
- Cada oleada spawnea un grupo de enemigos fuera del campo de visión del jugador. Conforme avanza el juego, aumentan el número y la velocidad de aparición.
- Al completar las 10 oleadas de un nivel, se carga el siguiente nivel automáticamente. Las estadísticas del jugador y las monedas se conservan entre niveles.
- Si el jugador muere (vida ≤ 0), se muestra la pantalla de Game Over.

Tienda:
- La tienda aparece automáticamente cada 5 oleadas completadas (con un pequeño retardo). El juego se congela mientras está activa.
- Se muestran 3 ítems aleatorios que se pueden comprar con monedas.
- Si ningún ítem te convence, puedes hacer Reroll para cambiar la selección. El primer reroll es gratis; los siguientes tienen un coste creciente.
- Las mejoras se aplican inmediatamente al comprar.

Ítems disponibles:
- Health Potion: Recupera vida al instante.
- Max Health Up: Aumenta la vida máxima permanentemente.
- Attack Damage: Aumenta el daño de todos los ataques.
- Attack Speed: Aumenta la velocidad de ataque (% multiplicativo).
- Movement Speed: Aumenta la velocidad de movimiento (% multiplicativo).
- Attack Range: Amplía el alcance melee y la distancia de los proyectiles.
- Shot Speed: Aumenta la velocidad de los proyectiles.
- Critical Chance: Aumenta la probabilidad de golpe crítico.
- Critical Multiplier: Aumenta el multiplicador de daño en golpe crítico.
- Knockback: Incrementa el retroceso que provocan tus ataques.
- Shot Pierce: Los proyectiles atraviesan un enemigo adicional por nivel.
- Armour:Reduce un 20% el daño recibido (máx. 80%).

Monedas y drops:
- Al morir un enemigo suelta entre 3 y 8 monedas que salen disparadas con física de impulso; recógelas acercándote a ellas. Hay un 10% de probabilidad de que también suelte un corazón que recupera vida al tocarlo.

Enemigos:
- Enemigo Melee:
    Persigue al jugador usando pathfinding A*. Cuando se acerca lo suficiente, se detiene y lanza un ataque en arco. Es el tipo de enemigo más común.
- Enemigo Rápido (Fast Enemy):
    Versión más ágil del enemigo melee. Menor tamaño y mayor velocidad de ataque, pero menos vida. Peligroso en grupos.
- Enemigo a Distancia (Ranged Enemy):
    Persigue al jugador hasta entrar en rango y luego se detiene para disparar proyectiles. Mantén la distancia con cuidado o usa el swipe para redirigir sus disparos.
- Jefe (Boss):
    Enemigo de gran tamaño y mucha vida. Lento pero con golpes devastadores y fuerte knockback. Aparece en oleadas especiales.

Estadísticas del jugador:
Las mejoras de la tienda modifican estas estadísticas:
- MAX_HEALTH / HEALTH:Vida máxima y vida actual.
- MOVEMENT_SPEED: Velocidad de desplazamiento.
- ATTACK_DAMAGE: Daño base de todos los ataques.
- ATTACK_SPEED: Ataques por segundo.
- SHOT_SPEED: Velocidad de los proyectiles.
- ATTACK_RANGE: Alcance melee y distancia máxima de proyectiles.
- SWING_AMPLITUDE: Amplitud del arco de golpe melee.
- ATTACK_KNOCKBACK: Fuerza de retroceso aplicada a los enemigos.
- DEFENSE: Reducción aditiva de daño recibido.
- ARMOR: Reducción porcentual de daño recibido (máx. 80%).
- RIT_CHANCE: Probabilidad de golpe crítico (0.0 – 1.0).
- CRIT_DAMAGE_MULTI: Multiplicador de daño en crítico.
- SHOT_PIERCE: Enemigos adicionales que atraviesa el proyectil.
- SHOT_SPREAD: Dispersión de disparos (valores negativos = más precisión).

Menú de pausa:
- Pulsa Escape durante la partida para pausar el juego. Desde aquí puedes Reanudar, volver al Menú Principal o Salir del juego.
