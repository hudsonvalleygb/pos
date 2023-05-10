from decimal import Decimal

from pos.models import Item

item_dict_list = [
    {
        'description': 'Slime',
        'quantity': 0,
        'cost': Decimal(0.69),
        'sale_price': Decimal('5.00'),
        'size': ''
    },
    {'description': 'Adult T-shirt, black', 'size': 'S', 'quantity': 1, 'cost': Decimal('9.65'), 'sale_price': Decimal('20.00')},
    {'description': 'Adult T-shirt, black', 'size': 'M', 'quantity': 2, 'cost': Decimal('9.65'), 'sale_price': Decimal('20.00')},
    {'description': 'Adult T-shirt, black', 'size': 'L', 'quantity': 1, 'cost': Decimal('9.65'), 'sale_price': Decimal('20.00')},
    {'description': 'Adult T-shirt, black', 'size': 'XL', 'quantity': 1, 'cost': Decimal('9.65'), 'sale_price': Decimal('20.00')},
    {'description': 'Adult T-shirt, black', 'size': 'XXL', 'quantity': 1, 'cost': Decimal('9.65'), 'sale_price': Decimal('20.00')},
    {'description': 'Adult T-shirt, black', 'size': 'XXXL', 'quantity': 1, 'cost': Decimal('9.65'), 'sale_price': Decimal('20.00')},
    {'description': 'Adult T-shirt, color', 'size': 'S', 'quantity': 2, 'cost': Decimal('9.65'), 'sale_price': Decimal('20.00')},
    {'description': 'Adult T-shirt, color', 'size': 'M', 'quantity': 2, 'cost': Decimal('9.65'), 'sale_price': Decimal('20.00')},
    {'description': 'Adult T-shirt, color', 'size': 'L', 'quantity': 1, 'cost': Decimal('9.65'), 'sale_price': Decimal('20.00')},
    {'description': 'Adult T-shirt, color', 'size': 'XL', 'quantity': 1, 'cost': Decimal('9.65'), 'sale_price': Decimal('20.00')},
    {'description': 'Adult T-shirt, color', 'size': 'XXL', 'quantity': 1, 'cost': Decimal('9.65'), 'sale_price': Decimal('20.00')},
    {'description': 'Adult T-shirt, color', 'size': 'XXXL', 'quantity': 2, 'cost': Decimal('9.65'), 'sale_price': Decimal('20.00')},
    {'description': 'Adult hoodie, oversized', 'size': 'XL', 'quantity': 2, 'cost': Decimal('24.00'), 'sale_price': Decimal('35.00')},
    {'description': 'Adult hoodie, oversized', 'size': 'XXL', 'quantity': 1, 'cost': Decimal('26.00'), 'sale_price': Decimal('38.00')},
    {'description': 'Adult hoodie, regular size', 'size': 'S', 'quantity': 2, 'cost': Decimal('24.00'), 'sale_price': Decimal('35.00')},
    {'description': 'Adult hoodie, regular size', 'size': 'M', 'quantity': 3, 'cost': Decimal('24.00'), 'sale_price': Decimal('35.00')},
    {'description': 'Adult hoodie, regular size', 'size': 'L', 'quantity': 1, 'cost': Decimal('24.00'), 'sale_price': Decimal('35.00')},
    {'description': "Children's T-shirt, black", 'size': 'S', 'quantity': 1, 'cost': Decimal('9.25'), 'sale_price': Decimal('15.00')},
    {'description': "Children's T-shirt, black", 'size': 'M', 'quantity': 1, 'cost': Decimal('9.25'), 'sale_price': Decimal('15.00')},
    {'description': "Children's T-shirt, black", 'size': 'L', 'quantity': 1, 'cost': Decimal('9.25'), 'sale_price': Decimal('15.00')},
    {'description': "Children's T-shirt, black", 'size': 'XS', 'quantity': 5, 'cost': Decimal('9.25'), 'sale_price': Decimal('15.00')},
    {'description': "Children's T-shirt, color", 'size': 'XS', 'quantity': 1, 'cost': Decimal('9.25'), 'sale_price': Decimal('15.00')},
    {'description': "Children's T-shirt, color", 'size': 'S', 'quantity': 1, 'cost': Decimal('9.25'), 'sale_price': Decimal('15.00')},
    {'description': "Children's T-shirt, color", 'size': 'M', 'quantity': 1, 'cost': Decimal('9.25'), 'sale_price': Decimal('15.00')},
    {'description': "Children's T-shirt, color", 'size': 'L', 'quantity': 1, 'cost': Decimal('9.25'), 'sale_price': Decimal('15.00')},
    {'description': 'Gift Box', 'size': '', 'quantity': 2, 'cost': Decimal('2.42'), 'sale_price': Decimal('10.00')},
    {'description': 'Green Screen Digital Only', 'size': '', 'quantity': 0, 'cost': Decimal('0.37'), 'sale_price': Decimal('7.00')},
    {'description': 'Green Screen Print', 'size': '', 'quantity': 5, 'cost': Decimal('0.75'), 'sale_price': Decimal('10.00')},
    {'description': 'HVGB Patch', 'size': '', 'quantity': 1, 'cost': Decimal('15.39'), 'sale_price': Decimal('20.00')},
    {'description': 'Joe Inga Print, 11x17', 'size': '', 'quantity': 3, 'cost': Decimal('0.00'), 'sale_price': Decimal('10.00')},
    {'description': 'Joe Inga Print, 8.5x11', 'size': '', 'quantity': 6, 'cost': Decimal('0.00'), 'sale_price': Decimal('5.00')},
    {'description': 'Joe Inga Print, Framed', 'size': '', 'quantity': 3, 'cost': Decimal('10.00'), 'sale_price': Decimal('20.00')},
]

def pop_db():
    for item_dict in item_dict_list:
        Item.objects.create(**item_dict)
