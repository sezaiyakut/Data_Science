import os
print("Current working directory: {0}".format(os.getcwd()))
os.chdir("D:\yazilim/VBO")
import pandas as pd
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)
pd.set_option('display.width', 500)

df=pd.read_csv("hafta4_Olcumlendirme_Siralama_AB/amazon_review.csv")
df.head()
df_ydk=df.copy()

####inceleme#########
df.describe().T
df.helpful.value_counts()
df.sort_values("helpful_yes", ascending=False).head(50)
df.sort_values("day_diff", ascending=False).tail(50)
df.asin.value_counts()


#1 ürün ortalama puanı
df.overall.mean()
#4.587589
df.head()
#Adım 2: Tarihe göre ağırlıklı puan ortalamasını hesaplayınız.

df["day_diff"].describe([0.05,0.1,0.15,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,0.99]).T
# %10=167, %20=248, 40% 361, %50=431, %70=562, %80=638 %95=748 %99=943

def time_based_weighted_average(dataframe, day, rating, w1=28, w2=26, w3=24, w4=22):
    return dataframe.loc[df[day] <= dataframe[day].quantile(0.25), rating].mean() * w1 / 100 + \
           dataframe.loc[(dataframe[day] > 180) & (dataframe[day] <= 366), rating].mean() * w2 / 100 + \
           dataframe.loc[(dataframe[day] > 366) & (dataframe[day] <= 550), rating].mean() * w3 / 100 + \
           dataframe.loc[(dataframe[day] > 550), rating].mean() * w4 / 100
#6ayllık periyotlarla bölünüd. Bu veri seti için; dağılımlar yaklaşık olarakw1:-%15 w2:-%30 w3:-%30 w4:+%30
time_based_weighted_average(df, "day_diff", "overall")
#4.6144817593690455 #tarih ağırlıklı ortalama1

# reviewTime değişkenini tarih değişkeni olarak tanıtnız
df.info()
df["reviewTime"]=pd.to_datetime(df["reviewTime"])

#• reviewTime'ın max değerini current_date olarak kabul etmeniz
df["reviewTime"].max()
#Out[17]: Timestamp('2014-12-07 00:00:00'
import datetime as dt
current_date = dt.datetime(2014, 12, 7)
df["yeni_day_diff"]=current_date-df["reviewTime"]
#Görev 1: Average Rating’i güncel yorumlara göre hesaplayınız ve var olan average rating ile kıyaslayınız.


#• her bir puan-yorum tarihi ile current_date'in farkını gün cinsinden ifade ederek yeni değişken oluşturmanız ve
# gün cinsinden ifade edilen değişkeni quantile fonksiyonu ile 4'e bölüp (3 çeyrek verilirse 4 parça çıkar) çeyrekliklerden
# gelen değerlere göre ağırlıklandırma yapmanız gerekir. Örneğin q1 = 12 ise ağırlıklandırırken
# 12 günden az süre önce yapılan yorumların ortalamasını alıp bunlara yüksek ağırlık vermek gibi.
q1,q2,q3=df.day_diff.quantile([0.25,0.5,0.75])

df["seg_qcut"] = pd.qcut(df["day_diff"],4,labels=["yeni","guncel","yilgecmis","eski"])
df["seg_quan_cut"]= pd.cut(df["day_diff"], [0,q1,q2,q3,df.day_diff.max()], labels=["yeni","guncel","yilgecmis","eski"])
df.head()
df.loc[df["seg_qcut"]!=df["seg_quan_cut"]]  #boş

#Adım 3: Ağırlıklandırılmış puanlamada her bir zaman diliminin ortalamasını karşılaştırıp yorumlayınız.
df.groupby("seg_qcut").agg({"overall": "mean"})

df[df["seg_qcut"]=="yeni"]["overall"].mean()  #4.695792
df[df["seg_qcut"]=="guncel"]["overall"].mean()  #4.636140637775961
df[df["seg_qcut"]=="yilgecmis"]["overall"].mean()  #4.571661237785016
df[df["seg_qcut"]=="eski"]["overall"].mean()  #4.446254



#Görev 2: Ürün için ürün detay sayfasında görüntülenecek 20 Copyright © Miuul, Inc. All Rights Reserved review’i belirleyini

#Adım 1: helpful_no değişkenini üretiniz.
df.head()
# • total_vote bir yoruma verilen toplam up-down sayısıdır.
# • up, helpful demektir.
# • Veri setinde helpful_no değişkeni yoktur, var olan değişkenler üzerinden üretilmesi gerekmektedir.
# • Toplam oy sayısından (total_vote) yararlı oy sayısı (helpful_yes) çıkarılarak yararlı bulunmayan oy sayılarını
# (helpful_no) bulunuz.

df["helpful_no"]=df["total_vote"]-df["helpful_yes"]
#Adım 2: score_pos_neg_diff, score_average_rating ve wilson_lower_bound skorlarını hesaplayıp veriye ekleyiniz.
#  score_pos_neg_diff, score_average_rating ve wilson_lower_bound skorlarını hesaplayabilmek için score_pos_neg_diff,
# score_average_rating ve wilson_lower_bound fonksiyonlarını tanımlayınız.

def score_up_down_diff(up, down):
    return up - down

df["score_pos_neg_diff"] = df.apply(lambda x: score_up_down_diff(x["up"],
                                                                             x["down"]), axis=1)

# score_average_rating
comments["score_average_rating"] = comments.apply(lambda x: score_average_rating(x["up"], x["down"]), axis=1)

# wilson_lower_bound
comments["wilson_lower_bound"] = comments.apply(lambda x: wilson_lower_bound(x["up"], x["down"]), axis=1)



# • score_pos_neg_diff'a göre skorlar oluşturunuz. Ardından; df içerisinde score_pos_neg_diff ismiyle kaydediniz.
# • score_average_rating'a göre skorlar oluşturunuz. Ardından; df içerisinde score_average_rating ismiyle kaydediniz.
# • wilson_lower_bound'a göre skorlar oluşturunuz. Ardından; df içerisinde wilson_lower_bound ismiyle kaydediniz.

# Adım 3: 20 Yorumu belirleyiniz ve sonuçları Yorumlayınız.
"""sozlu olarak anlatildi"""
#  wilson_lower_bound'a göre ilk 20 yorumu belirleyip sıralayanız.

# • Sonuçları yorumlayınız.



"""saltuk buğra hoca zoomdan attığı kod, daydif ile ilgili, bulunacaksa naıl bulunacak"""
#df['reviewTime'] = pd.to_datetime(df['reviewTime'], dayfirst=True)
# current_date = pd.to_datetime(str(df['reviewTime'].max()))
# df["day_diff"] = (current_date - df['reviewTime']).dt.days


"""gukdeniz hoca chatten attığı"""
#def score_average_rating(up, down):
#    if up + down == 0:
#        return 0
#    return up / (up + down)
