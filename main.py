from scraper import *
import sys
import argparse

def argManagement():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='List of commands')
    # A list command
    list_parser = subparsers.add_parser('list', help='List contents')
    list_parser.add_argument('dirname', action='store', help='Directory to list')
    # A create command
    create_parser = subparsers.add_parser('create', help='Create a directory')
    create_parser.add_argument('dirname', action='store', help='New directory to create')
    create_parser.add_argument('--read-only', default=False, action='store_true',
                               help='Set permissions to prevent writing to the directory',
                               )

def main():
    usage = f"""\033[1m \033[91m  Usage: python3 main.py --file=path_to_out_file --rubric=type_of_post --date=date  \033[0m 
    --rubric and --date are optional args"""
    if len(sys.argv) == 1:
        print(usage)
        exit()

    scraper = Scraper("https://lenta.ru/", filename="example.txt", rubric="articles")
    print(scraper.getUrlList()[0])
    print()
    print(Post(scraper.getUrlList()[0]).headline())
    print()
    print(Post(scraper.getUrlList()[0]).content())
    # with open("./example.txt", "w") as outfile:
    #     for n in scraper.getUrlList():
    #         outfile.write(Post(n).content.text)


if __name__ == "__main__":
    main()
