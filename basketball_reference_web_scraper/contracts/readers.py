import enum
from typing import Dict, Any, Optional

from lxml.etree import Element

from .data import PlayerData


class Column(enum.Enum):
    PLAYER = "player"
    TEAM = "team_id"
    FIRST_SEASON_SALARY = "y1"
    SECOND_SEASON_SALARY = "y2"
    THIRD_SEASON_SALARY = "y3"
    FOURTH_SEASON_SALARY = "y4"
    FIFTH_SEASON_SALARY = "y5"
    SIXTH_SEASON_SALARY = "y6"


class SingleCellFinder:
    def __init__(self, column: Column):
        self.column = column

    def find(self, row: Element) -> Optional[Element]:
        matching_cells = row.xpath(f'./td[@data-stat="{self.column.value}"]')
        if 1 == len(matching_cells):
            return matching_cells[0]


class SingleCellValueReader:
    def __init__(self, cell_finder: SingleCellFinder, cell_reader):
        self.cell_finder = cell_finder
        self.cell_reader = cell_reader

    def read(self, row: Element):
        cell = self.cell_finder.find(row=row)
        if cell:
            return self.cell_reader.read(cell=cell)


class RowDataReader:
    def __init__(self, cell_readers_by_column: Dict[Column, SingleCellValueReader]):
        self.cell_readers_by_column = cell_readers_by_column

    def read(self, row: Element) -> Dict[Column, Optional[Any]]:
        return dict(map(lambda e: [e[0], e[1].read(row=row)], self.cell_readers_by_column.items()))


class PlayerDataCellReader:
    def __init__(self, player_identifier_attribute_name):
        self.player_identifier_attribute_name = player_identifier_attribute_name

    def read(self, cell: Element) -> PlayerData:
        return PlayerData(name=cell.text_content(), identifier=cell.get(self.player_identifier_attribute_name))


class TeamDataCellReader:
    def read(self, cell: Element) -> str:
        return cell.text_content()
