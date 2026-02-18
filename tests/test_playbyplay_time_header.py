from lxml import html as lxml_html
from basketball_reference_web_scraper.html import PlayByPlayRow

def test_play_by_play_row_ignores_time_header_row():
    tr = lxml_html.fromstring("<tr><td>Time</td><td></td></tr>")
    row = PlayByPlayRow(html=tr)
    assert row.has_play_by_play_data is False
