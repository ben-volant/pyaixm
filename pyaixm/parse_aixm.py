from dataclasses import fields
from lxml import etree
import sys
from pprint import pprint
import typing

from . import aixm_types


def replace_xlinks(features: list) -> None:
    "Replaces XLink references on all features with the referenced object"
    for feature in features:
        if isinstance(feature, aixm_types.Feature):
            replace_xlinks_r(feature, set())


def replace_xlinks_r(entity: aixm_types.Feature | list, visited: set) -> None:

    entity_id = id(entity)
    if entity_id in visited:
        return

    visited.add(entity_id)

    if isinstance(entity, list):
        for element in entity:
            if isinstance(entity, aixm_types.Feature) or isinstance(entity, list):
                replace_xlinks_r(element, visited)
    elif isinstance(entity, aixm_types.Feature):
        for field in fields(entity):
            if field.name == "parent":
                continue
            attr = getattr(entity, field.name)
            if isinstance(attr, aixm_types.Feature) or isinstance(attr, list):
                replace_xlinks_r(attr, visited)
            if isinstance(attr, aixm_types.XLink):
                if attr.target is not None:
                    setattr(entity, field.name, attr.target)
    

def parse(files: list[str], resolve_xlinks = False) -> list:
    l = []
    for f in files:
        try:
            context = etree.iterparse(f)
        except FileNotFoundError:
            print(f"File not found: {f}")
            continue
        except etree.XMLSyntaxError as e:
            print(f"Error parsing file {f}: {e}")
            continue
        for action, elem in context:
            if action == 'end' and elem.tag in ['{http://www.aixm.aero/schema/5.1.1/message}hasMember', '{http://www.aixm.aero/schema/5.1/message}hasMember']:
                feature = aixm_types.parse_feature(elem[0])  # first child of 'hasMember' is aixm feature
                l.append(feature)

    aixm_types.XLink.resolve()

    if resolve_xlinks:
        replace_xlinks(l)

    return l


if __name__ == '__main__':
    files = sys.argv[1:]
    if not files:
        print("Please provide one or more filenames as command line arguments.")
        sys.exit(1)

    features = parse(files, resolve_xlinks=True)
    #pprint(features)