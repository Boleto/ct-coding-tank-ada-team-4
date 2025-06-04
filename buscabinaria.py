import argparse
import re
import os

TAM_LINHA = 201  # 200 chars + \n

def parse_linha(linha):
    """Garante que a linha tem todos os campos antes de retornar um registro."""
    linha = linha.rstrip('\n').strip()  # Remove \n e espaços extras
    if not linha:  # Se a linha estiver vazia, ignora
        return None
    
    partes = [parte.strip() for parte in linha.split('|')]
    if len(partes) < 4:  # Se não tiver todos os campos, ignora
        return None
    
    # Extrai o ID corretamente (usando regex para garantir)
    id_match = re.search(r'ID-(\d{6})', partes[0])
    if not id_match:  # Se não encontrar um ID válido, ignora
        return None
    
    return {
        'id': id_match.group(1),  # Pega só os dígitos (000123)
        'titulo': partes[1],
        'autor': partes[2],
        'code': partes[3]
    }

def imprimir_registro(reg):
    """Formata a saída conforme especificado"""
    print(f"id: {reg['id']}")
    print("----")
    print(f"titulo: {reg['titulo']}")
    print(f"autor: {reg['autor']}")
    print(f"code: {reg['code']}")

def extrair_id(linha):
    """Extrai o ID de uma linha usando regex"""
    match = re.search(r'ID-(\d{6})', linha)
    return match.group(0) if match else None

def busca_binaria_id(caminho_arquivo, id_busca):
    """Busca binária por um ID exato"""
    id_busca = id_busca.upper()  # Garante consistência
    
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        file_size = os.path.getsize(caminho_arquivo)
        total_linhas = file_size // TAM_LINHA
        ini, fim = 0, total_linhas - 1

        while ini <= fim:
            meio = (ini + fim) // 2
            f.seek(meio * TAM_LINHA)
            linha = f.read(TAM_LINHA)
            
            id_linha = extrair_id(linha)
            if not id_linha:
                continue

            if id_linha == id_busca:
                reg = parse_linha(linha)
                if reg:
                    imprimir_registro(reg)
                    return
            elif id_linha < id_busca:
                ini = meio + 1
            else:
                fim = meio - 1

        print("ID não encontrado.")

def busca_intervalo(caminho_arquivo, id_inicio, id_fim):
    """Busca por intervalo, exibindo apenas registros válidos."""
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        file_size = os.path.getsize(caminho_arquivo)
        total_linhas = file_size // TAM_LINHA

        print(f"ids: {id_inicio[3:]}-{id_fim[3:]}")
        print("----")

        encontrados = 0
        for i in range(total_linhas):
            f.seek(i * TAM_LINHA)
            linha = f.read(TAM_LINHA)
            id_linha = extrair_id(linha)  # Extrai o ID usando regex

            if not id_linha:  # Se não tem ID, pula
                continue

            if id_inicio <= id_linha <= id_fim:  # Se está no intervalo
                reg = parse_linha(linha)
                if reg:  # Só exibe se o registro for válido
                    imprimir_registro(reg)
                    print("----")
                    encontrados += 1
            elif id_linha > id_fim:  # Se passou do intervalo, para
                break

        if encontrados == 0:
            print("Nenhum registro encontrado no intervalo.")

def main():
    parser = argparse.ArgumentParser(description="Knowledge Base CLI")
    parser.add_argument("--file", required=True, 
                       help="Arquivo de base de conhecimento (ex: fictional_books_fixed.txt)")
    parser.add_argument("--id", 
                       help="Buscar um único ID (ex: ID-000123)")
    parser.add_argument("--range", 
                       help="Buscar intervalo de IDs (ex: ID-000123:ID-000130)")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print("Arquivo não encontrado!")
        return

    if args.id:
        if not re.fullmatch(r'ID-\d{6}', args.id, re.IGNORECASE):
            print("Formato de ID inválido. Use ID-xxxxxx (6 dígitos)")
            return
        busca_binaria_id(args.file, args.id)
    elif args.range:
        try:
            id_inicio, id_fim = args.range.split(':')
            if not (re.fullmatch(r'ID-\d{6}', id_inicio.strip(), re.IGNORECASE) and 
                    re.fullmatch(r'ID-\d{6}', id_fim.strip(), re.IGNORECASE)):
                print("Formato de ID inválido. Use ID-xxxxxx (6 dígitos)")
                return
            busca_intervalo(args.file, id_inicio.strip(), id_fim.strip())
        except ValueError:
            print("Formato de range inválido. Use ID-xxxxxx:ID-yyyyyy")
    else:
        print("Informe --id ou --range para buscar registros.")

if __name__ == "__main__":
    main()
