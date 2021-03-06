from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

import color
import exceptions
from dice import Dice

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item


class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""

    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if actor_location_x == item.x and actor_location_y == item.y:
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("Your inventory is full.")

                self.engine.game_map.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.items.append(item)

                self.engine.message_log.add_message(f"You picked up the {item.name}!")
                return

        raise exceptions.Impossible("There is nothing here to pick up.")


class ItemAction(Action):
    def __init__(
        self, entity: Actor, item: Item, target_xy: Optional[Tuple[int, int]] = None
    ):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        """Invoke the items ability, this action will be given to provide context."""
        if self.item.consumable:
            self.item.consumable.activate(self)


class DropItem(ItemAction):
    def perform(self) -> None:
        if self.entity.equipment.item_is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item)

        self.entity.inventory.drop(self.item)


class EquipAction(Action):
    def __init__(self, entity: Actor, item: Item):
        super().__init__(entity)

        self.item = item

    def perform(self) -> None:
        self.entity.equipment.toggle_equip(self.item)

5628
class WaitAction(Action):
    def perform(self) -> None:
        pass


class TakeStairsAction(Action):
    def perform(self) -> None:
        """
        Take the stairs, if any exist at the entity's location.
        """
        if (self.entity.x, self.entity.y) == self.engine.game_map.downstairs_location:
            self.engine.game_world.generate_floor()
            self.engine.message_log.add_message(
                "You descend the staircase.", color.descend
            )
        else:
            raise exceptions.Impossible("There are no stairs here.")


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack.")

        #Convereting the default melee action to a PF2E attack roll
        #damage = self.entity.fighter.power - target.fighter.defense

        attack_roll = Dice.roll(1,20, self.entity.fighter.strength_mod)
        hits = (attack_roll >= target.fighter.ac)

        if (hits):
            #TODO : Make the attack and damage rolls be handed to this function by the weapon itself, with a default for fists (shown here)
            damage = Dice.roll(self.entity.equipment.weapon.dice_number,
                               self.entity.equipment.weapon.dice_size,
                               self.entity.fighter.strength_mod)
        else:
            damage = 0

        attack_desc = f"{self.entity.name.capitalize()} attempts to attack {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk

        if (hits) :
            self.engine.message_log.add_message(
                f"{attack_desc} and hits! ({attack_roll} vs. AC{target.fighter.ac})", attack_color
                )
        else:
            self.engine.message_log.add_message(
                f"{attack_desc} and misses. ({attack_roll} vs. AC{target.fighter.ac})", attack_color
                )

        if damage > 0 and hits :
            if self.entity.name == "Player":
                self.engine.message_log.add_message(
                    f"{self.entity.name.capitalize()} deals {damage} {self.entity.equipment.weapon.equippable.damage_type} damage.", attack_color
                )
            else :
                self.engine.message_log.add_message(
                    f"{self.entity.name.capitalize()} deals {damage} {self.entity.equipment.weapon.damage_type} damage.", attack_color
                )
            target.fighter.hp -= damage
        else :
            if damage == 0 and hits :
                self.engine.message_log.add_message(
                    f"However, they deal no damage.", attack_color
                )


# TODO: Add Move Speed
"""
    Ideas for implementation :
        - Popup message after moving a number of squares away from starting pos, then ask to confirm action?
        - Reverse of that idea, asking if they'd like to commit to moving, then give them the alloted # of squres?
        - Mouse click being movement, shows line of certain color up to move speed, then changes color to represent range?
"""
class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # Destination is out of bounds.
            raise exceptions.Impossible("That way is blocked.")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination is blocked by a tile.
            raise exceptions.Impossible("That way is blocked.")
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            # Destination is blocked by an entity.
            raise exceptions.Impossible("That way is blocked.")

        self.entity.fighter.actions_remaining -= 1
        self.engine.message_log.add_message(f"{self.entity.name} has {self.entity.fighter.actions_remaining} actions remaining.")

        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
