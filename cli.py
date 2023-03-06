from typing import Any, Callable


def select_option(*options: Any, prompt: str = 'Select option: ', error: str = 'An error occurred while selecting an option. Try again.', str_builder: Callable[[Any], str] = lambda x: str(x)) -> Any:
    str_options = [f'{i + 1}. {str_builder(o)}' for i, o in enumerate(options)]
    while True:
        for option in str_options:
            print(option)

        try:
            value = int(input(prompt))

            if value >= 1 and value <= len(str_options):
                return options[value - 1]
        except:
            pass

        print(error)
