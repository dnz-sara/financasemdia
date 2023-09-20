# Finanças em dia - API

A finalidade dessa aplicação é dar suporte ao front-end da app Finanças em dia.
As Rotas implementadas possibilitam a criação, edição e exclusão de lançamentos no sistema.

---
## Como executar o projeto

1. Clonar ou fazer download do projeto.

2. Na folder src, executar o seguinte comando para instalar as dependências:
    ```
    (env)$ pip install -r requirements.txt
    ```

3. Na folder src, executar o seguinte comando para iniciar a API:
    ```
    (env)$ flask run --host 0.0.0.0 --port 5000
    ```

4. Abrir no navegador o endereço [http://localhost:5000/](http://localhost:5000/). Serão apresentadas as opções do Swagger, ReDoc e RapiDoc.
Informação adicional: para utilizar as Rotas, o campo mes_ano_referencia aceita valores no seguinte formato: mm-yyyy. Exemplo: 01-2023, 02-2023, etc...


---
## Frontend
Para acessar o frontend, favor observar esta documentação: [frontend](https://github.com/dnz-sara/financasemdia-frontend/blob/main/README.md)
