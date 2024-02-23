from configuration.configuration import get_database_airqualityserbia
import datetime
import matplotlib.pyplot as plt
import pandas as pd

collection = get_database_airqualityserbia()

def average_value_per_each_polutant_per_date():
    target_date = "2023-12-24"

    start_datetime = pd.to_datetime(f"{target_date}T00:00:00+00:00")
    end_datetime = pd.to_datetime(f"{target_date}T23:59:59+00:00")

    query = {
          "date.utc": {"$gte": f"{target_date}T00:00:00+00:00", "$lt": f"{target_date}T23:59:59+00:00"}
    }
    cursor = collection.find(query)
    df = pd.DataFrame(cursor)
    df['date'] = pd.to_datetime(df['date'].apply(lambda x: x['local']))

    prosecne_vrednosti = df.groupby(['date', 'parameter'])['value'].mean().reset_index()

    plt.figure(figsize=(12, 6))

    for polutant in df['parameter'].unique():
        if polutant != 'co':
            podaci_polutant = prosecne_vrednosti[prosecne_vrednosti['parameter'] == polutant]
            plt.plot(podaci_polutant['date'], podaci_polutant['value'], label=polutant)

    plt.title('Average value of polutant for 24.12.2023.')
    plt.xlabel('Date')
    plt.ylabel(f'Average value ({df["unit"].unique()[0]})')
    plt.legend()
    plt.show()