#!pip install lifetimes
import datetime as dt
import pandas as pd
import os
os.chdir("D:\yazilim")

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)
pd.set_option('display.width', 500)






# Görev 1: Veriyi Hazırlama
# Adım 1: flo_data_20K.csv verisini okuyunuz.
df=pd.read_csv("VBO/CRM_Analitik_3hafta/crm_odev_vbo/FLO_RFM_Analizi/flo_data_20k.csv")
# Adım 2: Aykırı değerleri baskılamak için gerekli olan outlier_thresholds ve replace_with_thresholds fonksiyonlarını tanımlayınız.
def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = (quartile3 + 1.5 * interquantile_range).round()
    low_limit = (quartile1 - 1.5 * interquantile_range).round()
    return low_limit, up_limit


def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    # dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit




# Not: cltv hesaplanırken frequency değerleri integer olması gerekmektedir.Bu nedenle alt ve üst limitlerini round() ile yuvarlayınız.
# Adım 3: "order_num_total_ever_online", "order_num_total_ever_offline", "customer_value_total_ever_offline",
# "customer_value_total_ever_online" değişkenlerinin aykırı değerleri varsa baskılayanız.

replace_with_thresholds(df, "order_num_total_ever_online")
replace_with_thresholds(df, "order_num_total_ever_offline")
replace_with_thresholds(df, "customer_value_total_ever_offline")
replace_with_thresholds(df, "customer_value_total_ever_online")

# Adım 4: Omnichannel müşterilerin hem online'dan hem de offline platformlardan alışveriş yaptığını ifade etmektedir.
# Her bir müşterinin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturunuz.
df["order_num_total_ever_both"]=df["order_num_total_ever_online"]+df["order_num_total_ever_offline"]
df["customer_value_total_ever_both"]=df["customer_value_total_ever_offline"]+df["customer_value_total_ever_online"]


# Adım 5: Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz
date_columns = df.columns[df.columns.str.contains("date")]
df[date_columns] = df[date_columns].apply(pd.to_datetime)


#Görev 2: CLTV Veri Yapısının Oluşturulması

# Adım 1: Veri setindeki en son alışverişin yapıldığı tarihten 2 gün sonrasını analiz tarihi olarak alınız.
#Out[21]: Timestamp('2021-05-30 00:00:00')    Out[22]: Timestamp('2020-05-30 00:00:00')
df.last_order_date.max()
today_date = dt.datetime(2021, 6, 1)
#dt.datetime.now()
# Adım 2: customer_id, recency_cltv_weekly, T_weekly, frequency ve monetary_cltv_avg
# değerlerinin yer aldığı yeni bir cltv dataframe'i oluşturunuz.
# Monetary değeri satın alma başına ortalama değer olarak, recency ve tenure değerleri ise haftalık cinsten ifade edilecek
df["recency"]=df["last_order_date"]-df["first_order_date"]
df["recency"]=df["recency"].apply(lambda x: (x).days)
df.head(),
df.info()
"""cltv_df = df.groupby("master_id").agg(
    {'InvoiceDate': [().days,
                     lambda InvoiceDate: (today_date - InvoiceDate.min()).days],
     'Invoice': lambda Invoice: Invoice.nunique(),
     'TotalPrice': lambda TotalPrice: TotalPrice.sum()})
"""


crm=pd.DataFrame()
crm["customer_id"]=df["master_id"]
crm["recency_cltv_weekly"]=df["recency"]/7
crm["T_weekly"] = (today_date-df["first_order_date"])/7
crm["T_weekly"] = crm["T_weekly"].apply(lambda x: (x).days)
crm.head()
crm["frequency"]=df["order_num_total_ever_both"]/df.shape[0]
crm["monetary_cltv_avg"] = df["customer_value_total_ever_both"]/df["order_num_total_ever_both"]
cltv_df=pd.DataFrame()
cltv_df=crm.copy()
cltv_df.drop("customer_id", axis=1, inplace=True)
cltv_df.head()
cltv_df.columns = ['recency', 'T', 'frequency', 'monetary']



# Görev 3: BG/NBD, Gamma-Gamma Modellerinin Kurulması ve CLTV’nin Hesaplanması

cltv_df
cltv_df=cltv_df[cltv_df["recency"]>0]
cltv_df[cltv_df["frequency"]==0]
cltv_df[cltv_df["recency"]==0]

import matplotlib.pyplot as plt
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.plotting import plot_period_transactions

bgf = BetaGeoFitter(penalizer_coef=0.001)

bgf.fit(cltv_df['frequency'],
        cltv_df['recency'],
        cltv_df['T'])

cltv_df[cltv_df[""]]
# Adım 1: BG/NBD modelini fit ediniz

# 3 ay içerisinde müşterilerden beklenen satın almaları tahmin ediniz ve exp_sales_3_month olarak cltv
# dataframe'ine ekleyiniz.



# • 6 ay içerisinde müşterilerden beklenen satın almaları tahmin ediniz ve exp_sales_6_month olarak cltv
# dataframe'ine ekleyiniz


# Adım 2: Gamma-Gamma modelini fit ediniz. Müşterilerin ortalama bırakacakları değeri tahminleyip exp_average_value olarak cltv
# dataframe'ine ekleyiniz.

#Adım 3: 6 aylık CLTV hesaplayınız ve cltv ismiyle dataframe'e ekleyiniz.

#Cltv değeri en yüksek 20kişiyi gözlemleyiniz.

# Görev 4: CLTV Değerine Göre Segmentlerin Oluşturulması

# Adım 1: 6 aylık CLTV'ye göre tüm müşterilerinizi 4 gruba (segmente) ayırınız ve grup isimlerini veri setine ekleyiniz.


# Adım 2: 4 grup içerisinden seçeceğiniz 2 grup için yönetime kısa kısa 6 aylık aksiyon önerilerinde bulununuz