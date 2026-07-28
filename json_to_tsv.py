import sys
import json
import argparse
from tabulate import tabulate

def parse_arguments():
    parser = argparse.ArgumentParser(description="Convert JSON to a table with options to exclude columns.")
    parser.add_argument('-e', '--exclude', nargs='+', help="Columns to exclude from the output table", default=[])
    return parser.parse_args()

def json_to_table(exclude_columns):
    # Ler a entrada JSON do stdin
    input_json = sys.stdin.read()
    data = json.loads(input_json)

    # Assumindo que a saída é uma lista de dicionários em data['result']
    results = data.get('result', [])

    if not results:
        print("Nenhum dado encontrado")
        return

    # Filtrar as colunas a serem excluídas
    headers = [key for key in results[0].keys() if key not in exclude_columns]

    # Construir uma lista de linhas para a tabela, excluindo as colunas especificadas
    table = [[result[key] for key in headers] for result in results]

    # Imprimir a tabela usando tabulate
    print(tabulate(table, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    args = parse_arguments()
    json_to_table(args.exclude)

