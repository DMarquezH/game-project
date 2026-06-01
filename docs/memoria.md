# Memoria del proyecto de Tecnología de Videojuegos

### Grupo de Trabajo B

### Integrantes:

- Daniel Márquez (Jefe)
- Sergio Socas
- Italo Giuseppe
- Luis Miguel

## 1. Contexto

### 1.1 Introducción

El proyecto consiste en el desarrollo de un videojuego, usando el lenguaje python y la librería arcade, aplicando
los conceptos teóricos aprendidos en clase. El objetivo era implementar un juego funcional siguiendo las
especificaciones definidas en el GDD (Game Design Document) y aplicando buenas prácticas de desarrollo de software.

#### Información del videojuego desarrollado

- Nombre del videojuego: Corpse Brigade
- Género del juego: Survivor incremental
- Tecnologías usadas: Python + Arcade

### 1.2 Equipo y roles

Durante el desarrollo del proyecto, ha habido varios participantes con distintos roles en el grupo:

- Daniel Márquez:
  - Roles: Jefe de proyecto y Programación.
  - Tareas: Organización del trabajo, reparto de tareas y definición de la estructura base del proyecto.

- Sergio Socas:
  - Roles: Diseño gráfico y Programación.
  - Tareas: Diseño de texturas del juego y programación enfocada en UI y sprites.

- Italo Giuseppe:
  - Roles: Diseño de sonido y Programación.
  - Tareas: Diseño de pistas de sonido y música, y programación de mecánicas principales y enfocada en sonido.

- Luis Miguel:
  - Roles: Tester
  - Tareas: Documentación de pruebas de sistemas finalizados para la obtención de feedback y errores, y desarrollo
            de documentos.

### 1.3 Organización del trabajo

Para una buena coordinación y comunicación en el equipo de desarrollo, hemos utilizado una serie de herramientas
para facilitar la tarea.

Para el reparto de tareas, documentación de errores y planificación del proyecto, hemos utilizado los tickets de
GitHub, como se indicó en clase para el desarrollo del proyecto.

Para comunicación e interacción directa hemos decidido crear un grupo de WhatsApp. De esta forma ha sido posible
resolver dudas, extender información para la realización de tareas y paso de imágenes y vídeos de errores o
adiciones de mecánicas de juego.

El flujo de las tareas se ha basado en la creación de tickets de GitHub, como se ha explicado antes. Estos tickets
han sido asignados a un único integrante del grupo, de forma correspondiente. Es decir, que cada integrante ha
recibido tickets de contexto relacionado con sus roles. Al finalizar una tarea designada en un ticket, los
integrantes los han ido cerrando, de esta manera es posible llevar un seguimiento, como si de una lista de tareas
se tratase.

## 2. Contenido

### 2.1 Mecánicas principales previstas

El objetivo inicial del proyecto planteaba una experiencia centrada en la supervivencia frente a oleadas de
enemigos, incorporando elementos que permitiesen al jugador mejorar progresivamente a lo largo de cada partida.

Durante la fase de diseño se definieron como mecánicas principales el combate cuerpo a cuerpo y a distancia,
la progresión mediante estadísticas y mejoras, un sistema de tienda entre oleadas y diversos sistemas de apoyo,
entre ellos la recolección de recursos y la fabricación de objetos.

Como primer objetivo de desarrollo se definió un MVP (Minimum Viable Product) compuesto por el movimiento del
jugador, un sistema básico de combate, un enemigo funcional, estadísticas básicas y un escenario jugable.
A partir de esta base se pretendía ampliar progresivamente las funcionalidades previstas en el GDD.

### 2.2 Resultados finales

A lo largo del desarrollo se consiguió implementar la mayor parte de las mecánicas principales definidas en el
GDD. Sin embargo, algunas funcionalidades fueron simplificadas o descartadas para garantizar la finalización del
proyecto dentro del tiempo disponible.

#### Resúmen de cumplimiento
- Movimiento del jugador: completado
- Combate cuerpo a cuerpo: completado
- Combate a distancia: completado
- Parry de ataques enemigos: completado
- Sistema de estadísticas: completado
- Sistema de oleadas: completado
- Escalado de dificultad: completado
- Tienda de mejoras: completado
- Listado de objetos de mejora: simplificado a solo aumentos de estadística del personaje
- Pickups (monedas, corazones): completado
- Diferentes tipos e enemigos: completado
- Menú Principal: completado
- Game Over: completado
- Múltiples niveles: simplificado
- Sistema de subida de nivel: descartado
- Jefes finales de nivel: refactorizado a jefes cada 10 oleadas
- Sistema de construcción: descartado
- Sistema de recolección de recursos: descartado

Durante las primeras fases del proyecto se planteó un alcance más ambicioso que incluía sistemas de recolección
de recursos, construcción y una progresión más extensa entre distintos escenarios. Conforme avanzó el desarrollo,
se decidió reducir el alcance de estas características por carencias de tiempo y para centrar los esfuerzos en
las mecánicas principales del juego en consecuencia.

La versión final se enfoca en tres pilares fundamentales:
- Sistema de combate cuerpo a cuerpo y a distancia.
- Sistema de oleadas con dificultad creciente.
- Sistema de progresión mediante una tienda de mejoras aleatorias.

Asimismo, la progresión entre múltiples niveles fue simplificada a un único escenario principal con oleadas
infinitas, permitiendo dedicar más tiempo al equilibrio de las mecánicas.

Las funcionalidades eliminadas o simplificadas no fueron descartadas por problemas técnicos, sino principalmente
por limitaciones de tiempo. Se consideró prioritario completar correctamente las mecánicas principales antes
que incorporar sistemas secundarios que podrían haber quedado incompletos o insuficientemente integrados.

Esta decisión permitió finalizar una versión estable y plenamente jugable del proyecto, manteniendo la identidad
principal definida en el GDD original.

### 2.3 Funcionalidades Implementadas

La versión final del juego incluye un conjunto de mecánicas centradas en el combate, la supervivencia frente a
oleadas de enemigos y la progresión mediante mejoras de personaje.

#### Sistema de combate

El jugador dispone de dos métodos de ataque:
- Cuerpo a cuerpo: el jugador crea un área de daño enfrente suya que daña a los enemigos a los que alcanza.
- A distancia: el jugador dispara proyectiles que dañan a los enemigos.

Ambos tipos de ataque comparten una velocidad de ataque común y utilizan las estadísticas del jugador para
calcular daño, alcance y efectos adicionales.

Además, se implementaron mecánicas avanzadas como:
- Parry entre ataques cuerpo a cuerpo.
- Redirección de proyectiles enemigos mediante ataques melee.
- Aplicación de daño, retroceso (knockback) e invulnerabilidad temporal tras recibir impactos (solo para el jugador).

#### Sistema de enemigos

Se desarrollaron varios tipos de enemigos con comportamientos distintos:
- Enemigos con ataque cuerpo a cuerpo.
- Enemigos con ataque a distancia.
- Enemigos rápidos.
- Enemigo jefe.

Los enemigos utilizan navegación mediante búsqueda de caminos (A*), permitiéndoles desplazarse alrededor de
obstáculos para alcanzar al jugador.

#### Sistema de oleadas

La partida se organiza en oleadas sucesivas de enemigos.

Cada nueva oleada incrementa progresivamente la dificultad mediante el aumento de la cantidad de enemigos y la
mejora de sus estadísticas. El sistema permite una progresión indefinida, incrementando constantemente el
desafío para el jugador.

#### Sistema de progresión

Los enemigos derrotados generan monedas y, ocasionalmente, objetos de curación.

Las monedas obtenidas permiten adquirir mejoras permanentes durante la partida a través de la tienda.
Estas mejoras afectan directamente a las estadísticas del personaje, permitiendo crear distintas estrategias
de progresión.

#### Tienda de mejoras

Tras cada oleada se muestra una tienda con una selección aleatoria de 3 objetos de mejoras.

El jugador puede elegir una de las opciones disponibles utilizando las monedas acumuladas o realizar un reroll
para generar nuevas opciones. Las mejoras adquiridas se aplican inmediatamente sobre las estadísticas del personaje.
Tras adquirir un objeto, la tienda se cierra. Sin embargo, el jugador puede optar por pasar a la siguiente oleada
sin adquirir ningún objeto, permitiendo el ahorro de monedas para futuras tiendas.

#### Sistema de estadísticas

Tanto el jugador como los enemigos utilizan un sistema común de estadísticas que controla atributos como:
- Salud.
- Defensa.
- Daño.
- Velocidad de movimiento.
- Velocidad de ataque.
- Alcance de ataque.
- Probabilidad de crítico.
- Daño crítico (multiplicador de daño).
- Retroceso de ataque.

Este sistema permite modificar dinámicamente el comportamiento de las entidades durante la partida, además de
permitir el uso de distintas estrategias en cada partida.

#### Interfaz de usuario (UI)

Se desarrollaron distintas interfaces para facilitar la interacción con el juego:
- Menú principal.
- Menú de pausa.
- Pantalla de tienda.
- Pantalla de Game Over.
- HUD durante la partida con información sobre salud, monedas y progreso de las oleadas.

Estas interfaces proporcionan al jugador toda la información necesaria para tomar decisiones durante la partida.

#### Modo debug

Adicionalmente, se ha implementado un modo debug activable en partida con la tecla 'F3'. Este modo permite
visualizar las hitboxes de todos los elementos de la pantalla, facilitando la tarea de debugging.

### 2.4 Arquitectura del proyecto

Uno de los principales objetivos técnicos del proyecto fue desarrollar una arquitectura modular que facilitase
la ampliación del juego y redujese el acoplamiento entre los distintos sistemas. Para ello, se diseñó una
estructura basada en servicios, sistemas especializados y comunicación mediante eventos.

#### Arquitectura general

La aplicación se divide en varias capas con responsabilidades claramente diferenciadas:
- Views: encargadas de la presentación visual y de la interacción con el usuario.
- World: representa el estado global de la partida y actúa como contenedor de las entidades y sistemas activos.
- Sistemas: componentes especializados que implementan una funcionalidad concreta del juego.
- Infraestructura: conjunto de servicios compartidos utilizados por el resto de la aplicación.

Esta separación permite aislar la lógica de negocio de los aspectos gráficos y facilita la incorporación de
nuevas funcionalidades sin afectar al resto del proyecto.

#### Infraestructura y servicios

La infraestructura del proyecto se basa en varios servicios centrales:

##### Contenedor de servicios

Se implementó un contenedor de servicios responsable de la creación y distribución de dependencias entre los
distintos componentes de la aplicación.

Este enfoque reduce el acoplamiento entre clases y simplifica la construcción de objetos complejos.

##### Bus de eventos

La comunicación entre gran parte de los sistemas se realiza mediante un bus de eventos.

Los distintos componentes pueden publicar eventos o suscribirse a ellos sin necesidad de conocer directamente
qué otros componentes participan en la operación.

Este mecanismo se utiliza extensivamente en acciones como:
- Input de usuario.
- Combate.
- Movimiento de entidades.
- Reproducción de sonidos.
- Eventos de juego.

Gracias a este enfoque, los sistemas permanecen desacoplados y resulta sencillo añadir nuevas reacciones
a eventos existentes.

##### Gestor de recursos

Se desarrolló un servicio encargado de la carga e inicialización de recursos compartidos como:
- Texturas
- Sonidos
- Fuentes
- Mapas
- Objetos

De esta forma se centraliza la gestión de recursos y se evita la duplicación de cargas durante la ejecución.

##### Navegación entre vistas

La transición entre pantallas del juego se realiza mediante un servicio específico de navegación.

Este servicio abstrae la creación de vistas y permite resolver automáticamente sus dependencias utilizando
el contenedor de servicios.

##### Servicio de entrada (Input Service)

El sistema de entrada fue diseñado para desacoplar los dispositivos físicos de las acciones del juego.

El flujo de procesamiento es el siguiente:
1) La vista recibe la entrada bruta del usuario.
2) La entrada se transforma en un modelo de entrada común.
3) El servicio de entrada procesa dicha información.
4) Se evalúan los bindings configurados para el contexto activo.
5) Se generan las acciones correspondientes.
6) Las acciones producen eventos que son enviados al bus de eventos.

Además, se implementó un sistema de contextos de entrada que permite activar distintos conjuntos de bindings
dependiendo del estado del juego (partida, menús, tienda, etc.).

Este diseño simplifica la gestión de controles y facilita futuras ampliaciones o cambios de configuración.

Nota para el profesor: Se recomienda la inspección del código del servicio de inputs (.../src/services/input/),
pues considero que es una pieza muy pulida y destacable de nuestro proyecto, que ha llevado algo de tiempo
perfeccionar para un uso sencillo y práctico. En el mismo directorio de los documentos del proyecto se incluye
uno de guía para el servicio de inputs que yo mismo redacté para mis compañeros de grupo.

##### Organización de la lógica de juego

La lógica principal de la partida se encuentra separada de la representación visual.

La vista principal se encarga únicamente de:
- Renderizar los elementos del juego.
- Capturar entradas del usuario.
- Coordinar la actualización visual.
- Gestionar UIs.

La clase World representa el estado de la partida y contiene:
- Entidades activas.
- Sistemas en funcionamiento.
- Datos globales del juego.

Actúa como punto central de coordinación de la lógica de juego.

##### Sistemas especializados

Las distintas mecánicas se implementan mediante sistemas independientes registrados en World.

Algunos ejemplos son:
- Sistema de movimiento
- Sistema de combate
- Sistema de oleadas
- Sistema de estadísticas
- Sistema de generación de enemigos

Cada sistema es responsable exclusivamente de su área funcional, favoreciendo la separación de responsabilidades
y la reutilización de código.

##### Modelo de entidades

Las entidades del juego siguen una jerarquía de herencia basada en una entidad base común.

A partir de esta entidad se derivan las distintas especializaciones: Player, Enemigos, Proyectiles, Pickups, entre
otros.

La entidad base proporciona funcionalidades compartidas mientras que las clases derivadas implementan el
comportamiento específico de cada tipo de objeto.

##### Ventajas de la arquitectura

Las principales ventajas de esta arquitectura han sido:
- Reducción del acoplamiento entre componentes.
- Mayor facilidad para añadir nuevas mecánicas.
- Reutilización de código entre entidades y sistemas.
- Separación clara entre lógica y presentación.
- Mayor mantenibilidad del proyecto.
- Facilidad para realizar pruebas y depuración.

La utilización intensiva del bus de eventos y de servicios compartidos ha permitido mantener una estructura
flexible incluso a medida que aumentaba la complejidad del proyecto.

Como conclusión opino que aunque diseñar una base sólida y escalable puede requerir de más tiempo (a veces mucho más),
merece mucho la pena en el futuro si dicha base se ha diseñado bien, pues permite que el flujo de trabajo se
acelere considerablemente.