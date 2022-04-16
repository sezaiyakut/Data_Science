import pandas as pd
import seaborn as sns
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)

#Görev 1: Seaborn kütüphanesi içerisinden Titanic veri setini tanımlayınız.

df = sns.load_dataset("titanic")
#print(df.info())

#Görev 2: Titanic veri setindeki kadın ve erkek yolcuların sayısını bulunuz
#print(df["sex"].value_counts())

#Görev 3: Her bir sutuna ait unique değerlerin sayısını bulunuz.
#print(df.nunique())

#Görev 4: pclass değişkeninin unique değerlerinin sayısını bulunuz
#print(df["pclass"].nunique())

#Görev 5: pclass ve parch değişkenlerinin unique değerlerinin sayısını bulunuz.
#print(df[["pclass", "parch"]].nunique())

#Görev 6: embarked değişkeninin tipini kontrol ediniz. Tipini category olarak değiştiriniz ve tekrar kontrol ediniz.

#yapılmadı
"""
df["embarked"].dtype
df["embarked"] = df["embarked"].astype("category")
df["embarked"].dtype
"""
#Görev 7: embarked değeri C olanların tüm bilgelerini gösteriniz.
#print(df[df["embarked"] == "C"].head(10))

#Görev 8: embarked değeri S olmayanların tüm bilgelerini gösteriniz
#print(df[df["embarked"] != "S"].head(10))

#Görev 9: Yaşı 30 dan küçük ve kadın olan yolcuların tüm bilgilerini gösteriniz.
#print(df[(df["age"]<30) & (df["sex"]=="female")])

#Görev 10: Fare'i 500'den büyük veya yaşı 70’den büyük yolcuların bilgilerini gösteriniz.
    #df[(df["age"]>70) | (df["fare"]>500)]

#Görev 11: Her bir değişkendeki boş değerlerin toplamını bulunuz.
#print(df.isnull().sum())

#Görev 12: who değişkenini dataframe’den çıkarınız.
#df.drop("who", axis=1, inplace=True)
#print(df.head())

#Görev 13: deck değikenindeki boş değerleri deck değişkenin en çok tekrar eden değeri (mode) ile doldurunuz.
""" cevap bu
mode=df["deck"].mode()
df["deck"]=np.where(df["deck"].isnull(), mode, df["deck"])

"""

"""diğer özümler çalışmadı. burası sorulacak"""
#df["deck"][df["deck"].isnull()] = [str(df["deck"].mode())*int((df["deck"].isnull().count()))]

#df["deck"].isnull().sum()

"""mode=df["deck"].mode()
 df.loc[df[df["deck"].isnull()].index.tolist(), "deck"] = mode
df["deck"].isnull().sum()"""

#Görev 14: age değikenindeki boş değerleri age değişkenin medyanı ile doldurunuz.
"""
df["age"].fillna(df["age"].median(), inplace=True)
df["age"].isnull().any()
"""
#Görev 15: survived değişkeninin pclass ve cinsiyet değişkenleri kırılımınında sum, count, mean değerlerini bulunuz.
#print(df.groupby(["pclass", "sex"]).agg({"survived" : ["sum","count","mean"] }))



#Görev 16: 30 yaşın altında olanlar 1, 30'a eşit ve üstünde olanlara 0 verecek bir fonksiyon yazın. Yazdığınız fonksiyonu kullanarak titanik veri
#setinde age_flag adında bir değişken oluşturunuz oluşturunuz. (apply ve lambda yapılarını kullanınız)
"""
def is_old(df, x):
"""    """
    DF adlı dataframe'de col sütunundaki değerler x değerinden küçük müdür sorusunu sorar.
    Parameters
    ----------
    df: Dataframe
    x: int, float
    Sınırı belirtir

    Returns
    -------
    """"""
    df["age_flag"] = pd.cut(df["age"],bins=[0, x, 90], labels=[1,0])
    print(df[["age_flag", "age"]].head())
is_old(df,30)
"""
def add_flag(df,x):
    """

    Parameters
    ----------
    df
    x

    Returns
    -------

    """
    df["age_flag"] = pd.cut(df["age"], [0,x,90], labels=[1,0])
    print(df.head())
df.head()
add_flag(df,30)
df["age_flag"] = pd.cut(df["age"]), [0,x,90], labels=[1,0])

def add_flag2(age):
    if age < 30:
        return 1
    else:
        return 0

df["flag_2"]= df["age"].apply(lambda x : add_flag2(x))
#df["flag_2"]= df["age"].apply(add_flag2)
#df["age_flag"] = df.age.apply(lambda x: 0 if x < 30 else 1)
#df['age_flag'] = df.apply(lambda row: cal(row['age']), axis=1


df.head()

#Görev 17: Seaborn kütüphanesi içerisinden Tips veri setini tanımlayınız.
dff = sns.load_dataset("tips")
#print(dff.head())

#Görev 18: Time değişkeninin kategorilerine (Dinner, Lunch) göre total_bill değerinin sum, min, max ve mean değerlerini bulunuz
#print(dff.groupby("time").agg({"total_bill":["sum","min","max","mean"]}))

#Görev 19: Day ve time’a göre total_bill değerlerinin sum, min, max ve mean değerlerini bulunuz.
#print(dff.groupby(["day", "time"]).agg({"total_bill":["sum","min","max","mean"]}))


#Görev 20: Lunch zamanına ve kadın müşterilere ait total_bill ve tip değerlerinin day'e göre sum, min, max ve mean değerlerini bulunuz
#print(dff[(dff["time"] == "Lunch") & (dff["sex"] == "Female")].groupby("day").agg({"total_bill" : ["sum","min","max","mean"],
                                                                                   #"tip" : ["sum","min","max","mean"]}))

#Görev 21: size'i 3'ten küçük, total_bill'i 10'dan büyük olan siparişlerin ortalaması nedir? (loc kullanınız)
"""print(dff.loc[(dff["size"] < 3) & (dff["total_bill"] > 10), ["total_bill", "tip"]].agg({"total_bill":["mean"],
                                                                                        "tip":["mean"],}))"""


#Görev 22: total_bill_tip_sum adında yeni bir değişken oluşturunuz. Her bir müşterinin ödediği totalbill ve tip in toplamını versin

#dff["total_bill_tip_sum"]=dff["tip"]+dff["total_bill"]
#print(dff.head())


"""Görev 23: Total_bill değişkeninin kadın ve erkek için ayrı ayrı ortalamasını bulunuz.
 Bulduğunuz ortalamaların altında olanlara 0, üstünde ve eşit olanlara 1 verildiği yeni bir total_bill_flag değişkeni oluşturunuz.
Kadınlar için Female olanlarının ortalamaları, erkekler için ise Male olanların ortalamaları dikkate alınacktır. 
Parametre olarak cinsiyet ve total_bill
alan bir fonksiyon yazarak başlayınız. (If-else koşulları içerecek)"""

#ort_dic = dff.groupby("sex").agg({"total_bill":"mean"})
#male_avg=ort_dic["total_bill"][0]
#female_avg=ort_dic["total_bill"][1]
#--------------------------------------------------
dff = sns.load_dataset("tips")

male_avg=dff[dff.sex=="Male"]["total_bill"].mean()
female_avg=dff[dff.sex=="Female"]["total_bill"].mean()
max_bill=dff["total_bill"].max()

dff["total_bill_flag"]=""
dff[["sex"] == "Male"]["total_bill_flag"]= pd.cut(dff[dff["sex"] == "Male"]["total_bill"],bins=[0, male_avg, max_bill], labels=[0,1])
dff["total_bill_flag"][dff["sex"] == "Female"] = pd.cut(dff[dff["sex"] == "Female"]["total_bill"],bins=[0, female_avg, max_bill], labels=[0,1])
dff.head()


"""güldeniz hoca attı. 
df.loc[(df['Sex'] == 'Female') & (df['total_bill'] < female_avg ), 'total_bill_flag]  = '0'
df.loc[(df['Sex'] == 'Female',  'total_bill_flag') & (df['total_bill'] < female_avg ), 'total_bill_flag]  = '0'
"""


def bill_flag(col,col2):

"""
    Parameters
    ----------
    col str
    Tırnak içinde işlem yapılacak kolon adını yazınız.
    sex: str
    Tırnak içinde işlem yapılacak cinsiyet adını yazınız.

    Returns
    -------
"""


#                          #başarısız fonk denemesi
    max_bill = dff[col].max()
    if dff[col2] == "Male":
        male_avg = dff[dff["sex"] == "Male"][col].mean()
        dff[col +"_flag"][dff["sex"] == "Male"] = pd.cut(dff[dff["sex"] == "Male"][col],
                                                              bins=[0, male_avg, max_bill], labels=[0, 1])
    elif dff[col2] == "Female":
        female_avg = dff[dff.sex == "Female"]["total_bill"].mean()
        dff[col + "_flag"][dff["sex"] == "Female"] = pd.cut(dff[dff["sex"] == "Female"][col],
                                                                bins=[0, female_avg, max_bill], labels=[0, 1])

bill_flag("total_bill","sex")

#####################################################################################################################
dff = sns.load_dataset("tips")




def new_bill (sex="sex", total_bill="total_bill"):

    if sex == "Female":
        female_avg = dff[dff.sex == "Female"]["total_bill"].mean()
        if total_bill >= female_avg:
            return 1
        else:
            return 0
    else:
        male_avg = dff[dff.sex == "Male"]["total_bill"].mean()
        if total_bill >= male_avg:
            return 1
        else:
            return 0



dff["total_bill_flag"]=dff.apply(lambda x: new_bill(x["sex"], x["total_bill"]), axis=1 )
dff.head()
#Görev 24: total_bill_flag değişkenini kullanarak cinsiyetlere göre ortalamanın altında ve üstünde olanların sayısını gözlemleyiniz.

dff[dff["total_bill_flag"] == 0].count()
dff[dff["total_bill_flag"] == 1].count()


#Görev 25: Veriyi total_bill_tip_sum değişkenine göre büyükten küçüğe sıralayınız ve ilk 30 kişiyi yeni bir dataframe'e atayınız
dff2=dff.sort_values("total_bill_tip_sum").head(30)
dff2