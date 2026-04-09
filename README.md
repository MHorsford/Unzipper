# Unzipper

Ferramenta para descompactação recursiva e automática de arquivos ZIP encadeados. Processa múltiplas camadas de arquivos comprimidos com backup automático e arquivamento seguro.

## Sobre

Unzipper foi desenvolvido para lidar com estruturas complexas de arquivos ZIP aninhados. A ferramenta automatiza o processo de extração recursiva, mantendo o histórico de transformações e garantindo a segurança dos dados originais através de backup automático.

## Features Atuais

- Descompactação recursiva de arquivos ZIP encadeados
- Mapeamento automático de estrutura de extração (scan)
- Extração automática com processamento em múltiplas iterações
- Backup automático da estrutura original
- Arquivamento de arquivos processados
- Rastreamento de status de cada arquivo ZIP
- Suporte a caminhos absolutos e relativos

## Features em Desenvolvimento

- Logging detalhado com salvamento em arquivo
- Pausa segura por níveis de profundidade
- Sistema de restauração de backup
- Comparação por hash para verificação de integridade
- Alertas e tratamento avançado de erros

## Requisitos

- Python 3.8+
- Bibliotecas padrão: `os`, `zipfile`, `pathlib`, `shutil`

## Instalação

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/Unzipper.git
cd Unzipper

# Criar ambiente virtual (opcional mas recomendado)
python -m venv venv

# Ativar ambiente virtual
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

## Como Usar

### Uso Básico

```python
from Unzipper import Unzipper

# Criar instância do Unzipper
uz = Unzipper(
    source_folder="caminho/para/arquivos_zip",
    destination_folder="caminho/para/destino"
)

# Mapear estrutura (sem extrair ainda)
uz.scan()

# Extrair arquivos (automático e recursivo)
uz.extract()
```

### Com Caminhos Completos

```python
from Unzipper import Unzipper
from pathlib import Path

uz = Unzipper(
    source_folder=r"C:\Users\horsf\Documents\Projetos\Unzipper\Teste",
    destination_folder=r"C:\Users\horsf\Documents\Projetos\Unzipper\Destino_Temp"
)

uz.scan()
uz.extract()
```

### Extrair no Mesmo Local (padrão)

```python
# Se destination_folder não for informado, usa a mesma pasta de source
uz = Unzipper(source_folder="arquivos")
uz.scan()
uz.extract()
```

## Estrutura do Projeto

```
Unzipper/
├── Unzipper.py              # Classe principal
├── README.md                # Este arquivo
├── .gitignore               # Configuração Git
├── process/
│   ├── backup/              # Backup automático da estrutura original
│   ├── archived/            # Arquivos ZIP já processados
│   └── log/                 # Logs (futuro)
├── teste/                   # Estrutura de teste
└── Destino_Temp/            # Saída padrão de testes
```

## API da Classe Unzipper

### ` __init__(source_folder, destination_folder=None, MAX_DEPTH=None)`

Inicializa a instância do Unzipper.

**Parâmetros:**
- `source_folder` (str | Path): Caminho para pasta com arquivos ZIP
- `destination_folder` (str | Path | None): Onde extrair; se None, usa source_folder
- `MAX_DEPTH` (int | None): Limite de profundidade (desenvolvimento futuro)

**Comportamento:**
- Cria pastas se não existirem
- Faz backup automático da estrutura original em `process/backup/`
- Cria diretório `process/archived/` para arquivos processados

### `scan(source_path=None)`

Mapeia todos os arquivos ZIP encontrados recursivamente.

```python
uz.scan()  # Usar source_path padrão
# OU
uz.scan(source_path="subcaminho/especifico")
```

**O que faz:**
- Procura por todos os arquivos `.zip` usando `rglob()`
- Cria plano de extração com destino calculado
- Define status inicial como "pending"
- Exibe estrutura completa do plano

### `extract()`

Executa a extração automática e recursiva.

```python
uz.extract()
```

**O que faz:**
- Extrai todos os arquivos com status "pending"
- Move arquivos ZIP processados para `process/archived/`
- Procura novos ZIPs na pasta de destino
- Repete processo recursivamente até não haver mais ZIPs
- Trata erros de forma silenciosa (futuro: logging)

## Fluxo de Funcionamento

```
1. Inicializar Unzipper
   └── Cria backup automático

2. Executar scan()
   └── Mapeia todos os ZIPs
   └── Cria plano de extração

3. Executar extract()
   └── Extrai primeiras camadas
   └── Move ZIPs para archived
   └── Procura novos ZIPs no destino
   └── Repete até não haver mais ZIPs
```

## Estrutura de Dados Interna

### extraction_plan

Dicionário contendo informações de cada arquivo ZIP:

```python
{
    Path('arquivo.zip'): {
        'Item': Path('caminho/arquivo.zip'),
        'Destination': Path('caminho/destino/arquivo'),
        'Status': 'pending'|'extracted',
        'Error': None|'mensagem de erro'
    },
    ...
}
```

## Exemplo Completo

```python
from Unzipper import Unzipper

# Configuração
uz = Unzipper(
    source_folder="C:/dados/zips",
    destination_folder="C:/dados/extraidos"
)

# Mapear estrutura
print("Mapeando arquivos...")
uz.scan()

# Processar
print("Iniciando extração...")
uz.extract()

print("Processo concluído!")
print(f"Pasta de backup: {uz.backup_path}")
print(f"Arquivos processados: {uz.archived_path}")
```

## Diretórios Criados Automaticamente

| Diretório | Função |
|-----------|--------|
| `process/backup/` | Backup da estrutura original antes de qualquer processamento |
| `process/archived/` | Arquivos ZIP já descompactados |
| `process/log/` | Logs de operação (futuro) |

## Tratamento de Erros

Atualmente, erros durante extração são capturados mas não exibidos. Exemplo:

- Arquivo ZIP corrompido: é pulado silenciosamente
- Arquivo ZIP protegido por senha: é pulado
- Permissões insuficientes: é pulado

Futuro: Sistema de logging detalhado com alertas específicos.

## Roadmap

- [ ] Sistema de logging em arquivo
- [ ] Pausa segura por níveis de profundidade (MAX_DEPTH)
- [ ] Restauração automática de backup
- [ ] Comparação por hash MD5/SHA256
- [ ] Alertas de erros com categorização
- [ ] Suporte a senhas protegidas
- [ ] Interface CLI
- [ ] Testes unitários
- [ ] Métricas de performance

## Limitações Conhecidas

- Não oferece suporte a ZIP protegidos por senha
- Erros não são reportados em tempo de execução
- Sem limite de profundidade (pode causar loop infinito com ZIPs malformados)
- Sem validação de integridade de arquivo

## Contribuindo

Sinta-se livre para reportar bugs, sugerir features ou enviar pull requests.

## Licença

MIT

## Autor

Desenvolvido para automação de descompactação complexa de estruturas ZIP encadeadas.
