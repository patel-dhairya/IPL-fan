from models import team
from dataclasses import dataclass


@dataclass
class Player:
    """
    A class representing a cricket player.

    Attributes:
    -----------
    _name : str
        The name of the player.
    _age : int
        The age of the player.
    _role : str
        The role of the player in the team (e.g. batsman, bowler, all-rounder).
    _batting_style : str
        The batting style of the player (e.g. right-handed, left-handed).
    _bowling_hand : str
        The hand with which the player bowls (e.g. right, left).
    _bowling_style : str
        The bowling style of the player (e.g. fast, spin).
    _team : str
        The name of the team the player belongs to.
    _captain : bool
        True if the player is the captain of the team, False otherwise.
    _overseas : bool
        True is player is overseas(not from India)
    """

    name: str
    age: int
    role: str
    batting_style: str
    bowling_hand: str
    bowling_style: str
    team: team.Team
    country: str
    captain: bool = False

    def make_captain(self):
        """
        Sets player captain to True
        """
        self.captain = True

    def is_captain(self) -> bool:
        """
        Returns True if the player is captain of team
        """
        return self.captain

    def __str__(self) -> str:
        """
        Returns a string representation of the object.
        """
        return f"{self.name}"
