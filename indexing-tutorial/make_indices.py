import pandas as pd
import recordlinkage as rl
import labutils as lu

# Import data
names_1 = ['alfred', 'bob', 'calvin', 'hobbes', 'rusty']
names_2 = ['alfred', 'danny', 'callum', 'hobie', 'rusty']
df_a = pd.DataFrame(pd.Series(names_1, name='names'))
df_b = pd.DataFrame(pd.Series(names_2, name='names'))

df_c = pd.DataFrame(pd.Series(['alexander', 'bob', 'bruce', 'bruce', 'alexander'], name='names'))
df_d = pd.DataFrame(pd.Series(['alice', 'beth', 'amy', 'beth', 'brittany'], name='names'))


indexer = rl.SortedNeighbourhoodIndex(on='names', window=3)
candidate_links = indexer.index(df_c, df_d)

lu.clip_df(candidate_links.to_frame())
