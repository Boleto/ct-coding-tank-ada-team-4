import argparse

TAM_LINHA = 200  # Tamanho fixo por linha

def parse_linha(linha):
    partes = [parte.strip() for parte in linha.split('|')]
    if len(partes) >= 4:
        return {
            'id': partes[0][3:],  # remove 'ID-'
            'titulo': partes[1],
            'autor': partes[2],
            'code': partes[3]
        }
    return None

def imprimir_registro(reg):
    print(f"id: {reg['id']}")
    print("----")
    print(f"titulo: {reg['titulo']}")
    print(f"autor: {reg['autor']}")
    print(f"code: {reg['code']}")

def busca_binaria_id(caminho_arquivo, id_busca):
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        f.seek(0, 2)
        total_linhas = f.tell() // TAM_LINHA
        ini = 0
        fim = total_linhas - 1

        while ini <= fim:
            meio = (ini + fim) // 2
            f.seek(meio * TAM_LINHA)
            linha = f.read(TAM_LINHA)
            id_linha = linha[:10].strip()

            if id_linha == id_busca:
                reg = parse_linha(linha)
                imprimir_registro(reg)
                return
            elif id_linha < id_busca:
                ini = meio + 1
            else:
                fim = meio - 1

        print("ID não encontrado.")

def busca_intervalo(caminho_arquivo, id_inicio, id_fim):
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        f.seek(0, 2)
        total_linhas = f.tell() // TAM_LINHA

        print(f"ids: {id_inicio[3:]}-{id_fim[3:]}")
        print("----")

        ini = 0
        fim = total_linhas - 1

        # Busca posição inicial (primeiro >= id_inicio)
        while ini <= fim:
            meio = (ini + fim) // 2
            f.seek(meio * TAM_LINHA)
            linha = f.read(TAM_LINHA)
            id_linha = linha[:10].strip()

            if id_linha < id_inicio:
                ini = meio + 1
            else:
                fim = meio - 1

        pos_inicio = ini

        for i in range(pos_inicio, total_linhas):
            f.seek(i * TAM_LINHA)
            linha = f.read(TAM_LINHA)
            id_linha = linha[:10].strip()
            if id_linha > id_fim:
                break
            reg = parse_linha(linha)
            imprimir_registro(reg)
            print("----")

def main():
    parser = argparse.ArgumentParser(description="Knowledge Base CLI")
    parser.add_argument("--file", required=True, help="Arquivo de base de conhecimento (ex: fictional_books.txt)")
    parser.add_argument("--id", help="Buscar um único ID (ex: ID-000123)")
    parser.add_argument("--range", help="Buscar intervalo de IDs (ex: ID-000123:ID-000130)")

    args = parser.parse_args()

    if args.id:
        busca_binaria_id(args.file, args.id)
    elif args.range:
        try:
            id_inicio, id_fim = args.range.split(':')
            busca_intervalo(args.file, id_inicio.strip(), id_fim.strip())
        except ValueError:
            print("Formato de range inválido. Use ID-xxxxx:ID-yyyyy")
    else:
        print("Informe --id ou --range para buscar registros.")

if __name__ == "__main__":
    main()
