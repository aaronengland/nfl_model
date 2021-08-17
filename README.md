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

# instantiate constant year
int_year = 2019

# scrape and prep
cls_nfl_model.scrape_and_prep(int_year=int_year)

# get win percentages
cls_nfl_model.get_winning_pct(int_year_home=int_year, int_year_away=int_year)

"""
Note: 

If wanting multi-year data, iterate through a range of years calling the scrape_and_prep method and save the output to a pandas data frame object.
Assign this data frame to cls_nfl_model.df_prepped_data.

Example:

import pandas as pd

# empty df
df_prepped_data_all = pd.DataFrame()
# iterate through seasons (starting 1985)
for int_year in range(1985, 2020+1):
	# scrape and prep
	cls_nfl_model.scrape_and_prep(int_year=int_year)
	# get the data
	df_prepped_data = cls_nfl_model.df_prepped_data
	# append to df_schedule
	df_prepped_data_all = df_prepped_data_all.append(df_prepped_data)

# save df_prepped_data_all into cls_nfl_model
cls_nfl_model.df_prepped_data = df_prepped_data_all

# get win percentages
cls_nfl_model.get_winning_pct(int_year_home=1985, int_year_away=1987)
"""

# generate prediction
cls_nfl_model.predict_from_matchup(str_home_team='Chicago Bears',
				   str_away_team='Miami Dolphins',
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
{'mean_home_pts': 20.817, 
 'mean_away_pts': 7.068, 
 'prob_home_win': 1.0, 
 'winning_team': 'Chicago Bears'}
```