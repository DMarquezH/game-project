# Documentación del servicio de inputs (InputService) #

El servicio de inputs tiene un funcionamiento algo complejo. Pero de forma resumida,
se define el flujo de un input desde que se recibe hasta que llega a una acción de
juego como puede ser, por ejemplo: <b>player_attack, player_move, toggle_pause, etc</b>.

## Funcionamiento básico ##

El servicio de inputs funciona junto al bus de eventos, para una comunicación desacoplada.
De esta forma, no es necesario que tanto las clases View como los listeners (player, pause_menu, etc)
conozcan el funcionamiento del servicio. Solo tienen que notificar al servicio, o reaccionar a él.

### Flujo del servicio ###

Input Físico (raw input) → View → GameInput (normalización/mapping) → InputService → Acción (se resuelve con bindings) → Event Bus → Listener (player, pause_menu, etc)

1) El input físico es emitido por el usuario
2) El input es capturado por arcade, a través de una View
3) La View normaliza el input usando una clase de utilidad del servicio
4) La View envia el input al servicio
5) El servicio busca un binding relacionado con el input
6) Se resuelve una acción a partir del binding
7) La acción se activa y emite un evento de input a través del bus de eventos
8) Un listener reacciona al evento, que contiene información del input

### Contextos de Input ###

Los contextos de input son contenedores de bindings. Para que un binding pueda ser resuelto por el servicio,
este debe estar registrado en un contexto, y este debe ser activado. Puede haber múltiples contextos activos
simultáneamente.

Por ejemplo: Si creamos una acción (player_attack), necesitamos asignarle un binding, y registrarlo en un
contexto de input (por ejemplo: gameplay). Una vez hecho esto, activamos el contexto, y entonces el servicio
podrá resolver todos los bindings contenidos en el contexto.

De esta forma, si tenemos asignadas las teclas WASD para mover al jugador, y al mismo tiempo para navegar por
el menú de pausa, podemos evitar un conflicto de acciones activando un contexto u otro (o incluso los dos).
Es decir, si activamos el contexto "pause", WASD activarán la acción "navigate_menu", pero si activamos el
contexto "gameplay", WASD entonces activará "move_player".

## Componentes para usar el servicio ##

Los módulos que se van a modificar/extender para usar el servicio son:

- registered_input_events.py
- registered_input_actions.py
- registered_input_bindings.py
- registered_input_contexts.py
- 
Todos contenidos en: <b>src/services/input/settings/</b>

También va a usarse funcionalidad de clases ubicadas en: <b>src/services/input/devices/</b>

- keyboard_device.py
- mouse_device.py
- gamepad_device.py

Estas clases contienen métodos de utilidad para definir componentes más adelante.

## Ejemplo 1: Toggle Pause ##

Esta acción se basa en activar/desactivar el menú de pausa, dentro de la partida.

Para poder implementar esta acción usando el servicio de inputs, tenemos que crear varias cosas:

- Un evento que se dispare cuando un input (tecla ESC) active la acción
- Una acción que dispare el evento
- Un binding para asignar un input a la acción (en este caso la tecla ESC)
- Un contexto que aloje el binding

### Paso 1: Evento ###

Creamos un nuevo evento llamado "TogglePauseInputEvent" en <b>registered_input_events.py</b>.

Nota: Es recomendable que el nombre acabe en ...InputEvent.

```python
class TogglePauseInputEvent(BaseEvent):
    pass
```

En este caso, el evento no necesita transmitir ningún dato, solo notificar cuando se activa la acción.

### Paso 2: Acción ###

Creamos una acción llamada "TogglePauseInputAction", que llame al evento en <b>registered_input_actions.py</b>.

Nota: Es recomendable que el nombre acabe en ...InputAction.

```python
class TogglePauseInputAction(InputAction):

    def activate(self, event_bus: EventBus, input_value: EmptyInput):
        event_bus.dispatch(TogglePauseInputEvent())
```

input_value contiene el valor del input físico recibido. Sin embargo, en este caso no es necesario
usarlo para nada, por lo que simplemente emitimos el evento usando el bus de eventos.

Nota: activate(event_bus, input_value) es un metodo heredado de InputAction.

### Paso 3: Binding ###

Creamos un binding para asignar un input a la acción (en este caso la tecla ESC),
en <b>registered_input_bindings.py</b>. En este caso los bindings son instancias, por lo que simplemente
declaramos una constante para el binding.

```python
TOGGLE_PAUSE = SimpleInputBinding(
        KeyboardInputDevice.signature_from_key(
            arcade.key.ESCAPE
        ),
        TogglePauseInputAction(),
        InputTrigger.PRESS
    )
```

Usaremos un binding simple (1 único input), el cual nos pide 3 parametros:

- El id o firma (signature) del input: un objeto que identifica de forma única al input
- La acción que será activada cuando el binding detecte el input
- El tipo de recepción del input: "PRESS" hace que la acción se active la primera vez que se recibe el input (nada más plusar la tecla ESC)

La firma (signature) de un input es un string compuesto asi: "<device>.<source>"

Ejemplo: "keyboard.key.119" → Tecla W del teclado

Para poder obtener esta firma, podemos usar la clase KeyboardInputDevice, que contiene un método para construir
la firma a partir de una tecla de arcade.

### Paso 4: Contexto ###

Ahora tenemos que registrar el binding en un contexto. En este caso será "PAUSE". Para ello vamos al módulo
<b>registered_input_contexts.py</b>

```python
GAMEPLAY = InputContext("gameplay")
PAUSE = InputContext("pause")

@staticmethod
    def init():
        RegisteredInputContexts.GAMEPLAY.bind(RegisteredInputBindings.TOGGLE_PAUSE)
        RegisteredInputContexts.PAUSE.bind(RegisteredInputBindings.TOGGLE_PAUSE)
```

Como se puede ver en el fragmento de código, definimos el contexto "PAUSE", así como el contexto "GAMEPLAY",
para poder pausar desde la partida, y en el método init, registramos el binding que hemos creado en ambos contextos.

De esta forma, cuando activemos uno de los dos contextos, el servicio tendrá en cuenta nuestro binding.

### Paso 5: activar/desactivar el contexto ###

Para que el servicio pueda tener en cuenta nuestro binding, hay que activar uno de los contextos donde esté
registrado. En este caso: "PAUSE" o "GAMEPLAY"

```python
class GameView(BaseView):

    def on_show_view(self):
        # Activamos el contexto "GAMEPLAY" cuando la vista se muestre
        self.input_service.enable_context(RegisteredInputContexts.GAMEPLAY)

    def on_hide_view(self):
        # Desactivamos el contexto "GAMEPLAY" cuando la vista se descarte
        self.input_service.disable_context(RegisteredInputContexts.GAMEPLAY)

    def pause(self):
        
        # Al pausar, activamos el contexto "PAUSE" y desactivamos "GAMEPLAY"
        
        self.input_service.enable_context(RegisteredInputContexts.PAUSE)
        self.input_service.disable_context(RegisteredInputContexts.GAMEPLAY)

        self.pause_menu.enable()

    def unpause(self):
        
        # Al salir de la pausa, activamos el contexto "GAMEPLAY" y desactivamos "PAUSE"

        self.input_service.enable_context(RegisteredInputContexts.GAMEPLAY)
        self.input_service.disable_context(RegisteredInputContexts.PAUSE)

        self.pause_menu.disable()
```

### Paso 6: Suscribir listeners al evento ###

Por último, vamos a suscribir un listener al evento para que pueda reaccionar cuando la acción "TogglePause"
se active.

```python
class GameView(BaseView):

    def __init__(self, input_service: InputService, event_bus: EventBus, nav_service: NavigationService):
        super().__init__(input_service)
        
        # Llamamos al método para suscribir listeners
        self.subscribe_listeners()

    def subscribe_listeners(self):
        # Suscribimos el método on_toggle_pause() al evento TogglePauseInputEvent.
        # Nota: Se pasa el TIPO del evento, no la instancia.
        self.event_bus.subscribe(TogglePauseInputEvent, self.on_toggle_pause)

    def on_toggle_pause(self, _: TogglePauseInputEvent):

        # Este es el método listener, que recibe el evento (en este caso se ignora, pues no se usa), que será
        # llamado cuando se active la acción "TogglePause"
        # Recordemos que la acción "TogglePause" emite el evento TogglePauseInputEvent.
        
        if self.pause_menu.is_enabled():
            self.unpause()
        else:
            self.pause()
```

Al ejecutar el juego y navegar a la GameView, si pulsamos la tecla ESC se abrirá el menú de pausa.
En el menú de pausa, si pulsamos la tecla ESC, volveremos a la partida.