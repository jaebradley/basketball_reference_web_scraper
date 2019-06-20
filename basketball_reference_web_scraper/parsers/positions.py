from basketball_reference_web_scraper.data import POSITION_ABBREVIATIONS_TO_POSITION


def parse_positions(positions_content):
    parsed_positions = list(
        map(
            lambda position_abbreviation: POSITION_ABBREVIATIONS_TO_POSITION.get(position_abbreviation),
            positions_content.split("-")
        )
    )
    return [position for position in parsed_positions if position is not None]