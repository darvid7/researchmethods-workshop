import matplotlib.pyplot as plt
import csv
import scipy.stats
import numpy as np
DATAPATH = 'tennis_data_updated.csv'

def parse_tennis_players(file_path):
	""" Returns an array of OrderedDicts for male and female tennis players."""
	males = []
	females = []
	fieldnames = [
		'ranking', 'country', 'player', 'age', 
		'points', 'tournplayed', 'born', 'weight', 
		'height', 'hand', 'gender'
	]
	with open(file_path,'r') as csvfile:
		reader = csv.DictReader(csvfile, fieldnames=fieldnames)
		
		for row in reader:
			if row['gender'].upper() == "M":
				males.append(row)
			elif row['gender'].upper() == "F":
				females.append(row)
	return males, females


def make_graph(x_data, y_data, y_data_ticks, x_label, y_label, group, plotline=True, extra_y_label=''):
	plt.yticks(y_data_ticks)
	if plotline:
		fit = np.polyfit(x_data, y_data, deg=1)
		correlation = np.corrcoef(x_data, y_data)[0,1]
		r2 = correlation**2
		print("numpy r^2:" + str(r2))

		slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x_data, y_data)
		print("scipy r^2: " + str(r_value**2))
		plt.plot(np.array(x_data), fit[0] * np.array(x_data) + fit[1], color='red')
	plt.scatter(x_data, y_data)
	plt.xlabel(x_label)
	plt.ylabel(y_label + extra_y_label)
	plt.suptitle('%s %s vs %s\nr^2 = %s' % (group, x_label, y_label, r2) if plotline \
		else '%s %s vs %s' %(group, x_label, y_label))
	name = '%s_%s_vs_%s.png' % (group, x_label, y_label)
	print(name)
	plt.savefig(name)
	plt.clf()

invalid = ('', ' ', 0, '0')

males, females = parse_tennis_players(DATAPATH)

males = [m for m in males if m['height'] not in invalid and m['ranking'] not in invalid and 140 <= int(m['height']) <= 300]
 
females = [f for f in females if f['height'] not in invalid and f['ranking'] not in invalid and 140 <= int(f['height']) <= 300]

# RANK vs HEIGHT

# males

male_ranking_height = [(int(od['ranking']), int(od['height'])) for od in males]
male_heights = [x[1] for x in male_ranking_height]
male_ranks = [x[0] for x in male_ranking_height]

make_graph(male_heights, male_ranks, [0, 100, 200, 300, 400, 500], 'Height', 'Rank', 'Male')

# females

female_ranking_height = [(int(od['ranking']), int(od['height'])) for od in females]

female_heights = [x[1] for x in female_ranking_height]
female_ranks = [x[0] for x in female_ranking_height]

make_graph(female_heights, female_ranks, [0, 100, 200, 300, 400, 500], 'Height', 'Rank', 'Female')

# combined 

combined_ranking_height = male_ranking_height + female_ranking_height

combined_heights = [x[1] for x in combined_ranking_height]
combined_ranks = [x[0] for x in combined_ranking_height]

make_graph(combined_heights, combined_ranks, [0, 100, 200, 300, 400, 500], 'Height', 'Rank', 'Combined (male & female)')

# HAND vs HAND

LEFT = 0
RIGHT = 1

handmappings = { "L": LEFT, "R": RIGHT}

# male

male_ranking_hands = [(int(od['ranking']), handmappings[od['hand'].upper()]) for od in males if od['hand'].upper() in ['L', 'R']]
male_hands = [x[1] for x in male_ranking_hands]
male_ranks = [x[0] for x in male_ranking_hands]

make_graph(male_ranks, male_hands, [0, 1], 'Rank', 'Hand', 'Male', plotline=False, extra_y_label=" (0=L, 1=R)")

# female

female_ranking_hands = [(int(od['ranking']), handmappings[od['hand'].upper()]) for od in females if od['hand'].upper() in ['L', 'R']]
female_hands = [x[1] for x in female_ranking_hands]
female_ranks = [x[0] for x in female_ranking_hands]

make_graph(female_ranks, female_hands, [0, 1], 'Rank', 'Hand', 'Female', plotline=False, extra_y_label=" (0=L, 1=R)")

# combined

combined_ranking_hands = males + females
combined_ranking_hands = [(int(od['ranking']), handmappings[od['hand'].upper()]) for od in combined_ranking_hands if od['hand'].upper() in ['L', 'R']]

combined_hands = [x[1] for x in combined_ranking_hands]
combined_ranks = [x[0] for x in combined_ranking_hands]

make_graph(combined_ranks, combined_hands, [0, 1], 'Rank', 'Hand', 'Combined (male & female)', plotline=False, extra_y_label=" (0=L, 1=R)")
