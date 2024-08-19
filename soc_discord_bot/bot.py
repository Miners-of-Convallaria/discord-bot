# Taair
# Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
# See LICENSE file for details.
import asyncio
import os

import hikari
import lightbulb
import miru
from commands.database import Database
from commands.gacha import GachaView
from commands.unit import UnitView

if os.name != "nt":
    try:
        # speedup for unix systems
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        print("Failed to import uvloop, which would improve the performance of the bot!")


bot = hikari.GatewayBot(token=os.environ.get("TOKEN", ""), logs="DEBUG")
lightbulb_client = lightbulb.client_from_app(bot)
miru_client = miru.Client(bot)

# Ensure the client starts once the bot is run
bot.subscribe(hikari.StartingEvent, lightbulb_client.start)

soc_group = lightbulb.Group("soc", "Sword of Convallaria commands")

database = Database.get_instance()
if local_db := os.environ.get("LOCAL_DB"):
    database.load_local(local_db)
else:
    database.load_remote("https://raw.githubusercontent.com/Miners-of-Convallaria/database/main/global")


UnitView.reinit_database()
GachaView.reinit_database()


async def autocomplete_callback(ctx: lightbulb.AutocompleteContext[str]) -> None:
    current_value: str = str(ctx.focused.value) or ""
    recommendations = UnitView.autocomplete(current_value)
    await ctx.respond(recommendations)


@soc_group.register()
class UnitCommand(
    lightbulb.SlashCommand,
    name="unit",
    description="shows information about the specified unit",
):
    name = lightbulb.string("name", "name of the unit", autocomplete=autocomplete_callback)

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        view = UnitView(self.name)
        await ctx.respond(embed=view.get_main(), components=view)
        miru_client.start_view(view)


@soc_group.register()
class GachaCommand(
    lightbulb.SlashCommand,
    name="gacha",
    description="shows current and upcoming banners",
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        view = GachaView()
        await ctx.respond(embed=view.get_main(), components=view)
        miru_client.start_view(view)


lightbulb_client.register(soc_group)


@lightbulb_client.register()
class UpdateDB(
    lightbulb.SlashCommand,
    name="update_db",
    description="Update the database",
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond("Updating database...")
        try:
            database.load_remote("https://raw.githubusercontent.com/Miners-of-Convallaria/database/main/global")
            UnitView.reinit_database()
            GachaView.reinit_database()
        except Exception as e:
            await ctx.respond(f"Failed to update database: {e}")
        else:
            await ctx.respond("Database updated")


if __name__ == "__main__":
    if "TOKEN" not in os.environ:
        raise ValueError('The environment "TOKEN" wasn\'t set')
    bot.run()
