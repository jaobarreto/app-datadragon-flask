# Projeto League of Legends Data Dragon

Este projeto consome a API **Data Dragon** do jogo **League of Legends** para exibir informações sobre campeões, como nome, título, tags e outras características importantes. Além disso, agora permite favoritar campeões e gerenciar essa lista com um CRUD completo.

## Tecnologias Utilizadas
- Python 3
- Flask
- Jinja2
- Flask-SQLAlchemy
- SQLite

## Pré-requisitos
Certifique-se de ter o **Python 3** instalado no seu sistema.

## Como Rodar o Projeto (Windows)
1. Clone o repositório:
```bash
 git clone git@github.com:jaobarreto/app-datadragon-flask.git
```

2. Crie e ative um ambiente virtual:
```bash
 python -m venv venv
 source venv/bin/activate  # Linux/macOS
 venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
 pip install -r requirements.txt
```

4. Execute o projeto:
```bash
 python app.py
```

5. Acesse o projeto no navegador através do endereço:
```bash
 http://localhost:4000
```

## Banco de Dados
O projeto utiliza **SQLite** como banco de dados. Para criar as tabelas, execute:
```bash
 flask db upgrade
```

## Licença
Este projeto está licenciado sob a [MIT License](LICENSE).

