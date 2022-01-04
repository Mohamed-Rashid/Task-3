import psycopg2
import pandas as pd
import time
conn = psycopg2.connect(database='register', user='postgres', password='Moha@123', host='localhost', port= '5432')
rash=conn.cursor()
#rash.execute('CREATE DATABASE register;')
#rash.execute("create table employee(id serial primary key,name char(25) not null,password char(16) not null,adhaar bigint not null,secQ text not null,secA text not null,mobile bigint not null,designation char(20),salary int,status char(18) default 'inactive', check (mobile between 4000000000 and 9999999999) );")
#rash.execute("create table emp_audit(id int not null,time text not null,reg char(5) default 'no',update char(5) default 'no');")
#rash.execute("create table admin(id int,password char(16));")
#rash.execute("insert into admin values(10529,'admin10529');")

def registration():
  
    rec=int(input("Enter the count of student record need to add:"))
    
    for i in range(rec):
        name=input("Enter name :")
        password=input("Password :")
        adhaar=int(input("Adhaar :"))
        mobile = int(input("Mobile number should be in 10 digits:")) 
        if mobile > 999999999:
            secQ=input("Sec question :")
            secA=input("Sec Answer :")
        else:
            print()
            print("please verify the Details")
            registration()
        
        y="insert into employee (name,password,adhaar,secQ,secA,mobile)values('{}','{}',{},'{}','{}',{});"
        
        
        rash.execute(y.format(name,password,adhaar,secQ,secA,mobile))
        
        
        temp = "select id from employee where name='{}';"
        x=temp.format(name)
        rash.execute(x)
        id=rash.fetchone()
        time.sleep(1)
        print()
        print("Registered Successfully your id is ",list(id))
        select()



def update():
    init=int(input("1.Update \n2.View \n3.log \n4.Update Status \nPlease Select the option :"))
    
    a_id = int(input("Enter admin id :"))
    a_pwd = input("Enter admin password :")
    
    a_temp="select * from admin where id={} and password='{}';"
    x=a_temp.format(a_id,a_pwd)
    
    rash.execute(x)
    d=rash.fetchall()
    
    if init ==1:
        if len(d)!=0:
            print("***** Hi admin ***** ")
                      
            up_id=int(input("please mention id to update :"))
            rash.execute("select status from employee where id="+str(up_id)+";")
            r=rash.fetchone()
            if type(r)==tuple:            
                if 'active' in r:                   
                    up=int(input("1.Mobile \n2.Designation \n3.Salary \nplesae select option what to update :"))
                    if up==1:
                        number=int(input("Enter the number to update :"))
                        rash.execute("update employee set mobile = "+str(number)+" where id="+str(up_id)+";")
                        print("Mobile Number Successfully updated ")
                        select()
             
                        
                    elif up==2:
                        des=input("Enter the Designation to update:")
                        d_temp = "update employee set designation ='{}' where id ={};"
                        d_up=d_temp.format(des,up_id)
                        rash.execute(d_up)
                        print("Designation Updated Successfully ")
                        select()
                    
                    elif up==3:
                        sal=input("Enter the Salary to update :")
                        rash.execute("update employee set salary = "+str(sal)+" where id="+str(up_id)+";")
                        print("Salary Updated Successfully ")
                        select()
                    
                    elif up==4:
                        up_s=input("enter the status to update ")
                        temp="update employee set status ='{}' where id={};"
                        s=temp.format(up_s,up_id)
                        rash.execute(s)
                        print("Status Updated Successfully")
                        select()
                    else:
                        print("please choose valid option")
                        select()
                else:
                    print("Since the person is inactive")
            else:
                print("No Record Found")
        
        else:
            print("*** Only admin can able to update ***")
            time.sleep(1)
            select()
    
    elif init ==2:
        if len(d)!=0:
            
            v_id = int(input("enter the id to view the deatils :"))
            rash.execute("select id,name,mobile,designation,status from employee where id="+str(v_id)+";")
            v=rash.fetchall()
    
            if len(v)!=0:
                print(v)
            else:
                print("Please enter the valid details to view the data")
                select()                
        else:
            print("*** Only admin can able to update ***")
            select()
            
        
    elif init==3:
        if len(d)!=0:
            
            rash.execute("select * from emp_audit order by time desc;")
            l=rash.fetchall()
            if len(l)!=0:
                df=pd.DataFrame(l,columns=['ID', 'TIME', 'REG', 'UPDATE'])
                print(df.to_string(index=False))
                    
            else:
                print("No records found ")
                
        else:
            print("*** Only admin can able to update ***")
            select()
    
    elif init==4:
        if len(d)!=0:
    
            up_sid=int(input("please mention id to update the status:"))
            up_s=input("enter the status to update active or inactive ")
            rash.execute("select id from employee where id ="+str(up_sid)+";")
            c=rash.fetchall()
            if len(c)!=0:
                
                temp="update employee set status ='{}' where id={};"
                s=temp.format(up_s,up_sid)
                rash.execute(s)            
                if up_s=='active':
                    des=input("Update the designation ")
                    sal=int(input("Update the salary"))
                    temp1="update employee set designation='{}',salary={} where id={};"
                    u=temp1.format(des,sal,up_sid)
                    rash.execute(u)
                    time.sleep(1)
                    print("Sucessfully updated")
                    select()
                
                elif up_s=='inactive':
                    rash.execute("update employee set designation =null ,salary = null where id="+str(up_sid)+";" )
                    time.sleep(1)
                    print("Status Updated sucess")
                    select()
            
            else:
                print()
                print("No records found please check with the ID")
                select()
        else:
            print("*** Only admin can able to update ***")
            select()
            
            
def login():
    print("please enter the user id and name to login ")
    l_id=int(input("User id :"))
    l_name=input("Enter the name :").capitalize()
    l_pwd=input("Enter the password :")
    
    rash.execute("select status from employee where id="+str(l_id)+";")
    l=rash.fetchone()
    if type(l)==tuple:
   
        if 'active' in l:      
            rash.execute("select * from employee where id="+str(l_id)+" and name='"+l_name+"' and password = '"+l_pwd+"';")
            z=rash.fetchall()
            print(z)
            if len(z)!=0:
                print("Hi {} Welcome to the page ".format(l_name))        
    
        else:
            print("Since the user is inactive ")
    else:
        print("No record found")
        
def forget_password():

    f_id=int(input("Enter your id to change your password :"))
    que=input("Enter your security question :")
    ans=input("Enter your Answer :")
    f_pwd=input("Enter your new password :")
    x = "select * from employee where id={} and secq='{}' and seca = '{}';"
    y = x.format(f_id,que,ans)
    rash.execute(y)
    z=rash.fetchall()
 
    if len(z)!=0:
        temp="update employee set password ='{}' where id={} and secq='{}' and seca='{}';"
        f=temp.format(f_pwd,f_id,que,ans)
        rash.execute(f) 
        time.sleep(2)
        print("Password changed successfully ")
        select()
    else:
        print("records not matched please give valid data")
        forget_password()
        
        
def select():
    print()
    select=int(input("1.Registration \n2.Login \n3.update and view \n4.Forget password \n5.Exit \nSelect the option :"))
    if select ==1:
        registration()
    elif select ==2:
        login()
    elif select ==3:
        update()
    elif select ==4:
        forget_password()
    elif select ==5:
        print("Thank you choosing")
    
    else:
        print("give valid option ")
select()

conn.commit()
conn.close()