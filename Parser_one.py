import csv

import requests
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

baseUrl = 'https://perm.hh.ru/search/vacancy?text=python&only_with_salary=false&clusters=true&enable_snippets=true&page=0'


def hhParse(baseUrl, headers):
    jobs = []   # Создаем список для заполнения его вакансиями
    urls = []   # Создаем список для заполнения его урлами
    urls.append(baseUrl)
    session = requests.Session()
    request = session.get(baseUrl, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'https://perm.hh.ru/search/vacancy?text=python&only_with_salary=false&clusters=true&enable_snippets=true&page={i}'
                if url not in urls:
                    urls.append(url)

        except:
            pass
    for url in urls:
        request = session.get(url, headers=headers)
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
        for div in divs:
            try:
                title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text    # Выборка заголовков работ
                href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']      # Выборка ссылок на работу
                company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text       # Выборка компаний-поисковиков
                text1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text     # Выборка что нужно делать
                text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text        # ВЫборка опыта
                content = 'Требования: ' + text1 + '\n' + 'Опыт: ' + text2
                jobs.append({
                    'title': title,
                    'href': href,
                    'company': company,
                    'content': content})
            except:
                pass
        print(len(jobs)) # Сколько работ нашлось

    else:
        print("ERROR or Done! " + str(request.status_code))
    return jobs


def fileWriter(jobs):
    with open('parsedJobs.csv', 'w') as file:  # Работа с файлом .cvs 'w' означает, что файл постоянно записывается
        aPen = csv.writer(file)
        aPen.writerow(('Название вакансии', 'URL', 'Название компании', 'Описание'))
        for job in jobs:
            aPen.writerow((job['title'], job['href'], job['company'], job['content']))

jobs = hhParse(baseUrl, headers)
fileWriter(jobs)
