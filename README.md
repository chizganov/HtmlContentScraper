# HtmlContentScraper
*HtmlContentScrapper extracts article text from news websites.*

The information available on web pages mostly contains noise like menus, ads and so on. HTML document does not discriminate between the text and the schema that represent the text. This requires to extract core content from websites using software like this one.
This project is a test task. My first project on Python.
### Contents
* [Startup](#startup)
* [Algorithm](#algorithm)
* [Future improvements](#future-improvements)
* [Tests](#tests)
## Startup
```
usage: launcher.py [-h] url

Extract article from website.

positional arguments:
  url         an website url

optional arguments:
  -h, --help  show this help message and exit
```
Launcher creates directory based on url and saves txt file with the extracted information there.
```
chizganov.com/article/index.html -> [CUR_DIR]/chizganov_com/article/index.txt
```
## Algorithm
HtmlContentScraper based on [ECON algorithm](https://songlh.github.io/paper/econ.pdf), but extends it with some changes when backtracking:
* Clear tags that have different classes than snippet-node branch. Most websites have article paragraphs with the same classes
* Allow backtracking with small changes in the text length between levels. Some websites have small noise that interrupt backtracking when it's unnecessary

I made this changes because ECON algorithm shows good results in chinesse websites, but has some problems in russian.
## Future improvements
* Finish current algorithm. Fix different paragraph styles
* Add another algorithm like CoreEx, visual algorithm
* Add template scraper
* Add template html formatter
* Encapsulate parsing mechanism
## Tests
Test urls | Results
----------|----------
[Lenta](https://lenta.ru/news/2018/05/31/passport/) | [link](res/lenta_ru/news/2018/05/31/passport/index.txt)
[Life](https://life.ru/t/%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8/1122126/smi_abramovich_otozval_zaiavku_na_britanskuiu_vizu) | [link](res/life_ru/t/%25D0%25BD%25D0%25BE%25D0%25B2%25D0%25BE%25D1%2581%25D1%2582%25D0%25B8/1122126/smi_abramovich_otozval_zaiavku_na_britanskuiu_vizu.txt)
[Meduza](https://meduza.io/news/2018/05/28/roskomnadzor-prigrozil-narushit-funktsionirovanie-appstore-esli-on-ne-udalit-telegram) | [link](res/meduza_io/news/2018/05/28/roskomnadzor-prigrozil-narushit-funktsionirovanie-appstore-esli-on-ne-udalit-telegram.txt)
[НГС](http://news.ngs.ru/articles/55347451/) | [link](res/news_ngs_ru/articles/55347451/index.txt)
[TVZvezda](https://tvzvezda.ru/news/vstrane_i_mire/content/201806010032-2e98.htm) | [link](res/tvzvezda_ru/news/vstrane_i_mire/content/201806010032-2e98.txt)
[Express](https://www.express.co.uk/news/world/967355/Donald-Trump-USA-EU-trade-war-European-Union-Theresa-May-Emmanuel-Macron) | [link](res/www_express_co_uk/news/world/967355/Donald-Trump-USA-EU-trade-war-European-Union-Theresa-May-Emmanuel-Macron.txt)
[ГазетаРу](https://www.gazeta.ru/comments/2018/05/30_e_11775763.shtml) | [link](res/www_gazeta_ru/business/2018/05/31/11780137.txt)
[Новая газета](https://www.novayagazeta.ru/articles/2018/05/31/76665-ekonomika-krepkih-tylov) | [link](res/www_novayagazeta_ru/articles/2018/05/31/76665-ekonomika-krepkih-tylov.txt)
[NYTimes](https://www.nytimes.com/2018/05/30/technology/google-project-maven-pentagon.html?rref=collection%2Fsectioncollection%2Ftechnology&action=click&contentCollection=technology&region=rank&module=package&version=highlights&contentPlacement=1&pgtype=sectionfront) | [link](res/www_nytimes_com/2018/05/30/technology/google-project-maven-pentagon.txt)
[Свобода](https://www.svoboda.org/a/29262109.html) | [link](res/www_svoboda_org/a/29262109.txt)
[Washington Post](https://www.washingtonpost.com/world/national-security/prosecutors-interview-comey-in-probe-of-his-former-deputy-andrew-mccabe/2018/05/31/1ede31f6-64e1-11e8-99d2-0d678ec08c2f_story.html?utm_term=.70f9c7e650eb) | [link](res/www_washingtonpost_com/world/national-security/prosecutors-interview-comey-in-probe-of-his-former-deputy-andrew-mccabe/2018/05/31/1ede31f6-64e1-11e8-99d2-0d678ec08c2f_story.txt)
[Wylsa](https://wylsa.com/proshhaj-eos-1v-canon-bolshe-ne-budet-prodavat-plenochnye-kamery/) | [link](res/wylsa_com/proshhaj-eos-1v-canon-bolshe-ne-budet-prodavat-plenochnye-kamery/index.txt)

All results in [res folder](https://github.com/chizganov/HtmlContentScraper/tree/master/res).
