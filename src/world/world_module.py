from typing import Dict, Type, Set, List

import arcade
from arcade import Scene, PhysicsEngineSimple
from pip._internal.resolution.resolvelib import candidates

from entities.base_entity import BaseEntity
from entities.enemies.boss_enemy import BossEnemy
from entities.enemies.fast_enemy import FastEnemy
from entities.item_entity import ItemEntity
from services.event_service import EventBus, BaseEvent
from entities.player_entity import Player
from settings.game_resources import GameResources
from services.input.settings.registered_input_events import ToggleDebugInputEvent, ToggleShopInputEvent
from settings.registered_gameplay_events import RerollShopEvent, ToggleShopEvent, BuyItemEvent

from world.level.registered_levels import RegisteredLevels
from world.systems import shop_system
from world.systems.combat.combat_system import CombatSystem
from world.systems.base_system import BaseSystem
from world.systems.combat.entity_stats import StatDefinition, EntityStats
from world.systems.movement.movement_system import MovementSystem, MovementMode
from world.level.base_level import BaseLevel
from world.level.level_loader import LevelLoader
from world.level.level_events import LevelChangeRequestEvent, LevelChangedEvent

import json
import random
from settings.registered_gameplay_events import EntityDeadEvent, CoinCollectedEvent
from world.systems.shop_system import ShopInstance
from world.systems.enemy_wave_system import EnemyWaveSystem, WaveCompleteEvent, AllWavesCompleteEvent
from entities.enemies.melee_enemy import MeleeEnemy
from entities.enemies.ranged_enemy import RangedEnemy
from world.systems.wave_definition import WaveDefinition, EnemySpawnEntry


class World:

    SHOP_DELAY_SECONDS = 1.5

    def __init__(self, event_bus: EventBus):

        self.current_level: BaseLevel | None = None
        self.event_bus = event_bus

        self.scene: Scene | None = None
        self.player: Player | None = None
        self.physics: PhysicsEngineSimple | None = None

        self.entities: Set[BaseEntity] = set()
        self.systems: Dict[Type[BaseSystem], BaseSystem] = {}
        self.items : List[ItemEntity] = []
        self.coins : int = 0
        self.debug = False

        # --- Progresión de niveles ---
        self._level_sequence: List[BaseLevel] = [
            RegisteredLevels.CEMENTERY,
        ]
        self._current_level_index: int = 0

        self._completed_waves: int = 0
        self._shop_delay_timer: float = 0.0
        self._shop_delay_active: bool = False
        self._pending_level_change: bool = False

        self.init()

    def init(self):

        self._init_systems()
        self._subscribe_events()
        self.load_items()
        self.load_level(self._level_sequence[self._current_level_index])

    def _init_systems(self):

        movement_system = MovementSystem(self.event_bus)
        combat_system = CombatSystem(self.event_bus)
        wave_system     = EnemyWaveSystem(self.event_bus)

        self.systems[MovementSystem] = movement_system
        self.systems[CombatSystem] = combat_system
        self.systems[EnemyWaveSystem]  = wave_system

        for system in self.systems.values():
            system.init()

    def load_level(self, level: BaseLevel) -> None:

        saved_stats: EntityStats | None = None
        saved_coins = self.coins
        if self.player:
            saved_stats = self.player.stats

        if self.current_level:
            self._unload()

        self.current_level = level
        data = LevelLoader(level)

        self._init_scene(data)
        self._init_player(data)
        self._init_physics(data)
        self._init_pathfinding(data)
        self._init_wave_system(data)
        
        combat_system: CombatSystem = self.systems.get(CombatSystem)
        combat_system.setup(self.scene, self.player)

        if saved_stats is not None:
            self.player.stats = saved_stats
        self.coins = saved_coins

        # Resetear control de oleadas para el nuevo nivel
        self._completed_waves = 0
        self._shop_delay_timer = 0.0
        self._shop_delay_active = False
        self._pending_level_change = False

    def _unload(self) -> None:

        wave_system: EnemyWaveSystem = self.systems.get(EnemyWaveSystem)
        wave_system.dispose()

        movement_system: MovementSystem = self.systems.get(MovementSystem)
        for entity in self.entities:
            movement_system.remove_entity(entity)

        for entity in self.entities:
            entity.dispose()

        self.scene = None
        self.player = None
        self.physics = None

        self.entities.clear()

    def _init_scene(self, data: LevelLoader):

        ### TILEMAP ###

        self.scene = Scene.from_tilemap(data.tile_map)

        ### SCENE ###

        self.scene.add_sprite_list_after("player", "Floor")

        ### ENEMIGOS ###

        self.scene.add_sprite_list_after("Enemies", "Floor")
        
        ### COMBATE ###
        self.scene.add_sprite_list("Hurtboxes")
        self.scene.add_sprite_list("Hitboxes")
        self.scene.add_sprite_list("Projectiles")
        self.scene.add_sprite_list("MeleeSwipes")
        self.scene.add_sprite_list("Pickups")

    def _init_player(self, data: LevelLoader):

        player_spritesheet = arcade.load_spritesheet(GameResources.get("textures") / "entity" / "spritesheet_player.png")

        self.player = Player(self.event_bus, player_spritesheet, scale=0.3)
        self.player.position = data.player_start

        self.scene.add_sprite("player", self.player)
        self.scene.add_sprite("Hurtboxes", self.player.hurtbox)

        movement_system: MovementSystem = self.systems.get(MovementSystem)
        movement_system.add_entity(self.player, MovementMode.FLOOR)

        self.entities.add(self.player)

    def _init_physics(self, data: LevelLoader):
        walls = [self.scene[name] for name in data.collision_layers]
        self.physics = PhysicsEngineSimple(self.player, walls, )

    def _init_pathfinding(self, data: LevelLoader):
        self.barrier_list = data.barrier_list

    def _init_wave_system(self, data: LevelLoader):
        wave_system: EnemyWaveSystem = self.systems.get(EnemyWaveSystem)
        walls = [self.scene[name] for name in data.collision_layers]
        wave_system.setup(
            generator = self._generate_waves,
            player = self.player,
            scene = self.scene,
            movement_system = self.systems.get(MovementSystem),
            barrier_list = self.barrier_list,
            walls = walls,
            bounds = self.current_level.bounds
        )

    def _generate_waves(self, wave_number: int) -> WaveDefinition:
        cycle = (wave_number - 1) // 10
        phase_round = ((wave_number - 1) % 10) + 1
        enemy_level = cycle + 1
        
        # Estancamos el contador base en la ronda 5 para no reventar el juego
        round_type = min(phase_round, 5) 
        base_count = 3 + (round_type * 2)
        spawn_interval = max(0.4, 2.0 - (round_type * 0.15))
        
        total_melee_equivalent = base_count
        base_ranged_count = (base_count // 3) * 2
        total_enemies = total_melee_equivalent + base_ranged_count
        
        entries = []
        
        if phase_round == 10:
            # Boss round
            entries.append(EnemySpawnEntry(BossEnemy, 1, level=enemy_level))
            entries.append(EnemySpawnEntry(RangedEnemy, base_count // 4, level=enemy_level))
        elif phase_round <= 3:
            entries.append(EnemySpawnEntry(MeleeEnemy, total_melee_equivalent, level=enemy_level))
            entries.append(EnemySpawnEntry(RangedEnemy, base_ranged_count, level=enemy_level))
        elif phase_round <= 6:
            step = phase_round - 3
            fast_count = int(total_melee_equivalent * (step / 3.0))
            melee_count = total_melee_equivalent - fast_count
            
            if melee_count > 0:
                entries.append(EnemySpawnEntry(MeleeEnemy, melee_count, level=enemy_level))
            if fast_count > 0:
                advanced_fast = max(1, int(fast_count * 0.2)) if phase_round > 4 else 0
                normal_fast = fast_count - advanced_fast
                if normal_fast > 0:
                    entries.append(EnemySpawnEntry(FastEnemy, normal_fast, level=enemy_level))
                if advanced_fast > 0:
                    entries.append(EnemySpawnEntry(FastEnemy, advanced_fast, level=enemy_level + 1))
            entries.append(EnemySpawnEntry(RangedEnemy, base_ranged_count, level=enemy_level))
        else:
            step = phase_round - 6
            remaining_fast = int(total_melee_equivalent * (1.0 - (step / 3.0)))
            new_ranged_count = total_enemies - remaining_fast
            
            if remaining_fast > 0:
                entries.append(EnemySpawnEntry(FastEnemy, remaining_fast, level=enemy_level))
            if new_ranged_count > 0:
                advanced_ranged = max(1, int(new_ranged_count * 0.2)) if phase_round > 7 else 0
                normal_ranged = new_ranged_count - advanced_ranged
                if normal_ranged > 0:
                    entries.append(EnemySpawnEntry(RangedEnemy, normal_ranged, level=enemy_level))
                if advanced_ranged > 0:
                    entries.append(EnemySpawnEntry(RangedEnemy, advanced_ranged, level=enemy_level + 1))
            
        wave = WaveDefinition(entries=entries, spawn_interval=spawn_interval)
        wave.enemy_level = enemy_level 
        return wave

    def _subscribe_events(self):
        self.event_bus.subscribe(ToggleDebugInputEvent, self.toggle_debug)
        self.event_bus.subscribe(ToggleShopInputEvent, self.open_shop)
        self.event_bus.subscribe(RerollShopEvent, self.on_shop_reroll)
        self.event_bus.subscribe(BuyItemEvent,self.update_stats)
        self.event_bus.subscribe(WaveCompleteEvent, self._on_wave_complete)
        self.event_bus.subscribe(AllWavesCompleteEvent, self._on_all_waves_complete)
        self.event_bus.subscribe(LevelChangeRequestEvent, self._on_level_change_request)
        self.event_bus.subscribe(EntityDeadEvent, self._on_entity_dead)
        self.event_bus.subscribe(CoinCollectedEvent, self._on_coin_collected)

    def _unsubscribe_events(self):
        self.event_bus.unsubscribe(ToggleDebugInputEvent, self.toggle_debug)
        self.event_bus.unsubscribe(ToggleShopInputEvent, self.open_shop)
        self.event_bus.unsubscribe(RerollShopEvent, self.on_shop_reroll)
        self.event_bus.unsubscribe(BuyItemEvent,self.update_stats)
        self.event_bus.unsubscribe(WaveCompleteEvent, self._on_wave_complete)
        self.event_bus.unsubscribe(AllWavesCompleteEvent, self._on_all_waves_complete)
        self.event_bus.unsubscribe(LevelChangeRequestEvent, self._on_level_change_request)
        self.event_bus.unsubscribe(EntityDeadEvent, self._on_entity_dead)
        self.event_bus.unsubscribe(CoinCollectedEvent, self._on_coin_collected)


    def _on_wave_complete(self, _: WaveCompleteEvent):
        self._completed_waves += 1
        self._shop_delay_active = True
        self._shop_delay_timer = self.SHOP_DELAY_SECONDS

    def _on_all_waves_complete(self, _: AllWavesCompleteEvent):
        self._pending_level_change = True

    def _on_level_change_request(self, event: LevelChangeRequestEvent):
        self.load_level(event.next_level)
        self.event_bus.dispatch(LevelChangedEvent(event.next_level))

    def _on_coin_collected(self, event):
        self.coins += event.amount

    def _on_entity_dead(self, event):
        from entities.enemies.base_enemy import BaseEnemy
        if isinstance(event.entity, BaseEnemy):
            import random
            from pyglet.math import Vec2
            from entities.combat.pickup_entity import CoinPickupEntity, HeartPickupEntity
            

            num_coins = random.randint(3, 8)
            for _ in range(num_coins):
                vel = Vec2(random.uniform(-4, 4), random.uniform(2, 6))
                coin = CoinPickupEntity((event.entity.center_x, event.entity.center_y), vel)
                self.scene.add_sprite("Pickups", coin)
                

            if random.random() < 0.10:
                vel = Vec2(random.uniform(-3, 3), random.uniform(3, 7))
                heart = HeartPickupEntity((event.entity.center_x, event.entity.center_y), vel)
                self.scene.add_sprite("Pickups", heart)

    def _do_level_change(self):
        self._pending_level_change = False

        next_index = self._current_level_index + 1

        if next_index >= len(self._level_sequence):
            next_index = 0

        self._current_level_index = next_index
        next_level = self._level_sequence[next_index]

        self.event_bus.dispatch(LevelChangeRequestEvent(next_level))

    def _open_auto_shop(self):
        items = self.randomize_items()
        shop = ShopInstance(self.event_bus, items)
        self.event_bus.dispatch(ToggleShopEvent(shop))


    def update(self, delta_time: float):

        if self._shop_delay_active:
            self._shop_delay_timer -= delta_time
            if self._shop_delay_timer <= 0.0:
                self._shop_delay_active = False
                self._open_auto_shop()
                return

        if self._pending_level_change and not self._shop_delay_active:
            self._do_level_change()
            return  

        self.physics.update()
        # Las físicas de los enemigos ahora se encargan de su movimiento posicional
        self.player.update_animation()

        wave = self.systems.get(EnemyWaveSystem)
        for enemy in wave.get_active_enemies():
            enemy.update_animation(delta_time)

        for system in self.systems.values():
            system.update()
            system.on_update(delta_time)

        for enemy in self.scene["Enemies"]:  
            enemy.on_update(delta_time)
    def draw(self):

        self.scene.draw()
        
        combat_system: CombatSystem = self.systems.get(CombatSystem)
        if combat_system:
            combat_system.draw()

        if self.debug:
            self.scene.draw_hit_boxes(arcade.color.RED, 3)

    def get_level_bounds(self) -> arcade.Rect:
        return self.current_level.bounds

    def toggle_debug(self, _: ToggleDebugInputEvent):
        self.debug = not self.debug

    def dispose(self):

        self._unsubscribe_events()

        for entity in self.entities:
            entity.dispose()

        for system in self.systems.values():
            system.dispose()

    def load_items(self):
        list = json.load(open(GameResources.get("data") / "items.json"))
        for item in list:
            aux_item = ItemEntity(item["texture"],item["name"],item["description"],item["cost"],item["value"],item["stat"])
            self.items.append(aux_item)

    def randomize_items(self,used_items: list[ItemEntity] | None = None,count = 3) -> List[ItemEntity]:
        candidatos =[]
        if used_items is None: used_items = []

        for item in self.items:
            if item not in used_items:
                candidatos.append(item)
        final_count = min(count,len(candidatos))

        return random.sample(candidatos,final_count)

    def on_shop_reroll(self, event: RerollShopEvent):

        shop = event.shop
        if shop.current_reroll_cost <= self.coins:
            self.coins -= shop.current_reroll_cost
            shop.reroll()
            shop.load_new_items(self.randomize_items(shop.used_items))

    def open_shop(self, _: ToggleShopInputEvent):

        items = self.randomize_items()
        shop = ShopInstance(self.event_bus, items)

        self.event_bus.dispatch(ToggleShopEvent(shop))
        # Cambiar evento
    def update_stats(self, event: BuyItemEvent):
        price = event.item.cost
        if price <= self.coins:
            self.coins -= price
            self.player.stats.increase(EntityStats.resolve(event.item.stat), event.item.value)
            from settings.registered_gameplay_events import ItemBoughtSuccessEvent
            self.event_bus.dispatch(ItemBoughtSuccessEvent(event.item))
            self.event_bus.dispatch(ToggleShopEvent(event.shop))

        # El evento tendra: El item dodne sacamos la stat y el valor
        # mediante: self.player.stats.increase( LO QUE SEA)
