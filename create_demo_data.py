import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from inventory.models import Stock
from transactions.models import Supplier, PurchaseBill, PurchaseItem, PurchaseBillDetails, SaleBill, SaleItem
from django.contrib.auth.models import User

# Create superuser if not exists
def create_superuser():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        print('Superuser created successfully!')
    else:
        print('Superuser already exists!')

# Create demo stock items
def create_stock_items():
    stock_items = [
        {'name': 'Laptop', 'quantity': 50},
        {'name': 'Desktop', 'quantity': 30},
        {'name': 'Mouse', 'quantity': 100},
        {'name': 'Keyboard', 'quantity': 80},
        {'name': 'Monitor', 'quantity': 40},
        {'name': 'Headphones', 'quantity': 60},
        {'name': 'Printer', 'quantity': 25},
        {'name': 'Scanner', 'quantity': 15},
        {'name': 'USB Drive', 'quantity': 120},
        {'name': 'External HDD', 'quantity': 35},
    ]
    
    for item in stock_items:
        stock, created = Stock.objects.get_or_create(
            name=item['name'],
            defaults={'quantity': item['quantity']}
        )
        if created:
            print(f"Created stock: {stock.name}")
        else:
            print(f"Stock {stock.name} already exists")

# Create demo suppliers
def create_suppliers():
    suppliers = [
        {
            'name': 'Tech Solutions Inc.',
            'phone': '9876543210',
            'address': '123 Tech Street, Silicon Valley',
            'email': 'info@techsolutions.com',
            'gstin': 'TECH1234567890'
        },
        {
            'name': 'Global Electronics',
            'phone': '8765432109',
            'address': '456 Global Avenue, New York',
            'email': 'sales@globalelectronics.com',
            'gstin': 'GLOB9876543210'
        },
        {
            'name': 'Digital Devices Ltd',
            'phone': '7654321098',
            'address': '789 Digital Road, Tokyo',
            'email': 'contact@digitaldevices.com',
            'gstin': 'DIGI5678901234'
        },
    ]
    
    for supplier_data in suppliers:
        supplier, created = Supplier.objects.get_or_create(
            email=supplier_data['email'],
            defaults={
                'name': supplier_data['name'],
                'phone': supplier_data['phone'],
                'address': supplier_data['address'],
                'gstin': supplier_data['gstin']
            }
        )
        if created:
            print(f"Created supplier: {supplier.name}")
        else:
            print(f"Supplier {supplier.name} already exists")

# Create demo purchase transactions
def create_purchases():
    # Get suppliers
    suppliers = Supplier.objects.all()
    if not suppliers.exists():
        print("No suppliers found. Please create suppliers first.")
        return
    
    # Get stock items
    stocks = Stock.objects.all()
    if not stocks.exists():
        print("No stock items found. Please create stock items first.")
        return
    
    # Create purchase bills
    for i, supplier in enumerate(suppliers):
        # Create purchase bill
        purchase_bill = PurchaseBill.objects.create(supplier=supplier)
        
        # Add items to the purchase bill
        for j in range(3):  # Add 3 items per bill
            stock_index = (i + j) % stocks.count()
            stock = stocks[stock_index]
            quantity = (j + 1) * 5  # 5, 10, 15
            per_price = (j + 1) * 100  # 100, 200, 300
            total_price = quantity * per_price
            
            PurchaseItem.objects.create(
                billno=purchase_bill,
                stock=stock,
                quantity=quantity,
                perprice=per_price,
                totalprice=total_price
            )
        
        # Add bill details
        PurchaseBillDetails.objects.create(
            billno=purchase_bill,
            eway=f"EW{i+1}00{i+1}",
            veh=f"VH-{i+1}00{i+1}",
            destination="Warehouse A",
            po=f"PO-{i+1}00{i+1}",
            cgst="9%",
            sgst="9%",
            igst="0%",
            cess="1%",
            tcs="1%",
            total=str(purchase_bill.get_total_price())
        )
        
        print(f"Created purchase bill #{purchase_bill.billno} for {supplier.name}")

# Create demo sales transactions
def create_sales():
    # Get stock items
    stocks = Stock.objects.all()
    if not stocks.exists():
        print("No stock items found. Please create stock items first.")
        return
    
    # Customer data
    customers = [
        {
            'name': 'John Doe',
            'phone': '1234567890',
            'address': '123 Main St, Anytown',
            'email': 'john@example.com',
            'gstin': 'CUST1234567890'
        },
        {
            'name': 'Jane Smith',
            'phone': '2345678901',
            'address': '456 Oak Ave, Somewhere',
            'email': 'jane@example.com',
            'gstin': 'CUST2345678901'
        },
        {
            'name': 'Bob Johnson',
            'phone': '3456789012',
            'address': '789 Pine Rd, Nowhere',
            'email': 'bob@example.com',
            'gstin': 'CUST3456789012'
        },
    ]
    
    # Create sale bills
    for i, customer in enumerate(customers):
        # Create sale bill
        sale_bill = SaleBill.objects.create(
            name=customer['name'],
            phone=customer['phone'],
            address=customer['address'],
            email=customer['email'],
            gstin=customer['gstin']
        )
        
        # Add items to the sale bill
        for j in range(2):  # Add 2 items per bill
            stock_index = (i + j) % stocks.count()
            stock = stocks[stock_index]
            quantity = (j + 1) * 2  # 2, 4
            per_price = (j + 1) * 150  # 150, 300
            total_price = quantity * per_price
            
            SaleItem.objects.create(
                billno=sale_bill,
                stock=stock,
                quantity=quantity,
                perprice=per_price,
                totalprice=total_price
            )
        
        print(f"Created sale bill #{sale_bill.billno} for {customer['name']}")

# Main function to create all demo data
def create_all_demo_data():
    print("Creating demo data...")
    create_superuser()
    create_stock_items()
    create_suppliers()
    create_purchases()
    create_sales()
    print("Demo data creation completed!")

if __name__ == "__main__":
    create_all_demo_data()