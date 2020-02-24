from scraper import *
import argparse


def argManagement():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='List of commands')
    parser.add_argument('-f', '--file', required=True)
    parser.add_argument('-r', '--rubric', default=None)
    parser.add_argument('-d', '--date', default=None)
    return parser


def main():
    args = argManagement()
    namespace = args.parse_args()
    path = namespace.file
    rubric = namespace.rubric
    date = namespace.date
    scraper = Scraper("https://lenta.ru/", filename=path, rubric=None, date=date)
    scraper.writeFile()


if __name__ == "__main__":
    main()
