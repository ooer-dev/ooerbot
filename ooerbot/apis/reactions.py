import os
from typing import List

import yaml
from aiofile import async_open

from ooerbot.models.reaction import Reaction

YAML_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'reactions.yml')


# This will eventually be replaced with a call to Crapi.
# For now, this will work for testing the bot.
async def get_reactions_for_guild(guild_id: int) -> List[Reaction]:
    async with async_open(YAML_PATH, 'r') as afp:
        stream = await afp.read()

    doc = yaml.safe_load(stream)

    reactions = []
    for trigger, crs in doc.items():
        for cr in crs:
            reactions.append(Reaction(
                guild_id=guild_id,
                trigger=str(trigger),
                response=str(cr['res']),
                delete_trigger=cr.get('ad', False),
                dm_response=cr.get('dm', False),
                contains_anywhere=cr.get('ca', False),
                has_target=cr.get('at', False),
            ))

    return reactions
