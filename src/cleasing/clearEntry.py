import os
from dotenv import load_dotenv
import re
import csv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Define variáveis globais
raw_file = os.getenv("RAW_PATH") + "/" + os.getenv("RAW_FILE_NAME")
prc_entry_file = os.getenv("PROCESSING_PATH") + "/" + os.getenv("PRC_ENTRY_FILE_NAME")



# Função para extraír os lançamentos do extrato
def extractEntries():
    # Leitura do extrato
    with open(raw_file, encoding="iso-8859-1") as file:
        # Retira as linhas iniciais e finais, mantendo somente os lançamentos
        raw_entries = re.sub(r"(Extrato).+|(Data;).+|(\d{2}\/\d{2}\/\d{2};SALDO).+|(;Total)[\s\S]+", '', file.read()).strip()

    
    # Cria arquivo temporário contendo apenas os Lançamentos
    with open(raw_file + "_tmp", "w", newline='', encoding="iso-8859-1") as file:
        file.write(raw_entries)

    # Leitura do arquivo temporário, iterando cada linha e montando o array para a criação do arquivo final    
    line_count = 0
    entry_output = [
        ["dat_lancamento", "operacao", "cod_operacao", "valor_entrada", "valor_saida", "estabelecimento"]
    ]

    with open(raw_file + "_tmp", "r", encoding="iso-8859-1") as file:
        for i, line in enumerate(file):          
            if bool(re.search(r"^\d{2}\/\d{2}\/\d{2};", line)):
                campos = re.split(r";", line)
                list_entry = [campos[0],campos[1].lstrip(),campos[2],campos[3].replace("\"",""),campos[4].replace("\"","")]
                entry_output.append(list_entry)
            else:                
                campos = re.split(r";", line)
                list_entry_ant.insert(5, campos[1])
                del entry_output[-1]
                entry_output.append(list_entry_ant)

            list_entry_ant = list_entry
            list_entry.clear      
        line_count = len(entry_output)                                        

    # Criacao do arquivo com os lançamentos
    with open(prc_entry_file, "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter="|", quoting=csv.QUOTE_ALL)
        writer.writerows(entry_output)

    # Remove arquivo temporário
    os.remove(raw_file + "_tmp")

    return "Total of entries extracted: " + str(line_count)

extractEntries()
