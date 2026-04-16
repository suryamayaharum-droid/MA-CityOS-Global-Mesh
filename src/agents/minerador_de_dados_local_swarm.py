import os
import sys

def count_lines(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return sum(1 for line in f)
    except Exception as e:
        print(f"Erro ao processar {filepath}: {e}")
        return -1

def main():
    directory = 'macityos'
    total_files = 0
    total_lines = 0

    try:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)

            if os.path.isfile(filepath):
                total_files += 1
                line_count = count_lines(filepath)

                if line_count != -1:
                    print(f"{filename}: {line_count} linhas")
                    total_lines += line_count

        print(f"\nTotal de arquivos: {total_files}")
        print(f"Total de linhas: {total_lines}")

    except FileNotFoundError:
        print(f"Diretório '{directory}' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


if __name__ == "__main__":
    main()