# nfl_model

To install:

```
pip install git+https://github.com/aaronengland/nfl_model.git
```

To update:

```
pip install git+https://github.com/aaronengland/nfl_model.git -U
```

To use:

```
from nfl_model.script_combined import NFLModelCombined

# instantiate class
cls_nfl_model = NFLModelCombined()

# scrape and prep
cls_nfl_model.scrape_and_prep(int_year=2019)

# generate prediction
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

# view prediction
print(cls_nfl_model.dict_results)
```

Results look like:

```
{'mean_home_pts': 23.777, 
 'mean_away_pts': 17.956, 
 'prob_home_win': 0.886, 
 'winning_team': 'Denver Broncos'}
```