import numpy as np
import pandas as pd
import seaborn as sns
import os
print("Current working directory: {0}".format(os.getcwd()))
os.chdir("D:\yazilim")
#Adım 1: flo_data_20K.csv verisini okuyunuz.Dataframe’in kopyasını oluşturunuz.
df=pd.read_csv("")
df_ydk=df.copy()

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)
pd.set_option('display.width', 500)

#Adım 2: Veri setinde
#a. İlk 10 gözlem,
df.head(10)
#b. Değişken isimleri,
df.columns
#c. Betimsel istatistik,
df.describe().T
#d. Boş değer,
df.isnull().sum()
#e. Değişken tipleri, incelemesi yapınız
df.info()

df.head()
df["order_channel"].value_counts()
df["last_order_channel"].value_counts()
df["order_channel"].value_counts()
#Adım 3: Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir. Her bir müşterinin toplam
#alışveriş sayısı ve harcaması için yeni değişkenler oluşturunuz.

df["order_num_total_ever_both"]=df["order_num_total_ever_online"]+df["order_num_total_ever_offline"]
df["customer_value_total_ever_both"]=df["customer_value_total_ever_offline"]+df["customer_value_total_ever_online"]

#Adım 4: Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
df['first_order_date']=pd.to_datetime(df['first_order_date'], format='%Y/%m/%d')
df['last_order_date']=pd.to_datetime(df['last_order_date'], format='%Y/%m/%d')
df['last_order_date_online']=pd.to_datetime(df['last_order_date_online'], format='%Y/%m/%d')
df['last_order_date_offline']=pd.to_datetime(df['last_order_date_offline'], format='%Y/%m/%d')
df.info()
"""
date_columns = df.columns[df.columns.str.contains("date")]
df[date_columns] = df[date_columns].apply(pd.to_datetime)
"""
#Adım 5: Alışveriş kanallarındaki müşteri sayısının, toplam alınan ürün sayısının ve toplam harcamaların dağılımına bakınız.

df2=df.groupby(["order_channel", "master_id"]).agg({"order_num_total_ever_both" : "sum",
                                              "customer_value_total_ever_both": "sum"})
df2=df2.reset_index()
df2.head()
#df2[df2["order_channel"] == "Android App"]["master_id"].count() #uzun yol, kullanilmadi
#kanallardaki toplam musteri sayilari
df2.order_channel.value_counts()
#kanalların toplam satis hacmi
df2.groupby("order_channel").agg("sum")

#Adım 6: En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.
df=df.sort_values("customer_value_total_ever_both", ascending=False)
df.head(10)

#Adım 7: En fazla siparişi veren ilk 10 müşteriyi sıralayınız.
df.sort_values("order_num_total_ever_both", ascending=False).head(10)

#Adım 8: Veri ön hazırlık sürecini fonksiyonlaştırınız.

def check_df(dataframe):
    print("### Tablo Head ######")
    print(df.head())
    print("##istatistikkler##")
    print(df.describe().T)
    print("### info ####")
    print(df.info())

def pre_proceses(dataframe):
    check_df(dataframe)
    dataframe["order_num_total_ever_both"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total_ever_both"] = dataframe["customer_value_total_ever_offline"] + dataframe[
        "customer_value_total_ever_online"]
    """
    date_columns = df.columns[df.columns.str.contains("date")]
    df[date_columns] = df[date_columns].apply(pd.to_datetime)
    """
    dataframe['first_order_date'] = pd.to_datetime(dataframe['first_order_date'], format='%Y/%m/%d')
    dataframe['last_order_date'] = pd.to_datetime(dataframe['last_order_date'], format='%Y/%m/%d')
    dataframe['last_order_date_online'] = pd.to_datetime(dataframe['last_order_date_online'], format='%Y/%m/%d')
    dataframe['last_order_date_offline'] = pd.to_datetime(dataframe['last_order_date_offline'], format='%Y/%m/%d')
    dataframe.info()
    df2 = dataframe.groupby(["order_channel", "master_id"]).agg({"order_num_total_ever_both": "sum",
                                                          "customer_value_total_ever_both": "sum",
                                                                 })
    df2 = df2.reset_index()
    return dataframe, df2

df, df2= pre_proceses(df)
df.head()
df2.head()
df2.groupby("order_channel").agg("sum")
df_ydk[df_ydk["order_channel"] == "Offline"]

#Görev 2: RFM Metriklerinin Hesaplanması
# Adım 1: Recency, Frequency ve Monetary tanımlarını yapınız.
df.head()
#receny
df["Recency"]=df["last_order_date"] - df["first_order_date"]
df.head()
#Frequency
df["Frequency"]=df["order_num_total_ever_both"]/ df.shape[0]
#monetary
df["Monetary"]=df["customer_value_total_ever_both"]
df[df["order_num_total_ever_both"]<2].value_counts().sum()
rfm_list=["master_id", "order_channel", "Recency", "Frequency", "Monetary", "interested_in_categories_12"]
df_rfm=df[rfm_list]
# Adım 2: Müşteri özelinde Recency, Frequency ve Monetary metriklerini hesaplayınız.
# Adım 3: Hesapladığınız metrikleri rfm isimli bir değişkene atayınız.
# Adım 4: Oluşturduğunuz metriklerin isimlerini recency, frequency ve monetary olarak değiştiriniz
df_rfm.head()

# Adım 1: Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çeviriniz.
# Adım 2: Bu skorları recency_score, frequency_score ve monetary_score olarak kaydediniz.
df_rfm["recency_score"] = pd.qcut(df_rfm["Recency"], 5, labels=["5", "4", "3", "2", "1"])
df_rfm.head()
df_rfm["frequency_score"] = pd.qcut(df_rfm["Frequency"].rank(method="first"), 5, labels=["1", "2", "3", "4", "5"])
df_rfm["monetary_score"] = pd.qcut(df_rfm["Monetary"], 5, labels=["1","2", "3", "4", "5"])

#df_rfm.drop("Monetary_score", axis=1, inplace=True)

# Adım 3: recency_score ve frequency_score’u tek bir değişken olarak ifade ediniz ve RF_SCORE olarak kaydediniz.
df_rfm["RF_SCORE"] = (df_rfm["recency_score"].astype(str) +
                    df_rfm['frequency_score'].astype(str))

# Adım 1: Oluşturulan RF skorları için segment tanımlamaları yapınız.
# Adım 2: Aşağıdaki seg_map yardımı ile skorları segmentlere çeviriniz.
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

df_rfm["segment"] = df_rfm["RF_SCORE"].replace(seg_map, regex=True)
df_rfm.head()
df_rfm[["segment", "Recency", "Frequency", "Monetary"]].groupby("segment").agg(["mean", "count"])



#df_rfm.to_csv("VBO/CRM_Analitik_3hafta/crm_odev_vbo/df_rfm.csv")

import pandas as pd
import os
os.chdir("D:\yazilim")
df_rfm=pd.read_csv("VBO/CRM_Analitik_3hafta/crm_odev_vbo/df_rfm.csv")


# a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri
# tercihlerinin üstünde. Bu nedenle markanın tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak
# iletişime geçmek isteniliyor. Sadık müşterilerinden(champions, loyal_customers) ve kadın kategorisinden alışveriş
# yapan kişiler özel olarak iletişim kurulacak müşteriler. Bu müşterilerin id numaralarını csv dosyasına kaydediniz

target_id = df_rfm[df_rfm["interested_in_categories_12"].str.contains("KADIN", na=False)]
target_id = target_id[(target_id["segment"] == "champions") | (target_id["segment"] == "loyal_customers")]
target_id.head()
target_id.to_csv("VBO/CRM_Analitik_3hafta/crm_odev_vbo/target_id.csv")

# b. Erkek ve Çocuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte
# iyi müşteri olan ama uzun süredir alışveriş yapmayan kaybedilmemesi gereken müşteriler, uykuda olanlar ve yeni
# gelen müşteriler özel olarak hedef alınmak isteniyor. Uygun profildeki müşterilerin id'lerini csv dosyasına kaydediniz.

df_rfm["segment"].value_counts()
#iyi müşteri olan ama uzun süredir alışveriş yapmayan
#at_Risk                3251, about_to_sleep         1517, cant_loose             2791, new_customers          1598
df_rfm[["segment", "Recency", "Frequency", "Monetary"]].groupby("segment").agg(["mean", "count"])
target_list=["at_Risk", "about_to_sleep", "cant_loose", "new_customers"]
target_id2=df_rfm[df_rfm["segment"].isin(["at_Risk", "cant_loose", "new_customers"])]["master_id"]
df_rfm.head()
target_id2.head()
#target_id2=df_rfm[(df_rfm["segment"] == "at_Risk") | (df_rfm["segment"] == "about_to_sleep") | ( df_rfm[(df_rfm["segment"] == "cant_loose" ) | (df_rfm["segment"] == "new_customers")]
target_id2["segment"].value_counts()
target_list = df_rfm[df_rfm['segment'].isin(['at_risk', 'cant_loose', 'new_costumers'])]["master_id"]
target_list.to_csv("D:\yazilim\VBO\CRM_Analitik_3hafta/target_id2_crm_odev")
target_list.head()

target_segments_customer_ids = rfm[rfm["segment"].isin(["cant_loose","hibernating","new_customers"])]["customer_id"]
cust_ids = df[(df["master_id"].isin(target_segments_customer_ids)) & ((df["interested_in_categories_12"].str.contains("ERKEK"))|(df["interested_in_categories_12"].str.contains("COCUK")))]["master_id"]
cust_ids.to_csv("indirim_hedef_müşteri_ids.csv", index=False)
