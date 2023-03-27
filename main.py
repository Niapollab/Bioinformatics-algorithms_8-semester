import string
from argparse import ArgumentParser, OPTIONAL
from algorithms import KarpRabinSubstringSearcher, WagnerFischerEditorialDistanceCalculator, EditorialDistanceCalculator, KnuthMorrisPrattSubstringSearcher, SimpleSubstringSearcher, SubstringSearcher
from cli import select_option


ALGORITHMS = {type(s).__name__: s for s in [
    SimpleSubstringSearcher(),
    KnuthMorrisPrattSubstringSearcher(),
    WagnerFischerEditorialDistanceCalculator(),
    KarpRabinSubstringSearcher(len(string.ascii_lowercase), 98321)
]}


def parse_arguments() -> tuple[SubstringSearcher | EditorialDistanceCalculator, str, str]:
    parser = ArgumentParser(
        description='Collection of algorithms for searching in substrings')
    parser.add_argument('algorithm', nargs=OPTIONAL, choices=ALGORITHMS.keys(
    ), help='Algorithm for working with strings')
    parser.add_argument('-t', '--text', help='original text')
    parser.add_argument('-s', '--sub', help='search substring')

    args = parser.parse_args()

    algorithm = ALGORITHMS[args.algorithm] if args.algorithm else ALGORITHMS[select_option(
        *ALGORITHMS.keys())]
    text = args.text if args.text else input('Input text: ')
    sub = args.sub if args.sub else input('Input substring: ')

    return (algorithm, text, sub)


def substring_searcher_handler(substring_searcher: SubstringSearcher, text: str, sub: str) -> None:
    BORDER = '-' * 20

    results = substring_searcher.enumerate_substrings(text, sub)
    for result in results:
        print(f'Comparison count: {result.comp_count}', f'First pass index: {result.pos}', sep='\n', end=BORDER)


def editorial_distance_calculator_handler(editorial_distance_calculator: EditorialDistanceCalculator, first: str, second: str) -> None:
    result = editorial_distance_calculator.get_editorial_distance(first, second)
    print(f'Editorial distance: {result}')


def main(args: tuple[SubstringSearcher | EditorialDistanceCalculator, str, str]) -> None:
    algorithm, text, sub = args

    match algorithm:
        case SubstringSearcher() as substring_searcher:
            substring_searcher_handler(substring_searcher, text, sub)
        case EditorialDistanceCalculator() as editorial_distance_calculator:
            editorial_distance_calculator_handler(editorial_distance_calculator, text, sub)
        case _:
            raise ValueError('Unsupported algorithm type.')


if __name__ == '__main__':
    main(parse_arguments())
