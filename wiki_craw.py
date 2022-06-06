from urllib.request import urlopen
from bs4 import BeautifulSoup

def main():

    continue_all = True
    memory = dict()

    while(continue_all):

        title = input("Nazev hledane stranky na wikipedii:")
        print("\n")

        # if title already exists in memory
        if title in memory.keys():
            if memory[title][0] == "1":
                print(memory[title][1])
            else:
                print("Článek s názvem '" + title + "' nebyl nalezen. Zadaný text se vyskytuje v článcích s tímto názvem:")
                for similar_header in memory[title][1:]:
                    print(similar_header)
        else:
            # obtaining resources
            url = 'https://cs.wikipedia.org/w/index.php?search=' + title
            source = urlopen(url).read()
            soup = BeautifulSoup(source,'lxml')

            heading = soup.find_all('h1', attrs={'firstHeading'})[0].text

            # if result is not found
            if heading == "Výsledky hledání":
                memory[title] = []
                memory[title].append("0")
                print("Článek s názvem '" + title + "' nebyl nalezen. Zadaný text se vyskytuje v článcích s tímto názvem:")
                for similar_header in soup.find_all('div', attrs={'mw-search-result-heading'}):
                    memory[title].append(similar_header.text)
                    print(similar_header.text)
                    
            # result is found
            else:
                paragraph = soup.find_all('p')[0].text
                memory[title] = []
                memory[title].append("1")
                memory[title].append(paragraph)
                print(paragraph)

        # ask for repeating
        continue_ending = True
        while(continue_ending):
            input_continue = input("\nPrejes si pokracovat? (y/n):")
            if input_continue == 'n':
                continue_all = False
                continue_ending = False
                print("\nUkonceni programu.")
            elif input_continue == 'y':
                continue_ending = False
            else:
                print("\nSpatny vstup.")


if __name__ == "__main__":
    main()