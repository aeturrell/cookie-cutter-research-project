#!/usr/bin/env python
"""
This script performs the dynamic factor model analysis
"""
import os
import pandas as pd
import yaml
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import numpy as np
import statsmodels.api as sm

# Get config file
config = {k: v for d in yaml.load(open('config.yaml')) for k, v in d.items()}
mpl.rcParams.update(mpl.rcParamsDefault)  # VS Code plots not black
plt.style.use(config['viz'])
# Load data and format datetime
df = pd.read_csv(os.path.join(config['data']['clnFilePath'], 'ts_data.csv'),
                 index_col=0,
                 parse_dates=True)

# Change format to one variable per column
df = df.reset_index().pivot(index='date', columns='value_name')['value']

# From here, follow Chad Fulton's dynamic factor tutorial:
# http://www.chadfulton.com/fulton_statsmodels_2017/sections/6-out-of-the-box_models.html
# Preliminary plotting of time series - save to scratch
(df.plot(subplots=True))
plt.savefig(os.path.join(config['data']['outPathScratch'], 'ts_plots.eps'))
plt.show()

# pct change series and normalise
for col in df.columns:
    df[col] = df[col].pct_change()*100
    df[col] = (df[col]-df[col].mean())/df[col].std()
# Clean across rows
df = df.dropna(how='any', axis=0)

# Look at correlations
fig, ax = plt.subplots()
sns.heatmap(df.corr(),
            annot=True, fmt="1.1f",
            cbar_kws=dict(ticks=np.linspace(-1, 1, 5)),
            cmap="PRGn_r", linewidths=.2, ax=ax, center=0,
            vmin=-1, vmax=1,
            annot_kws={"size": 15})
ax.set_xlabel('')
ax.set_ylabel('')
plt.tight_layout()
plt.savefig(os.path.join(config['data']['outPathScratch'], 'hmap.eps'))
plt.show()

# Create model
mod = sm.tsa.DynamicFactor(df,
                           k_factors=1,
                           factor_order=2,
                           error_order=2)
res = mod.fit()
print(res.summary(separate_params=False))
# Write latex table of model results to output
output_dir = os.path.join(config['data']['outPath'], 'DFM_model.tex')
with open(output_dir, 'w') as outfile:
    outfile.write(res.summary(separate_params=False).as_latex())

# Plot the factor - not for final so save to scratch
fig, ax = plt.subplots()
ax.plot(df.index._mpl_repr(), res.factors.filtered[0], label='Factor')
ax.set_title('Factor', loc='right')
plt.savefig(os.path.join(config['data']['outPathScratch'], 'factor_ts.eps'))
plt.show()

# Plot irfs
dfm_irfs = res.impulse_responses(12, impulse=0, orthogonalized=True)*100
fig, ax = plt.subplots()
dfm_irfs.plot(marker='o', ax=ax)
ax.set_ylabel('%')
ax.set_title('Impulse response to 1$\sigma$ change to factor', loc='right')
ax.set_xlabel('Months')
plt.tight_layout()
plt.savefig(os.path.join(config['data']['outPath'], 'df_irfs.eps'))
plt.show()

# Plot forecasts
fig, axes = plt.subplots(5, sharex=True, sharey=True)
for j in range(len(df.columns)):
    axes[j].plot(df.index._mpl_repr(),
                 res.forecasts[j],
                 color='k',
                 linestyle='-.',
                 lw=1.5)
    axes[j].plot(df.index, df.iloc[:, j],
                 color='coral',
                 linestyle='-',
                 lw=1.)
    axes[j].set_title(df.columns[j], loc='right')
plt.subplots_adjust(hspace=0.6)
plt.savefig(os.path.join(config['data']['outPath'], 'fcasts.eps'))
plt.show()
