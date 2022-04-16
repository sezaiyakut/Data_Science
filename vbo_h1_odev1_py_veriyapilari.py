#gorev1
"""x=8
y=3.2
z=8j+18
a="Hallo world!"
b=True
c=23<22
l=[1,2,3,4]
d={"Name":"Sezai",
   "Age":"27",
   "Adress":"DownTown"}
t=("Machine Learning","Data Science")
s={"Python", "Machine Learning","Data Science"}
values=[x,y,z,a,b,c,l,d,t,s]
for v in values:
    print(v)
    print(type(v))"""

#gorev2
"""text="The goal is to turn data into information, and information into insight"
a=text.upper().replace(",","").split()
print(a)"""

#gorev3
"""lst=["D","A","T","A","S","C","I","E","N","C","E"]
len(lst)

print(lst[0])
print(lst[10])

y_lst=lst[0:4]
y_lst

lst.pop(8)
lst.append("!")
lst.insert(8,"N")
lst"""

#gorev4
"""dict = {'Christian': ["America", 18],
       'Daisy': ["England", 12],
       'Antonio': ["Spain", 22],
       'Dante': ["Italy", 25]}

key_list=dict.keys()
print(key_list)
#print(dict.keys())
print(dict.values())
dict.update({"Daisy" : ["England", 13]})
dict["Ahmet"]=["Turkey",24]
dict.pop("Antonio")
print(dict)"""

#gorev5
"""Numbers= range(1,21)
print(type(Numbers))
def num_dec(L):
    num_list=[[],[]]
    for n in L:
        if n%2==0:
            num_list[1].append(n)
        else:
            num_list[0].append(n)
    print(f"Tek sayilar :{num_list[0]} ve Cift Sayilar: {num_list[1]}")
    return num_list

num_dec(Numbers)"""

#gorev6
"""import seaborn as sns
df = sns.load_dataset("car_crashes")
cols = ["NUM_"+ col.upper() if df[col].dtype != "O" else col.upper() for col in df.columns ]
df.columns=cols
df.head()"""

#gorev7
"""import seaborn as sns
df = sns.load_dataset("car_crashes")
cols=[col.upper() if "no" in col else col.upper() +"_FLAG" for col in df.columns ]
cols"""

#gorev8

og_list=["abbrev","no_previous"]
import seaborn as sns
df=sns.load_dataset("car_crashes")
new_cols=[col for col in df.columns if col not in og_list]
new_df=df[new_cols]
new_df.head()