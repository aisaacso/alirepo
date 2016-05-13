import sqlite3 as sq
import inspect
import pandas as pd

conn = sq.connect('Northwind.sl3')
conn.row_factory = sq.Row
conn.text_factory = str
cursor = conn.cursor()
names = []
#names = [x.replace(' ', '') for x in tables] #Actullay need to do this globally.

#names = [description[0] for description in cursor.description]

# Note on Employees data: the Notes column will print memory location, have to key into it. Why?

#for row in cursor.execute("select name from sqlite_master where type = 'table' order by name").fetchall(): print row[0]
#for row in cursor.execute("PRAGMA TABLE_INFO('Products')").fetchall(): print row[1]

#for getting info about objects
#info = inspect.getsource(pdi.values_in_col)

def all_db_tables():
    tables = []
    for row in cursor.execute("select name from sqlite_master where type = 'table' order by name").fetchall(): 
        tables.append(row[0])
        tables = [x.replace(' ', '') for x in tables] #Actullay need to do this globally.
    for i in tables:
        columns = []
        for k in cursor.execute("PRAGMA TABLE_INFO(" + i + ")").fetchall(): 
            columns.append(k[1])
        print i, ": ", columns
        print

#data = cursor.execute(query).fetchone()
#print data.keys()

products_query = "SELECT CategoryID, MIN(UnitPrice) AS Min, MAX(UnitPrice) AS Max, Avg(UnitPrice) as Avg, COUNT(ProductID) AS Count FROM Products GROUP BY CategoryID HAVING Count(*) > 10"

having_where_query = "SELECT CategoryID FROM Products WHERE UnitPrice > 10 GROUP BY CategoryID HAVING Count(*) > 7"

join_example_query = "SELECT CategoryName, Avg(UnitPrice) AS AvgPrice FROM Products INNER JOIN Categories ON Products.CategoryID=Categories.CategoryID GROUP BY Categories.CategoryID"

join_query = "SELECT CompanyName, Count(*) \
FROM Orders LEFT JOIN Customers ON Customers.CustomerID = Orders.CustomerID \
GROUP BY(Customers.CustomerID)" #How do you get it to limit to only 1995? OrderDate < doesn't work

self_join_query = "SELECT Employees.FirstName, Employees.LastName, Supervisors.LastName AS Super \
FROM Employees LEFT JOIN Employees AS Supervisors ON Employees.ReportsTo = Supervisors.EmployeeID"

query1 = "SELECT ProductName, UnitsInStock FROM Products WHERE (ReorderLevel - UnitsInStock) > 9"

query2 = "SELECT Sum(UnitPrice) FROM [Order Details] GROUP BY OrderID"

# For each order, what's the value?
order_val = "SELECT OrderID, Sum(UnitPrice * Quantity) AS OrdVal FROM [Order Details] GROUP BY OrderID"

# Prob 7 For each Customer, what's the value of their orders?
cust_val = "SELECT Orders.CustomerID, Count(OV.OrderID) AS CountOrders, Sum(OV.OrdVal) AS SumOrdVal FROM Orders INNER JOIN (" + order_val + ") AS OV ON Orders.OrderID = OV.OrderID GROUP BY Orders.CustomerID HAVING CountOrders > 15 OR SumOrdVal > 30000"

#All order IDs from Exotic Liquids
ex_liq_prods = "SELECT ProductID, Suppliers.CompanyName FROM Products INNER JOIN Suppliers ON Suppliers.SupplierID = Products.SupplierID WHERE Suppliers.CompanyName = 'Exotic Liquids'"

# All order details for every product ordered
order_prod_dets = "SELECT Orders.*, [Order Details].* FROM Orders INNER JOIN [Order Details] ON Orders.OrderID = [Order Details].OrderID"

# Prob 8
orders_by_exotic = "SELECT ELP.CompanyName AS Proof, OPD.OrderID AS OrderID, OPD.CustomerID AS CustomerID FROM (" + order_prod_dets + ") AS OPD INNER JOIN (" + ex_liq_prods + ") AS ELP ON ELP.ProductID = OPD.ProductID"

big_orders = "SELECT CustGroups.CustomerID FROM (SELECT Orders.CustomerID, OV.OrderID, OV.OrdVal FROM Orders INNER JOIN (" + order_val + ") AS OV ON Orders.OrderID = OV.OrderID WHERE OrdVal > 10000) AS CustGroups GROUP BY CustGroups.CustomerID"

# Prob 9
# Remove sum, count and groupby from cust_val, then join with customers for CompanyName
big_custs = "SELECT Customers.CompanyName FROM Customers INNER JOIN (" + big_orders + ") AS CustsBigOrders ON Customers.CustomerID = CustsBigOrders.CustomerID"

# Prob 10
no_big_ord = "SELECT Customers.CompanyName, Customers.CustomerID FROM Customers WHERE Customers.CompanyName NOT IN (" + big_custs + ")"

df = pd.read_sql_query(no_big_ord, conn)
print df

conn.close()

# NEXT: how to do space replacement globally
