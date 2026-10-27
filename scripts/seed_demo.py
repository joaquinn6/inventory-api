"""Puebla la base de demo a través de la API (tienda de tecnología).

Usa los endpoints reales, así que el stock, el historial de precios y el dashboard
se calculan con la misma lógica de negocio que en producción.

Variables de entorno:
  INVENTORY_API_URL  URL de la API (por defecto, la de Render)
  ADMIN_EMAIL        Correo de un usuario ADMIN existente
  ADMIN_PASSWORD     Contraseña de ese usuario
  DEMO_PASSWORD      Contraseña para los usuarios de prueba

Uso:
  python scripts/seed_demo.py

Es idempotente: actualiza usuarios, proveedores y productos que ya existan (por correo
o código) y solo registra compras y ventas si todavía no hay ninguna.
"""
import os
import random
import sys

import requests

API_URL = os.getenv('INVENTORY_API_URL',
                    'https://inventory-api-xetu.onrender.com').rstrip('/')
TIMEOUT = 90

CATEGORIES = ['Laptops', 'Celulares', 'Accesorios', 'Audio',
              'Almacenamiento', 'Monitores', 'Redes']

USERS = [
    {'email': 'admin@qwerty.com', 'full_name': 'Administrador Demo',
     'roles': ['ADMIN']},
    {'email': 'gerente@qwerty.com', 'full_name': 'Gerente Demo',
     'roles': ['MANAGER']},
    {'email': 'ventas@qwerty.com', 'full_name': 'Vendedor Demo',
     'roles': ['SALES']},
]

SUPPLIERS = [
    {'code': 'GOOGLE', 'name': 'Google',
     'contact': {'name': 'Andrea Morales', 'email': 'ventas@google-distribuidor.com', 'phone': '22501010'}},
    {'code': 'TECHDIST', 'name': 'Tech distribuidora',
     'contact': {'name': 'Carlos Rivas', 'email': 'carlos@techdist.com', 'phone': '22781234'}},
    {'code': 'COMPUMAY', 'name': 'Compumayor',
     'contact': {'name': 'Lucía Pérez', 'email': 'lucia@compumayor.com', 'phone': '22665544'}},
    {'code': 'ACCESCA', 'name': 'Accesorios centroamérica',
     'contact': {'name': 'Mario López', 'email': 'mario@accesca.com', 'phone': '22493377'}},
]

# code, nombre, descripción, categorías, garantía (medida, cantidad), proveedor,
# precio de compra inicial, precio de compra en la segunda compra, margen de venta
PRODUCTS = [
    ('A0001', 'Cable HDMI 2.1 2m', 'Soporta 4k a 120hz y 8k a 60hz',
     ['ACCESORIOS'], None, 'ACCESCA', 4.5, 4.0, 1.9),
    ('LAP001', 'Laptop Lenovo IdeaPad 3', 'Ryzen 5, 8gb ram, 512gb ssd, 15.6"',
     ['LAPTOPS'], ('YEAR', 1), 'COMPUMAY', 420, 435, 1.25),
    ('LAP002', 'Laptop HP 15', 'Intel core i5, 16gb ram, 512gb ssd',
     ['LAPTOPS'], ('YEAR', 1), 'COMPUMAY', 510, 495, 1.25),
    ('LAP003', 'MacBook Air M2', '8gb ram, 256gb ssd, 13.6"',
     ['LAPTOPS'], ('YEAR', 1), 'TECHDIST', 890, 870, 1.2),
    ('CEL001', 'Google Pixel 8a', '128gb, pantalla oled 6.1"',
     ['CELULARES'], ('MONTH', 6), 'GOOGLE', 360, 345, 1.3),
    ('CEL002', 'Samsung Galaxy A55', '256gb, 8gb ram',
     ['CELULARES'], ('MONTH', 6), 'TECHDIST', 330, 340, 1.3),
    ('CEL003', 'Xiaomi Redmi Note 13', '128gb, 6gb ram',
     ['CELULARES'], ('MONTH', 6), 'TECHDIST', 165, 158, 1.35),
    ('AUD001', 'Audífonos Sony WH-CH520', 'Inalámbricos, 50 horas de batería',
     ['AUDIO'], ('MONTH', 3), 'ACCESCA', 38, 41, 1.6),
    ('AUD002', 'Parlante JBL Flip 6', 'Bluetooth, resistente al agua ip67',
     ['AUDIO'], ('MONTH', 6), 'ACCESCA', 85, 82, 1.45),
    ('ALM001', 'SSD Kingston NV2 1TB', 'Nvme pcie 4.0',
     ['ALMACENAMIENTO'], ('YEAR', 3), 'COMPUMAY', 52, 48, 1.5),
    ('ALM002', 'Memoria USB SanDisk 64GB', 'Usb 3.2',
     ['ALMACENAMIENTO', 'ACCESORIOS'], ('YEAR', 1), 'ACCESCA', 6, 6.5, 1.8),
    ('MON001', 'Monitor LG 24" IPS', 'Full hd, 75hz, hdmi',
     ['MONITORES'], ('YEAR', 1), 'COMPUMAY', 98, 104, 1.35),
    ('RED001', 'Router TP-Link Archer AX23', 'Wifi 6, doble banda',
     ['REDES'], ('YEAR', 2), 'TECHDIST', 48, 46, 1.5),
    ('ACC001', 'Mouse Logitech M185', 'Inalámbrico',
     ['ACCESORIOS'], ('MONTH', 6), 'ACCESCA', 9, 9.5, 1.8),
    ('ACC002', 'Teclado mecánico Redragon Kumara', 'Switches red, retroiluminado',
     ['ACCESORIOS'], ('MONTH', 6), 'ACCESCA', 28, 26, 1.6),
    ('ACC003', 'Cargador USB-C 25W Samsung', 'Carga rápida',
     ['ACCESORIOS', 'CELULARES'], ('MONTH', 3), 'TECHDIST', 11, 12, 1.8),
]

# Unidades de la primera compra según la categoría principal
FIRST_UNITS = {'LAPTOPS': 6, 'CELULARES': 10, 'AUDIO': 15, 'ALMACENAMIENTO': 25,
               'MONITORES': 8, 'REDES': 12, 'ACCESORIOS': 30}

CUSTOMERS = ['', '', '', 'María González', 'José Martínez', 'Ana Castillo',
             'Luis Hernández', 'Carmen Flores', 'Pedro Sánchez', 'Sofía Ramírez',
             'Jorge Mendoza', 'Valeria Ortega']
PAY_TYPES = ['CASH', 'CASH', 'DEBIT_CARD', 'CREDIT_CARD', 'TRANSFER']


class Api:
  def __init__(self, base_url: str):
    self._base = base_url
    self._session = requests.Session()

  def login(self, email: str, password: str):
    data = self.request('POST', 'login', json={
                        'email': email, 'password': password})
    self._session.headers['Authorization'] = data['token']
    return data

  def request(self, method: str, path: str, **kwargs):
    res = self._session.request(
        method, f'{self._base}/{path}', timeout=TIMEOUT, **kwargs)
    if not res.ok:
      raise RuntimeError(f'{method} /{path} -> {res.status_code}: {res.text}')
    return res.json() if res.content else None

  def items(self, path: str) -> list:
    return self.request('GET', path)['items']


def seed_config(api: Api):
  config = api.request('GET', 'config')
  config['product']['categories'] = CATEGORIES
  api.request('PUT', 'config', json=config)
  print(f'Configuración: {len(CATEGORIES)} categorías')


def seed_users(api: Api, password: str):
  existing = {user['email'] for user in api.items('users')}
  for user in USERS:
    if user['email'] in existing:
      print(f'Usuario ya existe: {user["email"]}')
      continue
    api.request('POST', 'users', json={**user, 'password': password})
    print(f'Usuario creado: {user["email"]} ({user["roles"][0]})')


def seed_suppliers(api: Api) -> dict:
  existing = {s['code']: s for s in api.items('suppliers')}
  for supplier in SUPPLIERS:
    if supplier['code'] in existing:
      api.request(
          'PUT', f'suppliers/{existing[supplier["code"]]["_id"]}', json=supplier)
    else:
      api.request('POST', 'suppliers', json=supplier)
  print(f'Proveedores: {len(SUPPLIERS)}')
  return {s['code']: s['_id'] for s in api.items('suppliers')}


def seed_products(api: Api) -> dict:
  existing = {p['code']: p for p in api.items('products')}
  for code, name, description, categories, warranty, *_ in PRODUCTS:
    body = {
        'code': code,
        'name': name,
        'description': description,
        'categories': categories,
        'warranty': {
            'has_warranty': warranty is not None,
            'measure': warranty[0] if warranty else '',
            'quantity': warranty[1] if warranty else 0,
        },
    }
    if code in existing:
      api.request('PUT', f'products/{existing[code]["_id"]}', json=body)
    else:
      api.request('POST', 'products', json=body)
  print(f'Productos: {len(PRODUCTS)}')
  return {p['code']: p for p in api.items('products')}


def purchase(api: Api, supplier_id: str, lines: list, stock: dict, prices: dict):
  api.request('POST', 'purchases', json={
      'supplier_id': supplier_id,
      'products': [{'_id': product_id, 'units': units, 'purchase_price': cost,
                    'sale_price': sale} for product_id, units, cost, sale in lines],
  })
  for product_id, units, _, sale in lines:
    stock[product_id] = stock.get(product_id, 0) + units
    prices[product_id] = sale


def seed_purchases(api: Api, suppliers: dict, products: dict, stock: dict, prices: dict, second: bool):
  by_supplier = {}
  for code, _, _, categories, _, supplier, first_cost, second_cost, margin in PRODUCTS:
    units = FIRST_UNITS[categories[0]]
    cost = second_cost if second else first_cost
    if second:
      units = max(2, units // 2)
    line = (products[code]['_id'], units, cost, round(cost * margin, 2))
    by_supplier.setdefault(supplier, []).append(line)

  for supplier, lines in by_supplier.items():
    purchase(api, suppliers[supplier], lines, stock, prices)
  label = 'Segunda ronda de compras' if second else 'Compras iniciales'
  print(f'{label}: {len(by_supplier)}')


def seed_sales(api: Api, stock: dict, prices: dict, count: int, rng: random.Random):
  created = 0
  for _ in range(count):
    available = [product_id for product_id, units in stock.items() if units > 0]
    if not available:
      break
    lines = []
    for product_id in rng.sample(available, k=min(len(available), rng.choice([1, 1, 1, 2, 2, 3]))):
      units = min(stock[product_id], rng.choice([1, 1, 1, 2, 3]))
      lines.append({'_id': product_id, 'units': units,
                    'sale_price': prices[product_id]})
      stock[product_id] -= units
    api.request('POST', 'sales', json={
        'products': lines,
        'pay_type': rng.choice(PAY_TYPES),
        'customer': rng.choice(CUSTOMERS),
    })
    created += 1
  print(f'Ventas: {created}')


def main():
  missing = [name for name in ('ADMIN_EMAIL', 'ADMIN_PASSWORD', 'DEMO_PASSWORD')
             if not os.getenv(name)]
  if missing:
    sys.exit(f'Faltan variables de entorno: {", ".join(missing)}')

  api = Api(API_URL)
  print(f'API: {API_URL} (puede tardar si Render está dormido)')
  api.login(os.environ['ADMIN_EMAIL'], os.environ['ADMIN_PASSWORD'])

  seed_config(api)
  seed_users(api, os.environ['DEMO_PASSWORD'])
  suppliers = seed_suppliers(api)
  products = seed_products(api)

  if api.items('purchases') or api.items('sales'):
    print('Ya hay compras o ventas registradas; no se agregan más.')
    return

  rng = random.Random(2025)
  stock, prices = {}, {}
  seed_purchases(api, suppliers, products, stock, prices, second=False)
  seed_sales(api, stock, prices, 25, rng)
  seed_purchases(api, suppliers, products, stock, prices, second=True)
  seed_sales(api, stock, prices, 20, rng)


if __name__ == '__main__':
  main()
