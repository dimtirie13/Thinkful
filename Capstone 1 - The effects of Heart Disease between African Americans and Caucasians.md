
# Are African Americans at a Greater Risk of dying from Cardiovascular Disease than Caucasians?

Heart disease or(Cardiovascular Disease) is responsible for *800,000* deaths in the United States just in this past year. That comes out to one out of every three deaths, while more than **90Million** Americans are carrying a diagnosis of CVD. The most interesting statistic is that over 45% of Non-Hispanic Blacks live with CVD in the US. Let's take a closer look into this metric, by comparing the Heart Disease distribution rates of African Americans to the ones of Caucasians since they are the majority race. 


```python

from glob import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import seaborn as sb
%matplotlib inline

# import data sets
demo_path = glob('DEMOGRAPHICS.csv')
cause_path = glob('LEADINGCAUSESOFDEATH.csv')
factors_path = glob('RISKFACTORSANDACCESSTOCARE.csv')

# set data sets into pandas DataFrames
demo_df = pd.read_csv(demo_path[0]) 
cause_df = pd.read_csv(cause_path[0]) 
risk_df = pd.read_csv(factors_path[0])
```

### The Data
I worked with three different Data sets focusing on the Demograhics, Risk Factors, and the Leading Causes of Death in the United States. I have placed samples of each table below which seperate everything by State and by County. The "NaN" value represents the missing and or negative data points instead of replacing them with zero. Zero would of had an impact on the Measures of Central Tendency.


```python
# selected the needed RISKFACTORS Dataset coumns
risk_col = ['CHSI_State_Name','CHSI_County_Name', 'Uninsured', 'Obesity']
risk_df = risk_df[risk_col]

#Removing negative indexes function
risk_numeric_columns = risk_df.select_dtypes(include=[pd.np.number]).columns
for c in risk_numeric_columns:
    risk_df.loc[risk_df[c] < 0, c] = float('nan')
    

print('Risk Factors')
risk_df.sample(5)
```

    Risk Factors
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>CHSI_State_Name</th>
      <th>CHSI_County_Name</th>
      <th>Uninsured</th>
      <th>Obesity</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1252</th>
      <td>Michigan</td>
      <td>Emmet</td>
      <td>2857.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3118</th>
      <td>Wyoming</td>
      <td>Albany</td>
      <td>5182.0</td>
      <td>16.4</td>
    </tr>
    <tr>
      <th>2419</th>
      <td>South Dakota</td>
      <td>Todd</td>
      <td>3053.0</td>
      <td>36.4</td>
    </tr>
    <tr>
      <th>1936</th>
      <td>North Carolina</td>
      <td>Iredell</td>
      <td>14939.0</td>
      <td>24.3</td>
    </tr>
    <tr>
      <th>1834</th>
      <td>New York</td>
      <td>Chenango</td>
      <td>6316.0</td>
      <td>34.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Replacing Abbreviations 
cause_col_abbreviations = [column.replace('A_', 'Under 1').replace('B_', '1-14').replace('C_', '15-24') 
                               .replace('D_', '25-44').replace('E_', '45-64').replace('F_', '65+').replace
                               ('Wh_', 'White').replace('Bl_', 'Black').replace('Hi_', 'Hispanic')for column in cause_df.columns]
cause_df.columns = cause_col_abbreviations

# selected the LEADING CAUSES Dataset columns
cause_col = ['CHSI_State_Name','CHSI_County_Name', '25-44WhiteHeartDis',
             '25-44BlackHeartDis', '45-64WhiteHeartDis',
             '45-64BlackHeartDis', '65+WhiteHeartDis',
             '65+BlackHeartDis']
cause_df = cause_df[cause_col]

# Removing negative indexes function
cause_numeric_columns = cause_df.select_dtypes(include=[pd.np.number]).columns
for c in cause_numeric_columns:
    cause_df.loc[cause_df[c] < 0, c] = float('nan')
    
print('Leading Causes of Death')
cause_df.sample(5)
```

    Leading Causes of Death
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>CHSI_State_Name</th>
      <th>CHSI_County_Name</th>
      <th>25-44WhiteHeartDis</th>
      <th>25-44BlackHeartDis</th>
      <th>45-64WhiteHeartDis</th>
      <th>45-64BlackHeartDis</th>
      <th>65+WhiteHeartDis</th>
      <th>65+BlackHeartDis</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1021</th>
      <td>Kentucky</td>
      <td>Edmonson</td>
      <td>25.0</td>
      <td>NaN</td>
      <td>31.0</td>
      <td>NaN</td>
      <td>29.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1861</th>
      <td>New York</td>
      <td>Orange</td>
      <td>12.0</td>
      <td>22.0</td>
      <td>22.0</td>
      <td>24.0</td>
      <td>35.0</td>
      <td>35.0</td>
    </tr>
    <tr>
      <th>1429</th>
      <td>Mississippi</td>
      <td>Jasper</td>
      <td>12.0</td>
      <td>32.0</td>
      <td>31.0</td>
      <td>29.0</td>
      <td>41.0</td>
      <td>42.0</td>
    </tr>
    <tr>
      <th>1936</th>
      <td>North Carolina</td>
      <td>Iredell</td>
      <td>12.0</td>
      <td>NaN</td>
      <td>22.0</td>
      <td>23.0</td>
      <td>33.0</td>
      <td>32.0</td>
    </tr>
    <tr>
      <th>125</th>
      <td>Arkansas</td>
      <td>Crawford</td>
      <td>20.0</td>
      <td>NaN</td>
      <td>29.0</td>
      <td>NaN</td>
      <td>35.0</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
# DEMOGRAPHIC column Selection
demo_col = ['CHSI_County_Name','CHSI_State_Name','Population_Size','Poverty']
demo_df = demo_df[demo_col]

# Removing negative indexes function
demo_numeric_columns = demo_df.select_dtypes(include=[pd.np.number]).columns
for c in demo_numeric_columns:
    demo_df.loc[demo_df[c] < 0, c] = float('nan')
 

print('Demographics')
demo_df.sample(5)
```

    Demographics
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>CHSI_County_Name</th>
      <th>CHSI_State_Name</th>
      <th>Population_Size</th>
      <th>Poverty</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1812</th>
      <td>Otero</td>
      <td>New Mexico</td>
      <td>63538.0</td>
      <td>16.5</td>
    </tr>
    <tr>
      <th>3096</th>
      <td>Price</td>
      <td>Wisconsin</td>
      <td>15220.0</td>
      <td>9.0</td>
    </tr>
    <tr>
      <th>1198</th>
      <td>Charles</td>
      <td>Maryland</td>
      <td>138822.0</td>
      <td>6.9</td>
    </tr>
    <tr>
      <th>2086</th>
      <td>Logan</td>
      <td>Ohio</td>
      <td>46580.0</td>
      <td>9.3</td>
    </tr>
    <tr>
      <th>2935</th>
      <td>Martinsville City</td>
      <td>Virginia</td>
      <td>14925.0</td>
      <td>17.9</td>
    </tr>
  </tbody>
</table>
</div>



Here I merged all the data from the tables above into one master table.


```python
# Selecting which columns to avg, sum, and group by 
cols_to_be_avg = ['Poverty','Obesity','25-44WhiteHeartDis',
             '25-44BlackHeartDis', '45-64WhiteHeartDis',
             '45-64BlackHeartDis', '65+WhiteHeartDis',
             '65+BlackHeartDis']
cols_to_be_sum = ['Population_Size', 'Uninsured']

# Concatination of Columns
cause_risk_df = cause_df.merge(risk_df, on = ['CHSI_State_Name', 'CHSI_County_Name'], how = 'outer')
main_df = cause_risk_df.merge(demo_df, on = ['CHSI_State_Name', 'CHSI_County_Name'], how = 'outer')
main_df.sample(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>CHSI_State_Name</th>
      <th>CHSI_County_Name</th>
      <th>25-44WhiteHeartDis</th>
      <th>25-44BlackHeartDis</th>
      <th>45-64WhiteHeartDis</th>
      <th>45-64BlackHeartDis</th>
      <th>65+WhiteHeartDis</th>
      <th>65+BlackHeartDis</th>
      <th>Uninsured</th>
      <th>Obesity</th>
      <th>Population_Size</th>
      <th>Poverty</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1023</th>
      <td>Kentucky</td>
      <td>Estill</td>
      <td>10.0</td>
      <td>NaN</td>
      <td>32.0</td>
      <td>NaN</td>
      <td>38.0</td>
      <td>NaN</td>
      <td>2367.0</td>
      <td>NaN</td>
      <td>15089.0</td>
      <td>21.1</td>
    </tr>
    <tr>
      <th>702</th>
      <td>Indiana</td>
      <td>Carroll</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>28.0</td>
      <td>NaN</td>
      <td>30.0</td>
      <td>NaN</td>
      <td>2196.0</td>
      <td>32.6</td>
      <td>20426.0</td>
      <td>7.5</td>
    </tr>
    <tr>
      <th>2900</th>
      <td>Virginia</td>
      <td>Smyth</td>
      <td>13.0</td>
      <td>NaN</td>
      <td>31.0</td>
      <td>NaN</td>
      <td>32.0</td>
      <td>36.0</td>
      <td>3865.0</td>
      <td>22.8</td>
      <td>32640.0</td>
      <td>14.8</td>
    </tr>
    <tr>
      <th>2807</th>
      <td>Vermont</td>
      <td>Chittenden</td>
      <td>12.0</td>
      <td>NaN</td>
      <td>21.0</td>
      <td>NaN</td>
      <td>29.0</td>
      <td>NaN</td>
      <td>10177.0</td>
      <td>15.8</td>
      <td>149613.0</td>
      <td>7.6</td>
    </tr>
    <tr>
      <th>478</th>
      <td>Georgia</td>
      <td>McDuffie</td>
      <td>19.0</td>
      <td>10.0</td>
      <td>22.0</td>
      <td>28.0</td>
      <td>29.0</td>
      <td>30.0</td>
      <td>3546.0</td>
      <td>24.2</td>
      <td>21743.0</td>
      <td>17.5</td>
    </tr>
  </tbody>
</table>
</div>




```python
wht_young = main_df['25-44WhiteHeartDis']
wht_mid = main_df['45-64WhiteHeartDis']
wht_old = main_df['65+WhiteHeartDis']
blk_young = main_df['25-44BlackHeartDis']
blk_mid = main_df['45-64BlackHeartDis']
blk_old = main_df['65+BlackHeartDis']

all_wht = wht_young + wht_mid + wht_old
all_blk = blk_young + blk_mid + blk_old
```

### How do we break down this data set into groups for better visualization?

Using the Density Plots below you can see the distribution over one year between all CVD cases broken into two groups. The first one is by "Race" and the second by three age subgroups ranging from 25 to 65+. The reason behind using denisity plots is because there is vast majority in the Population Size between Caucasians and African Americans, making Non-Hispanic Whites 61.9% of the total population.

####  Group 1 - By Race


```python
# PLOTS FOR WHITE ONLY ALL AGES
plt.figure(figsize=(20,12))
plt.subplot(221)
wht_young.plot.kde(label='Ages 25-44')
wht_mid.plot.kde(label='Ages 45-64')
wht_old.plot.kde(label='Ages 65+')
plt.legend()
plt.xlim([0 , 50])
plt.text(2.6, .070, r'$\mu=15.2,\ \sigma=4$')
plt.text(17, .085, r'$\mu=25.8, \sigma=4.7$')
plt.text(28, .095, r'$\mu=32.6, \sigma=4.6$')
plt.title('Heart Disease Amongst Caucasians by Age Group')
sb.despine()

# PLOTS OF BLACKS ONLY  ALL AGES
plt.subplot(222)
blk_young.plot.kde(label='Ages 25-44')
blk_mid.plot.kde(label='Ages 45-64')
blk_old.plot.kde(label='Ages 65+')
plt.text(3.7, .070, r'$\mu=17.2,\ \sigma=4.8$')
plt.text(19.8, .065, r'$\mu=27.3,\ \sigma=6.5$')
plt.text(32, .070, r'$\mu=31.6,\ \sigma=6.2$')
plt.legend()
plt.xlim([0 , 50])
plt.title('Heart Disease Amongst African Americans by Age Group')
sb.despine()
```


![png](output_11_0.png)


The 25-44 age group seems to have the highest density as the 45-64 age group has the widest spread. The lowest Density level of Caucasians is .08 which is the highest level of the African Americans.  Let's investigate into these numbers by looking into the group 2 results.

#### Group 2 - Age Group


```python
# MIX RACE PER AGE GROUP
plt.figure(figsize=(15,15))
plt.subplot(311)
wht_young.plot.kde(label='Caucasian 25-44')
plt.text(5, .080, r'$\mu=15.2,\ \sigma=4$')
blk_young.plot.kde(label='African American 25-44')
plt.text(19, .070, r'$\mu=17.2,\ \sigma=4.8$')
plt.legend()
plt.xlim([0 , 50])
sb.despine()

plt.subplot(312)
wht_mid.plot.kde(label='Caucasian 54-64')
plt.text(17, .075, r'$\mu=25.8, \sigma=4.7$')
blk_mid.plot.kde(label='African American 45-64')
plt.text(31, .052, r'$\mu=27.3,\ \sigma=6.5$')
plt.legend()
plt.xlim([0 , 50])
sb.despine()

plt.subplot(313)
wht_old.plot.kde(label='Caucasian 65+')
plt.text(28, .095, r'$\mu=32.6, \sigma=4.6$')
blk_old.plot.kde(label='African American 65+')
plt.text(32, .070, r'$\mu=31.6,\ \sigma=6.2$')
plt.legend()
plt.xlim([0 , 50])
sb.despine()
```


![png](output_14_0.png)


### Key Insights
#### 1. African Americans have a Higher Average & Standard Deviation
The means seem to increase steadily in both races however, the African Americans have a higher mean in the 25-44 and 45-65 age groups than the Caucasians. They also have a higher Standard Deviation which correlates to their wider distribution shown throughout the plots in all the age groups. Blacks make up 12% of the US population(37million) and according to the [Henry J Kaiser Family Foundation]([https://www.kff.org/disparities-policy/fact-sheet/health-coverage-for-the-black-population-today-and-under-the-affordable-care-act/]) 21% under the age of 65 are uninsured, versus 13% of Whites who make up more than 60% of the population. Less access to health care means less diagnosis therefore a wider spread across all age groups. 

#### 2. Caucasians have a higher average in the 65+ age group
Caucasians have a higher mean in the 65+ age group because they have a higher life expectancy. According to [Business Insider]([http://www.businessinsider.com/huge-racial-gap-in-life-expectancy-2014-1?IR=T]) the average life expectancy of African Americans in the United States is 75. That’s the same as the average life expectancy of white men and women in 1979. Currently the average life expectancy of Caucasians is around 79. Since Whites live longer it actually increases their chances of being diagnosed with CVD in this age group.

### Is The Difference Between Whites & Blacks Significant?

To determine if the differences between the two races are indeed statistically significant I performed a series of tests with the results listed below


```python
print(ttest_ind(all_blk.dropna(),all_wht.dropna(), equal_var=False))
```

    Ttest_indResult(statistic=5.1360102452841545, pvalue=3.3240117649303344e-07)
    

As we can see there is a difference between these two variables however, the question remains as to why? Additional variables must be taken into consideration especially in the lower income communities with obesity being a major factor. Obesity is amongst the leading causes of CVD and poor social economic classes are the most effected by it. Unfortunately, the majority of African Americans happen to be in the lower income class with their median household income being $30,000 less than the Whites.  




### Is There a Correlation Between Poverty & Obesity? 

Below is the Correlation result between these Variables


```python
plt.figure(figsize=(10,5))
plt.scatter(main_df.Poverty,main_df.Obesity, alpha=0.2)
plt.title('Correlation between Poverty and Obesity')

# main_df_df.Poverty.corr(main_df.Obesity) to get correlation number.
print('Poverty & Obesity = '"%.4f" %0.4148590423831601,
      'although it is not substantial there is still \n a positive correlation and we can see the evidence in the scatter plot bellow') 
```

    Poverty & Obesity = 0.4149 although it is not substantial there is still 
     a positive correlation and we can see the evidence in the scatter plot bellow
    


![png](output_21_1.png)


### Conclusion
We must increase our efforts on employing and educating people in low income areas. Increasing the employment rates, will result in better nutrition since organic produce costs are at the minimum 20% more expensive. Improved nutrition means less cases of obesity and lowering the obesity percentages will decrease the number of deaths from CVD(lowering the African American mean).  Full time Employment will also decrease the number of the uninsured population which will narrow the African American distribution in the plots above. By educating and employing people from these areas we don’t just provide the chance of better health care, we provide the chance to improve the quality of their life.  
