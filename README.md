# Rasale-Cashback
    Microserviço responsável por cadastrar revendedores e compras, e acompanhar o cashback de cada compra cadastrada.

# Endpoints 
`POST /dealers` Reponsável por cadastrar um novo revendedor(a), onde os requisitos mínimos para cadastro são: nome completo, 
Cpf, e-mail e senha. 

Corpo da requisição

```json
Request
{
    "confirm_password": string,
    "email": string,
    "cpf": string,
    "full_name": string,
    "password": string,
    "active": bool
}

```

O campo "active" determina se o usuário terá permissóes de administrador. Uuários com o papel de administrador conseguem realizar consultas de outros usuários 
e outras compras. 

Exemplo: 
POST /dealers 
```json
Request
{
    "confirm_password": "147258",
    "email": "emailemail@gmail.com",
    "cpf": "3132132165",
    "full_name": "Vinicius Otavio",
    "password": "147258",
    "active": true
}

```json
Response
 {
  "data": {
    "active": true,
    "cpf": "3132132165",
    "email": "emailemail@gmail.com",
    "full_name": "Vinicius Otavio",
    "id": "5f20d27eb51be4b157d467c9"
  },
  "message": "Resource created",
  "resource": "Users",
  "status": 200
}
```
A resposta deve conter um Guid (id) gerado para consulta na base de dados do MOngoDb. 
Caso seja informado um cpf ou um email já existente exibiremos o seguinte response. 

```json
Response
{
  "errors": {
    "cpf": "Cpf já cadastrado"
  },
  "message": "Ocorreu um erro nos campos informados.",
  "resource": "Users"
}
```
`GET /admin/dealers/<int:page_id>` responsável por consultar todos os revendedores cadastrados por paginação.
caso não seja informado nenhum valor para paginação a api trata isso internamente passando um valor default
Para acesso a esse endpoint o usuário precisa ter papel de administrador. 
headers { Authorization: 'Bearer (Token gerador pela api)}

`Get /admin/dealers/<string:user_id>` Responsável por consultar um(a) revendedor(a) pelo seu id. Para realizar a 
consulta basta apenas passar o id por parâmetro na Url, e adicionar o Authorization no Header como monstrado no 
exemplo acima

```json
Response
{
   "data": {
    "active": true,
    "cpf": "3132132165",
    "email": "emailemail@gmail.com",
    "full_name": "Vinicius Otavio",
    "id": "5f1b45752e95a8f88291e97a"
  },
  "message": "Usuários retornado(a).",
  "resource": "Users",
  "status": 200 
}

Caso seja informado um usuário que não exista o retorna da requisição será...

```json
Response
{
   "message": "Este(a) Usuário não existe.",
   "resource": "Users"
}
```
E caso de algum Exception o erro é tratado internamente pela api, retornando na maioria das vees uma mensagem 
amigável para o usuário

`Post /auth` EndPoint responsável por autenticar o usuário na api, só serão autenticados os usuário que tiverem o campo 
active como true. 

Exemplo de como realizar a autenticação. 

```json 
Request
{
    "email": "vincius.otv@gmail.com",
    "password": "147258"
}
```

Lembrando que a senha do usuário é criptografada internamente, e a autenticação é feita via jwt

```json 
Response
{
  "data": {
    "active": true,
    "cpf": "3132132165",
    "email": "vincius.otv@gmail.com",
    "full_name": "Vinicius Otavio",
    "id": "5f1b45752e95a8f88291e97a"
  },
  "message": "Token criado.",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTU5ODcyOTUsIm5iZiI6MTU5NTk4NzI5NSwianRpIjoiZmFlNjIxNWQtOGY1YS00MmRjLTgxODQtMmViZTlmODU5ZWRhIiwiZXhwIjoxNTk4NTc5Mjk1LCJpZGVudGl0eSI6InZpbmNpdXMub3R2QGdtYWlsLmNvbSIsInR5cGUiOiJyZWZyZXNoIn0.9ilVFIhXe37K3JOt9LJLdIl31TXA7PGDSmaluDaVhxI",
  "resource": "Auth",
  "status": 200,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTU5ODcyOTUsIm5iZiI6MTU5NTk4NzI5NSwianRpIjoiNzYwN2U4M2MtYjFkYS00ZGNmLTg1MzctYWQxZGU2ZmY1MjU3IiwiZXhwIjoxNTk1OTg4NDk1LCJpZGVudGl0eSI6InZpbmNpdXMub3R2QGdtYWlsLmNvbSIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyIsInVzZXJfY2xhaW1zIjp7ImFjdGl2ZSI6dHJ1ZX19.r_XCS340qrjnM1GGwUQTHWZnss1ctXbmd-6QFKlsDio"
}
``` 

`Post '/auth/refresh'` Todo token dura até 20 minutos, esse endpoint é responsável por dar um refresh no token caso o mesmo expire

`Post /order` Endpoint responsável por cadastrar um novo pedido (compra). Através do valor do pedido calculamos a porcentagem do 
cashback e o valor do mesmo. Todas as compras entram no status de "Em Validação", exceto as compras que se originam do Cpf 15350946056, 
compras que possuem esse cpf já entram para o status "Aprovado"
Exemplo de Requisição 

```json 
Request
{
    "order_values": 1499, 
    "cpf_dealer": "15350946056"
}
```

```json 
Response
{ 
    "data": {
    "cashback": 0.15,
    "cashback_values": 224.85,
    "cpf_dealer": "15350946056",
    "created": "2020-07-28T22:12:40.610199",
    "id": "5f20cd08378f55846cb74e6d",
    "order_status": "Aprovado",
    "order_values": 1499.00
  },
  "message": "Resource created",
  "resource": "order",
  "status": 200
}