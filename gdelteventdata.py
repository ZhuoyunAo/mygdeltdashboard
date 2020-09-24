import pandas as pd
import sqlite3
import datetime
import time

from re import search

import gdelt
import platform
import multiprocessing

platform.platform()
multiprocessing.cpu_count()

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
    results = gd.Search(daterange,table='events',coverage=True)

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

    # ==============================================
    # Use the gdeltPyR package to access gdelt data
    gd = gdelt.gdelt(version=2)

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
    sd = '2019 8 1'
    ed = '2019 8 7'
    daterange = [sd,ed]
    
    print("Retrieve event data from GDELT for date range frome ", sd, " to ", ed)
    print(".........")
    start = datetime.datetime.now()
    results = retrieve(daterange)
    end = datetime.datetime.now()

    print("Time to download 7 days data: ", end - start)

    # The number of results we returned
    print(results.info())
    print(results.head())

    # ==================================================
    # Store data into a database
    db = 'data/gdeltdata_aus'
    table = 'gdelt2019_2020'
    tosql(db, table, results)

    print("Done!")
    '''
    '''
    # ===========================================
    # Accessing data stored in SQLite using Python and Pandas
    db = 'data/gdeltdata_aus'
    query = "SELECT * from gdelt2019_2020"
    df = query_db(db, query)
    print("Number of rows returned: ", len(df))
    print(df.head())
    '''

    







