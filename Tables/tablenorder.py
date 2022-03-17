import pickle
tablenorder=[{}]*7
j=0
for i in tablenorder:
    f=open('Table/' + str(j),'wb')
    pickle.dump(i,f)
    f.close()
    j=j+1
