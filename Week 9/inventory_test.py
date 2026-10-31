from inventory_manager import Product, PhysicalProduct, DigitalProduct, CanBeShipped

def check(label, condition):
    print(("PASS" if condition else "FAIL") + ": " + label)
    return condition

# ----- TEST PRODUCT -----
print("----- TEST PRODUCT -----")
product_results = []

try:
    Product("999", "Test", 1.0, 1)
    product_results.append(check("Product cannot be instantiated", False))
except TypeError:
    product_results.append(check("Product cannot be instantiated", True))

try:
    PhysicalProduct("9", "Test", 1.0, 1, 2.0)
    product_results.append(check("PhysicalProduct can be instantiated", True))
except TypeError:
    product_results.append(check("PhysicalProduct can be instantiated", False))

try:
    DigitalProduct("8", "Test", 1.0, 1, 2.0)
    product_results.append(check("DigitalProduct can be instantiated", True))
except TypeError:
    product_results.append(check("DigitalProduct can be instantiated", False))

print(f"{sum(product_results)} of {len(product_results)} checks passed")
print()

# ----- TEST CANBESHIPPED() -----
print("----- TEST CANBESHIPPED() -----")
shipping_results = []

p_light = PhysicalProduct("9", "Test", 1.0, 1, 0.5)
p_heavy = PhysicalProduct("10", "Test", 1.0, 1, 2.0)
d_item = DigitalProduct("8", "Test", 1.0, 1, 2.0)

shipping_results.append(check("PhysicalProduct is a CanBeShipped", isinstance(p_light, CanBeShipped)))
shipping_results.append(check("DigitalProduct is not a CanBeShipped", not isinstance(d_item, CanBeShipped)))
shipping_results.append(check("Shipping cost for 0.5 kg is 6.0", p_light.calculate_shipping_cost() == 6.0))
shipping_results.append(check("Shipping cost for 2.0 kg is 9.0", p_heavy.calculate_shipping_cost() == 9.0))
shipping_results.append(check("Heavier item costs more to ship", p_heavy.calculate_shipping_cost() > p_light.calculate_shipping_cost()))

print(f"{sum(shipping_results)} of {len(shipping_results)} checks passed")

# ----- TEST FULFILMENT MESSAGES -----
print("\n----- TEST FULFILMENT MESSAGES -----")
fulfilment_results = []

p_msg = PhysicalProduct("9", "Test", 1.0, 1, 0.5).get_fulfilment_info()
d_msg = DigitalProduct("8", "Test", 1.0, 1, 2.0).get_fulfilment_info()

fulfilment_results.append(check("PhysicalProduct returns its own fulfilment message", p_msg == "Ships to the customer's address."))
fulfilment_results.append(check("DigitalProduct returns a fulfilment message", isinstance(d_msg, str) and d_msg != ""))
fulfilment_results.append(check("Fulfilment messages differ between subclasses", p_msg != d_msg))

print(f"{sum(fulfilment_results)} of {len(fulfilment_results)} checks passed")