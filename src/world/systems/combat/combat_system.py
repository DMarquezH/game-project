import arcade
from pyglet.math import Vec2
from entities.player_entity import Player
from entities.enemies.base_enemy import BaseEnemy
from services.event_service import EventBus
from settings.registered_gameplay_events import EntityAttackedMeleeEvent, EntityAttackedRangedEvent, EntityDeadEvent
from world.systems.base_system import BaseSystem
from entities.combat.projectile_entity import ProjectileEntity
from entities.combat.melee_swipe_entity import MeleeSwipeEntity
from world.systems.combat.entity_stats import StatDefinition
from world.systems.movement.movement_events import EntityMoveEvent

class CombatSystem(BaseSystem):

    def __init__(self, event_bus: EventBus):
        super().__init__(event_bus)
        self.scene: arcade.Scene | None = None
        self.player: Player | None = None

    def setup(self, scene: arcade.Scene, player: Player):
        self.scene = scene
        self.player = player
        
        # Cacheamos las listas para no buscar en el diccionario cada frame (muy costoso)
        self._obstacles = self.scene.get_sprite_list("Obstacles")
        self._enemies = self.scene.get_sprite_list("Enemies")
        self._projectiles = self.scene.get_sprite_list("Projectiles")
        self._melee_swipes = self.scene.get_sprite_list("MeleeSwipes")
        self._pickups = self.scene.get_sprite_list("Pickups")

    def init(self):
        if self._initialized: return
        self.event_bus.subscribe(EntityAttackedMeleeEvent, self.on_entity_attacked_melee)
        self.event_bus.subscribe(EntityAttackedRangedEvent, self.on_entity_attacked_ranged)
        self._initialized = True

    def on_entity_attacked_melee(self, event: EntityAttackedMeleeEvent):
        if not self.scene: return
        swipe = MeleeSwipeEntity(event.attacker, event.attacker_pos, event.attack_dir, event.attack_range, event.amplitude, event.damage, event.knockback, event.life_time)
        self.scene.add_sprite("MeleeSwipes", swipe)

    def on_entity_attacked_ranged(self, event: EntityAttackedRangedEvent):
        if not self.scene: return
        projectile = ProjectileEntity(event.attacker, event.attacker_pos, event.attacker_velocity, event.attack_dir, event.speed, event.damage, event.knockback)
        self.scene.add_sprite("Projectiles", projectile)

    def on_update(self, delta_time: float):
        if not self.scene: return
        
        dt_scale = delta_time * 60

        # Proyectiles
        for proj in self._projectiles:
            proj.on_update(delta_time)
        
        # MeleeSwipes
        for swipe in self._melee_swipes:
            swipe.on_update(delta_time)
            
        for pickup in self._pickups:
            pickup.on_update(delta_time, self.player, self._obstacles)
            if arcade.check_for_collision(pickup, self.player):
                pickup.apply_effect(self.player, self.event_bus)
                pickup.kill()
            
        for enemy in self._enemies:
            if hasattr(enemy, "knockback_velocity") and enemy.knockback_velocity.length() > 0.1:
                if self._obstacles: # fokin colisiones tocapollas
                    enemy.center_x += enemy.knockback_velocity.x * dt_scale
                    if arcade.check_for_collision_with_list(enemy, self._obstacles):
                        enemy.center_x -= enemy.knockback_velocity.x * dt_scale
                        enemy.knockback_velocity = Vec2(0, enemy.knockback_velocity.y)
                        
                    enemy.center_y += enemy.knockback_velocity.y * dt_scale
                    if arcade.check_for_collision_with_list(enemy, self._obstacles):
                        enemy.center_y -= enemy.knockback_velocity.y * dt_scale
                        enemy.knockback_velocity = Vec2(enemy.knockback_velocity.x, 0)
                else:
                    enemy.center_x += enemy.knockback_velocity.x * dt_scale
                    enemy.center_y += enemy.knockback_velocity.y * dt_scale
                    
                enemy.knockback_velocity *= (0.8 ** dt_scale)
                
        # Process smooth knockback for player
        if hasattr(self.player, "knockback_velocity") and self.player.knockback_velocity.length() > 0.1:
            if self._obstacles:
                # Movemos en X y comprobamos
                self.player.center_x += self.player.knockback_velocity.x * dt_scale
                if arcade.check_for_collision_with_list(self.player, self._obstacles):
                    self.player.center_x -= self.player.knockback_velocity.x * dt_scale
                    self.player.knockback_velocity = Vec2(0, self.player.knockback_velocity.y)
                    
                # Movemos en Y y comprobamos
                self.player.center_y += self.player.knockback_velocity.y * dt_scale
                if arcade.check_for_collision_with_list(self.player, self._obstacles):
                    self.player.center_y -= self.player.knockback_velocity.y * dt_scale
                    self.player.knockback_velocity = Vec2(self.player.knockback_velocity.x, 0)
            else:
                self.player.center_x += self.player.knockback_velocity.x * dt_scale
                self.player.center_y += self.player.knockback_velocity.y * dt_scale
                
            self.player.knockback_velocity *= (0.8 ** dt_scale)
        
        self._check_parry_collisions()
        self._check_melee_collisions()
        self._check_projectile_collisions()

    def _check_parry_collisions(self):
        # Parry entre melés (Jugador vs Enemigo)
        for i, s1 in enumerate(self._melee_swipes):
            if not isinstance(s1.attacker, Player): continue
            for j in range(i + 1, len(self._melee_swipes)):
                s2 = self._melee_swipes[j]
                if not s1.sprite_lists or not s2.sprite_lists: continue
                
                # Si son de equipos diferentes (Player vs Enemy)
                if type(s1.attacker) != type(s2.attacker):
                    if arcade.check_for_collision(s1, s2):
                        # Ambos ataques colisionan: aplicar un leve knockback de parry a los atacantes
                        if hasattr(s1.attacker, "knockback_velocity") and hasattr(s2.attacker, "knockback_velocity"):
                            kb1 = (Vec2(s1.attacker.center_x, s1.attacker.center_y) - Vec2(s2.attacker.center_x, s2.attacker.center_y)).normalize()
                            s1.attacker.knockback_velocity = kb1 * (128.0 * 0.2)
                            s2.attacker.knockback_velocity = kb1 * (-128.0 * 0.2)
                        s1.kill()
                        s2.kill()
                        
        # 2. Melee (Player) vs Projectile (Redireccionar)
        for swipe in self._melee_swipes:
            if not swipe.sprite_lists or not isinstance(swipe.attacker, Player): continue
            
            hits = arcade.check_for_collision_with_list(swipe, self._projectiles)
            for proj in hits:
                if type(proj.attacker).__name__ != "Player":
                    # Redireccionar el proyectil y hacerlo del jugador
                    proj.direction = swipe.direction
                    import math
                    proj.angle = math.degrees(math.atan2(-proj.direction.y, proj.direction.x))
                    proj.velocity_vec = proj.direction * (proj.speed * 1.5)
                    proj.attacker = self.player

    def _check_melee_collisions(self):
        for swipe in self._melee_swipes:
            if not swipe.sprite_lists: continue
            
            if isinstance(swipe.attacker, Player):
                hits = arcade.check_for_collision_with_list(swipe, self._enemies)
                for hit in hits:
                    if hit not in swipe.hit_entities:
                        swipe.hit_entities.add(hit)
                        self._apply_damage_and_knockback(hit, swipe.damage, swipe.knockback, swipe.attacker, swipe)
            else:
                if arcade.check_for_collision(swipe, self.player):
                    if self.player not in swipe.hit_entities:
                        swipe.hit_entities.add(self.player)
                        self._apply_damage_and_knockback(self.player, swipe.damage, swipe.knockback, swipe.attacker, swipe)

    def _check_projectile_collisions(self):
        for proj in self._projectiles:
            if not proj.sprite_lists: continue
            
            # 1. Colision con Obstaculos
            if arcade.check_for_collision_with_list(proj, self._obstacles):
                proj.kill()
                continue
                
            # 2. Colisiones con Entidades
            if isinstance(proj.attacker, Player):
                hits = arcade.check_for_collision_with_list(proj, self._enemies)
                if hits:
                    hit = hits[0] # Solo afecta al primero a menos que perfore
                    self._apply_damage_and_knockback(hit, proj.damage, proj.knockback, proj.attacker, proj)
                    proj.kill()
            else:
                if arcade.check_for_collision(proj, self.player):
                    self._apply_damage_and_knockback(self.player, proj.damage, proj.knockback, proj.attacker, proj)
                    proj.kill()

    def _apply_damage_and_knockback(self, target, damage, knockback, attacker, attack_entity):
        # Damage
        target.stats.decrease(StatDefinition.HEALTH, damage)
        
        # Knockback Suave (decaying velocity)
        if knockback > 0.0:
            kb_dir = (Vec2(target.center_x, target.center_y) - Vec2(attacker.center_x, attacker.center_y)).normalize()
            if hasattr(target, "knockback_velocity"):
                target.knockback_velocity = kb_dir * (knockback * 0.2)
            
        if target.stats.get(StatDefinition.HEALTH) <= 0:
            self.event_bus.dispatch(EntityDeadEvent(target))

    def dispose(self):
        self.event_bus.unsubscribe(EntityAttackedMeleeEvent, self.on_entity_attacked_melee)
        self.event_bus.unsubscribe(EntityAttackedRangedEvent, self.on_entity_attacked_ranged)