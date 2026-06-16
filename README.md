## Integração Supabase + Z-API (WhatsApp)

Este repositório contém a resolução do desafio técnico de automação de disparos de mensagens personalizadas via WhatsApp. O objetivo do projeto é conectar a uma base de dados no Supabase, recolher informações de contactos cadastrados e realizar disparos utilizando a API da Z-API.

##  Funcionalidades e Boas Práticas Implementadas

- **Filtro na Origem (Performance):** A query ao banco de dados utiliza cláusula de paginação e limite direto (`.limit(3)`), evitando sobrecarga de memória no servidor e tráfego desnecessário de rede.
- **Fail-Fast (Segurança):** O script valida se todas as variáveis de ambiente cruciais estão presentes antes de iniciar qualquer conexão. Se algo faltar, a execução é interrompida imediatamente.
- **Resiliência e Isolamento:** O loop de disparos foi desenvolvido para ser resiliente. Caso o envio para um contacto falhe (número inválido, queda de rede), o erro é registado no console e o script passa automaticamente para o próximo registo sem quebrar o fluxo.
- **Arquitetura Plana (Flat Structure):** Estrutura de ficheiros minimalista para evitar excesso de engenharia (*overengineering*), permitindo legibilidade instantânea do código.

---

##  Configuração do Ambiente

### 1. Estrutura da Tabela no Supabase
O script espera uma tabela chamada `contatos` com as seguintes colunas e tipos:

| Nome da Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | int8 (Identity) | Chave primária automática |
| `name` | text | Nome do contacto (personalização) |
| `telefone` | text | Número de telemóvel (com DDI e DDD, ex: `5511999999999`) |

### 2. Variáveis de Ambiente (.env)
Crie um ficheiro chamado `.env` na raiz do projeto e preencha as suas chaves conforme o modelo abaixo (este ficheiro está devidamente protegido no `.gitignore`):

```env
# Credenciais do Supabase

SUPABASE_URL=[https://seu-subdominio.supabase.co](https://seu-subdominio.supabase.co)
SUPABASE_KEY=sua_chave_service_role_ou_anon_public

# Credenciais da Z-API
ZAPI_INSTANCE_ID=seu_id_da_instancia
ZAPI_INSTANCE_TOKEN=seu_token_da_instancia


# Virtualizaçao
# Criar o ambiente virtual (venv)
python -m venv venv

# Ativar no Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Ativar no Linux / macOS
source venv/bin/activate

# Instalar as Dependências
pip install -r requirements.txt

# Run
python main.py