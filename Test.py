import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import webbrowser
from tkinter import *

df_read = pd.read_csv('aq_historical_data.csv')

df = df_read.copy()
df['date'] = pd.to_datetime(df['Date and Time'])
df = df[df['Site'] == "EPA-25"]
df = df.drop(columns=['Unnamed: 0', 'Site', 'PM10', 'SO2', 'Date and Time'])
df = df.dropna()

df_site = df_read['Site']
print(df_site)


OPTIONS = ["Jan",
           "Feb",
           "Mar"] #etc

master = Tk()

variable = StringVar(master)
variable.set(OPTIONS[0]) # default value

w = OptionMenu(master, variable, *OPTIONS)
w.pack()


def ok():
    print("value is:" + variable.get())
    master.destroy()


button = Button(master, text="OK", command=ok)
button.pack()

mainloop()


# Define xticklabels
day_of_week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']


# Creating graphs of pollutant concentrations by hour, month and day of week
fig, axes = plt.subplots(1, 3, sharex=False, figsize=(18, 5))  # creating subplots, side by side
sns.set_style('whitegrid')

# concentration vs hour
axes[0] = sns.lineplot(ax=axes[0],
                       data=df,
                    x=df['date'].dt.hour,
                    y=df['PM2.5'],
                    color='red',
                    linewidth=1.5,
                    #hue=hue,
                    palette="hls")
axes[0].set(xticks=([0, 6, 12, 18, 24]))
axes[0].set_yticklabels(axes[0].get_yticks(), fontsize=13)
axes[0].set_xlabel('hour', fontsize=15)
axes[0].set_ylabel('PM2.5', fontsize=15)
axes[0].legend().set_title('')

# concentration vs month
axes[1] = sns.lineplot(ax=axes[1],
                       data=df,
                       x=df['date'].dt.month,
                       y=df['PM2.5'],
                       color='red',
                       linewidth=1.5,
                       #hue=hue,
                       palette="hls")
axes[1].set_xticks(np.arange(1, 13, 1))
axes[1].set_xticklabels(months, fontsize=13)
axes[1].set_yticklabels(axes[1].get_yticks(), fontsize=13)
axes[1].set_xlabel('month', fontsize=15)
axes[1].set_ylabel('')
axes[1].legend().set_title('')

pollutant_daily_max = max(df.groupby(df['date'].dt.dayofweek)['PM2.5'].mean()) * 1.3 # setting the lim of y due to max mean
# concentration vs day of week
axes[2] = sns.lineplot(ax=axes[2],
                       data=df,
                       x=df['date'].dt.dayofweek,
                       y=df['PM2.5'],
                       color='red',
                       linewidth=1.5,
                       #hue=hue,
                       palette="hls")
axes[2].set_xticks(np.arange(0, 7, 1))
axes[2].set_xticklabels(day_of_week, fontsize=13)
axes[2].set_ylim(0, pollutant_daily_max)
axes[2].set_xlabel('day of week', fontsize=15)
axes[2].set_ylabel('')
axes[2].legend().set_title('')

# creating graphs of concentration by hour by specific day of week
fig2, axes2 = plt.subplots(1, 7, sharex=True, figsize=(18, 2.25))  # subplots for each day of week

# Plots
pollutant_max = max(df.groupby(df['date'].dt.hour)['PM2.5'].mean()) * 1.3 # setting the lim of y due to max mean
for i in range(7):
    axes2[i] = sns.lineplot(ax=axes2[i], data=df,
                            x=df[df.date.dt.dayofweek == i]['date'].dt.hour,
                            y=df['PM2.5'],
                            color='red',
                            linewidth=1,
                            #hue=hue,
                            palette="hls",
                            ci=None)
    axes2[i].set_xlabel('hour', fontsize=6)
    if i == 0:
        axes2[i].set_ylabel('PM2.5', fontsize=12)
    else:
        axes2[i].set_ylabel('')
        axes2[i].set_yticklabels('')
    axes2[i].set_ylim(0, pollutant_max)
    axes2[i].set(xticks=([0, 8, 16, 24]))
    axes2[i].set_title(day_of_week[i])
    axes2[i].legend().set_title('')


fig.figure.savefig("snsplot.png")
#img = open('snsplot.png', 'rb').read()
webbrowser.open_new_tab('snsplot.png')
fig2.figure.savefig("snsplot2.png")
webbrowser.open_new_tab('snsplot2.png')

