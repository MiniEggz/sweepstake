"""Module to handle sweepstake."""
import random
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Sweepstake:
    """Object to hold information about the sweepstake.

    Attributes:
        participants (List[str]): names of participants in the sweepstake.
        teams (List[str]): teams in order of ranking.
        assignments (Dict[str, List[str]]): dictionary of assignments.
    """

    participants: List[str]
    teams: List[str]

    def __post_init__(self):
        self.segmented_teams = self.segment_teams()
        self.assignments = {participant: [] for participant in self.participants}

    @staticmethod
    def read_file(file_name: str) -> List[str]:
        """Read file by line and keep elements as a list.

        Parameters:
            file_name (str): name of the file containing data.

        Returns:
            List[str]: File contents separated by line breaks as a list.
        """
        with open(file_name, encoding="utf-8") as file:
            return file.read().split("\n")

    def take_segment(self, remaining_teams: List[str]) -> Tuple[List[str], List[str]]:
        """Take segment from list of teams.

        Parameters:
            remaining_teams (List[str]): list of remaining teams to segment.

        Returns:
            List[str]: the segment of teams.
            List[str]: the teams remaining to segment.
        """
        segment_index = min(len(self.participants), len(self.teams))
        return remaining_teams[:segment_index], remaining_teams[segment_index:]

    def segment_teams(self) -> List[List[str]]:
        """Segment teams into lists of n where n is the number of people.

        Returns:
            List[List[str]]: segmented list of teams.
        """
        segmented = []
        remaining_teams = self.teams
        while len(remaining_teams) > 0:
            current_segment, remaining_teams = self.take_segment(remaining_teams)
            segmented.append(current_segment)
        return segmented

    def assign_from_segments(self, segment: List[str]) -> None:
        """Assigns person from a segment.

        Parameters:
            segment (List[str]): segment of teams.
        """
        participants = self.participants.copy()
        for team in segment:
            participant = random.choice(participants)
            self.assignments[participant].append(team)
            participants.remove(participant)

    def assign_teams(self) -> None:
        """Assign all teams to people at random."""
        for segment in self.segmented_teams:
            self.assign_from_segments(segment)

    def display_assignments(self) -> None:
        """Display the assignments made."""
        for participant in self.participants:
            print(f"{participant} ({len(self.assignments[participant])}):")
            for team in self.assignments[participant]:
                print(f"  {team}")
            print()


if __name__ == "__main__":
    sweepstake = Sweepstake(
        participants=Sweepstake.read_file("people.txt"),
        teams=Sweepstake.read_file("world_cup_2022.txt"),
    )
    sweepstake.assign_teams()
    sweepstake.display_assignments()
