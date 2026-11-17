# DataSolutions — Controle e Qualidade de Dados de Vendas

## Português

### Sobre o projeto

Projeto de Análise de Dados desenvolvido com Python e Pandas para simular uma rotina profissional de importação, validação, tratamento e controle de qualidade de dados comerciais.

O objetivo é identificar inconsistências em uma base de vendas, separar registros válidos e pendentes e gerar relatórios que documentem os resultados do processo.

### Tecnologias utilizadas

- Python
- Pandas
- Pytest
- CSV
- Git e GitHub

### Estrutura do projeto

```text
controle-vendas/
├── data/
│   ├── vendas_brutas.csv
│   ├── vendas_brutas_backup.csv
│   └── vendas_tratadas.csv
├── src/
│   ├── importar_dados.py
│   ├── gerar_relatorio.py
│   ├── validar_dados.py
│   ├── tratar_dados.py
│   └── validar_base_tratada.py
├── tests/
│   ├── __init__.py
│   └── test_validar_dados.py
├── outputs/
│   ├── registros_pendentes.csv
│   ├── relatorio_diagnostico.txt
│   ├── relatorio_validacao.txt
│   ├── relatorio_base_tratada.txt
│   ├── relatorio_testes.txt
│   └── resultado_testes.xml
├── README.md
└── requirements.txt
```

### Funcionalidades implementadas

1. Importação da base de vendas em CSV.
2. Identificação de inconsistências nos dados.
3. Validação de identificadores e datas.
4. Verificação de campos obrigatórios.
5. Validação de quantidades e preços.
6. Separação entre registros válidos e pendentes.
7. Geração de relatórios de diagnóstico e validação.
8. Validação independente da base tratada.
9. Testes automatizados com Pytest.

### Tratamento dos dados

A base original contém 13 registros.

Após a validação:

- 7 registros foram considerados válidos.
- 6 registros foram encaminhados para análise de pendências.

Os registros inconsistentes foram preservados em um arquivo separado, acompanhados da identificação da linha de origem e do motivo da pendência.

Nenhum dado original foi sobrescrito. Não foram realizados preenchimentos ou exclusões automáticas de registros.

### Testes automatizados

Foram implementados 9 testes independentes com Pytest, utilizando pequenos DataFrames para simular diferentes cenários.

Os testes verificam:

- Identificação de IDs duplicados.
- Identificação de IDs ausentes.
- Identificação de datas inválidas.
- Identificação de quantidades negativas.
-