# script
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
#import wquantiles as weighted
# suppress the SettingWithCopyWarning
pd.options.mode.chained_assignment = None

# nfl model code
class NFLModelBase:
	# initialize
	def __init__(self):
		pass
	# scrape schedule
	def scrape_nfl_schedule(self, int_year=2019):
		# get url
		r = requests.get(f'https://www.pro-football-reference.com/years/{int_year}/games.htm')
		# get content of page
		soup = BeautifulSoup(r.content, 'html.parser')
		# get all table rows
		table_rows = soup.find_all('tr')
		# instantiate empty list
		list_dict_row = []
		# for each row
		for a, row in enumerate(table_rows):
			# instantiate empty dictionary
			dict_row = {}
			# get td elements
			td = row.find_all('td')
			# may need logic in case td is empty list
			# get week
			str_week = row.find('th').text
			# try converting to int
			try:
				int_week = int(str_week)
			# if week is not able to be converted to int
			except:
				# logic
				if str_week == 'WildCard':
					int_week = 18
				elif str_week == 'Division':
					int_week = 19
				elif str_week == 'ConfChamp':
					int_week = 20
				elif str_week == 'SuperBowl':
					int_week = 21
				else:
					# skip iteration
					continue
			# save to dict_row
			dict_row['week'] = int_week
			# get winning team
			str_winning_team = td[3].find('a').text
			dict_row['winning_team'] = str_winning_team
			# get game location
			str_game_loc = td[4].text
			dict_row['game_loc'] = str_game_loc
			# get losing team
			str_losing_team = td[5].find('a').text
			dict_row['losing_team'] = str_losing_team
			# get winning team points
			int_winning_points = int(td[7].text)
			dict_row['winning_team_points'] = int_winning_points
			# get losing team points
			int_losing_team_points = int(td[8].text)
			dict_row['losing_team_points'] = int_losing_team_points
			# append row to list_dict_row
			list_dict_row.append(dict_row)
		# put into df
		df_schedule_results = pd.DataFrame(list_dict_row)
		# save to object
		self.df_schedule_results = df_schedule_results
		self.int_year = int_year
		# return self
		return self
	# prepare data
	def prepare_data(self):
		# empty list
		list_dict_row = []
		# iterate through rows
		for row in self.df_schedule_results.iterrows():
			# empty dict
			dict_row = {}
			# get series
			ser_row = row[1]
			# get game loc
			str_game_loc = ser_row['game_loc']
			# logic
			if str_game_loc == '@':
				str_home_team = ser_row['losing_team']
				str_away_team = ser_row['winning_team']
				int_home_points = ser_row['losing_team_points']
				int_away_points = ser_row['winning_team_points']
			elif str_game_loc == '':
				str_home_team = ser_row['winning_team']
				str_away_team = ser_row['losing_team']
				int_home_points = ser_row['winning_team_points']
				int_away_points = ser_row['losing_team_points']
			elif str_game_loc == 'N': # super bowl
				continue
			# put into dict
			dict_row['week'] = ser_row['week']
			dict_row['home_team'] = str_home_team
			dict_row['away_team'] = str_away_team
			dict_row['home_score'] = int_home_points
			dict_row['away_score'] = int_away_points
			# append
			list_dict_row.append(dict_row)
		# put into df
		df_prepped_data = pd.DataFrame(list_dict_row)
		# helper function to get winning team
		def get_winner(home_team, away_team, home_score, away_score):
			if home_score > away_score:
				return home_team
			elif home_score < away_score:
				return away_team
			else:
				return 'tie'
		# apply function
		df_prepped_data['winning_team'] = df_prepped_data.apply(lambda x: get_winner(home_team=x['home_team'], 
																			         away_team=x['away_team'], 
																					 home_score=x['home_score'], 
																					 away_score=x['away_score']), axis=1)
		# drop unplayed games
		df_prepped_data = df_prepped_data.dropna(subset=['home_score'])
		# make col for year
		df_prepped_data['year'] = self.int_year
		# save to object
		self.df_prepped_data = df_prepped_data
		# return
		return self
	# define helper function (could get errors here)
	def win_pct_helper(list_teams_unique, df_prepped_data, int_year):
		# empty list
		list_dict_row = []
		# iterate through teams
		for team in list_teams_unique:
			# empty dict
			dict_row = {}
			# subset to where home team or away team == team
			df_subset = df_prepped_data[(df_prepped_data['home_team'] == team) | (df_prepped_data['away_team'] == team)]
			# see how many times team is in winning_team
			int_n_wins = list(df_subset['winning_team']).count(team)
			# get number of games
			int_n_games = df_subset.shape[0]
			# get win pct
			flt_win_pct = int_n_wins / int_n_games
			# if we have zero win pct make it .01
			if flt_win_pct == 0:
				flt_win_pct = 0.01
			# put into dict_row
			dict_row['team'] = team
			dict_row['win_pct'] = flt_win_pct
			# append to list
			list_dict_row.append(dict_row)
		# put into df
		df_win_pct = pd.DataFrame(list_dict_row)
		# make col for year
		df_win_pct['year'] = int_year
		# return
		return df_win_pct
	# get winning oct for year of home team
	def get_winning_pct_home(self, int_year_home=2019):
		# subset to int_year_home
		df_prepped_data_year = self.df_prepped_data[self.df_prepped_data['year']==int_year_home]
		# get all teams for int_year_home
		list_all_teams_year = list(df_prepped_data_year['home_team']) + list(df_prepped_data_year['away_team'])
		# rm dups
		list_teams_unique = list(dict.fromkeys(list_all_teams_year))
		# use helper
		df_win_pct_home = win_pct_helper(list_teams_unique=list_teams_unique, 
										 df_prepped_data=df_prepped_data_year, 
										 int_year=int_year_home)
		# save to object
		self.int_year_home = int_year_home
		self.df_win_pct_home = df_win_pct_home
		# return
		return self
	# get winning pct for each team for weighting later
	def get_winning_pct_away(self, int_year_away=2019):
		# subset to int_year_away
		df_prepped_data_year = self.df_prepped_data[self.df_prepped_data['year']==int_year_away]
		# get all teams for int_year_away
		list_all_teams_year = list(df_prepped_data_year['home_team']) + list(df_prepped_data_year['away_team'])
		# rm dups
		list_teams_unique = list(dict.fromkeys(list_all_teams_year))
		# use helper
		df_win_pct_away = win_pct_helper(list_teams_unique=list_teams_unique, 
										 df_prepped_data=df_prepped_data_year, 
										 int_year=int_year_away)
		# save to object
		self.int_year_away = int_year_away
		self.df_win_pct_away = df_win_pct_away
		# return
		return self
	# get predicted points scored by home team when they are home
	def get_points_scored_by_home_team(self, str_home_team='Denver Broncos',
										     int_last_n_games=4,
											 bool_weight_opp=True,
											 int_n_simulations=1000):
		# subset to year
		df_prepped_data_year = self.df_prepped_data[self.df_prepped_data['year']==self.int_year_home]
		# get all the games where the home_team was home
		df_prepped_data_year_home = df_prepped_data_year[(df_prepped_data_year['home_team'] == str_home_team)]

		# save to object at this stage so we dont have to subset again later
		self.df_prepped_data_year_home_copy = df_prepped_data_year_home.copy()

		# get n_rows
		int_n_rows = df_prepped_data_year_home.shape[0]
		# logic to prevent errors when subsetting games
		if int_last_n_games < int_n_rows:
			df_prepped_data_year_home = df_prepped_data_year_home.iloc[-int_last_n_games:]
		else:
			pass
		# if weighting each game by opponent win pct
		if bool_weight_opp:
			# merge with df_win_pct to get opponent win %
			df_prepped_data_year_home = pd.merge(left=df_prepped_data_year_home, 
							   					 right=self.df_win_pct_home, 
											     left_on='away_team', 
											     right_on='team', 
											     how='left')
			# save weights
			list_weights = list(df_prepped_data_year_home['win_pct'])

		# logic to catch potential errors
		if (np.sum(list_weights) == 0) or (not bool_weight_opp):
			# weight everything the same
			list_weights = [1 for x in df_prepped_data_year_home['win_pct']]
		
		# get median
		flt_home_score_avg = np.average(df_prepped_data_year_home['home_score'], weights=list_weights)
		# get random values from poisson distribution
		list_pred_home_score = list(np.random.poisson(flt_home_score_avg, int_n_simulations))
		# save to object
		self.str_home_team = str_home_team
		self.int_n_simulations = int_n_simulations
		self.list_pred_home_score = list_pred_home_score
		# return
		return self
	# get predicted points scored by away team when they are away
	def get_points_scored_by_away_team(self, str_away_team='Denver Broncos',
										     int_last_n_games=4,
											 bool_weight_opp=True):
		# subset to year
		df_prepped_data_year = self.df_prepped_data[self.df_prepped_data['year']==self.int_year_away]
		# get all the games where the away team was away
		df_prepped_data_year_away = df_prepped_data_year[(df_prepped_data_year['away_team'] == str_away_team)]

		# save to object at this stage so we dont have to subset again
		self.df_prepped_data_year_away_copy = df_prepped_data_year_away.copy()

		# get n_rows
		int_n_rows = df_prepped_data_year_away.shape[0]
		# logic to prevent errors when subsetting games
		if int_last_n_games < int_n_rows:
			df_prepped_data_year_away = df_prepped_data_year_away.iloc[-int_last_n_games:]
		else:
			pass
		# if weighting each game by opponent win pct
		if bool_weight_opp:
			# merge with df_win_pct to get opponent win %
			df_prepped_data_year_away = pd.merge(left=df_prepped_data_year_away, 
											     right=self.df_win_pct_away, 
											     left_on='home_team', 
											     right_on='team', 
											     how='left')
			# save weights
			list_weights = list(df_prepped_data_year_away['win_pct'])

		# logic to catch potential errors
		if (np.sum(list_weights) == 0) or (not bool_weight_opp):
			# weight everything the same
			list_weights = [1 for x in df_prepped_data_year_away['win_pct']]
		
		# get median
		flt_away_score_avg = np.average(df_prepped_data_year_away['away_score'], weights=list_weights)
		# get random values from poisson distribution
		list_pred_away_score = list(np.random.poisson(flt_away_score_avg, self.int_n_simulations))
		# save to object
		self.str_away_team = str_away_team
		self.list_pred_away_score = list_pred_away_score
		# return
		return self
	# get predicted points allowed by home team
	def get_points_allowed_by_home_team(self, int_last_n_games=4,
									          bool_weight_opp=True):
		# get all the games where the home_team was home (df_prepped_data_year_home_copy)
		df_home = self.df_prepped_data_year_home_copy.copy()
		# get n_rows
		int_n_rows = df_home.shape[0]
		# logic to prevent errors when subsetting games
		if int_last_n_games < int_n_rows:
			df_home = df_home.iloc[-int_last_n_games:]
		else:
			pass
		# if weighting each game by opponent win pct
		if bool_weight_opp:
			# merge with df_win_pct to get opponent win %
			df_home = pd.merge(left=df_home, 
							   right=self.df_win_pct_home, 
							   left_on='away_team', 
							   right_on='team', 
							   how='left')
			# save weights
			list_weights = list(df_home['win_pct'])

		# logic to catch potential errors
		if (np.sum(list_weights) == 0) or (not bool_weight_opp):
			# weight everything the same
			list_weights = [1 for x in list_weights]
		
		# get median
		flt_home_score_allowed_avg = np.average(df_home['away_score'], weights=list_weights)
		# get random values from poisson distribution
		list_pred_home_score_allowed = list(np.random.poisson(flt_home_score_allowed_avg, self.int_n_simulations))
		# save to object
		self.list_pred_home_score_allowed = list_pred_home_score_allowed
		# return
		return self
	# get predicted points allowed by away team
	def get_points_allowed_by_away_team(self, int_last_n_games=4,
									          bool_weight_opp=True):
		# get all the games where the away team was away
		df_away = self.df_prepped_data_year_away_copy.copy()
		# get n_rows
		int_n_rows = df_away.shape[0]
		# logic to prevent errors when subsetting games
		if int_last_n_games < int_n_rows:
			df_away = df_away.iloc[-int_last_n_games:]
		else:
			pass
		# if weighting each game by opponent win pct
		if bool_weight_opp:
			# merge with df_win_pct to get opponent win %
			df_away = pd.merge(left=df_away, 
							   right=self.df_win_pct_away, 
							   left_on='home_team', 
							   right_on='team', 
							   how='left')
			# save weights
			list_weights = list(df_away['win_pct'])

		# logic to catch potential errors
		if (np.sum(list_weights) == 0) or (not bool_weight_opp):
			# weight everything the same
			list_weights = [1 for x in list_weights]
		
		# get median
		flt_away_score_allowed_avg = np.average(df_away['home_score'], weights=list_weights)
		# get random values from poisson distribution
		list_pred_away_score_allowed = list(np.random.poisson(flt_away_score_allowed_avg, self.int_n_simulations))
		# save to object
		self.list_pred_away_score_allowed = list_pred_away_score_allowed
		# return
		return self
	# predict outcome
	def predict_outcome(self, bool_weight_opp=True):
		# put predictions into a df
		df_predictions = pd.DataFrame({'pred_points_scored_by_home': self.list_pred_home_score,
									   'pred_points_scored_by_away': self.list_pred_away_score,
									   'pred_points_allowed_by_home': self.list_pred_home_score_allowed,
									   'pred_points_allowed_by_away': self.list_pred_away_score_allowed})
		
		# if weighting
		if bool_weight_opp:
			# get win pct for home
			flt_win_pct_home = self.df_win_pct_home[self.df_win_pct_home['team']==self.str_home_team]['win_pct'].iloc[0]
			# get win pct for away
			flt_win_pct_away = self.df_win_pct_away[self.df_win_pct_away['team']==self.str_away_team]['win_pct'].iloc[0]
			# put into list
			list_weights = [flt_win_pct_home, flt_win_pct_away]
		else:
			list_weights = [1,1]
		
		# home score prediction
		df_predictions['pred_home_score'] = df_predictions.apply(lambda x: np.average([x['pred_points_scored_by_home'], x['pred_points_allowed_by_away']], weights=list_weights), axis=1)
		# away score prediction
		df_predictions['pred_away_score'] = df_predictions.apply(lambda x: np.average([x['pred_points_allowed_by_home'], x['pred_points_scored_by_away']], weights=list_weights), axis=1)
		# creat a col 1/0 to deal with ties
		df_predictions['rand_binomial'] = np.random.binomial(1, 0.5, self.int_n_simulations)
		
		# helper function for determining if home team won
		def did_home_win(pred_home_score, pred_away_score, rand_binomial):
			if pred_home_score > pred_away_score:
				return 1
			elif pred_home_score < pred_away_score:
				return 0
			elif pred_home_score == pred_away_score:
				return rand_binomial
		
		# apply function
		int_n_home_wins = np.sum(df_predictions.apply(lambda x: did_home_win(pred_home_score=x['pred_home_score'], 
																	         pred_away_score=x['pred_away_score'], 
																			 rand_binomial=x['rand_binomial']), axis=1))
		# get the proportion of games where the home team is > away team
		flt_prop_home_win = int_n_home_wins / df_predictions.shape[0]
		
		# get mean home score
		flt_mean_home_score = round(np.mean(df_predictions['pred_home_score']), 3)
		# get mean away score
		flt_mean_away_score = round(np.mean(df_predictions['pred_away_score']), 3)
		
		# get winning team
		if flt_prop_home_win >= .5:
			str_winning_team = self.str_home_team
		else:
			str_winning_team = self.str_away_team

		# create a dictionary to return objects
		dict_results = {'mean_home_pts': flt_mean_home_score,
						'mean_away_pts': flt_mean_away_score,
						'prob_home_win': flt_prop_home_win,
						'winning_team': str_winning_team}
		# save to object
		self.df_predictions = df_predictions
		self.dict_results = dict_results
		# return object
		return self