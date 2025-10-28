# Projeto de E-commerce em Python

Este projeto é um sistema de e-commerce desenvolvido em Python, aplicando conceitos de **Programação Orientada a Objetos (POO)** e diversos **padrões de projeto** para garantir modularidade, reutilização e fácil manutenção.

---

## Funcionalidades

- Cadastro e gerenciamento de produtos  
- Carrinho de compras com cálculo de valores  
- Sistema de pedidos, descontos e cupons  
- Avaliações de produtos  
- Simulação de entrega e pagamento  
- Interface textual para interação com o usuário  

---

## Padrões de Projeto Utilizados

### Padrões Criacionais

- **Singleton**  
  Utilizado na classe `EcommerceSystem`, garantindo que exista apenas **uma instância central do sistema**, responsável por gerenciar usuários, produtos, carrinho e pedidos.

- **Builder**  
  Aplicado na construção do objeto `Order` (pedido), utilizando as classes `OrderBuilder` e `OrderDirector`.  
  Isso permite que um pedido seja **montado passo a passo**, validando informações antes de ser finalizado.

- **Factory Method**  
  Presente em `PaymentFactory` e `DeliveryFactory`, que criam instâncias concretas de estratégias de pagamento e entrega.  
  Com isso, o sistema pode facilmente **adicionar novos métodos de pagamento ou entrega** sem alterar o código principal.

---

### Padrões Comportamentais

- **Strategy**  
  Define algoritmos intercambiáveis para **pagamento** e **entrega**.  
  Exemplo: alternar entre pagamento com cartão e boleto, ou entre entrega padrão e expressa.

- **Chain of Responsibility**  
  Usado no processamento de descontos durante o checkout.  
  Cada manipulador (`CouponHandler`, `LoyaltyHandler`, `ShippingDiscountHandler`, `FinalCostHandler`) aplica uma regra e encaminha o pedido ao próximo, de forma **sequencial e desacoplada**.

- **Observer**  
  Implementado no `Order` (pedido), que **notifica automaticamente observadores** (como `InventoryObserver`) após o pagamento ser aprovado.  
  Isso garante que o estoque seja atualizado sem dependência direta entre classes.

---

### Padrões Estruturais

- **Adapter**  
  Implementado em `CourierAdapter.py`.  
  Adapta uma **API externa simulada** (`ExternalCourierAPI`) ao formato esperado pelo sistema de entrega, permitindo integração sem alterar o código existente.

- **Decorator**  
  Implementado em `ProductDecorator.py`.  
  Permite **adicionar funcionalidades** aos produtos dinamicamente, como aplicar **descontos visuais automáticos** (ex: 10% off em produtos acima de R$50), sem modificar a classe original `Product`.

- **Facade**  
  Implementado em `CheckoutFacade.py`.  
  Simplifica o fluxo de checkout reunindo em um único ponto:  
  pagamento → criação do pedido → aplicação de descontos → notificação de estoque.  
  Dessa forma, o método `_payment_process` ficou muito mais limpo e de fácil manutenção.

