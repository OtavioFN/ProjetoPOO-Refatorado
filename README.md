# Projeto de E-commerce em Python

Este projeto é um sistema simples de e-commerce desenvolvido em Python, utilizando conceitos de Programação Orientada a Objetos e padrões de projeto.

## Funcionalidades

- Cadastro e gerenciamento de produtos  
- Carrinho de compras com cálculo de valores  
- Sistema de pedidos e cupons de desconto  
- Avaliações de produtos  
- Interface de texto para interação com o usuário

## Padrões de Projeto Utilizados

### Padrões Criacionais

- **Singleton**  
  Utilizado na classe `EcommerceSystem`, garantindo que exista apenas uma instância do sistema durante toda a execução.

- **Factory Method**  
  Aplicado na criação de pedidos na classe `Order`. Centraliza e controla a lógica de construção dos objetos.

- **Builder**  
  Usado na construção de cupons na classe `Coupon`. Facilita a criação de objetos complexos passo a passo, permitindo diferentes configurações sem múltiplos construtores.

### Padrões Comportamentais

- **Strategy**  
  Utilizado para aplicar diferentes estratégias de desconto em pedidos. Cada tipo de desconto é encapsulado em uma classe separada, permitindo alternar o comportamento em tempo de execução sem alterar o código do pedido.

- **Observer**  
  Aplicado no sistema de avaliações. Quando um produto recebe uma nova avaliação, os observadores interessados (como sistemas de notificação ou atualizações internas) são automaticamente notificados da mudança.
