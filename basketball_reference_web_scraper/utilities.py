from lxml import etree, html

def str_to_int(value, default=int(0)):
    stripped_value = value.strip()
    try:
        return int(stripped_value)
    except ValueError:
        return default


def str_to_float(value, default=float(0)):
    stripped_value = value.strip()
    try:
        return float(stripped_value)
    except ValueError:
        return default


def merge_two_dicts(first, second):
    combined = first.copy()
    combined.update(second)
    return combined

def extract_html_obj_in_comment(html_tree, xpath):
    for node in html_tree.iter(etree.Comment):
        comment = node.text
        extracted_html = html.fromstring(comment)
        if extracted_html.xpath(xpath):
            return extracted_html
