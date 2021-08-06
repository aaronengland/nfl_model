# script - apply
from script_combined import NFLModelCombined

# generate prediction
cls_nfl_model = NFLModelCombined()
cls_nfl_model.scrape_and_prep(int_year=2019)
cls_nfl_model.predict_from_matchup(str_home_team='Denver Broncos',
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
						  bool_weight_opp_final=True)

print(cls_nfl_model.dict_results)

