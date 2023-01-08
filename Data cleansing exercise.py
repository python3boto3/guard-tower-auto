

'''
Data Cleansing and validation exercise.
--------------------------------------------------------
A general approach using pandas and python, for spark, or using parallel lambda functions.
'''

#1. Re-shape the initial dataset - sort, drop columns, rename column headers

# GroupBy column A, descending values
df=df.groupby('A')['B'].sum().sort_values(ascending=False)

# drop column C
df.drop(['C'], axis=1)

# drop multiple columns
df.drop(['C', 'D', 'Q', 'R', 'Z'], axis=1)

# rename all headers to lowercase
df.columns = df.columns.str.lower()

# replace all spaces for underscore
df.columns = df.columns.str.replace(' ', '_')
#2. Remove duplicates

import pandas as pd
from pandas_dedupe import dedupe_dataframe

df = pd.DataFrame.from_dict({'name':['john', 'mark', 'frank', 'jon', 'john'], 'zip':['11', '22', '33', '11', '11']})
dd = dedupe_dataframe(df, ['name', 'zip'], canonicalize=True, sample_size=1)

# count duplicate records
print(df.duplicated().sum())
#3. Fix structural errors Structural errors - naming conventions, typos, incorrect capitalization. Inconsistencies can cause mislabeled categories. For example, you find “N/A” & “Not App”, but they should be analyzed as the same category.

# capitalize all words
df.columns = df.columns.str.title()
df.rename(columns=str.title, inplace=True)  
# ... inplace = false does NOT overwrite the existing dataframe, 
# inplace = true DOES overwrite the existing dataframe, 

# capitalize only the first n words
df.columns = df.columns.str.replace(r'(\w+)', lambda x: x.group().capitalize(), n=2, regex=True)

# replacing several items for one preferred version
df['RoleName'].replace(['N/A.', 'NA', 'Not applicable', 'not aplicable', 'Not Applicable'], 'not applicable')
#4. Maintain consistency

# make data consistent first …
Series.str.isnumeric()
# Check whether all characters in each string are numeric.

Series.str.isalpha
# Check whether all characters are alphabetic.

Series.str.isnumeric
# Check whether all characters are numeric.

Series.str.isalnum
# Check whether all characters are alphanumeric.

Series.str.isdigit
# Check whether all characters are digits.

Series.str.isdecimal
# Check whether all characters are decimal.

Series.str.isspace
# Check whether all characters are whitespace.

Series.str.islower
# Check whether all characters are lowercase.

Series.str.isupper
# Check whether all characters are uppercase.

Series.str.istitle
# Check whether all characters are titlecase.
#5. Handle missing data As a first option, you can drop observations that have missing values, doing this will drop/lose information. As a second option, you can input missing values based on other observations; there is an opportunity to lose data integrity because you may be using assumptions, not actual observations. As a third option, you might alter the way the data is used to effectively navigate null values.

# determine if any value is missing (true/false)			
df.isnull().values.any()

# list true false on missing items in a specific column			
df["STREET_ADDRESS"].isnull()

# count False/count True Data type, specific column			
df["STREET_ADDRESS"].isnull().value_counts()

# count missing values on each column				
df.isnull().sum()

# count total of all missing values in the entire dataframe 		
df.isnull().sum().sum()
#6. Validate and QA At the end of the data cleaning process, Does the data make sense?

# find the max value in a column
maxClm = df['x'].max()

# max value in multiple columns
maxValues = df[['x', 'z']].max()

# find the index position of maximum
# values in every column
maxValueIndex = df.idxmax()
print("Maximum values of columns are at row index position :")
print(maxValueIndex)
#7. Does the data follow the appropriate rules for its field?

Does it prove or disprove your working theory, or bring any insight to light?

# Filter Rows Based on String Length greater than a parameter greater than 50
df.loc[df['col1'].str.len() > 50]

# filter rows where col1 has string length of 5 and col3 has string length > 7
df.loc[(df['col1'].str.len() == 5) & (df['col3'].str.len() > 7)]
#8. Find trends in the data to help you form your next theory.

# Rule to assess two criteria on different columns
df.loc[(df['col1'].str.len() >9) & (df['col71'].str.len() < 12)]