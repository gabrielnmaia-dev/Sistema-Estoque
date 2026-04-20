# 📦 Sistema de Gerenciamento de Estoque

Sistema web desenvolvido com Django para controle de estoque, incluindo cadastro de produtos, categorias, movimentações e controle de usuários com diferentes níveis de acesso.

---

## 👥 Integrantes

- Felipe Gabriel
- Alvaro Antonio

---

## 🚀 Tecnologias Utilizadas

- Python
- Django
- PostgreSQL
- HTML, CSS (Bootstrap)

---

## 🎯 Objetivo do Projeto

Desenvolver um sistema de gerenciamento de estoque aplicando conceitos de:

- CRUD com Class-Based Views (CBVs)
- Autenticação de usuários
- Controle de permissões
- Modelagem de dados
- Boas práticas com Django

---

## 🧩 Funcionalidades

### 🔐 Autenticação

- Login e logout de usuários
- Controle de acesso por tipo de usuário:
  - Gerente
  - Vendedor

---

### 📦 Produtos

- Cadastro de produtos
- Listagem com paginação
- Edição de produtos
- Remoção lógica (soft delete)

---

### 📂 Categorias

- Cadastro de categorias
- Listagem
- Edição
- Remoção lógica (soft delete)

---

### 🔄 Movimentações de Estoque

- Registro de entrada de produtos
- Registro de saída de produtos
- Atualização automática do estoque
- Histórico de movimentações

---

### 👥 Usuários

- Cadastro de usuários pelo sistema (sem uso do admin do Django)
- Associação a grupos:
  - Gerente
  - Vendedor

---

## 🧠 Regras de Negócio

- Produtos não podem ter estoque negativo
- Movimentações não podem ser editadas ou excluídas
- Exclusões são feitas via soft delete
- Apenas gerentes podem cadastrar/editar produtos e categorias
- Vendedores podem apenas registrar saídas e consultar produtos

---

## 🏗️ Estrutura do Projeto

```text
projeto/
 ├── core/
 ├── produtos/
 ├── categorias/
 ├── movimentacoes/
 ├── usuarios/
```

---

## 🔐 Acesso ao Sistema

O cadastro de usuários é feito diretamente pelo sistema.
Usuários devem ser atribuídos a um grupo (Gerente ou Vendedor).

---

## 📌 Observações

- O sistema não utiliza o Django Admin
- Todas as funcionalidades foram implementadas manualmente com CBVs
- Projeto desenvolvido para fins acadêmicos

---

## 📄 Licença

Este projeto é apenas para fins educacionais.
