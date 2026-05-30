import arcade
                    
import math
from entities.enemies.boss_enemy import BossEnemy
from world.systems.movement.movement_events import EntityMoveEvent
from pyglet.math import Vec2
from entities.player_entity import Player
from entities.enemies.base_enemy import BaseEnemy
from services.event_service import EventBus
from settings.registered_gameplay_events import EntityAttackedMeleeEvent, EntityAttackedRangedEvent, EntityDeadEvent, EntityDamagedEvent
from world.systems.base_system import BaseSystem
from entities.combat.projectile_entity import ProjectileEntity
from entities.combat.melee_swipe_entity import MeleeSwipeEntity
from world.systems.combat.entity_stats import StatDefinition
from world.systems.movement.movement_events import EntityMoveEvent
from world.systems.combat.damage_numbers import DamageNumber
import random


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
        self._hitboxes = self.scene.get_sprite_list("Hitboxes")
        self._hurtboxes = self.scene.get_sprite_list("Hurtboxes")
        
        self._damage_numbers = []

    def init(self):
        if self._initialized: return
        self.event_bus.subscribe(EntityAttackedMeleeEvent, self.on_entity_attacked_melee)
        self.event_bus.subscribe(EntityAttackedRangedEvent, self.on_entity_attacked_ranged)
        self._initialized = True

    def on_entity_attacked_melee(self, event: EntityAttackedMeleeEvent):
        if not self.scene: return
        swipe = MeleeSwipeEntity(event.attacker, event.attacker_pos, event.attack_dir, event.attack_range, event.amplitude, event.damage, event.knockback, event.life_time, event.offset_distance)
        self.scene.add_sprite("MeleeSwipes", swipe)
        self.scene.add_sprite("Hitboxes", swipe)

    def on_entity_attacked_ranged(self, event: EntityAttackedRangedEvent):
        if not self.scene: return
        projectile = ProjectileEntity(event.attacker, event.attacker_pos, event.attacker_velocity, event.attack_dir, event.speed, event.damage, event.knockback, event.pierce, event.max_distance)
        self.scene.add_sprite("Projectiles", projectile)
        self.scene.add_sprite("Hitboxes", projectile)

    def on_update(self, delta_time: float):
        if not self.scene: return
        
        # Proyectiles y swipes (mantienen su on_update propio)
        for proj in self._projectiles:
            proj.on_update(delta_time)
        
        for swipe in self._melee_swipes:
            swipe.on_update(delta_time)
            
        for pickup in self._pickups:
            pickup.on_update(delta_time, self.player, self._obstacles)
            if arcade.check_for_collision(pickup, self.player):
                pickup.apply_effect(self.player, self.event_bus)
                pickup.kill()
                
        self._check_parry_collisions()
        self._check_hitbox_collisions()
        
        for dn in self._damage_numbers[:]:
            dn.update(delta_time)
            if dn.timer >= dn.lifetime:
                self._damage_numbers.remove(dn)

    def draw(self):
        for dn in self._damage_numbers:
            dn.draw()

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
                        kb_dir = (Vec2(s1.attacker.center_x, s1.attacker.center_y) - Vec2(s2.attacker.center_x, s2.attacker.center_y)).normalize()
                        
                        from world.systems.movement.movement_events import EntityMoveEvent
                        
                        # Atacante 1 (Player)
                        speed1 = s1.attacker.stats.get(StatDefinition.MOVEMENT_SPEED) or 1.0
                        s1.attacker.invulnerable_timer = 0.5  # Stun
                        self.event_bus.dispatch(EntityMoveEvent(s1.attacker, kb_dir * ((128.0 * 0.15) / speed1)))
                        
                        # Atacante 2 (Enemy)
                        speed2 = s2.attacker.stats.get(StatDefinition.MOVEMENT_SPEED) or 1.0
                        s2.attacker.invulnerable_timer = 0.5  # Stun
                        self.event_bus.dispatch(EntityMoveEvent(s2.attacker, kb_dir * ((-128.0 * 0.15) / speed2)))
                        
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
                    proj.angle = math.degrees(math.atan2(-proj.direction.y, proj.direction.x))
                    proj.velocity_vec = proj.direction * (proj.speed * 1.5)
                    proj.attacker = self.player

    def _check_hitbox_collisions(self):
        for hitbox in self._hitboxes:
            if not hitbox.sprite_lists: continue
            
            # Si es un proyectil, destruirlo con obstaculos
            if isinstance(hitbox, ProjectileEntity):
                if arcade.check_for_collision_with_list(hitbox, self._obstacles):
                    hitbox.kill()
                    continue

            hits = arcade.check_for_collision_with_list(hitbox, self._hurtboxes)
            for hurtbox in hits:
                owner = hurtbox.owner
                
                # Evitar fuego amigo
                if (isinstance(hitbox.attacker, Player) and isinstance(owner, BaseEnemy)) or \
                   (isinstance(hitbox.attacker, BaseEnemy) and isinstance(owner, Player)):
                    
                    if owner not in hitbox.hit_entities:
                        if owner.invulnerable_timer <= 0:
                            hitbox.hit_entities.add(owner)
                            self._apply_damage_and_knockback(owner, hitbox.damage, hitbox.knockback, hitbox.attacker, hitbox)
                            
                            if isinstance(hitbox, ProjectileEntity):
                                if hitbox.pierce_count < hitbox.max_pierce:
                                    hitbox.pierce_count += 1
                                else:
                                    hitbox.kill()
                                    break

    def _apply_damage_and_knockback(self, target, damage, knockback, attacker, attack_entity):
        is_critical = False
        actual_damage = damage
        
        if isinstance(attacker, Player):
            crit_chance = attacker.stats.get(StatDefinition.CRIT_CHANCE) or 0.05
            crit_damage = attacker.stats.get(StatDefinition.CRIT_DAMAGE_MULTI) or 1.5
            if random.random() < crit_chance:
                actual_damage *= crit_damage
                is_critical = True

        # Apply armor (percentage reduction)
        armor = target.stats.get(StatDefinition.ARMOR) or 0.0
        # Cap armor at 80% to prevent invincibility
        armor = min(0.8, armor)
        damage_after_armor = actual_damage * (1.0 - armor)
        
        # Calculate damage reduction based on defense
        defense = target.stats.get(StatDefinition.DEFENSE) or 0.0
        final_damage = max(1.0, damage_after_armor - defense)

        # Damage
        target.stats.decrease(StatDefinition.HEALTH, final_damage)
        self.event_bus.dispatch(EntityDamagedEvent(target, final_damage))
        
        # Floating damage numbers
        if isinstance(attacker, Player) and isinstance(target, BaseEnemy):
            text_str = f"{int(final_damage)}"
            if is_critical:
                text_str += "!!"
            color = arcade.color.RED if is_critical else arcade.color.WHITE
            self._damage_numbers.append(DamageNumber(text_str, target.center_x, target.center_y + 30, color, is_critical))
        
        # Reset Iframes
        target.invulnerable_timer = 0.5
        
        # Knockback 
        if knockback > 0.0 and not isinstance(target, BossEnemy):
            kb_dir = (Vec2(target.center_x, target.center_y) - Vec2(attacker.center_x, attacker.center_y)).normalize()
            speed = target.stats.get(StatDefinition.MOVEMENT_SPEED) or 1.0
            fake_dir = kb_dir * ((knockback * 0.25) / speed)
            
            
            self.event_bus.dispatch(EntityMoveEvent(target, fake_dir))
            
        if target.stats.get(StatDefinition.HEALTH) <= 0:
            self.event_bus.dispatch(EntityDeadEvent(target))

    def dispose(self):
        self.event_bus.unsubscribe(EntityAttackedMeleeEvent, self.on_entity_attacked_melee)
        self.event_bus.unsubscribe(EntityAttackedRangedEvent, self.on_entity_attacked_ranged)