# CondoZen

Sistema Inteligente de Zeladoria e Manutenção Condominial.

Este projeto é o MVP (Minimum Viable Product) desenvolvido para a disciplina de Programação Web Avançada (Turma SI5N). O objetivo do sistema é centralizar, gerenciar e rastrear o fluxo de chamados de manutenção e ocorrências em condomínios, substituindo processos informais por uma gestão baseada em rastreabilidade e métricas (SLA).

## Equipe Desenvolvedora

* Antonio Augusto de Almeida Lelis
* Bryan Campos Lopes
* Samuel Manhnani Salles

## Funcionalidades Principais

* **Gestão de Chamados (Ticketing):** Abertura de ocorrências detalhando o problema, o local (ex: Bloco A - Apto 302, ou Áreas Comuns) e a prioridade.
* **Painel Kanban:** Interface de administração para acompanhamento visual do fluxo de tarefas (Aberto, Em Andamento, Concluído).
* **Controle de SLA:** Cálculo automático de prazos e indicativos visuais baseados na prioridade (Baixa, Média, Alta, Urgente) para garantir a resolução rápida dos problemas.
* **Comunicação Centralizada:** Sistema de mensagens e histórico de alterações embutido em cada chamado, eliminando o uso de grupos de aplicativos de mensagens para gestão do prédio.
* **RBAC (Role-Based Access Control):** Perfilamento de usuários separando as visões e permissões de Moradores, Zeladores/Manutenção e Síndicos.

## Tecnologias e Arquitetura

O projeto adota uma arquitetura monolítica com Server-Side Rendering (SSR).

* **Backend / Web Framework:** Python 3 + Flask
* **Frontend:** Jinja2 (Templates) + HTML/CSS
* **Banco de Dados:** PostgreSQL (hospedado no Supabase)
* **ORM:** SQLAlchemy (utilizando o driver pg8000)
* **Testes Automatizados:** pytest
* **Automação de Tarefas:** Invoke

## Pré-requisitos

Para rodar o projeto localmente, certifique-se de ter instalado em sua máquina:

* Python 3.10 ou superior
* Git

## Configuração do Ambiente de Desenvolvimento

Siga os passos abaixo para configurar o projeto na sua máquina local.

**1. Clone o repositório**
```bash
git clone https://github.com/SEU_USUARIO/condozen.git
cd condozen
```

**2. Crie e ative o ambiente virtual**
* No Windows:
```powershell
python -m venv venv
venv\Scripts\activate
```
* No Linux / Mac:
```bash
python -m venv venv
source venv/bin/activate
```

**3. Instale as dependências**
```bash
pip install invoke
inv install
```

**4. Variáveis de Ambiente**
Crie um arquivo chamado `.env` na raiz do projeto e configure a URL de conexão com o banco de dados do Supabase. Utilize o modelo abaixo:

```env
DATABASE_URL=postgresql+pg8000://postgres.[ID_PROJETO]:[SENHA]@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

## Como Executar a Aplicação

Com o ambiente virtual ativado e as dependências instaladas, utilize o automatizador de tarefas para subir o servidor local:

```bash
inv run
```
O sistema estará disponível no navegador através do endereço: `[http://127.0.0.1:5000](http://127.0.0.1:5000)`

## Executando os Testes

O projeto utiliza a biblioteca `pytest` para a garantia de qualidade de software. Para rodar a suíte completa de testes automatizados, execute o comando:

```bash
inv test
```

## Estrutura do Projeto

Abaixo está a topologia de diretórios da aplicação:

```text
condozen/
├── app/                    # Código fonte da aplicação Flask
│   ├── __init__.py         # Configuração inicial (App Factory) e conexão com BD
│   ├── models.py           # Definição das tabelas e ORM
│   ├── routes.py           # Controladores e mapeamento de URLs
│   ├── static/             # Arquivos estáticos (CSS, JS, Imagens)
│   └── templates/          # Arquivos de visualização (HTML com Jinja2)
├── tests/                  # Diretório de testes automatizados
│   └── test_routes.py      # Casos de teste para as rotas da aplicação
├── .env                    # Variáveis de ambiente (não versionado)
├── .gitignore              # Arquivos ignorados pelo Git
├── requirements.txt        # Lista de dependências Python
├── run.py                  # Ponto de entrada do servidor
└── tasks.py                # Comandos de automação do Invoke
```