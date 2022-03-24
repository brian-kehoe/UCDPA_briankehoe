import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import webbrowser
from tkinter import *

# Read "top_sites_monthly_max_mean.csv"
# Filter to unique list of locations
df_month_max = pd.read_csv("top_sites_monthly_max_mean.csv")
df_location = df_month_max['location'].unique()

# Pop-up to allow user select location
window = Tk()
window.title("Historical air quality analysis")
window.geometry('300x90')

frame = LabelFrame(
    window,
    text='Select location:',
    bg='#f0f0f0',
    font=18
)
frame.pack(expand=TRUE, fill=BOTH)

variable = StringVar(window)

w = OptionMenu(window, variable, *df_location)
w.pack()


def ok():
    print("Chosen location is: " + variable.get())
    window.destroy()


button = Button(window, text="OK", command=ok)
button.pack()
mainloop()

# Read historical data
df_read = pd.read_csv('aq_data_merge.csv')

# Store user site selection
user_location = variable.get()
user_site = df_read.loc[df_read['location'] == user_location, 'Site'].unique()
user_site = user_site[0]

# Filter historical data to user_site selection
df = df_read.copy()
df['date'] = pd.to_datetime(df['Date and Time'], format="%d/%m/%Y %H:%M")
df = df[df['Site'] == user_site]
df = df.drop(columns=['Unnamed: 0', 'PM10', 'SO2', 'Date and Time'])
df = df.dropna()

# Set categorical order for months
df_month = df_month_max.copy()
df_month = df_month[df_month['Site'] == user_site]
df_month['month'] = pd.Categorical(df_month['month'], categories=[6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5], ordered=True)
df_month.sort_values('month', inplace=True)

# Define xticklabels
day_of_week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
months = ['jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'jan', 'feb', 'mar', 'apr', 'may', 'jun']


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
                       palette="hls")
axes[0].set(xticks=([0, 6, 12, 18, 24]))
axes[0].set_yticklabels(axes[0].get_yticks(), fontsize=13)
axes[0].set_xlabel('hour', fontsize=15)
axes[0].set_ylabel('PM2.5', fontsize=15)
#axes[0].legend().set_title('')

# concentration vs month
axes[1] = sns.pointplot(ax=axes[1],
                        data=df_month,
                        x='month',
                        y='monthly max mean',
                        color='red',
                        scale=0.6,
                        markers='',
                        order=df_month['month'])
axes[1].set_xticklabels(months, fontsize=13)
axes[1].set_yticklabels(axes[1].get_yticks(), fontsize=13)
axes[1].set_xlabel('month', fontsize=15)
axes[1].set_ylabel('')
axes[1].set_title(user_location, fontsize=18)

# concentration vs day of week
pollutant_daily_max = max(df.groupby(df['date'].dt.dayofweek)['PM2.5'].mean()) * 1.3 # setting the lim of y due to max mean
axes[2] = sns.lineplot(ax=axes[2],
                       data=df,
                       x=df['date'].dt.dayofweek,
                       y=df['PM2.5'],
                       color='red',
                       linewidth=1.5,
                       palette="hls")
axes[2].set_xticks(np.arange(0, 7, 1))
axes[2].set_xticklabels(day_of_week, fontsize=13)
axes[2].set_ylim(0, pollutant_daily_max)
axes[2].set_xlabel('day of week', fontsize=15)
axes[2].set_ylabel('')
#axes[2].legend().set_title('')


# creating graphs of concentration by hour by specific day of week
fig2, axes2 = plt.subplots(1, 7, sharex=True, figsize=(18, 2.25))  # subplots for each day of week

# Plots
pollutant_max = max(df.groupby(df['date'].dt.hour)['PM2.5'].mean()) * 1.35  # setting the lim of y due to max mean
pollutant_max_round5 = 2.5 * round(pollutant_max/2.5)
for i in range(7):
    axes2[i] = sns.lineplot(ax=axes2[i], data=df,
                            x=df[df.date.dt.dayofweek == i]['date'].dt.hour,
                            y=df['PM2.5'],
                            color='red',
                            linewidth=1,
                            palette="hls",
                            ci=None)
    axes2[i].set_xlabel('hour', fontsize=6)
    if i == 0:
        axes2[i].set_ylabel('PM2.5', fontsize=12)
    else:
        axes2[i].set_ylabel('')
        axes2[i].set_yticklabels('')
    if i == 3:
        axes2[i].set_title(user_location)
    else:
        pass
    axes2[i].set_ylim(0, pollutant_max_round5)
    axes2[i].set(xticks=([0, 8, 16, 24]))
    axes2[i].legend(loc='upper left').set_title(day_of_week[i])


fig.figure.savefig("snsplot.png")
webbrowser.open_new_tab('snsplot.png')
fig2.figure.savefig("snsplot2.png")
webbrowser.open_new_tab('snsplot2.png')

