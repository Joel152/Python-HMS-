from sys import exit
import mysql.connector as sql
conn=sql.connect(host='localhost',user='root',passwd='manager',database='marketing_system_and_sales_system')
if conn.is_connected():
      print('succesfully conected')
c1=conn.cursor()
print('marketing system and sales system')
print("1.login")
print("2.exit")
choice=int(input("enter your choice"))
if choice==1:
      name=input("enter the user name:")
      passwd=input("enter the password:")
      while name=='vishnu' and passwd=='vishnu103' :
            print('welcome')
            print('1. registry for customer ')
            print('2.registry for products seller')
            print('3.registry for order placement')
            print('4.modify the order details')
            print('5.registry for cancelation of order')
            print('6.display the customer details')
            print('7.display the products availability')
            print('8.display the datas about order placement')
            print('9.display the order details')
            print('10.display the cancellation of order')
            choice=int(input('enter your choice'))
            if choice==1:
                  customer_name=input('enter the customer name:')
                  product_name=input('enter the product name:')
                  sql_insert="insert into customer_details values(""'"+customer_name+"'," "'"+product_name+"'"")"
                  c1.execute(sql_insert)
                  conn.commit()
                  print('SUCCESSFULLY REGISTERD')

      

            elif choice==2:
                  customer_name=input('enter the customer name:')
                  product_type=input('enter the product type:')
                  product_brand=input('enter the product brand:')
                  products_available=input('ONLY 3000 stocks available:')
                  sql_insert="insert into products_brand values(""'"+customer_name+"'," "'"+product_type+"'," "'"+product_brand+"'," "'"+products_available+"'"")"
                  c1.execute(sql_insert)
                  conn.commit()
                  print('SUCCESSFULLY REGISTERD')

            elif choice==3: 
                 customer_name=input('enter the customer name:')
                 product_name=input('enter the product name:')
                 demanding_quantity=input('enter tne quantity:')
                 sql_insert="insert into order_placement values(""'"+customer_name+"'," "'"+product_name+"'," "'"+demanding_quantity+"'"")"
                 c1.execute(sql_insert)
                 conn.commit()
                 print('successfully registerd')

            elif choice==4:
                 customer_name=input('enter the customer name:')
                 mobile_number=input('enter mobile number:')
                 adress=input('enter your adress:')
                 date_to_deliver=input('enter the date:')
                 sql_insert="insert into order_details values(""'"+customer_name+"'," "'"+mobile_number+"'," "'"+adress+"'," "'"+date_to_deliver+"'"")"
                 c1.execute(sql_insert)
                 conn.commit()
                 print('SUCCESSFULLY REGISTERD')
      
      
            elif choice==5:
                 customer_name=input('enter tthe customer name:')
                 order_number=input('enter tyhe order number:')
                 products_contained=input('enter the product contained in your order:')
                 reason_for_cancelation=input('entetr the reason for cancelling the order:')
                 confirm_cancelation=input('say YES or NO:')
                 sql_insert="insert into cancelation_of_order values(""'"+customer_name+"'," "'"+order_number+"'," "'"+products_contained+"'," "'"+reason_for_cancelation+"',""'"+confirm_cancelation+"'"")"
                 c1.execute(sql_insert)
                 conn.commit()
                 print('SUCCESSFULLY REGISTERD')

            elif choice==6:
                sql_s="select*from customer_details"
                c1.execute(sql_s)
                a=c1.fetchall()
                for i in a:
                      print(i)
                      break
                  
            elif choice==7:
                 sql_s="select*from products_brand"
                 c1.execute(sql_s)
                 a=c1.fetchall()
                 for i in a:
                       print(i)
                       break
                  
            elif choice==8:
                 sql_s="select*from order_placement"
                 c1.execute(sql_s)
                 a=c1.fetchall()
                 for i in a:
                       print(i)
                       break

            elif choice==9:
                 sql_s="select*from order_details"
                 c1.execute(sql_s)
                 a=c1.fetchall()
                 for i in a:
                       print(i)
                       break

            elif choice==10:
                 sql_s="select*from cancelation_of_order"
                 c1.execute(sql_s)
                 a=c1.fetchall()
                 for i in a:
                       print(i)
                       break
                  
                  
      else:
            print('sorry')
      
