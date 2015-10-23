import urllib2
import lxml.html as html


class BoxScoresHtmlReturner:

    @staticmethod
    def return_html(box_score_url):
        content = urllib2.urlopen(box_score_url).read()
        box_score_html = html.fromstring(content)
        return box_score_html