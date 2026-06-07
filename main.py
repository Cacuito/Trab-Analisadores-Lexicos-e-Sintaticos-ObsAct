import sys
from parser import parser

def transpile(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        compiled_code = parser.parse(source_code)
        
        if compiled_code is None:
            print("Erro crítico na compilação. Nenhum código gerado.")
            return

        final_code = "from runtime import *\n\n" + compiled_code
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_code)
            
        print(f"🎉 Sucesso! Arquivo '{input_file}' transpilado para '{output_file}'.")
        
    except FileNotFoundError:
        print(f"Erro: O arquivo '{input_file}' não foi encontrado.")

if __name__ == '__main__':
    if len(sys.argv) > 2:
        transpile(sys.argv[1], sys.argv[2])
    else:
        transpile('teste.obsact', 'saida.py')