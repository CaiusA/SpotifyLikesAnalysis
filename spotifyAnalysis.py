import pandas as pd
import matplotlib.pyplot as plt

#pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 130)

df = pd.read_csv('spotify_liked_tracks.csv')

df['Song Added At'] = pd.to_datetime(df['Song Added At'], format='ISO8601').dt.tz_convert('America/Chicago')

dates = df['Song Added At'].sort_values()

monthlyActivity = dates.dt.strftime('%b %Y')
monthlyActivity = monthlyActivity.value_counts(sort=False).reset_index()

onlyMonths = dates.dt.month_name()
onlyMonths = onlyMonths.value_counts(sort=False)
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
onlyMonths = onlyMonths.reindex(month_order, axis=0).reset_index()

hours = dates.dt.strftime('%I %p')
hours = hours.value_counts(sort=False)
hour_order = ['01 AM', '02 AM', '03 AM', '04 AM', '05 AM', '06 AM', '07 AM', '08 AM', '09 AM', '10 AM', '11 AM', '12 PM',
              '01 PM', '02 PM', '03 PM', '04 PM', '05 PM', '06 PM', '07 PM', '08 PM', '09 PM', '10 PM', '11 PM', '12 AM']
hours = hours.reindex(hour_order, axis=0).reset_index().fillna(0)

rating = df['Explicit'].value_counts().reset_index()
rating['Explicit'] = rating['Explicit'].replace({False: 'Not Explicit', True: 'Explicit'})

# plot data
fig, axd = plt.subplot_mosaic(
    [['Only Month', 'Hourly', 'Explicit'],
     ['Monthly', 'Monthly', 'Explicit']],
    layout='constrained', figsize=(20, 6))

axd['Only Month'].plot(onlyMonths['Song Added At'], onlyMonths['count'])
axd['Only Month'].set_title('Songs Added to Library by Month')
axd['Only Month'].set_xlabel('Month')
axd['Only Month'].set_ylabel('Songs Added')

axd['Hourly'].plot(hours['Song Added At'], hours['count'])
axd['Hourly'].set_title('Songs Added to Library by Hour')
axd['Hourly'].set_xlabel('Time')
axd['Hourly'].set_ylabel('Songs Added')

axd['Monthly'].plot(monthlyActivity['Song Added At'], monthlyActivity['count'])
axd['Monthly'].set_title('Songs Added to Library Over Time')
axd['Monthly'].set_xlabel('Month and Year')
axd['Monthly'].set_ylabel('Songs Added')

axd['Explicit'].pie(rating['count'], labels=rating['Explicit'], autopct='%1.1f%%', colors=['green', 'red'])
axd['Explicit'].set_title('Songs Rated Explicit by Spotify')

# adjust axis formatting
for ax in axd:
    axd[ax].set_xmargin(0.005)
    axd[ax].tick_params(axis='x', labelrotation=45)
    axd[ax].grid(True, axis='y')
    for label in axd[ax].get_xticklabels():
        label.set_horizontalalignment('right')

plt.show()
