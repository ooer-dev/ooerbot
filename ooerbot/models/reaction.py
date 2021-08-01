# https://gitlab.com/Kwoth/nadekobot/-/blob/1.9/NadekoBot.Core/Services/Database/Models/CustomReaction.cs
class Reaction(object):
    def __init__(self, guild_id, trigger, response, delete_trigger, dm_response, contains_anywhere, has_target):
        self.guild_id = guild_id
        self.trigger = trigger
        self.response = response

        self.delete_trigger = delete_trigger
        self.dm_response = dm_response
        self.contains_anywhere = contains_anywhere
        self.has_target = has_target
