from collections import defaultdict
from dataclasses import dataclass
from typing import Optional, Dict, Callable

from lxml.etree import HTMLPullParser, LxmlError

from basketball_reference_web_scraper.contracts.data.models import PlayerContract


@dataclass(frozen=False)
class PlayerRowData:
    id: Optional[str]
    name: Optional[str]
    team_abbreviation: Optional[str]
    values_by_header: Dict[str, Optional[str]]


@dataclass(frozen=True)
class PlayerContractData:
    row: PlayerRowData
    headers: Dict[str, str]


class NothingMoreToParse(StopIteration):
    """
    Custom exception to indicate player contract data from player contracts page HTML has been fully parsed
    """
    pass


class PlayerContractsPageParser:
    def __init__(self, player_contract_data_processor: Callable[[PlayerContractData], PlayerContract]):
        self._data_processor = player_contract_data_processor
        self._seen_table = False
        self._started_processing_table_body = False
        self._headers = defaultdict(str)
        self._current_player_data = PlayerRowData(id=None, name=None, team_abbreviation=None, values_by_header={})

    def __enter__(self):
        self._html_parser = HTMLPullParser(events=["start", "end"], tag=["table", "tbody", "th", "tr", "td"])
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self._html_parser.close()
        except LxmlError:
            # LxmlErrors can occur when forcibly stopping processing (i.e. closing the parser) since there's no more
            # relevant data to parse
            pass

    def parse(self, chunk) -> None:
        self._html_parser.feed(str(chunk))

        for event, element in self._html_parser.read_events():
            if event == "start" and element.tag == "table" and element.attrib.get("id") == "player-contracts":
                self._seen_table = True
            elif self._seen_table:
                if event == "end" and element.tag == "table" and element.attrib.get("id") == "player-contracts":
                    raise NothingMoreToParse()

                elif self._started_processing_table_body:
                    if event == "start" and element.tag == "tr" and element.attrib.get("class") is None:
                        self._current_player_data = PlayerRowData(id=None, name=None, team_abbreviation=None,
                                                                  values_by_header={})
                    elif event == "end" and element.tag == "tr" and element.attrib.get("class") is None:
                        element.clear(keep_tail=True)
                        if self._current_player_data.id is not None:
                            self._data_processor(PlayerContractData(
                                row=self._current_player_data,
                                headers=self._headers
                            ))
                    elif event == "end" and element.tag == "td" and element.attrib.get("data-stat") is not None:
                        if element.attrib.get('data-stat') == "player":
                            self._current_player_data.id = element.attrib.get('data-append-csv')
                            self._current_player_data.name = "".join(element.itertext())
                        elif element.attrib.get('data-stat') == "team_id":
                            self._current_player_data.team_abbreviation = "".join(element.itertext())
                        else:
                            self._current_player_data.values_by_header[element.attrib.get('data-stat')] = element.attrib.get("csk")
                        element.clear(keep_tail=True)
                else:
                    if event == "end" and element.tag == "th" and element.attrib.get(
                            "data-stat") is not None and element.attrib.get("scope") == "col":
                        self._headers[element.attrib.get('data-stat')] = element.text
                        element.clear(keep_tail=True)
                    elif event == "start" and element.tag == "tbody":
                        self._started_processing_table_body = True
                        element.clear(keep_tail=True)

