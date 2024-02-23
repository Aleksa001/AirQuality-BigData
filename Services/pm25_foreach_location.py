from configuration.configuration import get_database_airqualityserbia
import datetime
import matplotlib.pyplot as plt

collection = get_database_airqualityserbia()

def pm25_foreach_location():
    query = [
        {
            '$match': {
                'parameter': 'pm25'
            }
        },
        {
            '$group': {
                '_id': "$location",
                'avg_pm25': { '$avg': "$value"}
            }
        },
        {
            '$project': {
                '_id': 0,
                'location': "$_id",
                'avg_pm25': 1
            }
        },
        {
            '$sort': {
                'location': 1  # 1 za rastući redosled (ascending)
            }
        }
        ]
    results = collection.aggregate(query)
    data = list(results)

    locations = [entry['location'] for entry in data]
    avg_pm25_values = [entry['avg_pm25'] for entry in data]

    color_ranges = [(0, 15), (15.01, 30), (30.01, 55), (55.01, 110)]

    colors = []
    for value in avg_pm25_values:
        if value <= color_ranges[0][1]:
            colors.append('green')
        elif color_ranges[1][0] < value <= color_ranges[1][1]:
            colors.append('blue')
        elif color_ranges[2][0] < value <= color_ranges[2][1]:
            colors.append('yellow')
        elif color_ranges[3][0] < value <= color_ranges[3][1]:
            colors.append('red')
        else:
            colors.append('purple')

    plt.figure(figsize=(14, 8))
    bars = plt.bar(locations, avg_pm25_values, color=colors)
    plt.title('Average value of pm25 bz location')
    plt.xlabel('Location')
    plt.ylabel('Average value of pm25 (µg/m³)')
    plt.xticks(rotation=45, ha='right')

    # Dodavanje legendi za boje
    legend_labels = ['0-15', '15.01-30', '30.01-55', '55.01-110', '>110']
    legend_colors = ['green', 'blue', 'yellow', 'red', 'purple']
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', label=label,
                                 markerfacecolor=color, markersize=10) for label, color in
                      zip(legend_labels, legend_colors)]
    plt.legend(handles=legend_handles)

    plt.tight_layout()
    plt.show()
