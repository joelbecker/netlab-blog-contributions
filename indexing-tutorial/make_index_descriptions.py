import pandas as pd
import labutils as lu

records = [
    {'Method': 'Full Index',
     'Description': 'All possible links are kept as candidate links.',
     'Advantages': 'Convenient when performance isn\'t an issue.',
     'Limitations': 'Highly inefficient with large data sets.'},
    {'Method': 'Block Index',
     'Description': 'Only links exactly equal on '
                    'specified values are kept as candidate links.',
     'Advantages': 'Extremely effective for high-quality, structured data.',
     'Limitations': 'Does not allow approximate matching.'},
    {'Method': 'Sorted Neighborhood Index',
     'Description': 'Rows are ranked by some value, and candidate links'
                    ' are made between rows with nearby values.',
     'Advantages': 'Useful for making approximate matches.',
     'Limitations': 'More conceptually difficult.'},
    {'Method': 'Random Index',
     'Description': 'Creates a random set of candidate links.',
     'Advantages': 'Useful for developing your data integration workflow on a subset of '
                          'candidate links, or creating training data for unsupervised learning models.',
     'Limitations': 'Not recommended for your final data integration workflow.'}
]

df = pd.DataFrame.from_records(records)

lu.clip_df(df[['Method', 'Description', 'Advantages', 'Limitations']])
