from dataclasses import dataclass


@dataclass
class Reaction(object):
    id: int  # noqa: A003
    guild_id: int

    trigger: str
    response: str

    delete_trigger: bool
    dm_response: bool
    contains_anywhere: bool
    has_target: bool

    created_at: str
    updated_at: str
