import requests
import re
import csv
from bs4 import BeautifulSoup


def scrapping(url: str) -> 'list[str]':
    targetMember = "مسرور احمد شاهاڻي"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        messageContents = soup.find_all('div', class_='messageContent')
        selectedCouplets = []
        for message_content in messageContents:
            text = message_content.get_text()
            author = message_content.find_previous(
                'li', class_='message')['data-author']
            if targetMember in author:
                if "(استاد بخاري)" in text or "استاد بخخاري" in text:
                    text = text.replace("(استاد بخاري)", "").replace(
                        "استاد بخاري", "")
                    couplets = re.split(r'\n\n+', text)
                    selectedCouplets.extend(couplets)
        # for i, couplet in enumerate(selectedCouplets, 1):
        #     print(f"Selected Couplet {i}:\n{couplet.strip()}\n")
        return selectedCouplets
    else:
        return f"Status code: {response.status_code}"


def scrappingBhitai(url: str) -> 'list[str]':
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        startingElement = soup.find(
            'h6', class_='text-info', id=lambda x: x and x.startswith('sur-'))
        selectedCouplets = []
        currentElement = startingElement
        while currentElement:
            stanza = currentElement.find_next('p', class_='_risalo_txt')
            if stanza:
                stanzaLines = stanza.get_text().strip().split('\n')
                if len(stanzaLines) == 2:
                    selectedCouplets.append(stanza.get_text())
            currentElement = currentElement.find_next(
                'h6', class_='text-info', id=lambda x: x and x.startswith('sur-'))
        # for i, couplet in enumerate(selectedCouplets, 1):
        #     print(f"Couplet {i}:\n{couplet}\n")
        return selectedCouplets
    else:
        return f"Status code: {response.status_code}"


def csvWriter(lst: 'list[str]', filePath: str, poetName: str) -> None:
    columns = ["Couplets", "Poet"]
    data = [(couplet, poetName) for couplet in lst]
    with open(filePath, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(data)


def main():
    # url = "https://sindhsalamat.com/threads/18956/"
    # poet = 'Ustad Bukhari'
    # couplets = scrapping(url)
    # print(couplets)
    url = 'https://bhittaipedia.org/risalo-by/gm-shahwani'
    poet = "Shah Bhitai"
    couplets = scrappingBhitai(url)
    filePath = "Data/dataBhitai.csv"
    csvWriter(couplets, filePath, poet)


if __name__ == '__main__':
    main()
