import pandas as pd
import sqlite3
import datetime
import time

from re import search

import gdelt
import platform
import multiprocessing


# =========================================================
# Load the featureidcommonnames-crosswalk within Australia
def getFeatureids():

    df = pd.read_csv('data/australialocations.csv')

    # extract the list of featureids within Australia
    featureids = df['featureid'].values.tolist()
    print('The number of featureIDs in Australia: ', len(featureids))
    #print(featureids[:10])
    return featureids


# ===========================================================
# Get date range from week number
# ===========================================================
def getDateRangeFromWeek(p_year,p_week):
    
    firstdayofweek = datetime.datetime.strptime(f'{p_year}-W{int(p_week )- 1}-1', "%Y-W%W-%w").date()
    lastdayofweek = firstdayofweek + datetime.timedelta(days=6.9)
    return firstdayofweek, lastdayofweek
# ====================================================
# Retrieve data from gdelt
# ====================================================
def retrieveandfilter(daterange):

    # This is for english, for translated data, we have to set translation=True
    # these two datasets are stored in different files in GDELT
    results = gd.Search(daterange,table='gkg',coverage=True)

    print("The number of rows for global: ", len(results))

    #results = results[(results.ActionGeo_FeatureID.isin(aus_featureids)) | 
    #                    (results.Actor1Geo_FeatureID.isin(aus_featureids)) |
    #                    (results.Actor2Geo_FeatureID.isin(aus_featureids))]
    #df = df[df['location'].str.contains('Australia', regex=False)]

    # results = results[results['Actor1CountryCode'] == 'AUS']
    # the same as
    # results = results[results.Actor1CountryCode == 'AUS']
    results = results[(results.Actor1CountryCode == 'AUS') | 
                        (results.Actor2CountryCode == 'AUS') | 
                        (results.Actor1Geo_CountryCode == 'AS') |
                        (results.Actor2Geo_CountryCode == 'AS')]
    

    print("The number of rows for Australia returned: ", len(results))
    
    return results

def tosql(db, table, df):
    conn = sqlite3.connect(db)
    df.to_sql(table, conn, if_exists="append")
    conn.close()

def query_db(db, query):
    conn = sqlite3.connect(db)
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df

def pulldata(year, startweek, endweek):

    for i in range(startweek, endweek):
        # ======================================================
        # 2019-01-07   2019-01-13
        # t.strftime('%m/%d/%Y') => 02/23/2012
        #print(firstdate.strftime('%Y %m %d'))
        # 2019 01 07
        # =======================================================
        firstdate, lastdate = getDateRangeFromWeek(year, str(i))
        firstdatestr = firstdate.strftime('%Y %m %d')
        lastdatestr = lastdate.strftime('%Y %m %d')
        print(firstdatestr, lastdatestr)
        daterange = [firstdatestr, lastdatestr]
        # Retrieve and filter data
        print("Retrieve and filter data .......")
        results = retrieveandfilter(daterange)
        print("Retrieve and filter done.")

        # Store data into a database
        print("Store data into database .....")
        db = 'data/gdeltdata_aus.db'
        table = 'gdelt2019_2020'
        tosql(db, table, results)
        print("Storing done.")

if __name__ == '__main__':

    print(platform.platform())
    print(multiprocessing.cpu_count())

    # ==============================================
    # Use the gdeltPyR package to access gdelt data
    gd = gdelt.gdelt(version=2)

    start = datetime.datetime.now()
    results = gd.Search(['2019 08 01', '2019 08 07'], table='gkg', coverage=True)
    end = datetime.datetime.now()
    print("Time to retrieve 7 days data: ", end - start)
    print(results.info())
    print('The number of rows returned: ', len(results))

    # Store data into a database
    print("Store data into database .....")
    db = 'data/gdeltgkd.db'
    table = 'gdeltgkg20192020'
    tosql(db, table, results)
    print("Storing done.")

    '''

    # ==============================================
    # We retrieve the data from GDELT week by week for 
    # the period between 01/07/2019 (Week 27) to 31/08/2020
    # (Week 36)
    # For Year 2019 
    #for i in range(27, 53):
    start = datetime.datetime.now()
    pulldata("2019", 27, 53)  
    end = datetime.datetime.now()
    print("Time to retrieve and filter data taken: ", end - start)

    # for Year 2020
    start = datetime.datetime.now()
    pulldata("2020", 1, 37)  
    end = datetime.datetime.now()
    print("Time to retrieve and filter data taken: ", end - start)

    # Time to retrieve and filter data taken:  1:28:32.245000
    # For the period of 2019 07 01 to 2020 09 06 (62weeks)
    # database memory: 910.9 MB
    # 1,903,536 rows
    '''
    '''
    Test results:
    =========================================
    Time to retrieve 7 days data:  0:13:09.531658
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1244551 entries, 0 to 1244550
Data columns (total 27 columns):
 #   Column                      Non-Null Count    Dtype  
---  ------                      --------------    -----  
 0   GKGRECORDID                 1244551 non-null  object 
 1   DATE                        1244540 non-null  float64
 2   SourceCollectionIdentifier  1244540 non-null  float64
 3   SourceCommonName            1244514 non-null  object 
 4   DocumentIdentifier          1244540 non-null  object 
 5   Counts                      206136 non-null   object 
 6   V2Counts                    206136 non-null   object 
 7   Themes                      1125480 non-null  object 
 8   V2Themes                    1125478 non-null  object 
 9   Locations                   959338 non-null   object 
 10  V2Locations                 957217 non-null   object 
 11  Persons                     970956 non-null   object 
 12  V2Persons                   959015 non-null   object 
 13  Organizations               947194 non-null   object 
 14  V2Organizations             913037 non-null   object 
 15  V2Tone                      1244540 non-null  object 
 16  Dates                       487392 non-null   object 
 17  GCAM                        1244540 non-null  object 
 18  SharingImage                966395 non-null   object 
 19  RelatedImages               83412 non-null    object 
 20  SocialImageEmbeds           76950 non-null    object 
 21  SocialVideoEmbeds           472380 non-null   object 
 22  Quotations                  272957 non-null   object 
 23  AllNames                    1172723 non-null  object 
 24  Amounts                     926804 non-null   object 
 25  TranslationInfo             0 non-null        float64
 26  Extras                      1066234 non-null  object 
dtypes: float64(3), object(24)
memory usage: 256.4+ MB
None
The number of rows returned:  1244551
'''

    

    







