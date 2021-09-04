from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Item

"""
TODO : Add kwargs to Equippable for
    Item Level
    Dice Size
    Dize Number
    Traits
        - Traits to implement first
        - Finesse
        - Reach
        - Agile
    Runes
    Misc Modifiers
"""
class Equippable(BaseComponent):
    parent: Item

    def __init__(
        self,
        equipment_type: EquipmentType,
        **kwargs
    ):
        self.equipment_type = equipment_type

        self.item_level = kwargs.get("item_level",0)
        self.dice_size = kwargs.get("dice_size", 4)
        self.dice_number = kwargs.get("dice_number", 1)
        self.damage_type = kwargs.get("damage_type", "bludgeoning")


class Dagger(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, damage_type = "slashing")


class Sword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, dice_size = 6, damage_type = "slashing")


class LeatherArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, ac_bonus = 1)


class ChainMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, ac_bonus = 4)
