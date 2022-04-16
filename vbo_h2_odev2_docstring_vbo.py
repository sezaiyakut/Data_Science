def cat_summary(dataframe, col_name, plot=False):

    """
    Dataframe üzerindeki tüm değişkenlerin kendilerinin toplam gözleme oranını yüzdelik oranla gösterir. İstenilirse çizim yapar.
    Parameters
    ----------
    dataframe:DataFrame
    işlem yapılacak dataframe adını ifade eder.
    col_name:string
    işlem yapılacak kolonun adını ifade eder.

    Çizim yapılıp yapılmayacağını ifade eder
    head: int, float
    Seçilen dataframe 'in ilk kaç gözleminin gösterileceğini ifade eder.

    Returns
    -------

    """
    print(pd.DataFrame({col_name: dataframe[col_name].value_counts(),
                        "Ratio": 100 * dataframe[col_name].value_counts() / len(dataframe)}))
    print("##########################################")

    if plot:
        sns.countplot(x=dataframe[col_name], data=dataframe)
        plt.show(block=True)


