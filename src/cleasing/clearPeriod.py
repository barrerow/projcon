import os
from dotenv import load_dotenv
import re
import csv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Define variáveis globais
raw_file = os.getenv("RAW_PATH") + "/" + os.getenv("RAW_FILE_NAME")
prc_period_file = os.getenv("PROCESSING_PATH") + "/" + os.getenv("PRC_PERIOD_FILE_NAME")

# Função para extraír o período a ser processado
def extractPeriod():
    # Leitura do extrato
    with open(raw_file, encoding="iso-8859-1") as file:
        first_line = file.readline()
        period = re.search(r"(\d{2}\/\d{2}\/\d{4} e \d{2}\/\d{2}\/\d{4})", first_line)
        period_start = re.findall(r"(\d{2}\/\d{2}\/\d{4})", period.group(0))[0]
        period_end = re.findall(r"(\d{2}\/\d{2}\/\d{4})", period.group(0))[1]

        period_output = [
            ["dat_inicio", "dat_fim"],
            [period_start, period_end]
        ]


    # Criacao do arquivo com o período
    with open(prc_period_file, "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter="|", quoting=csv.QUOTE_ALL)
        writer.writerows(period_output)

        
    return period.group(0)

#extractPeriod()
