from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item


player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(weapon = equippable.Dagger(), armor = equippable.LeatherArmor()),
    fighter=Fighter(
        hp=30, # # TODO:  Setup HP in pf2e way
        strength=18, constitution=14, dexterity=14, wisdom=12, intelligence=10,charisma=10),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=1000),
)

orc = Actor(
    char="o",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(weapon = equippable.Sword()),
    fighter=Fighter(hp=10,
        strength=16, constitution=16, dexterity=14, wisdom=12, intelligence= 8,charisma=10
        ),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)
goblin_pyro = Actor(
    char="G",
    color=(0, 127, 0),
    name="Goblin Pyro",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16,
                    strength=10, dexterity=18, constitution=14, wisdom=8, intelligence=10, charisma=16
                    ),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)

confusion_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
fireball_scroll = Item(
    char="~",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)
health_potion = Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)
lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

dagger = Item(
    char="/", color=(0, 191, 255), name="Dagger", equippable=equippable.Dagger()
)

sword = Item(char="/", color=(0, 191, 255), name="Sword", equippable=equippable.Sword())

leather_armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Leather Armor",
    equippable=equippable.LeatherArmor(),
)

chain_mail = Item(
    char="[", color=(139, 69, 19), name="Chain Mail", equippable=equippable.ChainMail()
)
