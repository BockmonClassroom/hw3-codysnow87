# -*- coding: utf-8 -*-
"""DS5110_HW3

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ib8atrj23Cbsng0FHB0v51tw_BEmWgs8
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_ind
from scipy import stats

df_t1 = pd.read_csv('data/t1_user_active_min.csv')
df_t2 = pd.read_csv('data/t2_user_variant.csv')
df_t3 = pd.read_csv('data/t3_user_active_min_pre.csv')
df_t4 = pd.read_csv('data/t4_user_attributes.csv')

# merge datasets such that variant number is associated with each uid
df_t2_selected = df_t2[['uid', 'variant_number']]
df_merged = df_t1.join(df_t2_selected.set_index('uid'), on='uid', how='right', lsuffix='_caller', rsuffix='_other')
df_merged.head()

# split the dataset into control and treatment groups
df_treatment = df_merged.loc[df_merged['variant_number'] == 1]
df_control = df_merged.loc[df_merged['variant_number'] == 0]

# sum the minutes for each user and remove other fields
df_treatment = df_treatment.groupby(['uid'])['active_mins'].sum()
df_control = df_control.groupby(['uid'])['active_mins'].sum()

# export the new csv files
#df_treatment.to_csv('treatment_group_active_min_sum.csv', index=True)
#df_control.to_csv('control_group_active_min_sum.csv', index=True)

# run independent t-test on the two groups
treatment = df_treatment[df_treatment > 0]
control = df_control[df_control > 0]
ttest_ind(treatment, control)

# the resulting pvalue of 0.7 is very high, which suggests no strong evidence of a difference
# I find this value suspicious

# find the mean and median for each group
print(treatment.mean())
print(treatment.median())
print(control.mean())
print(control.median())

# the means and medians are wildly skewed

plt.boxplot([treatment, control])
plt.ylabel('Minutes')
plt.xlabel('Treatment and Control Groups, respectively')
plt.show()

# this dataframe has an impossible value
df_t1.max()

# calculate Interquartile Range (IQR) for active_mins values in each set
Q1 = df_treatment.quantile(0.25)
Q3 = df_treatment.quantile(0.75)
IQR = Q3 - Q1

# identify outliers
outliers_treatment = df_treatment[(df_treatment < Q1 - IQR) | (df_treatment > Q3 + IQR)]

print(outliers_treatment)

# calculate IQR for active_mins
Q1 = df_control.quantile(0.25)
Q3 = df_control.quantile(0.75)
IQR = Q3 - Q1

# identify outliers
outliers_control = df_control[(df_control < Q1 - IQR) | (df_control > Q3 + IQR)]

print(outliers_control)

# exclude the outliers from both sets
df_treatment_filtered = df_treatment.drop(outliers_treatment.index)
df_control_filtered = df_control.drop(outliers_control.index)

# print maxes before and after
print(df_treatment.max())
print(df_control.max())

print(df_treatment_filtered.max())
print(df_control_filtered.max())
print(df_treatment_filtered.count())
print(df_control_filtered.count())

# create another boxplot to see the new sets
plt.boxplot([df_treatment_filtered, df_control_filtered])
plt.ylabel('Minutes')
plt.xlabel('Treatment and Control Groups, respectively')
plt.show()

# now that I can see the outlier max values, remove outliers manually
outliers_control = df_control_filtered[df_control_filtered >= 100]
df_control_filtered = df_control_filtered.drop(outliers_control.index)
outliers_treatment = df_treatment_filtered[(df_treatment_filtered >= 160)]
df_treatment_filtered = df_treatment_filtered.drop(outliers_treatment.index)

# create another boxplot to see the new sets
plt.boxplot([df_treatment_filtered, df_control_filtered])
# label plots
plt.ylabel('Minutes')
plt.xlabel('Treatment and Control Groups, respectively')
plt.show()

# run independent t-test on the two groups again now that outliers are filtered
treatment = df_treatment_filtered[df_treatment_filtered > 0]
control = df_control_filtered[df_control_filtered > 0]
ttest_ind(treatment, control)

# find the mean and median for each filtered group
print(df_treatment_filtered.mean())
print(df_treatment_filtered.median())
print(df_control_filtered.mean())
print(df_control_filtered.median())

# test the normality of each set
print(stats.shapiro(df_treatment_filtered))
print(stats.shapiro(df_control_filtered))

# analyze df_t3
# merge datasets such that variant number is associated with each uid
df_t2_selected = df_t2[['uid', 'variant_number']]
df_merged = df_t3.join(df_t2_selected.set_index('uid'), on='uid', how='right', lsuffix='_caller', rsuffix='_other')

# remove the treatment group
df_control_pre_update = df_merged.loc[df_merged['variant_number'] == 0]

# sum the minutes for each user and remove other fields
df_control_pre_update = df_control_pre_update.groupby(['uid'])['active_mins'].sum()
df_control_pre_update.head()

# remove outliers
# calculate IQR for active_mins
Q1 = df_control_pre_update.quantile(0.25)
Q3 = df_control_pre_update.quantile(0.75)
IQR = Q3 - Q1

# identify outliers
outliers_control_pre_update = df_control_pre_update[(df_control_pre_update < Q1 - IQR) | (df_control_pre_update > Q3 + IQR)]
df_control_pre_update = df_control_pre_update.drop(outliers_control_pre_update.index)

# boxplot new group
plt.boxplot([df_control_pre_update])
plt.show()

# remove outliers manually
outliers_control_pre_update = df_control_pre_update[df_control_pre_update >= 115]
df_control_pre_update = df_control_pre_update.drop(outliers_control_pre_update.index)

# plot again
plt.boxplot([df_control_pre_update])
# label
plt.ylabel('Minutes')
plt.xlabel('Control Group Pre-update')
plt.show()

# look for any statistically significant difference between control group pre and post update using t-test
control_pre_update = df_control_pre_update[df_control_pre_update > 0]
control_post_update = df_control_filtered[df_control_filtered > 0]
ttest_ind(control_pre_update, control_post_update)

# mean and median for new group
print(df_control_pre_update.mean())
print(df_control_pre_update.median())

# test the normality of the pre_update set
print(stats.shapiro(df_control_pre_update))

# analyze df_t4
# pre update
df_t2_selected = df_t2[['uid', 'variant_number']]
df_merged_pre_update = df_t3.join(df_t4.set_index('uid'), on='uid', how='right', lsuffix='_caller', rsuffix='_other')
df_merged_pre_update = df_merged_pre_update.join(df_t2_selected.set_index('uid'), on='uid', how='left')

# split the dataset into control and treatment groups
df_treatment_pre_update = df_merged_pre_update.loc[df_merged_pre_update['variant_number'] == 1]
df_control_pre_update = df_merged_pre_update.loc[df_merged_pre_update['variant_number'] == 0]

# post update
df_t2_selected = df_t2[['uid', 'variant_number']]
df_merged_post_update = df_t1.join(df_t4.set_index('uid'), on='uid', how='right', lsuffix='_caller', rsuffix='_other')
df_merged_post_update = df_merged_post_update.join(df_t2_selected.set_index('uid'), on='uid', how='left')


# Now you can split the dataset into control and treatment groups
df_treatment_post_update = df_merged_post_update.loc[df_merged_post_update['variant_number'] == 1]
df_control_post_update = df_merged_post_update.loc[df_merged_post_update['variant_number'] == 0]

print(df_treatment_post_update.head())
print(df_control_post_update.head())

# sum both pre and post sets on active_min
df_control_pre_update = df_control_pre_update.groupby(['uid', 'gender', 'user_type'])['active_mins'].sum()
df_control_post_update = df_control_post_update.groupby(['uid', 'gender', 'user_type'])['active_mins'].sum()
df_treatment_pre_update = df_treatment_pre_update.groupby(['uid', 'gender', 'user_type'])['active_mins'].sum()
df_treatment_post_update = df_treatment_post_update.groupby(['uid', 'gender', 'user_type'])['active_mins'].sum()

print(df_control_pre_update.head())
print(df_control_post_update.head())
print(df_treatment_pre_update.head())
print(df_treatment_post_update.head())

# filter outliers on pre and post sets using IQR
# calculate IQR for active_mins
Q1 = df_control_pre_update.quantile(0.25)
Q3 = df_control_pre_update.quantile(0.75)
IQR = Q3 - Q1

# identify outliers
outliers_control = df_control_pre_update[(df_control_pre_update < Q1 - IQR) | (df_control_pre_update > Q3 + IQR)]
df_control_pre_update = df_control_pre_update.drop(outliers_control.index)
print(df_control_pre_update.head())

# filter outliers on pre and post sets using IQR
# calculate IQR for active_mins
Q1 = df_control_pre_update.quantile(0.25)
Q3 = df_control_pre_update.quantile(0.75)
IQR = Q3 - Q1

# identify outliers
outliers_control = df_control_post_update[(df_control_post_update < Q1 - IQR) | (df_control_post_update > Q3 + IQR)]
df_control_post_update = df_control_post_update.drop(outliers_control.index)
print(df_control_pre_update.head())

# filter outliers on pre and post sets using IQR
# calculate IQR for active_mins
Q1 = df_control_pre_update.quantile(0.25)
Q3 = df_control_pre_update.quantile(0.75)
IQR = Q3 - Q1

# identify outliers
outliers_control = df_treatment_pre_update[(df_treatment_pre_update < Q1 - IQR) | (df_treatment_pre_update > Q3 + IQR)]
df_treatment_pre_update = df_treatment_pre_update.drop(outliers_control.index)
print(df_treatment_pre_update.head())

# filter outliers on pre and post sets using IQR
# calculate IQR for active_mins
Q1 = df_control_pre_update.quantile(0.25)
Q3 = df_control_pre_update.quantile(0.75)
IQR = Q3 - Q1

# identify outliers
outliers_control = df_treatment_post_update[(df_treatment_post_update < Q1 - IQR) | (df_treatment_post_update > Q3 + IQR)]
df_treatment_post_update = df_treatment_post_update.drop(outliers_control.index)
print(df_treatment_post_update.head())

# plot users by gender
gender_counts = df_control_pre_update.reset_index()['gender'].value_counts()
# Get unique genders and use them as labels
labels = gender_counts.index.tolist()
plt.pie(gender_counts, labels=labels, autopct='%1.1f%%')
plt.title('Control users by gender before update')
plt.show()

# plot users by gender
gender_counts = df_control_post_update.reset_index()['gender'].value_counts()
# Get unique genders and use them as labels
labels = gender_counts.index.tolist()
plt.pie(gender_counts, labels=labels, autopct='%1.1f%%')
plt.title('Control users by gender after update')
plt.show()

# plot users by user type
gender_counts = df_control_pre_update.reset_index()['user_type'].value_counts()
# Get unique genders and use them as labels
labels = gender_counts.index.tolist()
plt.pie(gender_counts, labels=labels, autopct='%1.1f%%')
plt.title('Control users by user type before update')
plt.show()

# plot users by user type
gender_counts = df_control_post_update.reset_index()['user_type'].value_counts()
# Get unique genders and use them as labels
labels = gender_counts.index.tolist()
plt.pie(gender_counts, labels=labels, autopct='%1.1f%%')
plt.title('Control users by user type after update')
plt.show()

# plot users by gender
gender_counts = df_treatment_pre_update.reset_index()['gender'].value_counts()
# Get unique genders and use them as labels
labels = gender_counts.index.tolist()
plt.pie(gender_counts, labels=labels, autopct='%1.1f%%')
plt.title('Treatment users by gender before update')
plt.show()

# plot users by gender
gender_counts = df_treatment_post_update.reset_index()['gender'].value_counts()
# Get unique genders and use them as labels
labels = gender_counts.index.tolist()
plt.pie(gender_counts, labels=labels, autopct='%1.1f%%')
plt.title('Treatment users by gender after update')
plt.show()

# plot users by user type
gender_counts = df_treatment_pre_update.reset_index()['user_type'].value_counts()
# Get unique genders and use them as labels
labels = gender_counts.index.tolist()
plt.pie(gender_counts, labels=labels, autopct='%1.1f%%')
plt.title('Control users by user type before update')
plt.show()

# plot users by user type
gender_counts = df_treatment_post_update.reset_index()['user_type'].value_counts()
# Get unique genders and use them as labels
labels = gender_counts.index.tolist()
plt.pie(gender_counts, labels=labels, autopct='%1.1f%%')
plt.title('Control users by user type after update')
plt.show()