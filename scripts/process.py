from enum import Enum
import os
import re
import sys
import xml.etree.ElementTree as ET

import countrynames
import pandas as pd
import requests


print("Kigali Amendment to the Montreal Protocol")
path = os.path.dirname(os.path.realpath(__file__))
treaty_url = "https://treaties.un.org/doc/Publication/MTDSG/Volume%20II/Chapter%20XXVII/XXVII-2-f.en.xml"
outfile = os.path.join(path, "../data/kigali-amendment.csv")
print("Fetching ", treaty_url)
r = requests.get(treaty_url)

if "urgent maintenance and is currently unavailable" in r.text:
    print("\nNo data found.")
    print(
        "\nMaybe https://treaties.un.org/Pages/ViewDetails.aspx?src=TREATY&mtdsg_no=XXVII-2-f&chapter=27&clang=_en is down?"
    )
    sys.exit()


xml = r.text
tree = ET.fromstring(xml)
columns = tree.find("Treaty/Participants/Table/TGroup/Thead/Row")
rows = tree.find("Treaty/Participants/Table/TGroup/Tbody/Rows")

expected_columns = [
    "Participant",
    "Provisional application under Article V",
    "Acceptance(A), Ratification, Approval(AA)",
]


class ParticipationType(Enum):
    RATIFICATION = "Ratification"
    ACCEPTANCE = "Acceptance"
    APPROVAL = "Approval"
    PROVISIONAL_ARTICLE_V = "Provisional application under Article V"


for i, c in enumerate(columns):
    assert c.text == expected_columns[i]

entries = []
for row in rows:
    # Remove footnotes from country names.
    name = re.sub("<superscript>.</superscript>", "", row[0].text)

    participation_type = None
    if row[1].text is not None:
        participation_type = ParticipationType.PROVISIONAL_ARTICLE_V
        date_col_idx = 1
    elif row[2].text is not None:
        date_col_idx = 2
    else:
        raise ValueError(f"No date found for country {name}")

    date_string = row[date_col_idx].text.replace("\t", "").strip()

    if date_col_idx == 2:
        if date_string.endswith(" A"):
            date_string = date_string[:-2]
            participation_type = ParticipationType.ACCEPTANCE
        elif date_string.endswith(" AA"):
            date_string = date_string[:-3]
            participation_type = ParticipationType.APPROVAL
        else:
            participation_type = ParticipationType.RATIFICATION

    date = pd.to_datetime(date_string)

    # Quickfix for Netherlands
    # TODO fix upstream?
    if name == "Netherlands (Kingdom of the)":
        name = "Netherlands"

    entries.append((name, date, participation_type.value))


df = pd.DataFrame.from_records(entries, columns=("Name", "Date", "Participation Type"))
df.index = df.Name.apply(countrynames.to_code_3)
df.index.name = "Code"

df.to_csv(outfile)

print("Count: {}".format(df.Name.count()))
print("Last five entries:")
print(df.sort_values("Date").tail(5))
