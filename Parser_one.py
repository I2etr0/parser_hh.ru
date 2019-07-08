import requests
from bs4 import BeautifulSoup as bs
import progressbar

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0(X11;Linux x86_64...)Geco/20100101 Firefox/60.0'}
base_url = 'https://hh.ru/search/vacancy?search_period=3&text=python&area=1&page=0'
out = 'output.txt'


def hh_parse(base_url, headers):
    session = requests.session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
        output_file = open(out, 'w')
        for div in divs:
            title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
            compensation = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
            if compensation == None:
                compensation = 'Не указанно'
            else:
                compensation = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
            href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
            company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
            text1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
            text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
            content = 'Условия:\n' + text1 + '\nТребования к кандидату:\n' + text2
            all = title + '\n' + compensation + '\n' + href + '\n' + company + '\n' + content + '\n\n\n\n\n'
            output_file.write(all)
            print(all)
        output_file.close()


    else:
        print('ERROR')


hh_parse(base_url, headers)

input('Press ENTER to exit')
