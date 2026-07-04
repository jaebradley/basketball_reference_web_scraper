from dataclasses import dataclass
from typing import Mapping

from data import Team, Position

"""
These models may not be used in v4, but they most likely will be used in v5.
"""

"""
From https://en.wikipedia.org/w/index.php?title=Quantity&oldid=1361899578:
"Quantity or amount is a property that includes numbers and quantifiable phenomena such as mass, time, distance, heat, angle, and information. 
Quantities can commonly be compared in terms of "more", "less", or "equal", or by assigning a numerical value multiple of a unit of measurement."
"""
@dataclass(frozen=True)
class Distance:
    value: float
    # For now, represent all distances in feet (since Basketball Reference represents all distances in feet / imperial units).
    unit = "feet"

@dataclass(frozen=True)
class ShotRange:
    starting_distance_from_basket: Distance
    length: Distance | None


@dataclass(frozen=True)
class ShotCategoryStatistics:
    percentage_of_total_field_goal_attempts: float
    field_goal_percentage: float


@dataclass(frozen=True)
class ShotCategorySummaryStatistics(ShotCategoryStatistics):
    assisted_percentage: float


@dataclass(frozen=True)
class HalfCourtShotStatistics:
    attempts: int
    made: int


@dataclass(frozen=True)
class DunkStatistics:
    percentage_of_total_field_goal_attempts: float
    made: int


@dataclass(frozen=True)
class CornerThreeStatistics:
    percentage_of_three_point_field_goal_attempts: float
    field_goal_percentage: float


@dataclass(frozen=True)
class TwoPointShotStatistics(ShotCategorySummaryStatistics):
    statistics_by_range: Mapping[ShotRange, ShotCategoryStatistics]
    dunks: DunkStatistics


@dataclass(frozen=True)
class ThreePointShotStatistics(ShotCategorySummaryStatistics):
    corner: CornerThreeStatistics
    half_court: HalfCourtShotStatistics


@dataclass
class PlayerShootingStatistics:
    name: str
    age: int
    team: Team
    position: Position
    games_played: int
    games_started: int
    minutes_played: int
    field_goal_percentage: float
    average_field_goal_attempt_distance_in_feet: float
    two_point_shot_statistics: TwoPointShotStatistics
    three_point_shot_statistics: ThreePointShotStatistics
