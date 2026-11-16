# Controle de Vendas | Sales Data Control — DataSolutions

**Projeto de Engenharia e Análise de Dados | Data Engineering and Data Analytics Project**

[Português](#português) | [English](#english)

---

# Português

## 1. Sobre o projeto

O Controle de Vendas é um projeto de Engenharia e Análise de Dados desenvolvido em Python e Pandas, com foco na importação, diagnóstico, validação e tratamento de dados comerciais.

O projeto implementa um fluxo automatizado para identificar inconsistências, aplicar regras de qualidade e separar registros aprovados daqueles que necessitam de análise manual.

A solução preserva os dados originais e mantém a rastreabilidade durante todo o processamento.

## 2. Objetivos

- Importar e analisar arquivos CSV.
- Identificar valores ausentes e registros duplicados.
- Validar identificadores, datas e regras comerciais.
- Identificar quantidades e preços inválidos.
- Separar registros válidos e pendentes.
- Gerar relatórios técnicos automaticamente.
- Validar novamente a base após o tratamento.

## 3. Tecnologias utilizadas

- Python 3
- Pandas
- CSV
- pathlib
- datetime
- Git e GitHub
- Ubuntu Linux

## 4. Estrutura do projeto

```text
controle-vendas/
├── data/
│   ├── vendas_brutas.csv
│   ├── vendas_brutas_backup.csv
│   └── vendas_tratadas.csv
│
├── src/
│   ├── importar_dados.py
│   ├── gerar_relatorio.py
│   ├── validar_dados.py
│   ├── tratar_dados.py
│   └── validar_base_tratada.py
│
├── outputs/
│   ├── relatorio_diagnostico.txt
│   ├── relatorio_validacao.txt
│   ├── registros_pendentes.csv
│   └── relatorio_base_tratada.txt
│
├── README.md
└── requirements.txt
```

## 5. Etapas do processamento

1. **Importação:** leitura do arquivo CSV e verificação da estrutura da base.
2. **Diagnóstico:** identificação de valores ausentes, duplicidades e inconsistências.
3. **Validação:** aplicação de regras de qualidade e regras comerciais.
4. **Tratamento:** separação entre registros aprovados e registros pendentes.
5. **Validação final:** nova verificação da base tratada.
6. **Relatórios:** geração automática de documentos técnicos.

## 6. Resultados obtidos

A base original continha 13 registros e 8 colunas.

| Indicador | Resultado |
|---|---:|
| Registros analisados | 13 |
| Registros aprovados | 7 |
| Registros pendentes | 6 |
| Percentual aprovado | 53,85% |
| Percentual pendente | 46,15% |

A base tratada foi aprovada nas verificações implementadas, sem inconsistências identificadas nos sete registros.

Os seis registros pendentes foram preservados em arquivo separado para análise manual.

## 7. Arquivos gerados

| Arquivo | Finalidade |
|---|---|
| `vendas_brutas.csv` | Base original |
| `vendas_tratadas.csv` | Registros aprovados |
| `registros_pendentes.csv` | Registros para análise manual |
| `relatorio_diagnostico.txt` | Diagnóstico inicial |
| `relatorio_validacao.txt` | Resultado das validações |
| `relatorio_base_tratada.txt` | Validação final |

## 8. Instalação e execução

Crie o ambiente virtual:

```bash
python3 -m venv .venv
```

Ative o ambiente:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Execute os módulos conforme a sequência do processamento:

```bash
python src/importar_dados.py
python src/gerar_relatorio.py
python src/validar_dados.py
python src/tratar_dados.py
python src/validar_base_tratada.py
```

**Observação:** os comandos pressupõem que cada módulo possui uma rotina de execução própria. A sequência deverá ser confirmada com a implementação atual.

## 9. Boas práticas adotadas

- Preservação da base original.
- Não preenchimento de valores ausentes por suposição.
- Não exclusão automática de registros duplicados.
- Separação entre validação e tratamento.
- Rastreabilidade dos registros pendentes.
- Validação independente após o tratamento.

## 10. Próximas melhorias

- Analisar manualmente os registros pendentes.
- Aprimorar a automação do processamento.
- Ampliar os testes automatizados.
- Documentar as regras de tratamento.
- Preparar a publicação do projeto no GitHub.

---

# English

## 1. About the project

Sales Data Control is a Data Engineering and Data Analytics project developed with Python and Pandas, focused on importing, profiling, validating, and cleaning sales data.

The project implements an automated workflow to identify inconsistencies, apply data quality rules, and separate approved records from those requiring manual review.

The solution preserves the original data and maintains traceability throughout the processing workflow.

## 2. Project objectives

- Import and analyze CSV files.
- Identify missing values and duplicate records.
- Validate identifiers, dates, and business rules.
- Identify invalid quantities and unit prices.
- Separate valid records from pending records.
- Automatically generate technical reports.
- Perform a new validation after data cleaning.

## 3. Technologies

- Python 3
- Pandas
- CSV
- pathlib
- datetime
- Git and GitHub
- Ubuntu Linux

## 4. Project structure

```text
controle-vendas/
├── data/
│   ├── vendas_brutas.csv
│   ├── vendas_brutas_backup.csv
│   └── vendas_tratadas.csv
│
├── src/
│   ├── importar_dados.py
│   ├── gerar_relatorio.py
│   ├── validar_dados.py
│   ├── tratar_dados.py
│   └── validar_base_tratada.py
│
├── outputs/
│   ├── relatorio_diagnostico.txt
│   ├── relatorio_validacao.txt
│   ├── registros_pendentes.csv
│   └── relatorio_base_tratada.txt
│
├── README.md
└── requirements.txt
```

## 5. Processing workflow

1. **Data import:** load the CSV file and verify the dataset structure.
2. **Data profiling:** identify missing values, duplicates, and inconsistencies.
3. **Data validation:** apply data quality checks and business rules.
4. **Data cleaning:** separate approved records from pending records.
5. **Final validation:** perform a new validation of the cleaned dataset.
6. **Reporting:** automatically generate technical reports.

## 6. Results

The original dataset contained 13 records and 8 columns.

| Metric | Result |
|---|---:|
| Records analyzed | 13 |
| Approved records | 7 |
| Pending records | 6 |
| Approval rate | 53.85% |
| Pending rate | 46.15% |

The cleaned dataset passed all implemented validation checks, with no identified inconsistencies across the seven approved records.

The six pending records were preserved in a separate file for manual review.

## 7. Generated files

| File | Purpose |
|---|---|
| `vendas_brutas.csv` | Original dataset |
| `vendas_tratadas.csv` | Approved records |
| `registros_pendentes.csv` | Records requiring manual review |
| `relatorio_diagnostico.txt` | Initial profiling report |
| `relatorio_validacao.txt` | Validation report |
| `relatorio_base_tratada.txt` | Final validation report |

## 8. Installation and execution

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the environment:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the modules according to the processing sequence:

```bash
python src/importar_dados.py
python src