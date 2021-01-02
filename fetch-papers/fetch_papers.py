#!/usr/bin/env python
"""
https://github.com/sindresorhus/awesome#readme
https://raw.githubusercontent.com/sindresorhus/awesome/main/readme.md
"""

import urllib.request
import pathlib
import re
import os


def read_readme():
    readme_url = "https://raw.githubusercontent.com/floodsung/Deep-Learning-Papers-Reading-Roadmap/master/README.md"

    with urllib.request.urlopen(readme_url) as f:
        readme = f.read().decode('utf-8')

    return readme


def apply_global_fixes(readme):
    return readme.replace("via\nRegion-based", "via Region-based")


def download_url(url, outfile):
    if not os.path.exists(outfile):
        try:
            with urllib.request.urlopen(url) as url_handle:
                with open(outfile, "wb") as f:
                    f.write(url_handle.read())
        except urllib.error.HTTPError:
            print(f"WARNING: Failed to download '{url}'")


def extract_pdf_link(line):
    m = re.search(r"\[\[pdf\]\]\((.*?)\)", line)
    if m is not None:
        target = m.group(1).strip()
        return target


def normalize_title(title):
    while title.startswith("(") and title.endswith(")"):
        title = title[1:-1]
    while title.startswith("“"):
        title = title[1:]
    return title


def extract_title_and_raw_authors(line):
    m = re.search(r"\*\*(.*?)\*\*(.*?)\*\*(.*?)\*\*", line)
    if m is not None:
        title = normalize_title(m.group(3).strip())
        authors = m.group(2).strip()
        return title, authors
    return None, None


def extract_year(line):
    # https://regex101.com/r/SrQ2UR/1
    m = re.search(r"(?<![\.-:])(\d\d\d\d)", line)
    if m is not None:
        return int(m.group(1))


def extract_authors(raw_authors):
    if raw_authors is None:
        return []

    replacements = {
        '"': "",
        ";": ",",
        "et al.": "",
        "etal.": "",
        " and ": "",
        "LeCun, Yann": "LeCun",
        "Yoshua Bengio": "Bengio",
        "Geoffrey Hinton": "Hinton",
        "Hinton, Geoffrey E.": "Hinton",
        "Hinton, Geoffrey": "Hinton",
        "Geoffrey E. Hinton": "Hinton",
        "Simon Osindero": "Osindero",
        "Yee-Whye Teh": "Teh",
        "Ruslan R. Salakhutdinov": "Salakhutdinov",
        "Krizhevsky, Alex": "Krizhevsky",
        "Ilya Sutskever": "Sutskever",
        "Simonyan, Karen": "Simonyan",
        "Andrew Zisserman": "Zisserman",
        "Szegedy, Christian": "Szegedy",
        "He, Kaiming": "He",
        "Graves, Alex": "Graves",
        "Abdel-rahman Mohamed": "Mohamed",
        "Navdeep Jaitly": "Jaitly",
        "Sak, Haşim": "Sak",
        "Amodei, Dario": "Amodei",
        "Srivastava, Nitish": "Srivastava",
        "Christian Szegedy": "Szegedy",
        "Courbariaux, Matthieu": "Courbariaux",
        "Jaderberg, Max": "Jaderberg",
        "Wei, Tao": "Wei",
        "Sutskever, Ilya": "Sutskever",
        "Kingma, Diederik": "Kingma",
        "Andrychowicz, Marcin": "Andrychowicz",
        "Iandola, Forrest N.": "Iandola",
        "Le, Quoc V": "Le",
        "Kingma, Diederik P.": "Kingma",
        "Goodfellow, Ian": "Goodfellow",
        "Radford, Alec": "Radford",
        "Gregor, Karol": "Gregor",
        "Oord, Aaron van den": "Oord",
        "Cho, Kyunghyun": "Cho",
        "Quoc V. Le": "Le",
        "Bahdanau, Dzmitry": "Bahdanau",
        "Zaremba, Wojciech": "Zaremba",
        "Weston, Jason": "Weston",
        "Sukhbaatar, Sainbayar": "Sukhbaatar",
        "Mnih, Volodymyr": "Mnih",
        "Lillicrap, Timothy P.": "Lillicrap",
        "Gu, Shixiang": "Gu",
        "Schulman, John": "Schulman",
        "Silver, David": "SilverDavid",
        "Silver, Daniel L.": "SilverDaniel",
        "Bengio, Yoshua": "Bengio",
        "Rusu, Andrei A.": "Rusu",
        "Parisotto, Emilio": "Parisotto",
        "Lake, Brenden M.": "Lake",
        "Koch, Gregory": "Koch",
        "Santoro, Adam": "Santoro",
        "Vinyals, Oriol": "Vinyals",
        "Hariharan, Bharath": "Hariharan",
        "Girshick, Ross": "Girshick",
        "Ren, Shaoqing": "Ren",
        "Redmon, Joseph": "Redmon",
        "Liu, Wei": "Liu",
        "Dai, Jifeng": "Dai",
        "He, Gkioxari": "He",
        "Bochkovskiy, Alexey": "Bochkovskiy",
        "Tan, Mingxing": "Tan",
        "Wang, Naiyan": "WangNaiyan",
        "Wang, Lijun": "WangLijun",
        "Held, David": "Held",
        "Bertinetto, Luca": "Bertinetto",
        "Nam, Hyeonseob": "Nam",
        "Farhadi,Ali": "Farhadi",
        "Kulkarni, Girish": "Kulkarni",
        "Donahue, Jeff": "Donahue",
        "Karpathy, Andrej": "Karpathy",
        "Fei Fei F. Li.": "Fei-Fei",
        "Fang, Hao": "Fang",
        "Chen, Xinlei": "Chen",
        "Mao, Junhua": "Mao",
        "Xu, Kelvin": "Xu",
        "Luong, Minh-Thang": "Luong",
        "Koutník, Jan": "Koutník",
        "Levine, Sergey": "Levine",
        "Pinto, Lerrel": "Pinto",
        "Zhu, Yuke": "Zhu",
        "Yahya, Ali": "Yahya",
        "Mirowski, Piotr": "Mirowski",
        "Mordvintsev, Alexander": "Mordvintsev",
        "Olah, Christopher": "Olah",
        "Tyka, Mike": "Tyka",
        "Gatys, Leon A.": "Gatys",
        "Zhu, Jun-Yan": "Zhu",
        "Champandard, Alex J.": "Champandard",
        "Zhang, Richard": "Zhang",
        "Johnson, Justin": "Johnson",
        "Gatys, Leon": "Gatys",
        "Ulyanov, Dmitry": "Ulyanov",
        "Lebedev, Vadim": "Lebedev",
        "(NVIDIA)": "",
        "Pinheiro, P.O.": "Pinheiro",
        "Dai, J.": "Dai",
        "He, K.": "He",
        "Sun, J.": "Sun",
        "Collobert, R.": "Collobert",
        "Dollar, P.": "Dollar",
    }

    print(raw_authors)
    for replace_from, replace_to in replacements.items():
        raw_authors = raw_authors.replace(replace_from, replace_to)

    raw_authors = raw_authors.strip()
    while raw_authors.endswith(".") or raw_authors.endswith("“"):
        raw_authors = raw_authors[:-1]

    raw_authors.sub(r"", raw_authors)

    print(raw_authors)

    authors = raw_authors.split(",")
    authors = [author for author in authors if len(author.strip()) > 0]

    def normalize_author(author):
        author = author.strip()
        fields = author.split()
        author = fields[-1] if len(fields) > 1 else fields[0]
        return author

    return [normalize_author(author) for author in authors]


def extract(readme, download=False):

    section = None
    for line in readme.split("\n"):
        pdf_link = extract_pdf_link(line)
        title, raw_authors = extract_title_and_raw_authors(line)
        year = extract_year(line)
        if pdf_link is not None:
            assert title is not None, f"Could not infer title for line {line}"
            assert year is not None, f"Could not infer year for line {line}"

            print("\n" + line)
            print("Title:", title)
            print("Year:", year)
            authors = extract_authors(raw_authors)
            print("Authors:", authors)

            if download:
                download_url(pdf_link, f"papers/{title}.pdf")


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
    readme = read_readme()
    readme = apply_global_fixes(readme)

    extract(readme)
    # import IPython; IPython.embed()


if __name__ == "__main__":
    main()
