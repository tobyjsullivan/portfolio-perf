import csv

openPositions = {}
closedProfit = {}

with open('transactions.csv', 'rb') as csvfile:
  txnreader = csv.reader(csvfile)
  i = 0
  for row in txnreader:
    date = row[0]
    asset = row[1]
    qty = float(row[2])
    unitPrice = float(row[3])
    fees = float(row[4])
    print 'process line', i
    i += 1
    if qty > 0:
      if asset in openPositions:
        a = openPositions[asset]
        a['qty'] += qty
        a['bookTotal'] += (qty * unitPrice) + fees
        openPositions[asset] = a
      else:
        openPositions[asset] = {
          'qty': qty,
          'bookTotal': (qty * unitPrice) + fees
        }
    else:
      if asset not in openPositions:
        raise Exception('unknown asset')
      a = openPositions[asset]
      bookUnit = a['bookTotal'] / a['qty']
      a['qty'] += qty
      a['bookTotal'] = bookUnit * a['qty']
      if a['qty'] < 0:
        a = {'qty': 0, 'bookTotal': 0.0}
      openPositions[asset] = a
  # Print report
  print 'Asset,Qty,TotalBook'
  for a in openPositions:
    if openPositions[a]['qty'] > 0:
      print a, ',', openPositions[a]['qty'], ',', openPositions[a]['bookTotal']

