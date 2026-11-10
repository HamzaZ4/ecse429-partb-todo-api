from xml.etree import ElementTree


def todo_payload(title, description):
    return {"title": title, "doneStatus": False, "description": description}


def todo_xml(title):
    todo = ElementTree.Element("todo")
    ElementTree.SubElement(todo, "title").text = title
    return ElementTree.tostring(todo, encoding="unicode")


def parse_xml(text):
    return ElementTree.fromstring(text)
