# Taair
# Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
# See LICENSE file for details.
import time
from datetime import UTC  # type: ignore
from datetime import datetime
from typing import TYPE_CHECKING

import attrs
import hikari
import miru

from .database import Database
from .utils import clean_name

if TYPE_CHECKING:
    from datetime import _TzInfo
    UTC: _TzInfo


@attrs.define(slots=True, frozen=True)
class GachaBanner:
    name: str
    text: str
    start: str
    end: str
    end_int: int


BANNERS: list[GachaBanner] = []


class GachaView(miru.View):
    @staticmethod
    def reinit_database() -> None:
        global BANNERS
        BANNERS.clear()

        database = Database.get_instance()

        for gacha_pool in database.online_gacha_pool.values():
            if gacha_pool.start_at == 0 or gacha_pool.end_at == 0:
                continue
            start = database.timestamp[gacha_pool.start_at].timestamp
            end = database.timestamp[gacha_pool.end_at].timestamp
            # if end < current_time:
            #    continue

            banner = GachaBanner(
                name=gacha_pool.name,
                text=(clean_name(gacha_pool.tip) if gacha_pool.tip else gacha_pool.label_icon),
                start=datetime.fromtimestamp(start, UTC).strftime("%Y-%m-%d"),
                end=datetime.fromtimestamp(end, UTC).strftime("%Y-%m-%d"),
                end_int=end,
            )
            BANNERS.append(banner)

        BANNERS.sort(key=lambda x: x.end_int)

    def get_main(self) -> hikari.Embed:
        embed = hikari.Embed(
            title="Current and upcoming banners",
        )

        now = int(time.time())
        for banner in BANNERS:
            if banner.end_int < now or banner.end_int == 2099999999:
                continue
            embed.add_field(
                name=f"{banner.start} ~ {banner.end}",
                value=f"__{banner.name}__\n{banner.text}",
                inline=False,
            )

        return embed
