from gevent import monkey
monkey.patch_all()
import gevent
import pandas as pd
import numpy as np
from worker import driver_setup, bulk_scrapper
from connection import databaseCRUD

INSTANCE = 5

def scrapping():
    try:
        df = pd.read_csv('minified_data.csv')

        df_split = np.array_split(df, INSTANCE)

        drivers = [driver_setup() for _ in range(INSTANCE)]
        threads = [gevent.spawn(bulk_scrapper, data, driver) for data,driver in zip(df_split, drivers)]
        gevent.joinall(threads)

        results = []
        for thread in threads:
            results.extend(thread.value)

        with databaseCRUD.DatabaseObject() as dbo:
            for result in results:
                dbo.insertOne(result)

    except Exception as e:
        print(e)

    finally:
        print('Done')

if __name__ == '__main__':
    scrapping()