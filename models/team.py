from dataclasses import dataclass


@dataclass
class Team:
    """
    A class representing a cricket team.

    Attributes:
    -----------
    name : str
        The full name of the team.
    short_name : str
        The short name or abbreviation of the team.
    home_stadium : str
        The name of the stadium where the team plays their home games.
    """
    name: str
    short_name: str
    home_stadium: str

    def __str__(self) -> str:
        """
        Returns the short name of the team as a string.
        """
        return self.short_name

    def set_name(self, name: str):
        """
        Sets the full name of the team.

        Parameters:
        -----------
        name : str
            The full name of the team.
        """
        self.name = name

    def set_short_name(self, short_name: str):
        """
        Sets the short name or abbreviation of the team.

        Parameters:
        -----------
        short_name : str
            The short name or abbreviation of the team.
        """
        self.short_name = short_name

    def set_home_stadium(self, home_stadium: str):
        """
        Sets the name of the stadium where the team plays their home games.

        Parameters:
        -----------
        home_stadium : str
            The name of the stadium where the team plays their home games.
        """
        self.home_stadium = home_stadium

    def validate_short_name(self):
        """
        Validates that the short name or abbreviation of the team is between 2 and 5 characters.

        Raises:
        -------
        ValueError
            If the short name is too short or too long.
        """
        if len(self.short_name) < 2 or len(self.short_name) > 5:
            raise ValueError("Short name must be between 2 and 5 characters long.")

    def validate_home_stadium(self):
        """
        Validates that the name of the stadium is not empty or too long.

        Raises:
        -------
        ValueError
            If the home stadium name is empty or too long.
        """
        if not self.home_stadium:
            raise ValueError("Home stadium name cannot be empty.")
        if len(self.home_stadium) > 50:
            raise ValueError("Home stadium name is too long.")
