Projeto de E-commerce em Python

Este projeto é um sistema simples de e-commerce desenvolvido em Python, utilizando conceitos de Programação Orientada a Objetos e três padrões de projeto criacionais.

Funcionalidades

Cadastro e gerenciamento de produtos

Carrinho de compras com cálculo de valores

Sistema de pedidos e cupons de desconto

Avaliações de produtos

Interface de texto para interação com o usuário


Padrões de Projeto Utilizados

1. Singleton

Utilizado na classe EcommerceSystem, garantindo que exista apenas uma instância do sistema durante toda a execução.

2. Factory Method

Utilizado para a criação de pedidos na classe Order. Esse padrão facilita a criação controlada de objetos, centralizando a lógica de construção.

3. Builder

Aplicado na construção de cupons na classe Coupon. Esse padrão facilita a criação de objetos complexos passo a passo, permitindo configurações diferentes sem precisar de múltiplos construtores.
