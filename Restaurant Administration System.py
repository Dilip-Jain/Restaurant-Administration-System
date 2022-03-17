# Imports
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import csv
import pickle
from time import *

# Variables
prioritytable=[0]*7
vacancy=[True]*7
toccupied=[0]*7
typepriority={"s":1,"m":10,"d":100}   #for priority scheduling
z=0
ordering={}
order={}
orderseqprod=[]
orderexe=[]

tstart=round(time())

menufile=open('Menu/menu','rb')
menu=pickle.load(menufile)  #dictionary={"fooditem":["type",price,bursttime]}
menufile.close()

tablenorder=[{},{},{},{},{},{},{}]
j=0
for i in tablenorder:
    orderfile=open('Tables/' + str(j),'rb')
    i=pickle.load(orderfile)
    orderfile.close()
    j=j+1


# 
main=Tk()
main.title("Hotel Administration Software")
main.geometry('640x480')
##mainstate="normal"

bgimg=PhotoImage(file="Restaurant Front.png")
bglabel=Label(main, image=bgimg).place(relwidth=1,relheight=1,x=0,y=0)

def create_circle(x,y,r,cv,tag):
        x0=x-r
        y0=y-r
        x1=x+r
        y1=y+r
        cv.create_oval(x0,y0,x1,y1,fill="#ffff00",outline="",tags=tag)

def table(cv):
    create_circle(200, 100, 40, cv,"1")
    create_circle(107, 240, 40, cv,"2")
    create_circle(200, 380, 40, cv,"3")
    create_circle(440, 100, 40, cv,"4")
    create_circle(533, 240, 40, cv,"5")
    create_circle(440, 380, 40, cv,"6")
    create_circle(320, 240, 40, cv,"0")

def manager():
##    global mainstate
##    if(mainstate=="normal"):
##        main.destroy()
##        mainstate="destroyed"
    managerwin=Toplevel()
    managerwin.geometry('640x480')
    managerwin.title("Manager Window")
    cv=Canvas(managerwin,bg="#ffffdd",height=480,width=640)
    cv.pack()
    table(cv)
    def onrclick(event):
        item=cv.find_closest(event.x, event.y)
        tableid = cv.itemcget(item, 'tags')
        global idtable
        idtable=int(tableid[0])
        if vacancy[idtable]==True:
            cv.itemconfig(item, fill='green')

        else:
            cv.itemconfig(item, fill='red')
    def onclick(event):
        item=cv.find_closest(event.x, event.y)
        tableid = cv.itemcget(item, 'tags')
        idtable=int(tableid[0])
        managerwin.destroy()
        managertableoption=Toplevel()
        managertableoption.geometry('300x300')
        managertableoption.title("Options")
        l=Label(managertableoption,text=("Table #"+tableid[0])).grid(column=0,row=0)
        def booktable():
            global vacancy,tablenorder
            if vacancy[idtable]==True:
                vacancy[idtable]=False
                toccupied[idtable]=(round(time()))
                print("Table#"+str(idtable)+", Arrival Time:"+str(toccupied[idtable]-tstart))#OS -Process Arrival Time
                prioritytable[idtable]=(max(prioritytable)+1)#OS -For Process FCFS
                messagebox.showinfo("Table Booked","Table Booked")
                managertableoption.lift()
            else:
                messagebox.showerror("Table Already Booked","Table Already Booked")
                managertableoption.lift()
        booktablebtn=Button(managertableoption, text="Book Table", command=booktable).place(relwidth=0.3,height=30,x=100,y=35)
        def bill():
            if vacancy[idtable]==False:
                managertableoption.withdraw()
                billwin=Toplevel()
                billwin.geometry('300x300')
                billwin.title("Bill Window")
                csv_columns = ['Order','Quantity','Amount']
                h1=Label(billwin,text="Order").grid(column=0,row=0)
                h2=Label(billwin,text="Quantity").grid(column=2,row=0)
                h3=Label(billwin,text="Amount").grid(column=3,row=0)
                j=1
                for key in tablenorder[idtable]:
                    Label(billwin, text=key).grid(column=0,row=j)
                    Label(billwin, text=tablenorder[idtable][key][0]).grid(column=2,row=j)
                    Label(billwin,text=(int(menu[key][1])*int(tablenorder[idtable][key][0]))).grid(column=3,row=j)
                    j=j+1
                def checkout():
                    billlist=[]
                    for key in tablenorder[idtable]:
                        billdic={"Order":key,"Quantity":tablenorder[idtable][key][0],"Amount":(int(menu[key][1])*int(tablenorder[idtable][key][0]))}
                        billlist.append(billdic)
                    bill_file="bill.csv"
                    with open('Bill/' + bill_file,'w') as billfile:
                        writer = csv.DictWriter(billfile, fieldnames=csv_columns)
                        writer.writeheader()
                        for data in billlist:
                            writer.writerow(data)
                    global toccupied, vacancy
                    vacancy[idtable]=True
                    toccupied[idtable]=0
                    tablenorder[idtable].clear()
                billoutbtn=Button(billwin, text="Check Out", command=checkout).place(width=75,height=30,x=50,y=260)
                def back():
                    managertableoption.deiconify()
                    billwin.destroy()
                backbtn=Button(billwin, text="Back", command=back).place(width=75,height=30,x=175,y=260)
        billbtn=Button(managertableoption, text="Bill and Order",command=bill).place(relwidth=0.3,height=30,x=100,y=135)
        def back():
                manager()
                managertableoption.destroy()
        backbtn=Button(managertableoption, text="Back", command=back).place(relwidth=0.3,height=30,x=100,y=235)
    cv.bind('<Button-3>', onrclick)
    cv.bind('<Button-1>', onclick)


def attendant():
    global vacancy
##    main.destroy()
    attendantwin=Toplevel()
    attendantwin.geometry('640x480')
    attendantwin.title("Attendant Window")
    
    cv=Canvas(attendantwin,bg="#ffffdd",height=480,width=640)
    cv.pack()
    table(cv)
    def onclick(event):
        item=cv.find_closest(event.x, event.y)
        tableid=cv.itemcget(item, 'tags')
        if vacancy[int(tableid[0])]==False:
            attendantwin.withdraw()
            attendanttableoption=Toplevel()
            attendanttableoption.geometry('300x300')
            attendanttableoption.title("Orders")
            l=Label(attendanttableoption,text=("Table #"+tableid[0])).grid(column=0,row=0)
            def ordered():
                attendanttableoption.withdraw()
                orderedwin=Toplevel()
                orderedwin.geometry('300x300')
                orderedwin.title('Orders')
                h1=Label(orderedwin,text="Order").grid(column=0,row=0)
                h2=Label(orderedwin,text="Quantity").grid(column=1,row=0)
                h3=Label(orderedwin,text="Table").grid(column=2,row=0)
                h4=Label(orderedwin,text="Status").grid(column=3,row=0)
                j=1
                for key in order:
                    Label(orderedwin,text=order[key]["Order"]).grid(column=0,row=j)
                    Label(orderedwin,text=order[key]["Quantity"]).grid(column=1,row=j)
                    Label(orderedwin,text=order[key]["Table No"]).grid(column=2,row=j)
                    Label(orderedwin,text=order[key]["Status"]).grid(column=3,row=j)
                    j=j+1
                def back():
                    orderedwin.destroy()
                    attendanttableoption.deiconify()
                backbtn=Button(orderedwin, text="Back",command=back).place(relwidth=0.3,height=30,x=100,y=260)
            orderbtn=Button(attendanttableoption, text="Order",command=ordered).place(relwidth=0.3,height=30,x=100,y=35)
            def orderadd():
                orderaddwin=Toplevel()
                orderaddwin.geometry('300x300')
                orderaddwin.title('Add Order')
                l=Label(orderaddwin,text=("Table #"+tableid[0])).grid(column=0,row=0)
                l1=Label(orderaddwin,text="Food:").place(x=30, y=75)
                global foodlist
                foodlist=list(menu.keys())
                food=ttk.Combobox(orderaddwin,values=foodlist,width=30)
                food.place(x=80,y=75)
                food.current(0)
                l2=Label(orderaddwin,text="Quantity:").place(x=30, y=150)
                q=Spinbox(orderaddwin,from_=1, to=500)
                q.place(x=100,y=150)
                def addmore():
                    global ordering,order,orderseqprod,z
##                    print(tableid[0])
                    (tablenorder[int(tableid[0])])[food.get()]=[q.get(),"pending"]
##                    print(tablenorder)
                    pickle.dump(tablenorder[int(tableid[0])],open('Tables/' + str(tableid[0]),'ab'))
                    op=(prioritytable[int(tableid[0])])*(round(time())-tstart) #request time * process arrival time   ##-,
                    ordering[z]=[food.get(),int(tableid[0]),op,typepriority[(menu[food.get()][0])],((menu[food.get()][2])*int(q.get())),int(q.get())] #*
##                    print(ordering)
                    order[food.get()]={"Table No":int(tableid[0]),"Order":food.get(),"Quantity":int(q.get()),"Amount":(menu[food.get()][1]*int(q.get())),"Status":"Pending",}
                    z=z+1
##                    print(order)
                    orderseqprod.append((op*typepriority[(menu[food.get()][0])]*(menu[food.get()][2])*int(q.get())))
##                    print(orderseqprod)
                    
                    
                addmorebtn=Button(orderaddwin, text="Add More",command=addmore).place(width=70,x=60,y=250)
                def sorting():
                    global orderexe
                    orderexe.clear()
                    global orderseqprod
                    orderseq=list(orderseqprod)
                    orderseq.sort()
                    for x in orderseq:
                        orderexe.append(orderseqprod.index(x))
##                    print(orderexe)
##                    print(orderseq)
                        
                def done():
                    addmore()
                    sorting()
                    attendanttableoption.deiconify()
                    orderaddwin.destroy()
                donebtn=Button(orderaddwin,text="Done",command=done).place(width=60,x=180,y=250)
            addorderbtn=Button(attendanttableoption, text="Add Order",command=orderadd).place(relwidth=0.3,height=30,x=100,y=135)
            def back():
                attendantwin.deiconify()
                attendanttableoption.destroy()
            backbtn=Button(attendanttableoption, text="Back", command=back).place(relwidth=0.3,height=30,x=100,y=235)
    cv.bind('<Button-1>', onclick)


def chef():
##    main.destroy()
    chefwin=Toplevel()
    chefwin.geometry('300x300')
    chefwin.title("Chef Window")
    def orderpending():
        chefwin.withdraw()
        orderpendingwin=Toplevel()
        orderpendingwin.geometry('300x300')
        orderpendingwin.title('Orders Pending')
        h1=Label(orderpendingwin,text="Food").grid(column=0,row=0)
        h2=Label(orderpendingwin,text="Quantity").grid(column=1,row=0)
        if ordering:
            j=1
            for i in orderexe:
                Label(orderpendingwin,text=ordering[i][0]).grid(column=0,row=j)
                Label(orderpendingwin,text=ordering[i][5]).grid(column=1,row=j)
                j=j+1
        else:Label(orderpendingwin,text="No Orders").grid(row=1)
        def ok():
            orderpendingwin.destroy()
            chefwin.deiconify()
        okbtn=Button(orderpendingwin,text="OK",command=ok).place(width=40,height=30,x=130,y=260)
    orderbtn=Button(chefwin, text="Orders",command=orderpending).place(relwidth=0.3,height=30,x=100,y=35)
    def updatebt():
        updatewin=Toplevel()
        updatewin.geometry('300x300')
        updatewin.title('Cook(Burst) Time Update')
        l1=Label(updatewin,text="Food:").place(x=30, y=75)
        global foodlist
        foodlist=list(menu.keys())
        food=ttk.Combobox(updatewin,values=foodlist,width=30)
        food.place(x=80,y=75)
        food.current(0)
        l2=Label(updatewin,text="Cook Time:").place(x=30, y=150)
        bt=Spinbox(updatewin,from_=0, to=100)
        bt.place(x=100,y=150)
        def done():
            menu[food.get()][2]=int(bt.get())
            print("Burst Time Updated for "+food.get()+":"+bt.get())
            f=open('Menu/menu','wb')
            pickle.dump(menu,f)
            f.close()
            updatewin.destroy()
        donebtn=Button(updatewin,text="Done",command=done).place(width=60,x=120,y=250)
    cooktimebtn=Button(chefwin, text="Cook Time", command=updatebt).place(relwidth=0.3,height=30,x=100,y=135)      #burst time for each process
    def back():
        chefwin.destroy()
    backbtn=Button(chefwin, text="Back", command=back).place(relwidth=0.3,height=30,x=100,y=235)
    

managerbtn=Button(main, text="Manager", command=manager).place(relwidth=0.15, x=80,y=435)
attendantbtn=Button(main, text="Attendant",command=attendant).place(relwidth=0.15,x=295,y=435)
chefbtn=Button(main, text="Chef",command=chef).place(relwidth=0.15,x=500,y=435)

def cookin():
    global z,orderexe,ordering,order,orderseqprod,tablenorder
    if ordering:
        key=orderexe[0]
        ordering[key][4]=int(ordering[key][4])-1
        if(ordering[key][4]<=0):
            print(ordering[key][0]+" is completed")
            order[ordering[key][0]]["Status"]="Complete"
            orderseqprod.remove((ordering[key][2]*ordering[key][3]*(menu[ordering[key][0]][2])*ordering[key][5]))
            tablenorder[ordering[key][1]][ordering[key][0]][1]="Complete"
            pickle.dump(tablenorder[int(ordering[key][1])],open('Tables/'+str(ordering[key][1]),'wb'))
            for i in range(key,(z-1)):
                ordering[i]=ordering[i+1]
            orderexe.pop(0)
            ordering.pop(z-1)
            z=z-1
        else:
            print(ordering[key][0]+" in progress")
    else:
        print("No process left!")
    main.after(60000,cookin)

main.after(120000,cookin)
main.mainloop()


