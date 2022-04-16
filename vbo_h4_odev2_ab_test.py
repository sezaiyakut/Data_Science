import os
os.chdir("D:\yazilim/VBO")
print("Current working directory: {0}".format(os.getcwd()))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#!pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest


pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)
pd.set_option('display.width', 500)


df=pd.read_excel("hafta4_Olcumlendirme_Siralama_AB/ab_testing.xlsx")
df_control=pd.read_excel("hafta4_Olcumlendirme_Siralama_AB/ab_testing.xlsx", sheet_name="Control Group")
df_test=pd.read_excel("hafta4_Olcumlendirme_Siralama_AB/ab_testing.xlsx", sheet_name="Test Group")
df_control.head()
df_test.head()
df_t_ydk=df_test.copy()
df_c_ydk=df_control.copy()

df_test.info()
df_control.info()

df_test.describe().T
df_control.describe().T

df=pd.concat([df_control, df_test], axis=0)
df.head()
df.tail()
df.info()
df.reset_index()


# Görev 2: A/B Testinin Hipotezinin Tanımlanması

# Adım 1: Hipotezi tanımlayınız.
# H0 : M1 = M2, iki grup arasında anlamlı bir farklılık yoktur
# H1 : M1!= M2, iki grup arasında anlamlı bir farklılık vardır.



# Adım 2: Kontrol ve test grubu için purchase (kazanç) ortalamalarını analiz ediniz.
df.head()
df_control.Purchase.mean() #550.894
df_test.Purchase.mean()  #582.106

#Görev 3: Hipotez Testinin Gerçekleştirilmesi
"""Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.
Bunlar Normallik Varsayımı ve Varyans Homojenliğidir. Kontrol ve test grubunun normallik varsayımına uyup 
uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz"""
# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.


#Normallik Varsayımı
#H0:Normallik varsayımı sağlanmaktadır
#H1:Normallik varsayımı sağlanmamaktadır.

test_stat, pvalue = shapiro(df_control["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#0.5891

test_stat, pvalue = shapiro(df_test["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#0.1541

#p value değeri > 0.05 olduğu için h0 red edlemez. sağlanmaktadır.

#Varyans homojenliği varsayımı
# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

test_stat, pvalue = levene(df_control["Purchase"], df_test["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#0.1083
#p value değeri > 0.05 olduğu için h0 red edlemez. sağlanmaktadır.


#Varsayımlar sağlanıyor; bağımsız iki örneklem t testi (parametrik test)


test_stat, pvalue = ttest_ind(df_control["Purchase"],
                              df_test["Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p value=0.34
#0.05den büyük olduğu şçin red edemeyiz. alamlı bir farkllık yoktur.


#görev4 yorumlama
#parametrik dağılım olduğu için iki örenklem T testini,varvasyon da sağlandığı için equal_var=true
# parametresiyle kullandım
#Ajansın yaptığı çalışma fark yaratamamış.