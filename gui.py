from Tkinter import *
from PIL import ImageFilter,Image
#from tkinter import filedialog, messagebox
import tkFileDialog
import tkMessageBox
import os
import psutil
import time
import subprocess
import cv2
import fnmatch


main_win = Tk()
# main_win.iconbitmap('3/favicon.ico')


def show_entry_fields():
    print(" Age: %s\n Veg-NonVeg:%s\n Weight%s\n Hight%s\n" % (e1.get(), e2.get(),e3.get(), e4.get()))


def Weight_Loss():
    print(" Age: %s\n Veg-NonVeg:%s\n Weight%s\n Hight%s\n" % (e1.get(), e2.get(),e3.get(), e4.get()))
    #!/usr/bin/env python
    # coding: utf-8
    import pandas as pd
    import numpy as np
    import os
    
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans
    import numpy as np
    # # New Section
    
    # In[44]:

    ## Reading of the Dataet
  

    # Reading the dataset
    data = pd.read_csv('input.csv')
    Breakfastdata = data['Breakfast']
    Lunchdata = data['Lunch']
    Dinnerdata = data['Dinner']
    Food_itemsdata = data['Food_items']

    breakfastfoodseparated, Lunchfoodseparated, Dinnerfoodseparated = [], [], []
    breakfastfoodseparatedID, LunchfoodseparatedID, DinnerfoodseparatedID = [], [], []

    for i in range(len(Breakfastdata)):
        if Breakfastdata[i] == 1:
            breakfastfoodseparated.append(Food_itemsdata[i])
            breakfastfoodseparatedID.append(i)
        if Lunchdata[i] == 1:
            Lunchfoodseparated.append(Food_itemsdata[i])
            LunchfoodseparatedID.append(i)
        if Dinnerdata[i] == 1:
            Dinnerfoodseparated.append(Food_itemsdata[i])
            DinnerfoodseparatedID.append(i)

    LunchfoodseparatedIDdata = data.iloc[LunchfoodseparatedID]
    LunchfoodseparatedIDdata = LunchfoodseparatedIDdata.T
    LunchfoodseparatedIDdata = LunchfoodseparatedIDdata.iloc[[0] + list(np.arange(5, 15))]
    LunchfoodseparatedIDdata = LunchfoodseparatedIDdata.T

    breakfastfoodseparatedIDdata = data.iloc[breakfastfoodseparatedID]
    breakfastfoodseparatedIDdata = breakfastfoodseparatedIDdata.T
    breakfastfoodseparatedIDdata = breakfastfoodseparatedIDdata.iloc[[0] + list(np.arange(5, 15))]
    breakfastfoodseparatedIDdata = breakfastfoodseparatedIDdata.T

    DinnerfoodseparatedIDdata = data.iloc[DinnerfoodseparatedID]
    DinnerfoodseparatedIDdata = DinnerfoodseparatedIDdata.T
    DinnerfoodseparatedIDdata = DinnerfoodseparatedIDdata.iloc[[0] + list(np.arange(5, 15))]
    DinnerfoodseparatedIDdata = DinnerfoodseparatedIDdata.T

    age = int(e1.get())
    veg = float(e2.get())
    weight = float(e3.get())
    height = float(e4.get())
    # E3 FIX: divide by 100 to convert cm to metres before squaring
    height_m = height / 100
    bmi = weight / (height_m ** 2)

    # BMI Classification
    if bmi < 16:
        clbmi = 4
    elif bmi < 18.5:
        clbmi = 3
    elif bmi < 25:
        clbmi = 2
    elif bmi < 30:
        clbmi = 1
    else:
        clbmi = 0

    # K-Means Clustering for Dinner Food
    Datacalorie = DinnerfoodseparatedIDdata.to_numpy()[1:, 1:]
    kmeans = KMeans(n_clusters=3, random_state=0).fit(Datacalorie)
    dnrlbl = kmeans.labels_

    # K-Means Clustering for Lunch Food
    Datacalorie = LunchfoodseparatedIDdata.to_numpy()[1:, 1:]
    kmeans = KMeans(n_clusters=3, random_state=0).fit(Datacalorie)
    lnchlbl = kmeans.labels_

    # K-Means Clustering for Breakfast Food
    Datacalorie = breakfastfoodseparatedIDdata.to_numpy()[1:, 1:]
    kmeans = KMeans(n_clusters=3, random_state=0).fit(Datacalorie)
    brklbl = kmeans.labels_

    # Load final dataset for predictions
    datafin = pd.read_csv('inputfin.csv')
    dataTog = datafin.T

    weightlosscat = dataTog.iloc[[1, 2, 7, 8]].T.to_numpy()[1:, :]
    weightgaincat = dataTog.iloc[[0, 1, 2, 3, 4, 7, 9, 10]].T.to_numpy()[1:, :]
    healthycat = dataTog.iloc[[1, 2, 3, 4, 6, 7, 9]].T.to_numpy()[1:, :]

    # Prepare training data
    weightlossfin = np.zeros((len(weightlosscat) * 5, 6), dtype=np.float32)
    yt = []

    for zz in range(5):
        for jj in range(len(weightlosscat)):
            valloc = list(weightlosscat[jj])
            valloc.append(zz)
            weightlossfin[jj + zz * len(weightlosscat)] = np.array(valloc)
            yt.append(brklbl[jj])

    X_test = np.zeros((len(weightlosscat), 6), dtype=np.float32)
    for jj in range(len(weightlosscat)):
        valloc = list(weightlosscat[jj])
        valloc.append(int(clbmi))
        valloc.append(int(zz))
        X_test[jj] = np.array(valloc)

    # Train Random Forest Classifier
    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(weightlossfin, yt)
    y_pred = clf.predict(X_test)

    # Calculate and print accuracy
    accuracy = accuracy_score(yt, y_pred)
    print(f'Accuracy: {accuracy * 100:.2f}%')

    print('SUGGESTED FOOD ITEMS ::')
    for ii in range(len(y_pred)):
        if y_pred[ii] == 2:  # weightloss
            print(Food_itemsdata[ii])
            e5.insert(0, Food_itemsdata[ii])
    
    print ('SUGGESTED FOOD ITEMS ::')
    for ii in range(len(y_pred)):
        if y_pred[ii]==2:
            print('#################')
            print (Food_itemsdata[ii])
            findata=Food_itemsdata[ii]
            if int(veg)==1:
                datanv=['Chicken Burger']
                for it in range(len(datanv)):
                    if findata==datanv[it]:
                        print('VegNovVeg')

def Weight_Gain():
    print(" Age: %s\n Veg-NonVeg:%s\n Weight%s\n Hight%s\n" % (e1.get(), e2.get(),e3.get(), e4.get()))
    import pandas as pd
    import numpy as np
    from sklearn.cluster import KMeans
    from sklearn.ensemble import RandomForestClassifier
    
    data = pd.read_csv('input.csv')
    Breakfastdata = data['Breakfast']
    Lunchdata = data['Lunch']
    Dinnerdata = data['Dinner']
    Food_itemsdata = data['Food_items']

    breakfastfoodseparated, Lunchfoodseparated, Dinnerfoodseparated = [], [], []
    breakfastfoodseparatedID, LunchfoodseparatedID, DinnerfoodseparatedID = [], [], []

    for i in range(len(Breakfastdata)):
        if Breakfastdata[i] == 1:
            breakfastfoodseparated.append(Food_itemsdata[i])
            breakfastfoodseparatedID.append(i)
        if Lunchdata[i] == 1:
            Lunchfoodseparated.append(Food_itemsdata[i])
            LunchfoodseparatedID.append(i)
        if Dinnerdata[i] == 1:
            Dinnerfoodseparated.append(Food_itemsdata[i])
            DinnerfoodseparatedID.append(i)

    LunchfoodseparatedIDdata = data.iloc[LunchfoodseparatedID]
    LunchfoodseparatedIDdata = LunchfoodseparatedIDdata.T
    LunchfoodseparatedIDdata = LunchfoodseparatedIDdata.iloc[[0] + list(np.arange(5, 15))]
    LunchfoodseparatedIDdata = LunchfoodseparatedIDdata.T

    age = int(e1.get())
    veg = float(e2.get())
    weight = float(e3.get())
    height = float(e4.get())
    height_m = height / 100
    bmi = weight / (height_m ** 2)

    if bmi < 16:
        clbmi = 4
    elif bmi < 18.5:
        clbmi = 3
    elif bmi < 25:
        clbmi = 2
    elif bmi < 30:
        clbmi = 1
    else:
        clbmi = 0

    Datacalorie = LunchfoodseparatedIDdata.to_numpy()[1:, 1:]
    kmeans = KMeans(n_clusters=3, random_state=0).fit(Datacalorie)
    lnchlbl = kmeans.labels_

    datafin = pd.read_csv('inputfin.csv')
    dataTog = datafin.T

    weightgaincat = dataTog.iloc[[0, 1, 2, 3, 4, 7, 9, 10]].T.to_numpy()[1:, :]

    bmicls = [0, 1, 2, 3, 4]
    agecls = [0, 1, 2, 3, 4]

    weightgainfin = np.zeros((len(weightgaincat) * 5, 10), dtype=np.float32)
    yr = []

    for zz in range(5):
        for jj in range(len(weightgaincat)):
            valloc = list(weightgaincat[jj])
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            weightgainfin[jj + zz * len(weightgaincat)] = np.array(valloc)
            yr.append(lnchlbl[jj])

    X_test = np.zeros((len(weightgaincat), 10), dtype=np.float32)
    for jj in range(len(weightgaincat)):
        valloc = list(weightgaincat[jj])
        valloc.append(int(clbmi))
        valloc.append(int(zz))
        X_test[jj] = np.array(valloc)

    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(weightgainfin, yr)
    y_pred = clf.predict(X_test)

    print('SUGGESTED FOOD ITEMS ::')
    for ii in range(len(y_pred)):
        if y_pred[ii] == 2:
            findata = Food_itemsdata[ii]
            if int(veg) == 1 and findata == 'Chicken Burger':
                continue
            print(findata)
            e5.insert(0, findata)

def Healthy():
    print(" Age: %s\n Veg-NonVeg:%s\n Weight%s\n Hight%s\n" % (e1.get(), e2.get(),e3.get(), e4.get()))
    #!/usr/bin/env python
    # coding: utf-8
    import pandas as pd
    import numpy as np
    import os
    
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans
    import numpy as np
    # # New Section
    ## Reading of the Dataet
    data=pd.read_csv('input.csv')
    data.head(5)
    Breakfastdata=data['Breakfast']
    BreakfastdataNumpy=Breakfastdata.to_numpy()
    
    Lunchdata=data['Lunch']
    LunchdataNumpy=Lunchdata.to_numpy()
    
    Dinnerdata=data['Dinner']
    DinnerdataNumpy=Dinnerdata.to_numpy()
    
    Food_itemsdata=data['Food_items']
    breakfastfoodseparated=[]
    Lunchfoodseparated=[]
    Dinnerfoodseparated=[]
    
    breakfastfoodseparatedID=[]
    LunchfoodseparatedID=[]
    DinnerfoodseparatedID=[]
    
    for i in range(len(Breakfastdata)):
      if BreakfastdataNumpy[i]==1:
        breakfastfoodseparated.append(Food_itemsdata[i])
        breakfastfoodseparatedID.append(i)
      if LunchdataNumpy[i]==1:
        Lunchfoodseparated.append(Food_itemsdata[i])
        LunchfoodseparatedID.append(i)
      if DinnerdataNumpy[i]==1:
        Dinnerfoodseparated.append(Food_itemsdata[i])
        DinnerfoodseparatedID.append(i)
    
    #print ('BREAKFAST FOOD ITEMS')
    #print (breakfastfoodseparated)
    #print ('LUNCH FOOD ITEMS')
    #print (Lunchfoodseparated)
    #print ('DINNER FOOD ITEMS')
    #print (Dinnerfoodseparated)
    
    # retrieving rows by loc method |
    LunchfoodseparatedIDdata = data.iloc[LunchfoodseparatedID]
    print(LunchfoodseparatedID)
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.T
    val=list(np.arange(5,15))
    Valapnd=[0]+val
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.iloc[Valapnd]
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.T
    #print (LunchfoodseparatedIDdata)
    
    # retrieving rows by loc method 
    breakfastfoodseparatedIDdata = data.iloc[breakfastfoodseparatedID]
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.T
    val=list(np.arange(5,15))
    Valapnd=[0]+val
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.iloc[Valapnd]
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.T
    #print (breakfastfoodseparatedIDdata)
    
    
    # retrieving rows by loc method 
    DinnerfoodseparatedIDdata = data.iloc[DinnerfoodseparatedID]
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.T
    val=list(np.arange(5,15))
    Valapnd=[0]+val
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.iloc[Valapnd]
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.T
    #print (DinnerfoodseparatedIDdata)
    #print (DinnerfoodseparatedIDdata.describe())
    #DinnerfoodseparatedIDdata.iloc[]
    
    
    # In[47]:
    age=int(e1.get())
    veg=float(e2.get())
    weight=float(e3.get())
    height=float(e4.get())
    # E3 FIX: divide by 100 to convert cm to metres before squaring
    height_m = height / 100
    bmi = weight / (height_m ** 2) 
    agewiseinp=0
    
    for lp in range (0,80,20):
        test_list=np.arange(lp,lp+20)
        for i in test_list: 
            if(i == age):
                print('age is between',str(lp),str(lp+10))
                tr=round(lp/20)  
                agecl=round(lp/20)    
    # In[280]:

    
    #conditions
    print("Your body mass index is: ", bmi)
    if ( bmi < 16):
        print("severely underweight")
        clbmi=4
    elif ( bmi >= 16 and bmi < 18.5):
        print("underweight")
        clbmi=3
    elif ( bmi >= 18.5 and bmi < 25):
        print("Healthy")
        clbmi=2
    elif ( bmi >= 25 and bmi < 30):
        print("overweight")
        clbmi=1
    elif ( bmi >=30):
        print("severely overweight")
        clbmi=0    
    val1=DinnerfoodseparatedIDdata.describe()
    valTog=val1.T
    print (valTog.shape)
    print (valTog)
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.to_numpy()
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.to_numpy()
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.to_numpy()
    ti=(bmi+agecl)/2
    #print(val)
    #print (val.iloc[6]) ##75 percenct data
    #print (val.iloc[5]) ##50 percenct data
    #print (val.iloc[4]) ##50 percenct data
    #dt=np.delete(DinnerfoodseparatedIDdata, [1,3], axis=1)
    #print (dt)
    
    # In[132]:
    ## K-Means Based  Dinner Food
    import matplotlib.pyplot as plt
    Datacalorie=DinnerfoodseparatedIDdata[1:,1:len(DinnerfoodseparatedIDdata)]
    #print(Datacalorie)
    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
    print ('## Prediction Result ##')
    print(kmeans.labels_)
    print (kmeans.predict([Datacalorie[0]]))
    XValu=np.arange(0,len(kmeans.labels_))
    # fig,axs=plt.subplots(1,1,figsize=(15,5))
    # plt.bar(XValu,kmeans.labels_)
    dnrlbl=kmeans.labels_
    # plt.title("Predicted Low-High Weigted Calorie Foods")
    # In[49]:
    ## K-Means Based  lunch Food
    import matplotlib.pyplot as plt
    Datacalorie=LunchfoodseparatedIDdata[1:,1:len(LunchfoodseparatedIDdata)]
    #print(Datacalorie)
    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
    print ('## Prediction Result ##')
    print(kmeans.labels_)
    XValu=np.arange(0,len(kmeans.labels_))
    # fig,axs=plt.subplots(1,1,figsize=(15,5))
    # plt.bar(XValu,kmeans.labels_)
    lnchlbl=kmeans.labels_
    # plt.title("Predicted Low-High Weigted Calorie Foods")
    # In[128]:
    ## K-Means Based  lunch Food
    import matplotlib.pyplot as plt
    Datacalorie=breakfastfoodseparatedIDdata[1:,1:len(breakfastfoodseparatedIDdata)]
    #print(Datacalorie)
    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
    print ('## Prediction Result ##')
    print(kmeans.labels_)
    XValu=np.arange(0,len(kmeans.labels_))
    # fig,axs=plt.subplots(1,1,figsize=(15,5))
    # plt.bar(XValu,kmeans.labels_)
    brklbl=kmeans.labels_
    # print (len(brklbl))
    # plt.title("Predicted Low-High Weigted Calorie Foods")
    inp=[]
    ## Reading of the Dataet
    datafin=pd.read_csv('inputfin.csv')
    datafin.head(5)
    ## train set
    #arrayfin=[agecl,clbmi,]
    dataTog=datafin.T
    bmicls=[0,1,2,3,4]
    agecls=[0,1,2,3,4]
    weightlosscat = dataTog.iloc[[1,2,7,8]]
    weightlosscat=weightlosscat.T
    weightgaincat= dataTog.iloc[[0,1,2,3,4,7,9,10]]
    weightgaincat=weightgaincat.T
    healthycat = dataTog.iloc[[1,2,3,4,6,7,9]]
    healthycat=healthycat.T
    weightlosscatDdata=weightlosscat.to_numpy()
    weightgaincatDdata=weightgaincat.to_numpy()
    healthycatDdata=healthycat.to_numpy()
    weightlosscat=weightlosscatDdata[1:,0:len(weightlosscatDdata)]
    weightgaincat=weightgaincatDdata[1:,0:len(weightgaincatDdata)]
    healthycat=healthycatDdata[1:,0:len(healthycatDdata)]
    
    #print(weightgaincat)
    #print (len(weightlosscat))
    weightlossfin=np.zeros((len(weightlosscat)*5,6),dtype=np.float32)
    weightgainfin=np.zeros((len(weightgaincat)*5,10),dtype=np.float32)
    healthycatfin=np.zeros((len(healthycat)*5,9),dtype=np.float32)
    t=0
    r=0
    s=0
    yt=[]
    yr=[]
    ys=[]
    for zz in range(5):
        for jj in range(len(weightlosscat)):
            valloc=list(weightlosscat[jj])
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            weightlossfin[t]=np.array(valloc)
            yt.append(brklbl[jj])
            t+=1
        for jj in range(len(weightgaincat)):
            valloc=list(weightgaincat[jj])
            print (valloc)
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            weightgainfin[r]=np.array(valloc)
            yr.append(lnchlbl[jj])
            r+=1
        for jj in range(len(healthycat)):
            valloc=list(healthycat[jj])
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            healthycatfin[s]=np.array(valloc)
            ys.append(dnrlbl[jj])
            s+=1

    X_test=np.zeros((len(healthycat)*5,9),dtype=np.float32)
    print('####################')
    # In[287]:
    for jj in range(len(healthycat)):
        valloc=list(healthycat[jj])
        valloc.append(agecl)
        valloc.append(clbmi)
        X_test[jj]=np.array(valloc)*ti
    # print (X_test)
    # print (len(weightlosscat))
    print (weightgainfin.shape)
    # Import train_test_split function
    from sklearn.model_selection import train_test_split
    
    X_train=healthycatfin# Features
    y_train=ys # Labels
    
    # Split dataset into training set and test set
#    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3) #
    
    # Import train_test_split function
    from sklearn.model_selection import train_test_split
    
    # X_train= weightlossfin# Features
    # y_train=yt # Labels
    
    #Import Random Forest Model
    from sklearn.ensemble import RandomForestClassifier
    
    #Create a Gaussian Classifier
    clf=RandomForestClassifier(n_estimators=100)
    
    #Train the model using the training sets y_pred=clf.predict(X_test)
    clf.fit(X_train,y_train)
    
    print (X_test[1])
    X_test2=X_test
    y_pred=clf.predict(X_test)
    print('ok')
    
    
    print ('SUGGESTED FOOD ITEMS ::')
    for ii in range(len(y_pred)):
        if y_pred[ii]==2:
            print('#################')
            print (Food_itemsdata[ii])
            findata=Food_itemsdata[ii]
            if int(veg)==1:
                datanv=['Chicken Burger']
                for it in range(len(datanv)):
                    if findata==datanv[it]:
                        print('VegNovVeg')

#master = tk.Tk()
Label(main_win,text="Age").grid(row=0,column=0,sticky=W,pady=4)
Label(main_win,text="veg/Non veg").grid(row=1,column=0,sticky=W,pady=4)
Label(main_win,text="Weight").grid(row=2,column=0,sticky=W,pady=4)
Label(main_win,text="Height").grid(row=3,column=0,sticky=W,pady=4)

# Label(main_win,text="Age").grid(row=2,column=0)

e1 = Entry(main_win)
e2 = Entry(main_win)
e3 = Entry(main_win)
e4 = Entry(main_win)
e5 = Entry(main_win)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)
e5.grid(row=6, column=1)

Button(main_win,text='Quit',command=main_win.quit).grid(row=5,column=0,sticky=W,pady=4)
Button(main_win,text='Weight Loss',command=Weight_Loss).grid(row=1,column=4,sticky=W,pady=4)
Button(main_win,text='Weight Gain',command=Weight_Gain).grid(row=2,column=4,sticky=W,pady=4)
Button(main_win,text='Healthy',command=Healthy).grid(row=3,column=4,sticky=W,pady=4)
main_win.geometry("400x700")
main_win.wm_title("DIET RECOMMENDATION SYSTEM")
#GUIEXECUTION
main_win.mainloop()
