import logging
import datetime

import hikari
import lightbulb
import shortuuid
from lightbulb.ext import tasks

from src import utils, main

plugin = utils.Plugin("Channel autodelete")


@plugin.command()
@lightbulb.command("autodelete", "Checks if the bot is alive.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ping(ctx: utils.Context) -> None:
    await ctx.respond("Pong!")


@tasks.CronTrigger("0 * * * *")
async def autodelete_task(bot: main.CiberBot) -> None:
    """
    Task that programatically erases messages on a channel by their configured permanence time (in hours).
    """

    logging.info("fent coses")

    configs = await bot.db.execute_asyncio(
        "SELECT channel_id, persistence_time FROM autodelete_config",
    )

    if not configs:
        return

    for config in configs:
        if not config.persistence_time:
            return

        now = datetime.now()
        delta = now + datetime.timedelta(hours=config.persistence_time)

        messages = await bot.db.execute_asyncio(
            "SELECT channel_id, datetime, message_id FROM reminder WHERE datetime < %s ALLOW FILTERING",
            (delta),
        )

        if not messages:
            pass

        for message in messages:
            logging.info(message.message_id)

        # await bot.db.execute_asyncio(
        #     "DELETE FROM reminder WHERE id = %s AND user_id = %s AND datetime = %s",
        #     (row.id, row.user_id, row.datetime),
        # )


def load(bot: main.CiberBot) -> None:
    autodelete_task.start()
    bot.add_plugin(plugin)
