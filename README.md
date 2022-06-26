# py-tpb
TPB Getter.

Small Python module to get search results from The Pirate Bay. Uses 'Selenium' (headless) and 'requests', as well as 'bs4' for parsing.

### **USES SELENIUM WEBDRIVER, SO MAKE SURE TO HAVE IT PROPERLY INSTALLED AND ADDED TO PATH**



Use example:
```
from py-tpb import Getter

results = Getter('search term', limit=3)
magnet = results.tltm.magnet[0]
source = results.page
```
---

## Getter():
- *param* ***search*** str with your search terms
- *param* ***url*** optional, default first result on https://proxy-bay.one/
- *param* ***order*** optional, default 6
- *param* ***cat*** optional, default "all"
- *param* ***limit*** optional, default 1
- *return* None

## Getter().tltm:
- *TLTM* instance of dataclass TLTM containing the name of the top result torrents, their description link, and magnet links

## Getter().tltm.link
- *list* list containing the links of the torrents

## Getter().tltm.name
- *list* list containing the names of the torrents

## Getter().tltm.magnet
- *list* list containing the magnets of the torrents

## Getter().tltm.all
- *list\[tuples]* list containing tuples of the torrents' links, names, and magnets

## Getter.page:
- *str* html page of TPB search results page

## Getter.top_link_title_magnet():
- *param* ***url*** str with the TPB proxy url
- *param* ***source*** html page
- *return* list\[str] = \[name, link, magnet]

## Getter.top_proxy():
- *return* url of first result on https://proxy-bay.one/
