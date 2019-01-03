from lxml import html


def parse_game_urls(page):
    tree = html.fromstring(page)
    games = tree.xpath('//td[contains(@class, "gamelink")]/a')
    return list(map(lambda game: game.attrib['href'], games))
