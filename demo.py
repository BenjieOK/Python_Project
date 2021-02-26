import pandas as pd
import numpy as np
import csv

fruits = ['oranges', 'apples', 'mangoes']
# data = pd.Series([1, 2, 3], index=fruits)
# print(data.index)

# fury = ['oranges', 'grapes', 'apples', 'pawpaw']
# sample = pd.Series([12, 34, 45, 65], index=fury)
# sample.plot()
# print(sample.apply(np.sin), '\n')
# print(sample.apply(lambda x: x if x>15 else 0))
# print(sample.index)

cities = {
    'name': [
        'London', 'Accra', 'Lome', 'Budapest', 'Berlin', 'Abidjan',
        'Paris', 'Rome', 'Rio de Janeiro', 'Tokyo', 'Abuja', 'Washington'
    ],
    'population': [
        44589033, 12847539, 1234553, 23424232, 897797983, 123234322,
        98231342, 12324233, 9992333, 82323234, 243232432, 9328283823
    ],
    'country': [
        'England', 'Ghana', 'Togo', 'Hungary', 'Germany', 'Ivory Coast',
        'France', 'Italy', 'Brazil', 'Japan', 'Nigeria', 'USA'
    ]
}

city_frame = pd.DataFrame(cities, columns=['country', 'name', 'population'])
# city_frame.set_index('country', inplace=True)
# print(city_frame)
# print(city_frame.pivot(columns='name'))
# weight = np.random.random(5)
# print(weight)
# summation = np.sum(weight)
# print(weight/summation)

# users = pd.read_csv('500-us-users.csv')

with open('data/500-us-users.csv', newline='') as user_file:
    data = csv.DictReader(user_file, delimiter=',')
    users = np.empty((0, 9))

    for row in data:
        hommie = np.array([
            [row['first_name'], row['last_name'], row['address'],
             row['city'], row['county'], row['state'],
             row['zip'], row['phone1'], row['phone2']]
            ])
        users = np.append(users, hommie, axis=0)
print(users)
