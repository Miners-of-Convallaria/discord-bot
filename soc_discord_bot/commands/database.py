# Taair
# Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
# See LICENSE file for details.
from __future__ import annotations

import json
from typing import Type
from typing import TypeVar
from urllib.request import urlopen

import attr

T = TypeVar("T")

_DATABASE: Database | None = None


@attr.define(frozen=True, slots=True)
class Database:
    unit: dict[int, Unit] = attr.field(factory=dict)
    unit_model: dict[int, UnitModel] = attr.field(factory=dict)
    online_role_unit: dict[int, OnlineRoleUnit] = attr.field(factory=dict)
    unit_personality: dict[int, UnitPersonality] = attr.field(factory=dict)
    unit_personality_skill: dict[int, UnitPersonalitySkill] = attr.field(factory=dict)
    unit_skin: dict[int, UnitSkin] = attr.field(factory=dict)
    skill: dict[int, Skill] = attr.field(factory=dict)
    profession: dict[int, Profession] = attr.field(factory=dict)
    faction: dict[int, Faction] = attr.field(factory=dict)
    world_map_color: dict[int, WorldMapColor] = attr.field(factory=dict)
    weapon_type: dict[int, WeaponType] = attr.field(factory=dict)
    move_type: dict[int, MoveType] = attr.field(factory=dict)
    online_role: dict[int, OnlineRole] = attr.field(factory=dict)
    online_role_life_story: dict[int, OnlineRoleLifeStory] = attr.field(factory=dict)
    timestamp: dict[int, Timestamp] = attr.field(factory=dict)
    online_gacha_pool: dict[int, OnlineGachaPool] = attr.field(factory=dict)
    online_unit_rank_modify: dict[int, OnlineUnitRankModify] = attr.field(factory=dict)
    online_unit_rank_modify_rank: dict[int, OnlineUnitRankModifyRank] = attr.field(factory=dict)

    @staticmethod
    def get_instance() -> Database:
        global _DATABASE
        if _DATABASE is None:
            _DATABASE = Database()  # type: ignore
        return _DATABASE

    def get_table_mapping(self) -> list[tuple[str, type]]:
        return [
            ("unit", Unit),
            ("unit_model", UnitModel),
            ("online_role_unit", OnlineRoleUnit),
            ("unit_personality", UnitPersonality),
            ("unit_personality_skill", UnitPersonalitySkill),
            ("skill", Skill),
            ("profession", Profession),
            ("faction", Faction),
            ("world_map_color", WorldMapColor),
            ("weapon_type", WeaponType),
            ("unit_skin", UnitSkin),
            ("move_type", MoveType),
            ("online_role", OnlineRole),
            ("online_role_life_story", OnlineRoleLifeStory),
            ("timestamp", Timestamp),
            ("online_gacha_pool", OnlineGachaPool),
            ("online_unit_rank_modify", OnlineUnitRankModify),
            ("online_unit_rank_modify_rank", OnlineUnitRankModifyRank),
        ]

    def load_local(self, fp: str) -> None:
        def _load_local(name: str, clz: Type[T]) -> dict[int, T]:
            with open(f"{fp}/{name}.json", "r", encoding="utf8") as f:
                items = json.load(f)
                return {v["id"]: clz(**v) for v in items}

        for k, c in self.get_table_mapping():
            getattr(self, k).clear()
            getattr(self, k).update(_load_local(k, c))

    def load_remote(self, url_prefix: str) -> None:
        for k, c in self.get_table_mapping():
            url = f"{url_prefix}/{k}.json"
            print(f"Downloading {url}")
            data = json.loads(urlopen(url).read())
            getattr(self, k).clear()
            getattr(self, k).update({v["id"]: c(**v) for v in data})


@attr.define(frozen=True, slots=True)
class OnlineRoleUnit:
    id: int
    m_online_unit_builds: list[int]
    m_online_role_unit_voice_samples: list[int]
    m_online_role_unit_special_skills: list[int]
    name: str
    idonline_role: int
    idunit: int
    rarity: int
    online_unit_modify_id: int
    online_unit_rank_modify_id: int
    skill_preview_video: str
    enable: bool
    enable_time_id: int
    extra_voice_units: str
    sp_name: str


@attr.define(frozen=True, slots=True)
class Unit:
    id: int
    m_skills: list[int]
    m_unit_performs: list[int]
    m_unit_builds: list[int]
    m_feature_skills: list[int]
    m_preset_skills: list[int]
    m_default_skills: list[int]
    m_weapon_types: list[int]
    m_unit_pool_skills: list[int]
    m_unit_tags: list[int]
    m_unit_voices: list[int]
    m_unit_phantom_skills: list[int]
    m_unit_voice_languages: list[int]
    m_unit_skins: list[int]
    name: str
    editor_name: str
    gender: int
    desc: str
    icon: str
    model: str
    race: int
    profession: int
    faction: int
    tp: int
    tp_max: int
    hp: int
    physic_attack: int
    spell_attack: int
    physic_defence: int
    spell_defence: int
    mobility: int
    move_type: int
    stay_type: int
    jump_up: int
    jump_down: int
    height: int
    speed: int
    melee_skill: int
    reactive_skill: int
    leader_skill: int
    skill_ids: str
    walk_speed: int
    charge_speed: int
    palette: str
    idweapon_main: int
    idweapon_offhand: int
    isplayer: bool
    isdefault: bool
    unit_modify_id: int
    crit_resist: int
    crit_reduce: int
    crit_damage: int
    crit_ratio: int
    default_skills: str
    feature_skills: str
    preset_skills: str
    hp_rarity: int
    physic_attack_rarity: int
    spell_attack_rarity: int
    physic_defence_rarity: int
    spell_defence_rarity: int
    speed_rarity: int
    preset_level: int
    preset_name: str
    preset_random_skill_count: int
    unit_model_id: int
    weapon_type_ids: str
    training_perform_skill: int
    is_hero: bool
    personality_id: int
    tp_icon: str
    tarot_card: str
    unit_tag_ids: str
    unit_words: int
    hide_reboundmove: bool


@attr.define(frozen=True, slots=True)
class UnitModel:
    id: int
    m_unit_model_animations: list[int]
    m_unit_model_performs: list[int]
    m_unit_model_move_smokes: list[int]
    m_weapons: list[int]
    m_public_unit_model_performs: list[int]
    m_public_unit_model_move_smokes: list[int]
    m_unit_palettes: list[int]
    name: str
    model: str
    gender: int
    icon: str
    icon_offset: str
    idweapon_main: int
    idweapon_offhand: int
    weapon_ids: str
    unit_large_id: int


@attr.define(frozen=True, slots=True)
class UnitPersonality:
    id: int
    m_unit_personality_skills: list[int]
    name: str
    editor_name: str
    icon: str


@attr.define(frozen=True, slots=True)
class UnitPersonalitySkill:
    id: int
    idunit_personality: int
    star: int
    desc: str
    type: int
    skill_id: int
    skill_group_id: int
    skill_strength: int


@attr.define(frozen=True, slots=True)
class UnitSkin:
    id: int
    idunit: int
    name: str
    type: int
    icon_card: str
    star: int
    idunit_model: int
    palette: str
    flag: int
    rarity: int
    system_redirect_id: int
    icon: str
    skill_preview_video: str
    desc: str
    editor_name: str
    open_at: int


@attr.define(frozen=True, slots=True)
class Profession:
    id: int
    name: str
    editor_name: str
    desc: str
    type: int
    category: int
    icon: str
    small_flag: str
    tendency_tag_id: int


@attr.define(frozen=True, slots=True)
class Skill:
    id: int
    m_specialitys: list[int]
    m_skill_tags: list[int]
    name: str
    editor_name: str
    desc: str
    icon: str
    type: int
    phase: int
    category: int
    damage_type: int
    attack_method: int
    tp: int
    hp: int
    range_min: int
    range_max: int
    range_width: int
    attack_up: int
    attack_down: int
    damage: int
    damage_percent: int
    damage_factor: int
    physic_factor: int
    spell_factor: int
    defence_ignore: int
    target_method: int
    target_select: int
    target_width: int
    touch_method: int
    cooldown: int
    pre_cooldown: int
    clip_capacity: int
    crit_chance: int
    speciality_ids: str
    limit_count: int
    limit_count_turn: int
    anim_name: str
    animation_id: int
    idskill_follow: int
    duration: int
    perform_name: str
    skill_type: int
    target_type: int
    restrict: int
    active_param: str
    skill_tag_ids: str
    range_tag: int
    hit_method: int
    injured_duration: int
    rarity: int
    class_type: int
    target_param: str
    need_equip: bool
    sparam: str
    bg_desc: str
    overwritten_skill_id: int
    cast_param: str
    skill_cast_id: int
    skill_cast_parent_target: bool
    voice_tag_id: int
    simplified_desc: str
    enable_icon_effects: bool
    active_tip: str
    shot_range_tag: int


@attr.define(frozen=True, slots=True)
class Faction:
    id: int
    m_exclusive_block_idss: list[int]
    m_battle_block_idss: list[int]
    m_haunt_block_idss: list[int]
    m_involved_block_idss: list[int]
    m_enemy_faction_idss: list[int]
    m_battle_faction_idss: list[int]
    m_occupied_block_idss: list[int]
    type: str
    name: str
    editor_name: str
    desc: str
    icon: str
    influence: int
    reputation: int
    reputation_level: int
    involved_block_ids: str
    haunt_block_ids: str
    occupied_block_ids: str
    enemy_faction_ids: str
    policy_type: int
    is_world_faction: bool
    block_color_id: int
    icon_color_id: int
    face_icon: str
    recent_development_id: int
    bg_color: str
    sort_id: int
    line_color: int


@attr.define(frozen=True, slots=True)
class WorldMapColor:
    id: int
    type: str
    name: str
    r: int
    g: int
    b: int
    a: int
    is_default: bool


@attr.define(frozen=True, slots=True)
class WeaponType:
    id: int
    type: str
    name: str
    main_hand: bool
    order_id: int
    icon: str


@attr.define(frozen=True, slots=True)
class MoveType:
    id: int
    type: str
    name: str
    desc: str


@attr.define(frozen=True, slots=True)
class OnlineRoleLifeStory:
    id: int
    idonline_role: int
    sort_id: int
    title: str
    content: str
    require_story_id: int


@attr.define(frozen=True, slots=True)
class OnlineRole:
    id: int
    m_online_role_units: list[int]
    m_online_role_life_storys: list[int]
    m_online_role_storys: list[int]
    name: str
    editor_name: str
    intro: str
    friendship_head_portrait_id: int
    has_friendship: bool
    sort_id: int
    is_npc: bool


@attr.define(frozen=True, slots=True)
class OnlineGachaPool:
    id: int
    m_rate_up_idss: list[int]
    m_online_gacha_pool_battles: list[int]
    idgacha_package: int
    name: str
    editor_name: str
    is_open: bool
    time_type: int
    start_at: int
    end_at: int
    allowed_times: str
    limit_times: int
    rate_up_ids: str
    rate_up_probability: int
    label_icon: str
    advertisement: str
    tip: str
    sort_id: int
    selectable_count: int


@attr.define(frozen=True, slots=True)
class OnlineGachaPackage:
    id: int
    m_online_gacha_package_groups: list[int]
    name: str
    editor_name: str
    desc: str
    rule_id: int
    ticket_treasure_type: int
    ticket_param0: int
    ticket_param1: int
    anim_type: int
    chance_template_id: int


# not frozen, as patched by OperatingAreaData
@attr.define(slots=True)
class Timestamp:
    id: int
    name: str
    timestamp: int


@attr.define(frozen=True, slots=True)
class OperatingAreaData:
    id: int
    table_name: str
    col_name: str
    idvalue: int
    param_cn: int
    param_tw: int
    param_jp: int
    param_kr: int
    param_us: int


@attr.define(frozen=True, slots=True)
class OnlineUnitRankModify:
    id: int
    m_online_unit_rank_modify_ranks: list[int]
    name: str
    skill_line_id: int
    tier1_name: str
    tier2_name: str


@attr.define(frozen=True, slots=True)
class OnlineUnitRankModifyRank:
    id: int
    idonline_unit_rank_modify: int
    rank: int
    money: int
    material1_id: int
    material1_count: int
    material2_id: int
    material2_count: int
    hp_add: int
    physic_attack_add: int
    spell_attack_add: int
    physic_defence_add: int
    spell_defence_add: int
    skill1_id: int
    is_skill1_share: bool
    skill2_id: int
    is_skill2_share: bool
