# Taair
# Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
# See LICENSE file for details.
from copy import deepcopy
from typing import Optional

import attr
import hikari
import miru
import miru.view

from .database import Database
from .database import OnlineRoleLifeStory
from .database import OnlineRoleUnit
from .database import Unit
from .database import UnitModel
from .icons import RARITY_ICON
from .icons import UNIT_GENDER_ICON
from .icons import UNIT_PROFESSION_ICON
from .icons import UNITS_CATEGORY_ICON
from .utils import DUMMY_SKILL
from .utils import clean_name
from .utils import format_skill_desc

UNITNAMES: list[str] = []


@attr.define(frozen=True, slots=True)
class UnitEntry:
    role: OnlineRoleUnit
    unit: Unit
    model: UnitModel
    story: Optional[OnlineRoleLifeStory]


UNITS: dict[str, UnitEntry] = {}


def reinit_unit_dbs() -> None:
    database = Database.get_instance()

    stories_role = {story.idonline_role: story for story in database.online_role_life_story.values()}

    for role in database.online_role_unit.values():
        if not role.enable or role.idunit not in database.unit:
            continue

        unit = database.unit[role.idunit]
        model = database.unit_model[unit.unit_model_id]
        story = stories_role.get(role.idonline_role, None)

        # clean unit name
        name = clean_name(unit.name)
        if not name:
            continue
        if name in UNITNAMES:
            name = f"{name} ({unit.id})"
        UNITNAMES.append(name)
        UNITS[name] = UnitEntry(role, unit, model, story)


HEAD_ICON_URL = "https://media.githubusercontent.com/media/Miners-of-Convallaria/wiki/master/images/icon/character_head/character_head_{}.webp"
CHARACTER_IMAGE_URL = "https://media.githubusercontent.com/media/Miners-of-Convallaria/wiki/master/images/icon/character/character_{}.webp"
CHARACTER_CARD_URL = (
    "https://media.githubusercontent.com/media/Miners-of-Convallaria/wiki/master/images/icon/card_full/card_{}.webp"
)
CHARACTER_SKIN_CARD_URL = (
    "https://media.githubusercontent.com/media/Miners-of-Convallaria/wiki/master/images/icon/skin_card_full/{}.webp"
)


class UnitView(miru.View):
    key: str
    role: OnlineRoleUnit
    unit: Unit
    model: UnitModel
    story: Optional[OnlineRoleLifeStory]
    _base_embed = None

    def __init__(self, key: str) -> None:
        super().__init__()
        self.key = key
        match = UNITS[key]
        self.role = match.role
        self.unit = match.unit
        self.model = match.model
        self.story = match.story
        self.check_buttons()

    @staticmethod
    def reinit_database() -> None:
        reinit_unit_dbs()

    def check_buttons(self) -> None:
        if len(self.unit.m_unit_skins) == 2:
            return

        button_map = {child.label: child for child in self.children if isinstance(child, miru.Button)}

        match len(self.unit.m_unit_skins):
            case 0:
                button_map["Ascension"].disabled = True
                button_map["Skin"].disabled = True
            case 1:
                button_map["Skin"].disabled = True
            case _:
                print("Unit with more than one skin!", self.unit.id)

        button_map["Story"].disabled = self.story is None

    @staticmethod
    def autocomplete(value: str, limit: int = 25) -> list[str]:
        result = [""] * limit
        j = 0
        for name in UNITNAMES:
            if value.lower() in name.lower():
                result[j] = name
                j += 1
                if j >= limit:
                    break
        return result[:j]

    @miru.button(label="Main", style=hikari.ButtonStyle.PRIMARY, emoji="📋")
    async def button_main_callback(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        print("Button clicked!")
        embed = self.get_main()
        await ctx.edit_response(embed=embed, components=self)

    @miru.button(
        label="Ascension",
        style=hikari.ButtonStyle.SUCCESS,
        emoji="🌟",
    )
    async def button_ascension_callback(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        print("Button clicked!")
        embed = self.get_skin(num=0)
        await ctx.edit_response(embed=embed, components=self)

    @miru.button(label="Skin", style=hikari.ButtonStyle.SUCCESS, emoji="🎨")
    async def button_skin_callback(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        print("Button clicked!")
        embed = self.get_skin(num=1)
        await ctx.edit_response(embed=embed, components=self)

    @miru.button(label="Story", style=hikari.ButtonStyle.SECONDARY, emoji="📖")
    async def button_story_callback(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        print("Button clicked!")
        embed = self.get_story()
        await ctx.edit_response(embed=embed, components=self)

    @miru.button(label="Skills L", style=hikari.ButtonStyle.DANGER, emoji="⚡")
    async def button_skills1_callback(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        print("Button clicked!")
        embed = self.get_skils(1)
        await ctx.edit_response(embed=embed, components=self)

    @miru.button(label="Skills R", style=hikari.ButtonStyle.DANGER, emoji="⚡")
    async def button_skills2_callback(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        print("Button clicked!")
        embed = self.get_skils(2)
        await ctx.edit_response(embed=embed, components=self)

    def get_base_embed(self) -> hikari.Embed:
        if self._base_embed:
            return deepcopy(self._base_embed)

        database = Database.get_instance()

        role = self.role
        unit = self.unit

        icon_id = self.unit.icon or self.model.icon
        faction = database.faction.get(unit.faction, None)

        color = None
        title = f"{RARITY_ICON[role.rarity]} {clean_name(unit.name)}"
        if faction:
            title += f" ({faction.name})"
            if world_map_color := database.world_map_color.get(faction.line_color, None):
                color = hikari.Colour.from_rgb(
                    world_map_color.r,
                    world_map_color.g,
                    world_map_color.b,
                )
            elif faction.bg_color:
                color = hikari.Colour(int(faction.bg_color.split("|")[0], 16))

        self._base_embed = hikari.Embed(
            title=title,
            color=color,
        )

        self._base_embed.set_author(
            name=self.key,
            icon=HEAD_ICON_URL.format(icon_id),
        )
        self._base_embed.set_thumbnail(CHARACTER_IMAGE_URL.format(icon_id))
        return deepcopy(self._base_embed)

    def get_main(self) -> hikari.Embed:
        database = Database.get_instance()

        unit = self.unit

        icon_id = self.unit.icon or self.model.icon
        profession = database.profession[unit.profession]
        try:
            personality = database.unit_personality[unit.personality_id]
            trait = database.skill[database.unit_personality_skill[personality.m_unit_personality_skills[-1]].skill_id]
        except KeyError:
            trait = DUMMY_SKILL

        weapons = [
            database.weapon_type[int(weapon_id)].name
            for weapon_id in unit.weapon_type_ids.split("|")
            if weapon_id not in ["1", "2"]
        ]

        embed = self.get_base_embed()
        embed.set_image(CHARACTER_CARD_URL.format(icon_id))
        embed._fields = [
            hikari.EmbedField(
                name="Profession",
                value=f"{UNIT_PROFESSION_ICON[profession.category]} {profession.name}",
                inline=False,
            ),
            hikari.EmbedField(
                name="Categories",
                value="".join(UNITS_CATEGORY_ICON[int(category)] for category in unit.unit_tag_ids.split("|"))
                + UNIT_GENDER_ICON[unit.gender],
                inline=True,
            ),
            hikari.EmbedField(
                name="Weapon(s)",
                value=", ".join(weapons) if weapons else "/",
                inline=True,
            ),
            # TODO: remove when stats done
            hikari.EmbedField(
                name="Move",
                value=f"{unit.mobility} - {database.move_type[unit.move_type].type}",
                inline=True,
            ),
            hikari.EmbedField(name="Jump", value=f"⇑ {unit.jump_up} / ⇓ {unit.jump_down}", inline=True),
            hikari.EmbedField(name="SPD", value=f"{unit.speed}", inline=True),
            # /end
            hikari.EmbedField(
                name=f"Trait - {trait.name}",
                value=format_skill_desc(trait.desc),
                inline=False,
            ),
        ]

        return embed

    def get_skin(self, num: int) -> hikari.Embed:
        database = Database.get_instance()

        skin = database.unit_skin[self.unit.m_unit_skins[num]]
        model = self.model
        embed = self.get_base_embed()
        if skin.idunit_model != 0 and skin.idunit_model != model.id:
            model = database.unit_model[skin.idunit_model]
            icon_id = skin.icon or model.icon
            embed.set_author(
                name=self.key,
                icon=HEAD_ICON_URL.format(icon_id),
            )
            embed.set_thumbnail(CHARACTER_IMAGE_URL.format(icon_id))

        if skin.icon_card:
            embed.set_image(CHARACTER_SKIN_CARD_URL.format(skin.icon_card))

        return embed

    def get_story(self) -> hikari.Embed:
        embed = self.get_base_embed()
        content = self.story.content if self.story else "/"
        embed.description = f"**Story**\n{content}"
        return embed

    def get_stats(self) -> hikari.Embed:
        database = Database.get_instance()

        unit = self.unit

        embed = self.get_base_embed()
        embed._fields = [
            hikari.EmbedField(
                name="Move",
                value=f"{unit.mobility} - {database.move_type[unit.move_type].type}",
                inline=True,
            ),
            hikari.EmbedField(name="Jump", value=f"⇑ {unit.jump_up} / ⇓ {unit.jump_down}", inline=True),
            # hikari.EmbedField("P.ATK", RARITY_ICON[unit.physic_attack_rarity], True),
            # hikari.EmbedField("M.ATK", RARITY_ICON[unit.spell_attack_rarity], True),
            # hikari.EmbedField("P.DEF", RARITY_ICON[unit.physic_defence_rarity], True),
            # hikari.EmbedField("M.DEF", RARITY_ICON[unit.spell_defence_rarity], True),
            # hikari.EmbedField("Max HP", RARITY_ICON[unit.hp_rarity], True),
            # hikari.EmbedField("SPD", RARITY_ICON[unit.speed_rarity], True),
        ]

        return embed

    def get_skils(self, num: int) -> hikari.Embed:
        database = Database.get_instance()

        rank_modify = database.online_unit_rank_modify[self.role.online_unit_rank_modify_id]

        members: list[str] = []
        skill_tree_name = getattr(rank_modify, f"tier{num}_name")
        members.append(f"### __{skill_tree_name}__")
        for rank_num, rank_id in enumerate(rank_modify.m_online_unit_rank_modify_ranks):
            rank = database.online_unit_rank_modify_rank[rank_id]
            skill_id = getattr(rank, f"skill{num}_id")
            if skill_id == 0:
                continue
            skill = database.skill[skill_id]
            members.append(f"### {rank_num + 1}: {skill.name}\n{format_skill_desc(skill.desc)}")

        embed = self.get_base_embed()
        embed.description = "\n".join(members)
        return embed
