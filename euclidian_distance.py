import pandas as pd
import math


df = pd.read_csv('filtered/csv/data.csv')

df_miasta = pd.read_csv('filtered/csv/cities_all.csv')


def euclidian(row):
	# x2 - x1 + 
	distance_arr = []
	city_ = None
	for e, city in enumerate(df_miasta.values):
		d = math.sqrt((row[0] - city[0])**2 + (row[1] - city[1])**2)
		
		if e > 0 and d > buff: 
			# print("Current distance: {} is closest. new distance: {}".format(buff, d))
			pass

		else:
			buff = d
			city_ = city

	print('Returning city: {} with distance: {}'.format(city_, buff))
	return city_


near_arr = []
for en, i in enumerate(df.values):
	print('Checking knn for: {}'.format(i))
	nearest_city = euclidian(i)
	near_arr.append(nearest_city[2])
	print('Done {}/{}'.format(en, len(df.values)))

df['nearest_city'] = near_arr

df.to_csv('filtered/csv/clasificated_spots.csv')

