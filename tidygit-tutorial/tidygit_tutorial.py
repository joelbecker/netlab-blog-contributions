import datetime as dt
import pandas as pd
import seaborn as sns

# Load pre-extracted data_2. Pretend this didn't happen.
commits_df = pd.DataFrame.from_csv('tf_commits.csv', parse_dates=True)
# changes_df = pd.DataFrame.from_csv('tf_changes.csv', parse_dates=True)

commits_df['authored_datetime'] = commits_df['authored_datetime'].apply(
    lambda s: dt.datetime.strptime(s[:-6], '%Y-%m-%d %H:%M:%S')
)

# Shorten dates to month strings.
commits_df['authored_month'] = commits_df['authored_datetime'].apply(lambda date: date.strftime('%Y%m'))
commits_df = commits_df[(commits_df.authored_month != '201707') & (commits_df.authored_month != '201511')]

# Make a deduplicated, sorted list of months.
month_list = sorted(list(set(commits_df['authored_month'])))

# Convert Months to ints using the month's position in the sorted list.
commits_df['Month'] = commits_df['authored_month'].apply(lambda s: month_list.index(s))

# Group data_2 by month.
commits_by_month = commits_df.groupby(['Month'])

# Save a count of
monthly_commits = pd.concat([commits_by_month['hexsha'].count(),
                             commits_by_month.sum()[['total_lines',
                                                     'total_insertions',
                                                     'total_deletions',
                                                     'total_files']]],
                            axis=1)

# Rename columns
monthly_commits.columns = ['Commits', 'Lines', 'Insertions', 'Deletions', 'Files']

# Reset index
monthly_commits = monthly_commits.reset_index()

# Plot total commits by month
plot1 = sns.lmplot('Month', 'Commits', data=monthly_commits, order=1, palette=['#f03838'], size=4, aspect=1.61)
plot2 = sns.lmplot('Month', 'Commits', data=monthly_commits, order=2, palette=['#f03838'], size=4, aspect=1.61)

# Save figures
plot1.savefig('tidygit_plot_1.svg')
plot2.savefig('tidygit_plot_2.svg')
