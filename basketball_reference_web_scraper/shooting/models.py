from dataclasses import dataclass

from data import Team, Position


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
    statistics_by_range: [[int, ShotCategoryStatistics]]
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
