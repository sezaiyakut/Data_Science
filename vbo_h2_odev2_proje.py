pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)

# Görev 1: Aşağıdaki Soruları Yanıtlayınız

# Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.

df= pd.read_csv("D:\yazilim\VBO\odev2_np_pd_ve_plot_kesifci_fonk\persona.csv")
df_ydk=df.copy()
df.head()
# § Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?
df[["SOURCE"]].value_counts()
# § Soru 3: Kaç unique PRICE vardır?
df["PRICE"].nunique()

# § Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
df["PRICE"].value_counts()
# § Soru 5: Hangi ülkeden kaçar tane satış olmuş?
df["COUNTRY"].value_counts()
# § Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?
df.head()
df.groupby("COUNTRY").agg({"PRICE": ["sum"]})
# § Soru 7: SOURCE türlerine göre satış sayıları nedir?
df.groupby("SOURCE").agg({"PRICE": ["sum"]})
# § Soru 8: Ülkelere göre PRICE ortalamaları nedir?
df.groupby("COUNTRY").agg({"PRICE": ["mean"]})
# § Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?
df.groupby("SOURCE").agg({"PRICE": ["sum"]})
# § Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
df.groupby(["COUNTRY","SOURCE"]).agg({"PRICE": ["mean"]})



# Görev 2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
df2=df.groupby(["COUNTRY","SOURCE", "SEX", "AGE"]).agg({"PRICE": ["sum", "count"]})
df2.head()
df2["avg_profit"]=df2["PRICE"]["sum"]/df2["PRICE"]["count"]
df2.head()
# Görev 3: Çıktıyı PRICE’a göre sıralayınız.

df.sort_values("PRICE")

# Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE’a göre uygulayınız.
# Çıktıyı agg_df olarak kaydediniz.
agg_df=df.sort_values("PRICE", ascending=False)
agg_df.head()
#
# Görev 4: Indekste yer alan isimleri değişken ismine çeviriniz
df["new_col"]=df.index
df.head()

# Görev 5: Age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz
df["AGE"].dtype
df["AGE"] = df["AGE"].astype("category")
df["AGE"].dtype


# Age sayısal değişkenini kategorik değişkene çeviriniz.
# • Aralıkları ikna edici şekilde oluşturunuz.
# • Örneğin: ‘0_18', ‘19_23', '24_30', '31_40', '41_70'
df[["AGE"]].value_counts()
df["NEW_AGE"] = pd.cut(df["AGE"], [0, 18, 23, 30, 40, 70], labels=["0_18", "19_23", "24_30", "31_40", "41_70"])
df[["NEW_AGE"]].value_counts()
df["NEW_AGE"].dtype
agg_df["NEW_AGE"]=df["NEW_AGE"]
agg_df.head()
# Görev 6: Yeni seviye tabanlı müşterileri (persona) tanımlayınız

agg_df["customers_level_based"] = [val[3].upper() + "_" + val[1].upper() + "_" + val[2].upper() + "_"+val[5] for val in agg_df.values ]
agg_df["customers_level_based"].head()
agg_df["new_col"]=agg_df.index
agg_df = agg_df.groupby("customers_level_based").agg({"PRICE":"mean"})
agg_df.sort_values("customers_level_based",ascending=False)
agg_df.reset_index(inplace=True)


# Yeni seviye tabanlı müşterileri (persona) tanımlayınız ve veri setine değişken olarak ekleyiniz.
# • Yeni eklenecek değişkenin adı: customers_level_based
# • Önceki soruda elde edeceğiniz çıktıdaki gözlemleri bir araya getirerek customers_level_based değişkenini oluşturmanız gerekmektedir



# Görev 7: Yeni müşterileri (personaları) segmentlere ayırınız
# Yeni müşterileri (Örnek: USA_ANDROID_MALE_0_18) PRICE’a göre 4 segmente ayırınız.
# • Segmentleri SEGMENT isimlendirmesi ile değişken olarak agg_df’e ekleyiniz.
# • Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız)

agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"],4,["D","C","B","A"])
agg_df.groupby("SEGMENT").agg({"PRICE" : ["mean", "min", "max", "sum"] })

"""
agg_list = ["mean", "min", "max", "sum"]
agg_df.groupby("SEGMENT")["PRICE"].agg(agg_list)
"""

# Görev 8: Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz
# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
agg_df.head()
new_user="TUR_ANDROID_FEMALE_31_40"
agg_df[(["customers_level_based"] == new_user)]["SEGMENT"]
