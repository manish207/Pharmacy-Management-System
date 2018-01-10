from Tkinter import *
import mysql.connector
import tkMessageBox
import datetime

try:
    conn=mysql.connector.connect(user='root',password='',host='localhost',database='test')
    cur = conn.cursor(buffered=True)

except Exception as e:
  print e

class mainw:

    def error(self,string):
        tkMessageBox.showerror("Error", string)

    
    def __init__(self,master):
        frame=Frame(master,width=100,height=100)
        frame.pack()

        self.but1=Button(frame,text="New Order",command=self.Order)
        self.but2=Button(frame,text="Add new medicine",command=self.medicine)
        self.but3=Button(frame,text="Previous orders",command=self.past)
        self.but4=Button(frame,text="View Stock",command=self.stock)
        self.quit=Button(frame,text="Quit",command=self.OnChildClose)

        self.but1.pack(side=LEFT,fill=X)
        self.but2.pack(side=RIGHT,fill=X)
        self.but3.pack(side=TOP,fill=X)
        self.but4.pack(side=BOTTOM,fill=X)

       
            #self.quit.pack(side=BOTTOM,fill=X)

    ####################  new Order ##########################################  

    def Order(self):
        self.top1 = Toplevel()
        self.no = Label(self.top1,text="Enter no. of medicines to order")
        self.enter = Entry(self.top1)
        self.proceed = Button(self.top1,text="Proceed",command=self.medUtil)        
        self.no.pack()
        self.enter.pack()
        self.proceed.pack()
        #print("text is",s)

    def medUtil(self):
        string = self.enter.get()
        try:
            q = int(string)
            if q <=0:
                self.error("Quantity should be positive")
                return
            if q >5:
                self.error("Maximum of 5 medicines can be ordered at a time")
                return
        except ValueError:
        #Handle the exception
            self.error("enter valid quantity")
            return
        self.newOrder();
        
    def newOrder(self):
        s=self.enter.get()
        self.n=(int(s))
        self.top1.destroy()
        self.top = Toplevel()
        self.med = []
        self.quant = []
        pid_label = Label(self.top,text="enter patient name")
        pid_label.pack()
        pid  =Entry(self.top)
        pid.pack()
        p_age_label = Label(self.top,text="enter patient's age")
        p_age_label.pack()
        p_age =Entry(self.top)
        p_age.pack()
        psex_label = Label(self.top,text="enter patient's sex ")
        psex_label.pack()
        psex  =Entry(self.top)
        psex.pack()
        self.p_age=p_age
        self.psex=psex
        self.pid = pid
        for i in range(0,self.n):
            self.id = Label(self.top,text="Medicine name")
            self.med.append(Entry(self.top))
            self.qno = Label(self.top,text="Quantity")
            self.quant.append(Entry(self.top))

            self.id.pack()
            self.med[i].pack()
            self.qno.pack()
            self.quant[i].pack()
        
        self.topButton = Button(self.top, text="Bill", command = self.orderUtil)
        self.topButton.pack()


    def orderUtil(self):
        for i in range(0,self.n):
            string = self.quant[i].get()
            try:
                q = int(string)
                if q <=0:
                    self.error("Quantity should be positive")
                    return
            except ValueError:
            #Handle the exception
                self.error("enter valid quantity")
                return
        age = self.p_age.get()
        try:
            a = int(age)
            if a <=0:
                self.error("Age should be positive")
                return
        except ValueError:
        #Handle the exception
            self.error("enter valid age")
            return
        sex=str(self.psex.get())
        #print sex
        if sex <> "m":
            if sex <> "f":
                if sex <> "o":
                    self.error("Enter valid sex (m,f or o)")
                    return
        p=self.pid.get()
        m1=self.med[i].get()
        if p is "" or m1 is "":
            self.error("Fields can't be left blank")
            return
        self.bill();
        

    def bill(self):
        num = self.n
        price = 0
        price_arr = []
        #print self.quant[0].get()
            
        for i in range(0,len(self.med)):
            cur.execute("select mname,quantity,price from medicines where mname=('%s')" % (self.med[i].get()))
            data = cur.fetchall()
            
            #print data[0][0]
            
            if len(data) == 0:
                self.error("no such medicine")
                return
            if int(data[0][1])< int(self.quant[i].get()):
                self.error("This quantity not available")
                return
            price_arr.append(data[0][2])   
            price = price + ( int(data[0][2]) * int(self.quant[i].get()) )
            #print price
        for i in range(0,len(self.med)):
           
            cur.execute("update medicines set quantity = quantity - ('%s') where mname = ('%s')" % (self.quant[i].get(),self.med[i].get()))

        for i in range(0,len(self.med)):
            cur.execute("select mname,quantity,price from medicines where mname=('%s')" % (self.med[i].get()))
            data = cur.fetchall()
            if data[0][1] == 0:
                self.error("Ordering medicine for " + data[0][0])
                cur.execute("update medicines set quantity = quantity + 100 where mname = ('%s')" % (self.med[i].get()))
      
        
        #print price_arr
        for i in range(0,len(self.med)):
            mname = Label(self.top,text="Medicine name = " +str(self.med[i].get()))
            quantity = Label(self.top,text="Quantity = "+str(self.quant[i].get()))
            price_label = Label(self.top,text="Price ="+str(price_arr[i]))
            mname.pack()
            quantity.pack()
            price_label.pack()
        tot_price = Label(self.top,text="Amount = "+str(price))
        tot_price.pack()

        for i in range(0,len(self.med)):
            cur.execute("Insert into orders values (%s,%s,%s,%s,%s)", (str(self.pid.get()), str(self.med[i].get()), self.quant[i].get(),self.p_age.get(),str(self.psex.get())))
    
        
        
    def OnChildClose(self):
        self.top.destroy()

############## new Medicine ######################################################

    def insertData(self):
        string = self.quant.get()
        try:
            quantity = int(string)
            if quantity <=0:
                self.error("Quantity should be positive")
                return
        except ValueError:
        #Handle the exception
            self.error("enter valid quantity")
            return

        string = self.cost.get()
        try:
            price = int(string)
            if price <= 0:
                self.error("Price should be positive")
                return
        except ValueError:
        #Handle the exception
            self.error("enter valid price")
            return
        m=self.med.get()
        m_name=self.med_name.get()
        date=self.exp_date.get()
        m_id=self.man.get()
        manu_name=self.man_name.get()
        
        if m is "" or m_name is "" or date is "" or m_id is "" or manu_name is "":
            self.error("Fields can't be left blank")
            return
        try:
            date1 = datetime.datetime.strptime(date,'%d-%m-%Y')
        except:
            self.error("Date should be of DD-MM-YYYY format")
            return
        if date1 <= datetime.datetime.today():
            self.error("Expiry date should be greater than today")
        self.insertUtil(m,m_name,date,m_id,manu_name,self.cost.get(),self.quant.get())


    def insertUtil(self,m,med_name,date,m_id,manu_name,price,quantity):

        #print str(m)
        #print str(med_name)
        #query = "Insert into medicines values(" + str(m) + "," + str(med_name)+"," + str(price)+","+str(quantity)+","+str(date)+","+str(m_id)+","+str(manu_name)+")"
        try:
            #cur.execute(query)
            cur.execute("Insert into medicines values (%s,%s,%s,%s,%s,%s,%s)", (str(m), str(med_name), price, quantity, date, str(m_id), str(manu_name)))
        except Exception as e:
            print e
        

    def medicine(self):
        self.top = Toplevel()

        self.id = Label(self.top,text="Medicine ID")
        self.med = Entry(self.top)
        self.name = Label(self.top,text="Medicine name")
        self.med_name = Entry(self.top)
        self.qno = Label(self.top,text="Quantity")
        self.quant = Entry(self.top)
        self.label_p = Label(self.top,text="Price")
        self.cost = Entry(self.top)
        self.exp = Label(self.top,text="Expiry Date")
        self.exp_date = Entry(self.top)
        self.exp_date.insert(0,"DD-MM-YYYY")
        self.man_id = Label(self.top,text="Manufacturer ID")
        self.man = Entry(self.top)
        self.m_name = Label(self.top,text="Manufacturer name")
        self.man_name = Entry(self.top)
        
        self.id.pack()
        self.med.pack()
        self.qno.pack()
        self.quant.pack()
        self.name.pack()
        self.med_name.pack()
        self.label_p.pack()
        self.cost.pack()
        self.exp.pack()
        self.exp_date.pack()
        self.man_id.pack()
        self.man.pack()
        self.m_name.pack()
        self.man_name.pack()
        
        self.topButton = Button(self.top, text="ADD", command = self.insertData)
        self.topButton.pack()


############## previous orders  #################################################
    
    def past(self):
        
        cur.execute("Select * from orders")
        data = cur.fetchall()
        if len(data) == 0:
            self.error("No previous orders found")
            return
        self.top = Toplevel()
        self.topButton = Button(self.top, text="CLOSE", command = self.OnChildClose)
        self.topButton.pack()
        for row in data :
            label_title = Label(self.top, text="Patient name = " + row[0])
            label_title_1 = Label(self.top, text="Medicine name = "+row[1])
            label_title_2 = Label(self.top, text="Quantity = "+str(row[2]))
            label_title_3 = Label(self.top, text="Age = "+str(row[3]))
            label_title_4 = Label(self.top, text="Sex = "+str(row[4]))
            
            label_title_7 = Label(self.top, text=" ")
            
            label_title.pack()
            label_title_1.pack()
            label_title_2.pack()
            label_title_3.pack()
            label_title_4.pack()
           
            label_title_7.pack()
        
        #print("previous orders")

 ################ Stock #######################################################

        
    def stock(self):
       
        
        cur.execute("Select * from medicines")
        data = cur.fetchall()
        if len(data) == 0:
            self.error("No previous orders found")
            return
        self.top = Toplevel()
        rows = len(data)
        col = len(data[0])
        self.topButton = Button(self.top, text="CLOSE", command = self.OnChildClose)
        self.topButton.pack()
        #print("stocks")

        for row in data :
            label_title = Label(self.top, text="Medicine id = " + row[0])
            label_title_1 = Label(self.top, text="Medicine name = "+row[1])
            label_title_2 = Label(self.top, text="Price = "+str(row[2]))
            label_title_3 = Label(self.top, text="Quantity = " + str(row[3]))
            label_title_4 = Label(self.top, text="Expiry Date = "+row[4])
            label_title_5 = Label(self.top, text="Manufacturer id = "+row[5])
            label_title_6 = Label(self.top, text="Manufacturer name = "+row[6])
            label_title_7 = Label(self.top, text=" ")
            
            label_title.pack()
            label_title_1.pack()
            label_title_2.pack()
            label_title_3.pack()
            label_title_4.pack()
            label_title_5.pack()
            label_title_6.pack()
            label_title_7.pack()
        
               
tk=Tk()
tk.geometry("300x300")
ob=mainw(tk)
tk.mainloop()
