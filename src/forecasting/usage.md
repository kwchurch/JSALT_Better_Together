## Environment Variables

Before running the scripts, ensure the following environment variables are set:

```bash
# Path to JSALTdir with required subdirectories
export JSALTdir=/path/to/JSALTdir

# Path to walkdir with walk files in the specified subdirectories
export walkdir=/path/to/dir/with/walkfiles
```

## Script Usage

### Predicting_from_Random_Walks.py

This script performs forecasting using random walks and various models. It predicts for all splits and handles missing values based on specified models.

#### Usage Examples:

   
```bash
#1.Predict with ProNE model; if missing values, sample from the prior:
python Predicting_from_Random_Walks.py -o prone_forecast_prior -t 1 -m prone_prior
#2. Predict with ProNE model; if missing values, use Specter1 model:
python Predicting_from_Random_Walks.py -o prone_forecast_specter1 -t 1 -m prone_specter1
#3. Predict with Specter1 model; if missing values, sample from the prior:
python Predicting_from_Random_Walks.py -o specter1_forecast_prior -t 1 -m specter1_prior   
 ```

### hybrid_plots.py

This script generates plots comparing forecasting results for different models across ProNE models with different max bins. Plots will written to the floder specified with -o:

```bash
python Random_Walks_Hybrid_Plots.py -p prone_forecast_prior -s specter1_forecast_prior -ps prone_forecast_specter1 -o comparing_forecasting_timesteps
```

### Random_Walks_Plot.py

This script creates plots specifically for ProNE-only forecasting. Plots will written to the floder specified with -o:
```bash
python Random_Walks_Plot.py -i prone_forecast_prior -o prone_prior_plots/
```