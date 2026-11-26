# DataSolutions — Controle e Qualidade de Dados de Vendas
# DataSolutions — Sales Data Control and Quality

---

# Português

## 1. Sobre o projeto

Projeto de Engenharia e Qualidade de Dados desenvolvido em Python e Pandas para simular uma rotina profissional de processamento de dados comerciais.

O sistema realiza importação, validação, auditoria, tratamento e aprovação de uma base de vendas, identificando inconsistências e separando registros válidos daqueles que precisam de análise.

O projeto também gera relatórios técnicos, mantém um histórico de execução e utiliza testes automatizados para verificar a confiabilidade do processamento.

## 2. Objetivos

- Automatizar a importação de dados comerciais.
- Identificar inconsistências e problemas de qualidade.
- Validar identificadores, datas e regras comerciais.
- Auditar a base original.
- Separar registros válidos e pendentes.
- Validar independentemente a base tratada.
- Gerar relatórios técnicos.
- Manter rastreabilidade das execuções.
- Verificar a confiabilidade por meio de testes automatizados.

## 3. Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python 3.12 | Desenvolvimento |
| Pandas | Manipulação e tratamento de dados |
| CSV | Armazenamento de dados |
| Pytest | Testes automatizados |
| Git | Controle de versão |
| GitHub | Hospedagem e integração contínua |
| GitHub Actions | Automação de testes |

## 4. Estrutura do projeto

```text
DataSolutions/
├── README.md
├── requirements.txt
└── controle-vendas/
    ├── data/
    │   ├── vendas_brutas.csv
    │   ├── vendas_brutas_backup.csv
    │   └── vendas_tratadas.csv
    │
    ├── outputs/
    │   ├── historico_execucoes.csv
    │   ├── registros_pendentes.csv
    │   ├── relatorio_auditoria.txt
    │   ├── relatorio_auditoria_teste.txt
    │   ├── relatorio_base_tratada.txt
    │   ├── relatorio_diagnostico.txt
    │   ├── relatorio_testes.txt
    │   ├── relatorio_testes_integracao.txt
    │   ├── relatorio_validacao.txt
    │   ├── resultado_integracao.xml
    │   └── resultado_testes.xml
    │
    ├── src/
    │   ├── auditoria_dados.py
    │   ├── executar_pipeline.py
    │   ├── executar_pipeline_backup.py
    │   ├── gerar_relatorio.py
    │   ├── importar_dados.py
    │   ├── registrar_log.py
    │   ├── tratar_dados.py
    │   ├── validar_base_tratada.py
    │   └── validar_dados.py
    │
    ├── tests/
    │   ├── __init__.py
    │   ├── test_falhas.py
    │   ├── test_historico_falhas.py
    │   ├── test_importacao.py
    │   ├── test_pipeline.py
    │   └── test_validar_dados.py
    │
    ├── .gitignore
    └── requirements.txt
```

## 5. Arquitetura e responsabilidades dos módulos

| Módulo | Responsabilidade |
|---|---|
| importar_dados.py | Importação da base CSV e identificação de cabeçalhos repetidos |
| validar_dados.py | Validação de identificadores, datas e regras comerciais |
| auditoria_dados.py | Auditoria da qualidade dos dados |
| gerar_relatorio.py | Geração do relatório de validação |
| tratar_dados.py | Identificação de pendências e separação dos registros |
| validar_base_tratada.py | Validação independente da base tratada |
| registrar_log.py | Registro do histórico de execução |
| executar_pipeline.py | Orquestração do processamento completo |
| executar_pipeline_backup.py | Versão histórica do pipeline, não utilizada como entrada oficial |

## 6. Fluxo de processamento

O pipeline principal é organizado em cinco etapas:

1. Importação dos dados.
2. Validação e auditoria da base original.
3. Tratamento e separação dos registros.
4. Validação independente da base tratada.
5. Geração dos relatórios e registro da execução.

### Fluxo simplificado

```text
Base original (CSV)
        |
        v
Importação
        |
        v
Validação e auditoria
        |
        v
Tratamento dos dados
        |
        +----------------------+
        |                      |
        v                      v
Registros válidos       Registros pendentes
        |
        v
Validação da base tratada
        |
        v
Relatórios finais
        |
        v
Histórico de execução
```

## 7. Regras de tratamento

O sistema identifica inconsistências como:

- Identificadores ausentes ou duplicados.
- Registros integralmente duplicados.
- Datas ausentes ou inválidas.
- Quantidades ausentes, não numéricas ou menores ou iguais a zero.
- Preços ausentes, não numéricos ou menores ou iguais a zero.
- Campos obrigatórios vazios.

Os registros inconsistentes são separados para análise, acompanhados dos motivos das pendências.

O tratamento não realiza preenchimentos ou exclusões automáticas dos registros inconsistentes.

A base original é mantida separada da base tratada.

## 8. Relatórios e histórico de execução

O projeto gera arquivos para documentar os resultados do processamento.

| Arquivo | Finalidade |
|---|---|
| vendas_tratadas.csv | Registros considerados válidos |
| registros_pendentes.csv | Registros que precisam de análise |
| relatorio_validacao.txt | Resultado da validação da base original |
| relatorio_auditoria.txt | Resultado da auditoria |
| relatorio_base_tratada.txt | Resultado da validação final |
| historico_execucoes.csv | Histórico das execuções do pipeline |

O histórico registra informações como data, horário, quantidade de registros importados, válidos, pendentes e aprovados, além dos status da validação e da execução e eventuais mensagens de erro.

## 9. Instalação

### Requisitos

- Python 3.12 ou compatível.
- Git.

Clone o repositório:

```bash
git clone https://github.com/vitor1914/DataSolutions.git
```

Acesse a pasta do projeto:

```bash
cd DataSolutions/controle-vendas
```

Crie o ambiente virtual:

```bash
python3 -m venv .venv
```

Ative o ambiente virtual no Linux:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## 10. Execução do pipeline

Na raiz da pasta `controle-vendas`, execute:

```bash
python src/executar_pipeline.py
```

A entrada principal do processamento é:

```text
data/vendas_brutas.csv
```

Os arquivos gerados são armazenados nas pastas `data/` e `outputs/`.

## 11. Testes automatizados

Execute os testes com:

```bash
python -m pytest -v
```

A suíte contempla testes de:

- Importação de dados.
- Validação de registros.
- Regras comerciais.
- Tratamento de falhas.
- Execução do pipeline.
- Histórico de execuções.
- Preservação da base original.

### Resultado da execução de 26/11/2026

```text
24 passed in 0.76s
```

Todos os 24 testes foram aprovados nessa execução.

## 12. Controle de versão e integração contínua

O projeto utiliza Git e GitHub para controle de versão e armazenamento do código.

A automação de testes é realizada por meio do GitHub Actions, permitindo verificar a integridade do projeto durante o fluxo de integração contínua.

O arquivo `.gitignore` exclui ambientes virtuais, arquivos temporários, caches e arquivos locais que não devem ser versionados.

## 13. Considerações finais

A DataSolutions utiliza este projeto como simulação de uma rotina profissional de Engenharia e Qualidade de Dados.

O sistema demonstra a aplicação prática de importação, validação, auditoria, tratamento, testes automatizados e rastreabilidade de processamento.

---

# English

## 1. About the Project

A Data Engineering and Data Quality project developed with Python and Pandas to simulate a professional business data processing workflow.

The system performs data import, validation, auditing, processing, and approval of a sales dataset, identifying inconsistencies and separating valid records from those requiring further analysis.

The project also generates technical reports, maintains an execution history, and uses automated tests to verify processing reliability.

## 2. Objectives

- Automate business data imports.
- Identify inconsistencies and data quality issues.
- Validate identifiers, dates, and business rules.
- Audit the original dataset.
- Separate valid and pending records.
- Independently validate the processed dataset.
- Generate technical reports.
- Maintain execution traceability.
- Verify reliability through automated testing.

## 3. Technologies

| Technology | Application |
|---|---|
| Python 3.12 | Development |
| Pandas | Data manipulation and processing |
| CSV | Data storage |
| Pytest | Automated testing |
| Git | Version control |
| GitHub | Code hosting and continuous integration |
| GitHub Actions | Test automation |

## 4. Project Structure

The project is organized into four main areas:

- `data/`: original, backup, and processed datasets.
- `src/`: application modules and processing pipeline.
- `tests/`: automated test suite.
- `outputs/`: reports, pending records, and execution history.

## 5. Module Responsibilities

| Module | Responsibility |
|---|---|
| importar_dados.py | CSV import and repeated header identification |
| validar_dados.py | Identifier, date, and business rule validation |
| auditoria_dados.py | Data quality auditing |
| gerar_relatorio.py | Validation report generation |
| tratar_dados.py | Pending record identification and data separation |
| validar_base_tratada.py | Independent validation of the processed dataset |
| registrar_log.py | Execution history recording |
| executar_pipeline.py | Full processing orchestration |
| executar_pipeline_backup.py | Historical pipeline version, not used as the official entry point |

## 6. Processing Workflow

The main pipeline consists of five stages:

1. Data import.
2. Original dataset validation and auditing.
3. Data processing and record separation.
4. Independent validation of the processed dataset.
5. Report generation and execution history recording.

### Simplified Workflow

```text
Original Dataset (CSV)
        |
        v
Data Import
        |
        v
Validation and Auditing
        |
        v
Data Processing
        |
        +----------------------+
        |                      |
        v                      v
Valid Records           Pending Records
        |
        v
Processed Dataset Validation
        |
        v
Final Reports
        |
        v
Execution History
```

## 7. Data Processing Rules

The system identifies inconsistencies such as:

- Missing or duplicated identifiers.
- Fully duplicated records.
- Missing or invalid dates.
- Missing, non-numeric, or non-positive quantities.
- Missing, non-numeric, or non-positive prices.
- Empty mandatory fields.

Inconsistent records are separated for further analysis, with their respective pending reasons.

The processing workflow does not automatically fill in or delete inconsistent records.

The original dataset remains separate from the processed dataset.

## 8. Reports and Execution History

The project generates files to document processing results.

| File | Purpose |
|---|---|
| vendas_tratadas.csv | Records considered valid |
| registros_pendentes.csv | Records requiring further analysis |
| relatorio_validacao.txt | Original dataset validation report |
| relatorio_auditoria.txt | Data auditing report |
| relatorio_base_tratada.txt | Final processed dataset validation report |
| historico_execucoes.csv | Pipeline execution history |

The execution history records information such as date, time, imported records, valid records, pending records, approved records, validation and execution statuses, and error messages.

## 9. Installation

### Requirements

- Python 3.12 or compatible.
- Git.

Clone the repository:

```bash
git clone https://github.com/vitor1914/DataSolutions.git
```

Access the project directory:

```bash
cd DataSolutions/controle-vendas
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## 10. Pipeline Execution

From the `controle-vendas` project directory, run:

```bash
python src/executar_pipeline.py
```

The main input file is:

```text
data/vendas_brutas.csv
```

Generated files are stored in the `data/` and `outputs/` directories.

## 11. Automated Tests

Run the test suite with:

```bash
python -m pytest -v
```

The test suite covers:

- Data import.
- Record validation.
- Business rules.
- Failure handling.
- Pipeline execution.
- Execution history.
- Original dataset preservation.

### Test execution result — November 26, 2026

```text
24 passed in 0.76s
```

All 24 tests passed in that execution.

## 12. Version Control and Continuous Integration

The project uses Git and GitHub for version control and code hosting.

Automated testing is performed through GitHub Actions, helping verify project integrity during the continuous integration workflow.

The `.gitignore` file excludes virtual environments, temporary files, caches, and local files that should not be versioned.

## 13. Final Considerations

DataSolutions uses this project to simulate a professional Data Engineering and Data Quality workflow.

The system demonstrates practical applications of data import, validation, auditing, processing, automated testing, and execution traceability.
