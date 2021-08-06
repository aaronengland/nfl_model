# script - combined
from .script_base import NFLModelBase

# new class with combined methods
class NFLModelCombined(NFLModelBase):
	# make a function that scrapes and preps
	def scrape_and_prep(self, int_year=2019):
		# scrape
		self.scrape_nfl_schedule(int_year=int_year)
		# prepare
		self.prepare_data()
		# get winning pct
		self.get_winning_pct()
		# return self
		return self
	# make a function that predicts a matchup
	def predict_from_matchup(self, str_home_team='Denver Broncos',
						           str_away_team='Cleveland Browns',
								   int_n_simulations=1000,
						           int_last_n_games_pts_for_home=4,
								   int_last_n_games_pts_for_away=4,
								   int_last_n_games_pts_allow_home=4,
								   int_last_n_games_pts_allow_away=4,
								   bool_weight_opp_pts_for_home=True,
								   bool_weight_opp_pts_for_away=True,
								   bool_weight_opp_pts_allow_home=True,
								   bool_weight_opp_pts_allow_away=True,
								   bool_weight_opp_final=True):
		# get points scored by home team
		self.get_points_scored_by_home_team(str_home_team=str_home_team,
										    int_last_n_games=int_last_n_games_pts_for_home,
											bool_weight_opp=bool_weight_opp_pts_for_home,
											int_n_simulations=int_n_simulations)
		# get points scored by away team
		self.get_points_scored_by_away_team(str_away_team=str_away_team,
										    int_last_n_games=int_last_n_games_pts_for_away,
											bool_weight_opp=bool_weight_opp_pts_for_away)
		# get points allowed by home team
		self.get_points_allowed_by_home_team(int_last_n_games=int_last_n_games_pts_allow_home,
									         bool_weight_opp=bool_weight_opp_pts_allow_home)
		# get points allowed by away team
		self.get_points_allowed_by_away_team(int_last_n_games=int_last_n_games_pts_allow_away,
									         bool_weight_opp=bool_weight_opp_pts_allow_away)
		# predict
		self.predict_outcome(bool_weight_opp=bool_weight_opp_final)
		# return
		return self




