from util_package import *
import wikipedia
wikipedia.set_lang("zh-tw")
import wikitextparser as wtp
print("wiki crawler and wiki parser loaded was imported!")


print("get_pages_from_wiki(site_name, stopwords)")

def get_pages_from_wiki(site_name, stopwords):
    # given a site name, the function will return the wikipage object define
    # by wikipedia
    tokens = tokenize(site_name, stopwords)
    count = 0
    no_page = True
    pages = dict()
    for term in generate_combination(tokens):
        count = count + 1
        try:
            page = wikipedia.page(term)
            if(page.title == term):
                pages[page.title] = page
                print(term)
                print(page.title)
        except:
            None
    return pages

print("convert_to_strings(wikipage)")
def convert_to_strings(wikipage):
    # given a wikipage object, the function will return a structurlized
    # dictionary that holds all information from a wikipage.
    from hanziconv import HanziConv
    import wikitextparser as wtp
    import pprint
    try:
        summary = HanziConv.toTraditional(
            wtp.parse(wikipage.content).sections[0].pprint())
    except:
        summary = None
    try:
        sections = [HanziConv.toTraditional(
            sec.pprint()) for sec in wtp.parse(wikipage.content).sections[1:]]
        try:
            sub_titles = [HanziConv.toTraditional(
                sec.title[1:-1]) for sec in wtp.parse(wikipage.content).sections[1:]]
        except:
            sub_titles = None
        try:
            section_content = [s[s.find('\n') + 1:] for s in sections]
        except:
            section_content = None
    except:
        sections = None

    try:
        sections = list(zip(sub_titles, section_content))
    except:
        sections = None
    try:
        links = wikipage.links
    except:
        links = None
    return {'title': wikipage.title, 'summary': summary, 'sections': sections, 'links': links}
