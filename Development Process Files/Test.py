import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

aq_daily_max_mean_and_population = pd.read_csv('aq_daily_max_mean_and_population.csv')

sns.set(style="ticks", color_codes=True)
g = sns.pairplot(aq_daily_max_mean_and_population)

plt.show()
