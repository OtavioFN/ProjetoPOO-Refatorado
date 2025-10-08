# Projeto de E-commerce em Python

Este projeto é um sistema simples de e-commerce desenvolvido em Python, utilizando conceitos de Programação Orientada a Objetos e padrões de projeto.

## Funcionalidades

- Cadastro e gerenciamento de produtos
- Carrinho de compras com cálculo de valores
- Sistema de pedidos e cupons de desconto
- Avaliações de produtos
- Interface de texto para interação com o usuário

---

## Padrões de Projeto Utilizados

### Padrões Criacionais

- **Singleton**
  Utilizado na classe `EcommerceSystem`, garantindo que exista apenas uma instância central do sistema para gerenciar o estado global (como listas de produtos e usuários).

- **Builder**
  Aplicado na construção complexa de objetos **Pedido** (`Order`), utilizando as classes `OrderBuilder` e `OrderDirector`. Isso garante que o pedido seja montado e validado passo a passo antes de ser finalizado.

- **Factory Method**
  Utilizado na criação de **Estratégias de Pagamento** (`PaymentFactory`) e **Estratégias de Entrega** (`DeliveryFactory`). Ele isola a lógica de decisão sobre qual classe concreta deve ser instanciada.

### Padrões Comportamentais

- **Strategy**
  Utilizado para definir algoritmos intercambiáveis de **Pagamento** (processamento de cartão vs. boleto) e **Entrega** (custo padrão vs. expresso). Permite que o cliente alterne o comportamento em tempo de execução.

- **Chain of Responsibility**
  Aplicado no fluxo de checkout para o processamento de descontos. Ele estabelece uma **cadeia de manipuladores** (`CouponHandler`, `LoyaltyHandler`, etc.) para que o pedido passe por todas as regras de desconto sequencialmente, sem que o código principal precise saber de todas elas.

- **Observer**
  Aplicado na classe **Pedido** (`Order`), que atua como **Subject**. Notifica observadores registrados (como o `InventoryObserver`) imediatamente após a aprovação do pagamento, garantindo a baixa de estoque de forma desacoplada.