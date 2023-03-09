from argparse import ArgumentParser, OPTIONAL
from algorithms import SimpleSubstringSearcher, SubstringSearcher
from cli import select_option


SUBSTRING_SEARCHERS = {type(s).__name__: s for s in [
    SimpleSubstringSearcher()
]}


def parse_arguments() -> tuple[SubstringSearcher, str, str]:
    parser = ArgumentParser(
        description='Collection of algorithms for searching in substrings')
    parser.add_argument('searcher', nargs=OPTIONAL, choices=SUBSTRING_SEARCHERS.keys(
    ), help='Substring search algorithm')
    parser.add_argument('-t', '--text', help='original text')
    parser.add_argument('-s', '--sub', help='search substring')

    args = parser.parse_args()

    searcher = SUBSTRING_SEARCHERS[args.searcher] if args.searcher else SUBSTRING_SEARCHERS[select_option(
        *SUBSTRING_SEARCHERS.keys())]
    text = args.text if args.text else input('Input text: ')
    sub = args.sub if args.sub else input('Input substring: ')

    return (searcher, text, sub)


def main(args: tuple[SubstringSearcher, str, str]) -> None:
    searcher, text, sub = args
    result = searcher.find_substring(text, sub)

    print(f'Comparison count: {result.comp_count}',
          f'First pass index: {result.pos}', sep='\n')


if __name__ == '__main__':
    main(parse_arguments())
