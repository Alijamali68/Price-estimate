#%%
'''# Machine learning car_validator'''
#----->Imports
from tkinter import *  

import re
import jdatetime
from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import mysql.connector
import matplotlib.pyplot as plot

class DB:
    car_data=[]
    def __init__(self,Host,Password,User,Database):
        #TODO: this Will make connector and curser
        try:
            self.db_connector=mysql.connector.connect(
            host=Host,
            password=Password,
            user=User,
            database=Database)
            self.curser=self.db_connector.cursor()
        except mysql.connector.Error as err:
            if(err.errno==1146):
                print('Table  doesn\'t exist')
            else:
                print(err)    
        
    def Read_all_data(self):
        fig, ax = plot.subplots()
        usage=[]
        price=[]
        self.curser.execute('SELECT car_name,car_price,car_usage FROM car_ads order by car_price asc limit 20')
        result=self.curser.fetchall()
        for i in result:
            usage.append((i[0]))
            price.append((i[1]))
     
        ax.bar(price,usage)
        plot.show()    
    def Read_all_data2(self,make,price,usage,city):
        query='SELECT (car_make,car_price,car_usage,car_city)\
        FROM car_ads where car_city=%s and car_usage=%d a'
        value=(self.city,self.usage)    
        self.curser.execute(query,value)
        result=self.curser.fetchall()
        for i in result:
            DB.car_data.append(i)

    def save_data2(self,make,car_type,Model,fuel_type,price,usage,city,info):
        query='INSERT INTO car_ads VALUES (%s,%s,%s,%s,%d,%d,%s,%s)'
        values=(make,car_type,Model,fuel_type,price,usage,city,info)
        self.curser.execute(query,values)
        self.db_connector.commit() 
    def save_data(self,name,Model,price,usage,city):
        query='INSERT IGNORE INTO car_ads(car_name,car_model,car_price,car_usage,car_city) VALUES (%s,%s,%d,%d,%s)'
        values=(name,Model,price,usage,city)
        self.curser.execute(query,values)
        self.db_connector.commit()
        
        

class Fetch_data:
    fetch_info=[]
    def __init__(self,url):
    #this will make browser object
        try:
            self.browser=webdriver.Chrome(executable_path='D:\
            //tamrin python/python_pishrafte/venv/Lib/\
            site-packages/chromedriver_py/chromedriver.exe') 
            self.browser.get(url)
        except (ConnectionRefusedError) as e:
            print(e)
            

    def Get_data(self): 
        
        scroll_page_counter=0
         #This will scroll down to last if while-->True
         #scroll_page_counter-->>how many scroll do u need

        last_height = self.browser.execute_script(\
                      "return document.body.scrollHeight")
        self.result=self.browser.find_elements(By.CLASS_NAME,'kt-post-card__body')
        while scroll_page_counter<1:
            # Scroll down to bottom
            self.browser.execute_script(\
                "window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(3)

            # Calculate new scroll height\
            # and compare with last scroll height
            
            new_height = self.browser.execute_script(\
                "return document.body.scrollHeight")
            scroll_page_counter+=1
            if new_height == last_height:
                break
            last_height = new_height
            self.result=self.browser.find_elements(By.CLASS_NAME,'kt-post-card__body')          
            for every_car in self.result:
                
                self.fetch_info.append(every_car.text.split('\n'))



        self.browser.close()
        
class Mlearning:
    
    def __init__(self,make,model,price,usage):
        self.make=make
        self.price=price
        self.usage=usage
        self.model=model 
    def guess_price(self):
        DB_Object.Read_all_data2(self.make,self.price,self.usage,self.city)
        print('gheimat_taghribi: %d',max(DB_Object.car_data[1])-min(DB_Object.car_data[1]))
        
        




DB_Object=DB('127.0.0.1','Ali@921@','DB_Admin','test')
def Option():
    
    print('1:Fetch Data')
    print('2:Estimate Price')
    answer=int(input())
    if(answer==1):
        data=Fetch_data('https://divar.ir/s/tehran-province/car/samand?price=1-&exchange=exclude-exchanges')
        data.Get_data()
        #this array hold the feched car_info
        for every_car in data.fetch_info:
            
            city=every_car[-1].split(' ')[-1]
            mod=every_car[0].split(' مدل ')
            name=mod[0]
            usage=float(unidecode((every_car[1].split(' '))[0]).replace(',',''))
            price=float(unidecode((every_car[2].split(' '))[0]).replace(',',''))
            
            if(len(mod)>1):
               model=float(unidecode(mod[1])) 
               DB_Object.save_data(name,model,price,usage,city)
            else:
                pass 
        print('Data saved successfully')  
    elif(answer==2):        
        mlearn_object=Mlearning(input('make:'),input('model:'),int(input('price:')),int(input('usage:')))
        mlearn_object.guess_price()
            #name is سمند X7 بنزینی، model is ۱۳۸۶ usage is 230,000   price is 125,000,000 city is تهران
    else:
        pass
#DB_Object.Read_all_data()

def ui():
    rootui=Tk()
    counter=0
    rootui.title('estimate usedcar price')
    Label(rootui,text=('تخمین بزن '),fg='black').pack()
    rootui.geometry('400x300')
    Button(rootui,text='تخمین',command='btn_pushed').pack()
    # rootui.resizable(width=True,height=False)
    rootui.mainloop()   
    
ui()    
    


# %%
