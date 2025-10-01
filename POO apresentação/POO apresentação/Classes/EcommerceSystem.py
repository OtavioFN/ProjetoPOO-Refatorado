from Classes.User import Admin, Customer
from Classes.Coupon import FixedCoupon, PercentageCoupon
from Classes.UI import UI
from Classes.Cart import Cart
from Classes.Product import Product
from Classes.Order import Order, OrderDirector, OrderBuilder
from Classes.Review import Review
from Classes.Ticket import Ticket
from Classes.PaymentFactory import PaymentFactory
from Classes.DeliveryFactory import DeliveryFactory
from Classes.OrderObserver import InventoryObserver
import time

class ECommerceSystem:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ECommerceSystem, cls).__new__(cls)
            cls._instance._initialized = False 
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self.users = {}
        self.products = []
        self.reviews = []
        self.coupons = []
        self.tickets = []
        self.orders = []
        self.cart = Cart()
        self.current_user = None
        
        self.inventory_observer = InventoryObserver()
        
        self._load_initial_data()
        self._initialized = True
        
    def _load_initial_data(self):
        admin = Admin('admin', '1234')
        self.users['admin'] = admin
        customer = Customer('customer', '123')
        customer.add_address('Home', 'Fictional Street, 123', 'Maceió, AL')
        self.users['customer'] = customer
        
        self.products.extend([
            Product(1, 'Gaming Notebook', 'Notebook with RTX 4080 graphics card', 8500.00),
            Product(2, 'Gaming Mouse', 'Wireless mouse with 16000 DPI', 350.50),
            Product(3, 'Mechanical Keyboard', 'Keyboard with blue switches and RGB', 450.00)
        ])
        
        self.coupons.append(PercentageCoupon('PROMO10', 10))

    def _generate_new_id(self, data_list):
        return max(item.id for item in data_list) + 1 if data_list else 1

    def find_product_by_id(self, product_id):
        return next((p for p in self.products if p.id == product_id), None)

    def _calculate_average_rating(self, product_id):
        product_reviews = [r.rating for r in self.reviews if r.product_id == product_id]
        if not product_reviews: return 0, 0
        return sum(product_reviews) / len(product_reviews), len(product_reviews)

    def run(self):
        while True:
            self.current_user = self._login_signup_menu()
            if self.current_user is None:
                break
            
            exit_command = self._main_menu()
            if exit_command == 'exit':
                break
        
        UI.clear_screen()
        print("\n\tThank you for using the system. See you soon!\n")

    def _login_signup_menu(self):
        while True:
            UI.clear_screen()
            print("\n\tWelcome!\n\t1 - Login\n\t2 - Sign Up\n\t0 - Exit System")
            try:
                option = int(input("\n\t=> "))
                if option == 1:
                    UI.clear_screen()
                    print("\n\t--- Login Screen ---")
                    user, password = input("\tLogin: "), input("\tPassword: ")
                    logged_in_user = self.users.get(user)
                    if logged_in_user and logged_in_user.password == password:
                        UI.clear_screen()
                        print(f"\n\tWelcome, {user}.")
                        UI.pause_and_clear()
                        return logged_in_user
                    else:
                        print("\n\t[ERROR] Invalid login or password.")
                        UI.pause_and_clear()
                elif option == 2:
                    UI.clear_screen()
                    print("\n\t--- Sign Up Screen ---")
                    new_user = input("\tUsername: ")
                    if new_user in self.users:
                        print("\n\t[ERROR] User already exists.")
                    elif not new_user:
                        print("\n\t[ERROR] Username cannot be empty.")
                    else:
                        new_password = input("\tPassword: ")
                        if new_password:
                            self.users[new_user] = Customer(new_user, new_password)
                            print(f"\n\tUser '{new_user}' registered!")
                        else:
                            print("\n\t[ERROR] Password cannot be empty.")
                    UI.pause_and_clear(3)
                elif option == 0:
                    return None
            except ValueError:
                print("\n\t[ERROR] Invalid option.")
                UI.pause_and_clear()

    def _main_menu(self):
        while True:
            UI.clear_screen()
            print(f"\n\tUser: {self.current_user.username}\n\tWhat do you want to do?")
            print("\t" + "="*45)
            print("\t1 - Catalog\n\t2 - Cart\n\t3 - Checkout\n\t4 - My Orders\n\t5 - Review Products\n\t6 - My Profile\n\t7 - Customer Support")
            if isinstance(self.current_user, Admin):
                print("\t--- Administrator Panel ---")
                print("\t8 - Manage Products\n\t9 - Manage Coupons\n\t10 - Handle Tickets")
            print("\t" + "="*45 + "\n\t99 - Logout\n\t0 - Exit System\n" + "\t" + "="*45)
            
            try:
                choice = int(input("\t=> "))
                if choice == 1: self._view_catalog_and_add()
                elif choice == 2: self._manage_cart()
                elif choice == 3: self._place_order()
                elif choice == 4: self._check_orders()
                elif choice == 5: self._add_review()
                elif choice == 6: self._manage_profile()
                elif choice == 7: self._customer_support_menu()
                elif choice == 8 and isinstance(self.current_user, Admin): self._manage_products_admin()
                elif choice == 9 and isinstance(self.current_user, Admin): self._manage_coupons_admin()
                elif choice == 10 and isinstance(self.current_user, Admin): self._support_menu_admin()
                elif choice == 99: self.cart.clear(); return 'logout'
                elif choice == 0: return 'exit'
            except ValueError:
                print("\n\t[ERROR] Invalid option."); UI.pause_and_clear()

    def _view_catalog_and_add(self):
        search_term, sort_order = "", None
        while True:
            UI.clear_screen()
            products_to_display = list(self.products)
            if search_term: products_to_display = [p for p in products_to_display if search_term.lower() in p.name.lower()]
            if sort_order == 'price_asc': products_to_display.sort(key=lambda p: p.price)
            elif sort_order == 'price_desc': products_to_display.sort(key=lambda p: p.price, reverse=True)
            elif sort_order == 'name_asc': products_to_display.sort(key=lambda p: p.name)

            print("\n\t--- Product Catalog ---")
            print(f"\tActive filters: [Search: '{search_term}' | Sort: {sort_order or 'Default'}]")
            print("\t" + "="*60)
            if not products_to_display: print("\n\tNo products found.")
            else:
                for p in products_to_display:
                    average, n_rev = self._calculate_average_rating(p.id)
                    rating_str = f"| Rating: {average:.1f}/5 ({n_rev})" if n_rev > 0 else "| No reviews"
                    print(f"\tID {p.id}: {p.name} ($ {p.price:.2f}) {rating_str}")

            print("\n\t--- Actions ---\n\t1 - View details\n\t2 - Add to cart\n\t3 - Search\n\t4 - Filter / Sort\n\t5 - Clear filters\n\t0 - Back")
            try:
                choice = int(input("\n\t=> "))
                if choice == 1:
                    details_id = int(input("\tProduct ID to view details: "))
                    self._display_product_details(details_id)
                elif choice == 2:
                    add_id = int(input("\tProduct ID to add: "))
                    product = self.find_product_by_id(add_id)
                    if product:
                        quantity = int(input(f"\tQuantity of '{product.name}': "))
                        if self.cart.add(add_id, quantity):
                            print(f"\n\t>>> Added!"); time.sleep(1)
                    else: print("\n\t[ERROR] Product not found."); time.sleep(2)
                elif choice == 3: search_term = input("\tTerm to search for: ")
                elif choice == 4:
                    new_order = self._filter_menu()
                    if new_order: sort_order = new_order
                elif choice == 5: search_term, sort_order = "", None; print("\n\tFilters cleared."); time.sleep(1)
                elif choice == 0: break
            except (ValueError, KeyError): print("\n\t[ERROR] Invalid option."); time.sleep(2)

    def _display_product_details(self, product_id):
        UI.clear_screen()
        product = self.find_product_by_id(product_id)
        if not product: print("\n\t[ERROR] Product not found."); UI.pause_and_clear(); return

        average, num_reviews = self._calculate_average_rating(product_id)
        print(f"\n\t--- Details of: {product.name} ---")
        print(f"\tID: {product.id}\n\tPrice: $ {product.price:.2f}\n\tDescription: {product.description}")
        if num_reviews > 0: print(f"\tAverage Rating: {average:.1f}/5.0 ({UI.generate_stars(average)})")
        print("\t" + "="*50 + "\n\n\tCUSTOMER REVIEWS:")

        comments = [r for r in self.reviews if r.product_id == product_id]
        if not comments: print("\tThis product has no reviews yet.")
        else:
            for review in comments:
                print("\t" + "-"*30 + f"\n\tUser: {review.user}\n\tRating:   {UI.generate_stars(review.rating)}\n\tComment: {review.comment}")
        UI.wait_for_enter()

    def _filter_menu(self):
        UI.clear_screen()
        print("\n\t--- Apply Filters and Sorting ---\n\t1 - By Price (Lowest to Highest)\n\t2 - By Price (Highest to Lowest)\n\t3 - By Name (A-Z)\n\t0 - Back")
        try:
            option = int(input("\n\t=> "))
            if option == 1: return 'price_asc'
            if option == 2: return 'price_desc'
            if option == 3: return 'name_asc'
            return None
        except ValueError: return None

    def _manage_cart(self):
        while True:
            UI.clear_screen(); print("\n\t--- Shopping Cart ---")
            if self.cart.is_empty(): print("\n\tYour cart is empty.")
            else:
                for p_id, quantity in self.cart.items.items():
                    product = self.find_product_by_id(p_id)
                    if product:
                        subtotal = product.price * quantity
                        print(f"\t- {product.name} | Qty: {quantity} | Subtotal: $ {subtotal:.2f}")
                cart_total = self.cart.get_total(self)
                print("\n\t" + "="*30 + f"\n\tTOTAL: $ {cart_total:.2f}\n" + "\t" + "="*30)

            print("\n\t1 - Add more items\n\t2 - Remove item\n\t0 - Back")
            try:
                option = int(input("\n\t=> "))
                if option == 1: self._view_catalog_and_add()
                elif option == 2:
                    if self.cart.is_empty(): print("\n\t[ERROR] Cart is already empty."); UI.pause_and_clear(); continue
                    remove_id = int(input("\tProduct ID to remove: "))
                    if remove_id in self.cart.items:
                        name = self.find_product_by_id(remove_id).name
                        print(f"\n\tYou have {self.cart.items[remove_id]} of '{name}'.")
                        remove_qty = int(input("\tHow many do you want to remove? "))
                        result = self.cart.remove(remove_id, remove_qty)
                        if result == "partially_removed": print(f"\n\t{remove_qty} unit(s) removed.")
                        elif result == "fully_removed": print(f"\n\tItem '{name}' removed.")
                        else: print("\n\t[ERROR] Invalid quantity.")
                    else: print("\n\t[ERROR] Product not in cart.")
                    UI.pause_and_clear()
                elif option == 0: break
            except (ValueError, KeyError): print("\n\t[ERROR] Invalid option or ID."); UI.pause_and_clear()

    def _place_order(self):
        UI.clear_screen(); print("\n\t--- Checkout ---")
        if self.cart.is_empty(): print("\n\tYour cart is empty."); UI.pause_and_clear(); return

        original_total = self.cart.get_total(self)
        print(f"\n\tSubtotal: $ {original_total:.2f}")

        applied_coupon, discount = None, 0
        coupon_code = input("\tDiscount coupon? (Leave blank if none): ").upper()
        if coupon_code:
            coupon = next((c for c in self.coupons if c.code == coupon_code), None)
            if coupon and coupon.active:
                discount = coupon.apply_discount(original_total)
                applied_coupon = {'code': coupon.code, 'calculated_discount': discount}
                print(f"\n\t>>> Coupon '{coupon.code}' applied! Discount of $ {discount:.2f} <<<")
            else: print("\n\t[ERROR] Invalid or inactive coupon.")

        products_total = max(0, original_total - discount)

        delivery_method, delivery_cost = self._select_delivery(products_total)
        if delivery_method is None: return 
        
        final_total = products_total + delivery_cost
        
        print("\n\t" + "="*40)
        print(f"\tProducts Total: $ {products_total:.2f}")
        print(f"\tDelivery Cost ({delivery_method.get_name()}): $ {delivery_cost:.2f}")
        print(f"\tFINAL TOTAL: $ {final_total:.2f}")
        print("\t" + "="*40)
        UI.wait_for_enter()

        if not isinstance(self.current_user, Customer) or not self.current_user.addresses: print("\n\tNo registered addresses."); UI.pause_and_clear(); return
        print("\n\tSelect the address:")
        for i, addr in enumerate(self.current_user.addresses): print(f"\t{i+1} - {addr['nickname']}")
        try:
            selected_address = self.current_user.addresses[int(input("\n\t=> ")) - 1]
        except (ValueError, IndexError): print("\n\t[ERROR] Invalid choice."); UI.pause_and_clear(); return
        
        UI.clear_screen(); print("\n\t--- Select Payment Method ---")
        print("\t1 - Credit Card\n\t2 - Bank Slip\n\t0 - Cancel")
        try:
            payment_option = int(input("\n\t=> "))
            if payment_option == 1:
                payment_method = 'creditcard'
            elif payment_option == 2:
                payment_method = 'bankslip'
            elif payment_option == 0:
                print("\n\t[INFO] Order cancelled."); UI.pause_and_clear(); return
            else:
                raise ValueError
        except ValueError:
            print("\n\t[ERROR] Invalid option."); UI.pause_and_clear(); return

        success = self._payment_process(payment_method, selected_address, final_total, applied_coupon, delivery_method.get_name(), delivery_cost)
        if success: print("\n\tOrder placed successfully!"); self.cart.clear()
        else: print("\n\tPayment failed. The order was not completed.")
        UI.pause_and_clear(4)

    def _select_delivery(self, products_total):
        while True:
            UI.clear_screen(); print("\n\t--- Select Delivery Method ---")
            
            factory = DeliveryFactory()
            standard = factory.create_delivery_strategy('standard')
            express = factory.create_delivery_strategy('express')
            
            standard_cost = standard.calculate_cost(products_total)
            express_cost = express.calculate_cost(products_total)
            
            print(f"\t1 - {standard.get_name()} ({standard.get_estimated_time()}) | Cost: $ {standard_cost:.2f}")
            print(f"\t2 - {express.get_name()} ({express.get_estimated_time()}) | Cost: $ {express_cost:.2f}")
            print("\t0 - Cancel Order")

            try:
                choice = int(input("\n\t=> "))
                if choice == 1: return standard, standard_cost
                elif choice == 2: return express, express_cost
                elif choice == 0: return None, None
                else: print("\n\t[ERROR] Invalid option."); UI.pause_and_clear()
            except ValueError: print("\n\t[ERROR] Invalid option."); UI.pause_and_clear()

    def _payment_process(self, payment_method, address, total, coupon_info, delivery_method_name, delivery_cost):
        UI.clear_screen(); print("\n\t--- Payment simulation ---")
        
        try:
            factory = PaymentFactory()
            strategy = factory.create_payment_strategy(payment_method)
            payment_approved = strategy.process_payment(total)
        
        except ValueError as e:
            print(f"\n\t[ERROR] {e}"); return False

        if payment_approved:
            print("\n\tPayment confirmed!")
            
            builder = OrderBuilder()
            director = OrderDirector(builder)
            
            try:
                new_order = director.construct_full_order(
                    order_id=self._generate_new_id(self.orders),
                    user=self.current_user.username,
                    cart_items=self.cart.items.copy(),
                    total=total,
                    address=address,
                    delivery_method=delivery_method_name,
                    delivery_cost=delivery_cost,
                    coupon_info=coupon_info
                )

                new_order.attach(self.inventory_observer)
                
                self.orders.append(new_order)
                
                new_order.notify(self)
                
                return True
            except ValueError as e:
                print(f"\n\t[ERRO] Falha ao construir o pedido: {e}")
                return False
        else:
            print("\n\t[ERRO] The payment was recused.")
            return False

    def _check_orders(self):
        UI.clear_screen(); print("\n\t--- My Orders ---")
        user_orders = [o for o in self.orders if o.user == self.current_user.username]
        if not user_orders: print("\n\tYou have no orders.")
        else:
            for order in user_orders:
                print("\n" + "="*45)
                print(f"\tOrder ID: {order.id} | Status: {order.status}\n\tTOTAL PAID: $ {order.total:.2f}")
                print(f"\tDelivery Method: {order.delivery_method} | Cost: $ {order.delivery_cost:.2f}")
                if order.applied_coupon: print(f"\tDiscount: $ {order.applied_coupon['calculated_discount']:.2f} (Coupon: {order.applied_coupon['code']})")
                print(f"\tAddress: {order.delivery_address['street']}")
                print("\tItems:")
                for p_id, quantity in order.items.items(): print(f"\t  - {quantity}x {self.find_product_by_id(p_id).name}")
                print("="*45)
        UI.wait_for_enter()

    def _add_review(self):
        UI.clear_screen(); print("\n\t--- Review Purchased Products ---")
        orders = [o for o in self.orders if o.user == self.current_user.username]
        if not orders: print("\n\tYou have no orders to review."); UI.pause_and_clear(); return
        
        purchased_products = {id_p: self.find_product_by_id(id_p) for o in orders for id_p in o.items}
        print("\n\tSelect the product to review:")
        for id_prod, prod_info in purchased_products.items(): print(f"\tID {id_prod}: {prod_info.name}")
        
        try:
            review_id = int(input("\n\t=> "))
            if review_id not in purchased_products: raise ValueError
            rating = int(input("\tRating from 1 to 5: "))
            if not 1 <= rating <= 5: print("\n\t[ERROR] Invalid rating."); UI.pause_and_clear(); return
            comment = input("\tComment (optional): ")
            self.reviews.append(Review(review_id, self.current_user.username, rating, comment))
            print("\n\tReview registered!"); UI.pause_and_clear()
        except (ValueError, KeyError): print("\n\t[ERROR] Invalid ID."); UI.pause_and_clear()

    def _manage_profile(self):
        while True:
            UI.clear_screen()
            print(f"\n\t--- Manage Profile of {self.current_user.username} ---\n\t1 - Change Password\n\t2 - Manage Addresses\n\t0 - Back")
            try:
                choice = int(input("\n\t=> "))
                if choice == 1:
                    current_password = input("\tCurrent password: ")
                    if self.current_user.password == current_password:
                        new_password = input("\tNew password: ")
                        if new_password and new_password == input("\tConfirm: "): 
                            self.current_user.password = new_password
                            print("\n\tPassword changed!")
                        else: print("\n\t[ERROR] Passwords do not match or are blank.")
                    else: print("\n\t[ERROR] Incorrect current password.")
                    UI.pause_and_clear()
                elif choice == 2:
                    if isinstance(self.current_user, Customer):
                        self._manage_addresses()
                    else:
                        print("\n\t[ERROR] This user type does not manage addresses."); UI.pause_and_clear()
                elif choice == 0: break
            except ValueError: print("\n\t[ERROR] Invalid option."); UI.pause_and_clear()

    def _manage_addresses(self):
        while True:
            UI.clear_screen()
            addresses = self.current_user.addresses
            print("\n\t--- My Addresses ---")
            if not addresses: print("\n\tNo registered addresses.")
            else:
                for i, addr in enumerate(addresses): print(f"\t{i+1} - {addr['nickname']}: {addr['street']}, {addr['city']}")
            print("\n\t1 - Add Address\n\t2 - Remove Address\n\t0 - Back")
            try:
                choice = int(input("\n\t=> "))
                if choice == 1:
                    nickname, street, city = input("\tNickname: "), input("\tStreet and number: "), input("\tCity and state: ")
                    if nickname and street and city:
                        self.current_user.add_address(nickname, street, city)
                        print("\n\tAddress added!")
                    else: print("\n\t[ERROR] All fields are required.")
                elif choice == 2:
                    if not addresses: print("\n\t[ERROR] No addresses to remove."); UI.pause_and_clear(); continue
                    remove_num = int(input("\tNumber of the address to remove: "))
                    if 1 <= remove_num <= len(addresses): print(f"\n\tAddress '{addresses.pop(remove_num - 1)['nickname']}' removed!")
                elif choice == 0: break
                UI.pause_and_clear()
            except ValueError: print("\n\t[ERROR] Invalid option."); UI.pause_and_clear()

    def _customer_support_menu(self):
        while True:
            UI.clear_screen(); print("\n\t--- Customer Support ---\n\t1 - Open Ticket\n\t2 - My Tickets\n\t0 - Back")
            try:
                choice = int(input("\n\t=> "))
                if choice == 1:
                    subject = input("\tSubject: ")
                    message = input("\tDescribe your problem: ")
                    if subject and message:
                        new_ticket = Ticket(self._generate_new_id(self.tickets), self.current_user.username, subject, message)
                        self.tickets.append(new_ticket)
                        print("\n\tTicket created successfully!")
                    else: print("\n\t[ERROR] Subject and message cannot be empty.")
                    UI.pause_and_clear()
                elif choice == 2:
                    UI.clear_screen(); print("\n\t--- My Support Tickets ---")
                    user_tickets = [t for t in self.tickets if t.user == self.current_user.username]
                    if not user_tickets: print("\n\tYou have not opened any tickets.")
                    else:
                        for ticket in user_tickets:
                            print("\n\t" + "="*40 + f"\n\tID: {ticket.id} | Status: {ticket.status}\n\tSubject: {ticket.subject}\n\tYour Message: {ticket.message}")
                            if ticket.admin_response: print(f"\tSupport Response: {ticket.admin_response}")
                    UI.wait_for_enter()
                elif choice == 0: break
            except ValueError: print("\n\t[ERROR] Invalid option."); UI.pause_and_clear()

    def _manage_products_admin(self):
        while True:
            UI.clear_screen(); print("\n\t--- Manage Products ---\n\n\t1 - List\n\t2 - Add\n\t3 - Edit\n\t4 - Remove\n\t0 - Back")
            try:
                option = int(input("\n\t=> "))
                if option == 1:
                    UI.clear_screen(); print("\n\t--- Catalog ---")
                    for p in self.products: print(f"\tID {p.id}: {p.name} - $ {p.price:.2f}")
                    UI.wait_for_enter()
                elif option == 2:
                    UI.clear_screen(); print("\n\t--- Add ---")
                    name, desc, price = input("\tName: "), input("\tDescription: "), float(input("\tPrice: "))
                    self.products.append(Product(self._generate_new_id(self.products), name, desc, price)); print("\n\tProduct added!")
                    UI.pause_and_clear()
                elif option == 3:
                    UI.clear_screen(); print("\n\t--- Edit ---")
                    product = self.find_product_by_id(int(input("\tProduct ID: ")))
                    if product:
                        print(f"\n\tEditing '{product.name}'. Leave blank to not change.")
                        new_name, new_desc, new_price = input("\tNew name: "), input("\tNew description: "), input("\tNew price: ")
                        if new_name: product.name = new_name
                        if new_desc: product.description = new_desc
                        if new_price: product.price = float(new_price)
                        print("\n\tProduct updated!")
                    else: print("\n\t[ERROR] Product not found.")
                    UI.pause_and_clear()
                elif option == 4:
                    UI.clear_screen(); print("\n\t--- Remove ---")
                    product = self.find_product_by_id(int(input("\tProduct ID: ")))
                    if product: self.products.remove(product); print(f"\n\tProduct '{product.name}' removed!")
                    else: print("\n\t[ERROR] Product not found.")
                    UI.pause_and_clear()
                elif option == 0: break
            except (ValueError, KeyError): print("\n\t[ERROR] Invalid option or ID."); UI.pause_and_clear()

    def _manage_coupons_admin(self):
        while True:
            UI.clear_screen(); print("\n\t--- Manage Coupons ---\n\t1 - List\n\t2 - Add\n\t3 - Activate/Deactivate\n\t0 - Back")
            try:
                choice = int(input("\n\t=> "))
                if choice == 1:
                    UI.clear_screen(); print("\n\t--- Coupon List ---")
                    if not self.coupons: print("\n\tNo coupons.")
                    else:
                        for c in self.coupons: print(c.get_display_info())
                    UI.wait_for_enter()
                elif choice == 2:
                    UI.clear_screen(); print("\n\t--- Add Coupon ---")
                    code = input("\tCode: ").upper()
                    if any(c.code == code for c in self.coupons): print("\n\t[ERROR] Code already exists."); UI.pause_and_clear(); continue
                    coupon_type = input("\tType ('percentage' or 'fixed'): ").lower()
                    if coupon_type not in ['percentage', 'fixed']: print("\n\t[ERROR] Invalid type."); UI.pause_and_clear(); continue
                    value = float(input(f"\tValue ({'%' if coupon_type=='percentage' else '$'}): "))
                    if coupon_type == 'percentage':
                        self.coupons.append(PercentageCoupon(code, value))
                    else:
                        self.coupons.append(FixedCoupon(code, value))
                    print("\n\tCoupon added!")
                    UI.pause_and_clear()
                elif choice == 3:
                    code = input("\tCoupon code to change: ").upper()
                    coupon = next((c for c in self.coupons if c.code == code), None)
                    if coupon:
                        coupon.active = not coupon.active
                        print(f"\n\tStatus changed to {'ACTIVE' if coupon.active else 'INACTIVE'}.")
                    else: print("\n\t[ERROR] Coupon not found.")
                    UI.pause_and_clear()
                elif choice == 0: break
            except ValueError: print("\n\t[ERROR] Invalid option."); UI.pause_and_clear()

    def _support_menu_admin(self):
        while True:
            UI.clear_screen()
            open_tickets = [t for t in self.tickets if t.status == 'Open']
            print(f"\n\t--- Customer Service (Admin) ---\n\tYou have {len(open_tickets)} open ticket(s).")
            print("\n\t1 - View/Reply to Open Tickets\n\t2 - View Full History\n\t0 - Back")
            try:
                choice = int(input("\n\t=> "))
                if choice == 1:
                    UI.clear_screen(); print("\n\t--- Open Tickets ---")
                    if not open_tickets: print("\n\tNo open tickets."); UI.pause_and_clear(); continue
                    for ticket in open_tickets: print("\n\t" + "="*40 + f"\n\tID: {ticket.id} | User: {ticket.user}\n\tSubject: {ticket.subject}\n\tMessage: {ticket.message}")
                    reply_id = int(input("\n\tID of the ticket to reply to (0 to go back): "))
                    if reply_id == 0: continue
                    target = next((t for t in open_tickets if t.id == reply_id), None)
                    if target:
                        target.admin_response = input(f"\tYour response to ticket #{target.id}: ")
                        target.status = 'Answered'
                        print("\n\tResponse sent!"); UI.pause_and_clear()
                    else: print("\n\t[ERROR] Invalid ID."); UI.pause_and_clear()
                elif choice == 2:
                    UI.clear_screen(); print("\n\t--- Ticket History ---") # <-- Linha Corrigida
                    if not self.tickets: print("\n\tNo tickets.")
                    else:
                        for ticket in self.tickets:
                            print("\n\t" + "="*40 + f"\n\tID: {ticket.id} | Status: {ticket.status}\n\tSubject: {ticket.subject}")
                            if ticket.admin_response: print(f"\tResponse: {ticket.admin_response}")
                    UI.wait_for_enter()
                elif choice == 0: break
            except ValueError: print("\n\t[ERROR] Invalid option."); UI.pause_and_clear()