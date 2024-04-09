from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from bs4 import BeautifulSoup

import json

# Load HTML
# loader = AsyncChromiumLoader(["https://meine.doag.org/events/javaland/2024/agenda/#eventDay.all"])
# html = loader.load()

with open("javaland-agenda.html","r") as html:

# f.write(html[0].page_content)
# f.close()


    soup = BeautifulSoup(html)
    sessions_html = soup.find_all(class_="agendaEventSlotTeaser")
    print(len(sessions_html))
    print(sessions_html[5])

    import html2text

    h = html2text.HTML2Text()
    h.ignore_links = True
    h.escape_snob = True
    h.drop_white_space = True
    h.wrap_list_items = True
    h.ignore_emphasis = True
    h.wrap_tables = True

    with open('javaland-details.json', 'r') as f:
        details = json.load(f)

    sessions_docs = []
    for session in sessions_html:
        data = session.a.div
        agendaId = session['data-agenda-id']
        detail = next((item for item in details if str(item.get('agendaId')) == agendaId), None)
        if detail:

            if len(data.find(class_="speaker").contents) > 0:
                info = {
                    "speaker": data.find(class_="speaker").contents[0],
                    "title": data.find(class_="BasicText Widget title").contents[0],
                    "day": data.find(class_="day").contents[0],
                    "start": data.find(class_="beginTime").contents[0],
                    "end": data.find(class_="endTime").contents[0],
                    "agenda-id": session['data-agenda-id'],
                    "text":h.handle(detail["textSearch"]),
                    "main_focus": ",".join(detail["main_focus"]),
                    "language_code": detail["languageCode"]
                }
                sessions_docs.append(info)
    print(sessions_docs[0])
    print(len(sessions_docs))


with open('javaland-agenda.json', "w") as file:
    file.write(json.dumps(sessions_docs))