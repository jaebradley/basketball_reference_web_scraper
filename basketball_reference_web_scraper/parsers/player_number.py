from basketball_reference_web_scraper.errors import InvalidPlayer


def parse_player_link(player_name, html_bytecode):
    html_str = html_bytecode.decode('utf-8')
    html_rows = html_str.split('\n')
    ext = None

    for row in html_rows:
        if player_name in row:
            for pair in row.split():
                if 'data-append-csv' in pair:
                    ext = pair.split('\"')[1]
                    return ext

    if not ext:
        raise InvalidPlayer(player_name)


def parse_player_number(html_bytecode):
    # Example DOM path for Kemba Walker: / html / body / div[2] / div[2] / div[2] / a[4] / svg / text
    # Lines with players numbers contain a special svg img

    html_str = html_bytecode.decode('utf-8')
    html_rows = html_str.split('\n')
    nums = []

    for row in html_rows:
        if 'svg viewBox' in row:
            text_list = row.split('<text')
            nums.append(text_list[-1].split('>')[1].split('<')[0])

    if len(nums) == 0:
        return 'Number not found'

    return nums[-1]