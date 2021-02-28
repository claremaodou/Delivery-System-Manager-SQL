#----------------------------------------------------
# Personal Project: Small Business Deliveries
# Author: Clare (ME!)
#----------------------------------------------------
import pyodbc
    
def printInstructions():
    '''
    Inputs: None
    Returns: user_input
    '''
    title = 'Welcome to the Small Business Delivery Program'
    print('*'*len(title))
    print(title)
    print('*'*len(title))
    
    print('What would you like to do?')
    print('1. Display DELIVERY SUMMARY TABLE for this week')
    print('2. Display and save DELIVERY ORDER for specific address')
    print('3. Quit')
    user_input = input('> ')
    return user_input


def readOrderFile():
    '''
    Inputs: None
    Returns: order_info
    ''' 
    order_info = []
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=LAPTOP-6DR29Q9A\SQLEXPRESS;'
                          'Database=Project;'
                          'Trusted_Connection=yes;')
    
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Project.dbo.ORDERS')
    
    for row in cursor:
        order_info.append(list(row))
    return order_info

def createOrderDict(order_info):
    '''
    Inputs: order_info
    Returns: order_dict
    '''
    order_dict = {}
    for i in order_info: 
        key = i[2] # address is the key
        val = [i[0].replace('-',''), i[3], i[4]] # gets rid of '-'
        if key in order_dict:
            order_dict[key].append(val) # makes list of lists as value
        else:
            order_dict[key] = [val]
    return order_dict

def readProductFile():
    '''
    Inputs: None
    Returns: product_info
    '''
    product_info = []
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=LAPTOP-6DR29Q9A\SQLEXPRESS;'
                          'Database=Project;'
                          'Trusted_Connection=yes;')
    
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Project.dbo.PRODUCTS')
    
    for row in cursor:
        product_info.append(list(row))
    return product_info

def createProductDict(product_info):
    '''
    Inputs: product_info
    Returns: product_dict
    '''
    product_dict = {}
    for i in product_info:
        key = i[0]
        val = [i[1], i[2]]
        product_dict[key] = val
    return product_dict
    
def readZoneFile():
    '''
    Inputs: None
    Returns: zone_info
    '''
    zone_info = []
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=LAPTOP-6DR29Q9A\SQLEXPRESS;'
                          'Database=Project;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Project.dbo.ZONES')  
    for row in cursor:
        zone_info.append(list(row))
    return zone_info
    
def createZoneDict(zone_info):
    '''
    Inputs: zone_info
    Returns: zone_dict
    '''
    zone_dict = {}
    for i in zone_info:
        if i[0] in zone_dict:
            s = zone_dict[i[0]]
            s.append(i[1])
            zone_dict[i[0]] = s
        else:
            zone_dict[i[0]] = [i[1]]
    return zone_dict

def getPostalCode(order_info):
    '''
    Inputs: order_info
    Returns: postal_code
    '''
    # Get postal code from addresses
    address = []
    for i in order_info:
        address.append(i[2])
    address = set(address) # make sure that the same addresses are grouped together
    postal_code = []
    for i in address:
        postal_code.append(i[-7:-4])
    return postal_code

def getDistricts(postal_code, zone_dict):
    '''
    Inputs: postal_code, zone_dict
    Returns: districts
    '''
    # Get list of districts from the postal code
    districts = list()
    for i in postal_code:
        for key, val in zone_dict.items():
            if i in val:
                districts.append(key)
    return districts

def getDeliveries(districts):
    '''
    Inputs: districts
    Returns: district_dict
    '''
    # Get number of deliveries per district and total deliveries
    district_dict = dict()
    # Iterate over each element in list
    for i in districts:
        # If element exists in dict then increment its value else add it in dict
        if i in district_dict:
            district_dict[i] += 1 
        else:
            district_dict[i] = 1  
    return district_dict
    
            
def deliveryTotal(districts, district_dict):
    '''
    Inputs: districts, district_dic
    Returns: delivery_total
    '''
    delivery_total = 0
    for i in districts:
        # If element exists in dict then increment its value else add it in dict
        if i in district_dict:
            delivery_total += 1
        else:
            delivery_total += 1
    return delivery_total
        
    
            
def deliveryCost(delivery_total):
    '''
    Input: delivery_total
    Return: delivery_cost
    '''
    delivery_cost = delivery_total*12
    return delivery_cost

def alphabeticalDistricts(district_dict):
    '''
    Input: district_dict
    Returns: unique_districts
    '''
    unique_districts = list(district_dict.keys()) # get list of districts alphabetical
    unique_districts.sort()
    return unique_districts

def driverNum(unique_districts, district_dict):
    '''
    Inputs: unique_districts, district_dict
    Returns: driver_dict
    '''
    driver_dict = {}
    for i in unique_districts:
        key = i
        deliveries = district_dict[i]
        if deliveries%10 != 0:
            drivers = (deliveries//10) +1
        else:
            drivers = deliveries//10
        val = drivers
        driver_dict[key] = val
    return driver_dict

def driverTotal(unique_districts, district_dict):
    ''''
    Inputs: unique_districts, district_dict
    Returns: driver_total
    '''
    driver_total = 0
    for i in unique_districts:
        key = i
        deliveries = district_dict[i]
        if deliveries%10 != 0:
            drivers = (deliveries//10) +1
        else:
            drivers = deliveries//10
        driver_total += int(drivers)
    return driver_total



def printOption1(district_dict, driver_dict, driver_total, delivery_cost, unique_districts):
    '''
    Inputs: district_dict, driver_dict, driver_total, delivery_cost
    Returns: None
    '''
    txt1 = 'Delivery Zone'
    txt2 = 'Deliveries'
    txt3 = 'Drivers'
    txt4 = 'Total drivers needed'
    txt5 = 'Total delivery cost'
    txt6 = 'Delivery cost/purchases'
    print("+{}+{}+{}+".format('-'*15, '-'*12, '-'*11)) # first row divider
    print("|{:<15}|{:^12}|{:^11}|".format(' '+txt1, txt2, txt3)) # aligning titles
    print("+{}+{}+{}+".format('-'*15, '-'*12, '-'*11)) # second row divider
    for i in unique_districts:
        print("|{:<15}|{:^12}|{:^11}|".format(' '+i, district_dict[i], driver_dict[i] )) 
    print("+{}+{}+{}+".format('-'*15, '-'*12, '-'*11)) # third row divider
    print("|{:<15}{:>19}|".format(' '+txt4, str(driver_total)+' ')) # total driver
    print("|{:<15}".format(' ' +txt5) + "$  {:.2f} |".format(delivery_cost).rjust(21)) # total delivery cost
    print("|{:<15}".format(' ' +txt6) + "$  {:.2f} |".format(delivery_cost).rjust(17)) # percentage
    print("+{}+{}+{}+".format('-'*15, '-'*12, '-'*11)) # fourth row divider

def orderDates(order_dict, option2_input):
    '''
    Order dictionary according to date
    Inputs: order_dict, option2_input
    Returns: order_dict
    '''
    order_dict[option2_input].sort(key = lambda x: x[1]) 
    return order_dict


def getDates(order_dict, option2_input):
    '''
    Inputs: order_dict, option2_input
    Returns: dates
    '''
    # sets up dates 
    dates = []
    for i in order_dict[option2_input]:
        dates.append(i[0])
    return dates

def getMonthName(dates):
    '''
    Inputs: dates
    Returns: mon
    '''
    months = {'01': 'JAN', '02':'FEB', '03':'MAR', '04':'APR', '05':'MAY', '06':'JUN', '07':'JUL', 
        '08': 'AUG', '09': 'SEP', '10':'OCT', '11':'NOV', '12':'DEC'}   
    mon_num = []
    mon = []
    for i in dates: 
        mon_num.append(i[4:6]) # get the month number     
    for i in mon_num: # get the corresponding month from month number
        mon.append(months[i])
    return mon

def getDay(dates):
    '''
    Inputs: dates
    Returns: day
    '''
    day = []
    for i in dates: 
        day.append(i[6:9]) # get the day number   
    return day
    
 
def getOrderId(order_dict, option2_input):
    '''
    Inputs: order_dict, option2_input
    Returns: order_id
    '''
    order_id = []
    for i in order_dict[option2_input]:
        order_id.append(i[1])
    return order_id
        
def getOrderQuantity(order_dict, option2_input):
    '''
    Inputs: order_dict, option2_input
    Returns: order_id
    '''
    order_q = []
    for i in order_dict[option2_input]:
        order_q.append(i[2])   
    return order_q

def getProductName(order_id, product_dict):
    '''
    Inputs: order_id, product_dict
    Returns: product_name
    '''
    product_name = []
   
    for i in order_id:
        product_name.append((product_dict[i])[0])
    return product_name
        
def getProductPrice(order_id, product_dict):
    '''
    Inputs: order_id, product_dict
    Returns: product_price
    '''
    product_price = []
    for i in order_id:
        product_price.append((product_dict[i])[1])   
    return product_price
    
def checkProductNameLength(product_name):
    '''
    Input: product_name
    Returns: product_name
    '''
    for i in range(len(product_name)): # check if product name is over 20 characters
        if len(product_name[i]) > 20:
            product_name[i] = str(((product_name[i])[0:19]))+'*'
    return product_name

def calculatePrices(product_price, order_q):
    '''
    Inputs: order_1, product_price
    Returns: prices
    '''
    prices = []
    for i in range(len(order_q)):
        prices.append((int(order_q[i])*int(product_price[i])))
    return prices

    
def checkAdressLength(option2_input):
    '''
    Input: option2_input
    Returns: option2_input
    '''
    if len(option2_input) > 30: # checks if address is over 30 characters________
        option2_input = str(option2_input[0:29])+'*'
    return option2_input

def checkAddress(order_info, option2_input):
    '''
    Inputs: order_info, option2_input
    Returns: option2_input
    '''
    address = []
    for i in order_info:
        address.append(i[2])
    address = set(address)    
    while option2_input not in address:
        print('Enter a Valid Address')
        option2_input = input('Address: ')
    return option2_input
        
def printOption2(option2_input, mon, day, order_q, product_name, prices):
    '''
    Inputs: option2_input, mon, day, order_1, product_name, prices
    Returns: None
    '''
    txt7 = 'Delivery for:'
    txt8 = 'Date'
    txt9 = 'Item'
    txt10 = 'Price'
    print("{:<15}{:>30}".format(txt7, option2_input)) 
    print('='*45)
    print("{:<8}{:<28}{:<9}".format(txt8, txt9, txt10)) # aligning titles
    print("{:<8}{:<28}{:<9}".format('-'*6, '-'*26, '-'*9)) # aligning titles
    for i in range(len(mon)):
        print("{:<8}".format(mon[i] + ' '+ day[i])+"{:03d} x {}".format(int(order_q[i]),product_name[i]).ljust(28)+'{:.2f}'.format(prices[i]/100).ljust(9)) 


        
def main():
    
        
    order_info = readOrderFile()
    order_dict = createOrderDict(order_info)
    product_info = readProductFile()
    product_dict = createProductDict(product_info)
    zone_info = readZoneFile()
    zone_dict = createZoneDict(zone_info)
    postal_code = getPostalCode(order_info)
    districts = getDistricts(postal_code, zone_dict)
    district_dict = getDeliveries(districts)
    delivery_total = deliveryTotal(districts, district_dict)
    delivery_cost = deliveryCost(delivery_total)
    unique_districts = alphabeticalDistricts(district_dict)
    driver_dict = driverNum(unique_districts, district_dict)
    driver_total = driverTotal(unique_districts, district_dict)
    user_choice = printInstructions()
    if user_choice == '3':
        print("Thank you for using the Small Business Delivery Program! Goodbye.")   
        exit()
    while user_choice == '1' or '2':
        while user_choice == '1':
            printOption1(district_dict, driver_dict, driver_total, delivery_cost, unique_districts)
            user_choice = printInstructions()
        while user_choice == '2':
            option2_input = input('Address: ')
            option2_input = checkAddress(order_info, option2_input)
            order_dict = orderDates(order_dict, option2_input)
            dates = getDates(order_dict, option2_input)
            mon = getMonthName(dates)
            day = getDay(dates)
            order_id = getOrderId(order_dict, option2_input)
            order_q = getOrderQuantity(order_dict, option2_input)
            product_name = getProductName(order_id, product_dict)
            product_price = getProductPrice(order_id, product_dict)
            product_name1 = checkProductNameLength(product_name)
            prices = calculatePrices(product_price, order_q)
            option2_input1 = checkAdressLength(option2_input)
            printOption2(option2_input1, mon, day, order_q, product_name1, prices)
            user_choice = printInstructions()
        while user_choice == '3':
            print("Thank you for using the Small Business Delivery Program! Goodbye.")    
            exit()
    

    
main()
    
