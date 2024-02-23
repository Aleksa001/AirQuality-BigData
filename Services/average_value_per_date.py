from configuration.configuration import get_database_airqualityserbia
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.arima.model import ARIMA

collection = get_database_airqualityserbia()


def average_value_per_date():
    cursor = collection.find({"parameter": "pm25"})

    df = pd.DataFrame(list(cursor))

    df['value'] = pd.to_numeric(df['value'], errors='coerce')

    df['date'] = pd.to_datetime(
        df['date'].apply(lambda x: x['utc'])).dt.date
    df.set_index('date', inplace=True)

    df = df.dropna(subset=['value'])

    result = df.groupby('date')['value'].agg(avg_value='mean').reset_index()

    colors = []
    for value in result['avg_value']:
        if 0 <= value <= 15:
            colors.append('green')
        elif 15.01 <= value <= 30:
            colors.append('blue')
        elif 30.01 <= value <= 55:
            colors.append('yellow')
        elif 55.01 <= value <= 110:
            colors.append('red')
        else:
            colors.append('purple')


    plt.subplots_adjust(hspace=1.5)
    plt.subplot(2, 1, 1)

    plt.bar(result['date'], result['avg_value'], color=colors)
    plt.title('Average value of parameter pm25 per date')
    plt.xlabel('Date')
    plt.ylabel('Average value')

    plt.xticks(result['date'], rotation=45, ha='right')

    model = ARIMA(result['avg_value'], order=(5, 1, 3))
    fit_model = model.fit()

    forecast_steps = 30
    forecast = fit_model.get_forecast(steps=forecast_steps)

    plt.subplot(2, 1, 2)
    plt.plot(result['date'], result['avg_value'], label='Historical data')
    plt.plot(pd.date_range(start=result['date'].max(), periods=forecast_steps + 1, freq='D')[1:],
             forecast.predicted_mean, label='Prediction')
    plt.title('Predict average bz date')
    plt.xlabel('Date')
    plt.ylabel('Average value')
    plt.legend()

    plt.show()
