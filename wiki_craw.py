import signal
import time
import readchar
from urllib.request import urlopen
from bs4 import BeautifulSoup


BASE_URL = 'https://cs.wikipedia.org/w/index.php?search='

def output(text):
    """ Sends resulting text to output """
    print(text)

def handler(signum, frame):
    """ Ctrl+c handler """
    res = input("Bylo stisknuto Ctrl-c. Prejes si ukoncit program? ano/ne ")
    if res == 'ano':
        exit(1)

def crawling(memory, title):
    """ Sends resulting text from crawling to output """
    # obtaining resources
    url = BASE_URL + title
    try:
        source = urlopen(url).read()
    except:
        output("Nelze cist url. Ukonceni programu.")
        exit(1)
    soup = BeautifulSoup(source,'lxml')

    heading = soup.find_all('h1', attrs={'firstHeading'})[0].text

    # if result is not found
    if heading == "Výsledky hledání":
        memory[title] = ["0"]
        output("Článek s názvem '" + title + "' nebyl nalezen. Zadaný text se vyskytuje v článcích s tímto názvem:")
        for similar_header in soup.find_all('div', attrs={'mw-search-result-heading'}):
            memory[title].append(similar_header.text)
            output(similar_header.text)
            
    # result is found
    else:
        paragraph = soup.find_all('p')[0].text
        memory[title] = ["1"]
        memory[title].append(paragraph)
        output(paragraph)

def get_memory_text(memory, title):
    """ Sends resulting text from memory to output """
    if memory[title][0] == "1":
        output(memory[title][1])
    else:
        output("Článek s názvem '" + title + "' nebyl nalezen. Zadaný text se vyskytuje v článcích s tímto názvem:")
        for similar_header in memory[title][1:]:
            output(similar_header)


def get_text(memory, title):
    """ Sends resulting text from memory or crawling to output """
    # if title already exists in memory
    if title in memory:
        get_memory_text(memory, title)
        
    else:
        crawling(memory, title)
        
def main():

    continue_all = True
    memory = dict()

    signal.signal(signal.SIGINT, handler)

    while(continue_all):

        title = ''
        try:
            title = input("Nazev hledane stranky na wikipedii:")
        except RuntimeError:
            pass
        output("\n")
        
        if title:
            title = title.lower()
            get_text(memory, title)

        else:
            output("Prazdny vstup")

        # ask for repeating
        continue_ending = True
        while(continue_ending):
            input_continue = ''
            try:
                input_continue = input("\nPrejes si pokracovat? (ano/ne):")
            except RuntimeError:
                pass

            input_continue = input_continue.lower()
            if input_continue == 'ne':
                continue_all = False
                continue_ending = False
                output("\nUkonceni programu.")

            elif input_continue == 'ano':
                continue_ending = False
            else:
                output("\nSpatny vstup.")


if __name__ == "__main__":
    main()