import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

aq_daily_max_mean_and_population = pd.read_csv('aq_daily_max_mean_and_population.csv')

sns.set(style="ticks", color_codes=True)
g = sns.pairplot(aq_daily_max_mean_and_population)

plt.show()

site_total_average_max = pd.read_csv("site_total_average_max.csv")
h = sns.relplot(x="location", y="site max mean", data=site_total_average_max)
h.set(ylabel='Daily Max PM2.5 (Mean μg/m3)')
h.set(xlabel=None)
h.set(xticklabels=[])
plt.show()
