import xml.etree.ElementTree as ET
import re
import json

def parse_sections(xml_path, revision_date):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    sections = []
    for section in root.iter("DIV8"):
        if section.get("TYPE") == "SECTION":

            meta = json.loads(section.get("hierarchy_metadata", "{}"))
            citation = meta.get("citation", "")
            identifier = section.get("N")
            head = section.findtext("HEAD", "")
            paragraphs = section.findall("P")

            body = " ".join("".join(p.itertext()) for p in paragraphs)

            sections.append({
                "identifier": identifier,
                "heading": re.sub(r"\s+", " ", head).strip(),
                "body": re.sub(r"\s+", " ", body).strip(),
                "citation": citation,
                "revision_date": revision_date,
            })

    if not sections:
        raise ValueError(f"Inga sektioner i {xml_path}")

    return sections


if __name__ == "__main__":
    for date in ("2017-01-01", "2021-04-21"):
        sections = parse_sections(f"data/raw/part107-{date}.xml", date)
        with open(f"data/sections-{date}.json", "w", encoding="utf-8") as f:
            json.dump(sections, f, indent=2, ensure_ascii=False)
        print(date, len(sections))