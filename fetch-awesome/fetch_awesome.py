#!/usr/bin/env python
"""
https://github.com/sindresorhus/awesome#readme
https://raw.githubusercontent.com/sindresorhus/awesome/main/readme.md
"""

import urllib.request
import pathlib
import re


def read_awesome():
    awesome_url = "https://raw.githubusercontent.com/sindresorhus/awesome/main/readme.md"

    with urllib.request.urlopen(awesome_url) as f:
        readme = f.read().decode('utf-8')

    return readme


def extract_links(readme):
    links = []

    section = None
    for line in readme.split("\n"):
        m = re.search(r"##(.*)", line)
        if m is not None:
            section = m.group(1).strip()

        m = re.search(r"\[(.*)\]\((.*)\)", line)
        if m is not None:
            title = m.group(1).strip()
            target = m.group(2).strip()
            if not target.startswith("#"):
                link = {
                    "title": title,
                    "target": target,
                    "ownLabels": []
                }
                if section is not None:
                    link["ownLabels"] = [section]
                links.append(link)

    links = sorted(links, key=lambda x: x["target"])

    return links


def write_notemarks_data(readme, links):
    link_db_data = ["links:"] + [
        x
        for link in links
        for x in [
            f"  - title: '{link['title']}'",
            f"    target: '{link['target']}'",
        ] + ([
            f"    ownLabels: {link['ownLabels']}"
        ] if "ownLabels" in link else [])
    ] + [""]

    pathlib.Path("./demo-awesome/.notemarks").mkdir(parents=True, exist_ok=True)
    with open("./demo-awesome/.notemarks/link_db.yaml", "w") as f:
        f.write("\n".join(link_db_data))

    with open("./demo-awesome/Awesome.md", "w") as f:
        f.write(readme)


def main():
    readme = read_awesome()
    links = extract_links(readme)
    write_notemarks_data(readme, links)


if __name__ == "__main__":
    main()
