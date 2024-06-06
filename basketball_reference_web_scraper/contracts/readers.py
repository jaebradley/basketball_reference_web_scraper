import enum
from typing import Optional, Callable, Dict, Any

from lxml.etree import Element

from .data import PlayerData


def read_player_cell_data(cell: Element) -> PlayerData:
    return PlayerData(name=cell.text_content(), identifier=cell.get("data-append-csv"))


def read_team_identifier_cell_data(cell: Element) -> str:
    return cell.text_content()


class Column(enum.Enum):
    PLAYER = "player"
    TEAM = "team_id"
    FIRST_SEASON_SALARY = "y1"
    SECOND_SEASON_SALARY = "y2"
    THIRD_SEASON_SALARY = "y3"
    FOURTH_SEASON_SALARY = "y4"
    FIFTH_SEASON_SALARY = "y5"
    SIXTH_SEASON_SALARY = "y6"


class CellIdentifier:
    def __init__(self, column: Column):
        self.column = column

    def identify_cell(self, row: Element) -> Optional[Element]:
        matching_cells = row.xpath(f'./td[@data-stat="{self.column.value}"]')
        if 1 == len(matching_cells):
            return matching_cells[0]


class RowDataReader:

    def __init__(self,
                 cell_identifiers_by_column: Dict[Column, CellIdentifier],
                 cell_value_readers_by_column: Dict[Column, Callable[[Element], Any]]):
        self.cell_identifiers_by_column = cell_identifiers_by_column
        self.cell_value_readers_by_column = cell_value_readers_by_column

    def read(self, row: Element) -> Dict[Column, Optional[Any]]:
        return dict(map(lambda column_and_cell: [
            column_and_cell[0],
            None if column_and_cell[1] is None \
                else self.cell_value_readers_by_column.get(column_and_cell[0])(column_and_cell[1])
        ], map(
            lambda e: [e[0], e[1].identify_cell(row=row)],
            self.cell_identifiers_by_column.items())))

    @staticmethod
    def instance():
        # TODO: don't recreate the object on each invocation
        return RowDataReader(
            cell_identifiers_by_column={
                Column.PLAYER: CellIdentifier(column=Column.PLAYER),
                Column.TEAM: CellIdentifier(column=Column.TEAM),
            },
            cell_value_readers_by_column={
                Column.PLAYER: read_player_cell_data,
                Column.TEAM: read_team_identifier_cell_data
            }
        )
