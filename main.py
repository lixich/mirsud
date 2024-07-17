import logging

import pandas as pd

from parser import Parser
from transformer import HtmlTransformer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def main() -> None:
    parser = Parser()
    results = []
    for html in parser.run():
        transformer = HtmlTransformer(html)
        row = transformer.run()
        results.append(row)

    df = pd.DataFrame(results)
    df.to_csv('results.csv', index=False, encoding='utf-8')


if __name__ == '__main__':
    main()
