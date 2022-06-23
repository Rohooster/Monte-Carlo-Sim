import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

sns.set_style('whitegrid')
average = 1
standard_deviation = .1
number_repetitions = 500
number_simulations = 1000
pct_to_target = np.random.normal(average, standard_deviation, number_repetitions).round(2)
sales_target_values = [75_000, 100_000, 200_000, 300_000, 400_000, 500_000]
sales_target_prob = [.3, .3, .2, .1, .05, .05]
sales_target = np.random.choice(sales_target_values, number_repetitions, p=sales_target_prob)
dataframe = pd.DataFrame(index=range(number_repetitions), data={'Pct_To_Target': pct_to_target,
                                               'Sales_Target': sales_target})

dataframe['Sales'] = dataframe['Pct_To_Target'] * dataframe['Sales_Target']
def calc_commission_rate(x):
    """ Return the commission rate based on the table:
    0-90% = 2%
    91-99% = 3%
    >= 100 = 4%
    """
    if x <= .90:
        return .02
    if x <= .99:
        return .03
    else:
        return .04
dataframe['Commission_Rate'] = dataframe['Pct_To_Target'].apply(calc_commission_rate)
dataframe['Commissions_Amount'] = dataframe['Commission_Rate'] * dataframe['Sales']
# Define a list to keep all the results from each simulation that we want to analyze
stats_track = []

# Loop through many simulations
for i in range(number_simulations):

    # Utilize randomness for sales targets and target percents
    sales_target = np.random.choice(sales_target_values, number_repetitions, p=sales_target_prob)
    pct_to_target = np.random.normal(average, standard_deviation, number_repetitions).round(2)

    # Build the dataframe based on the inputs and number of reps
    dataframe = pd.DataFrame(index=range(number_repetitions), data={'Pct_To_Target': pct_to_target,
                                                   'Sales_Target': sales_target})

    # Back into the sales number using the percent to target rate
    dataframe['Sales'] = dataframe['Pct_To_Target'] * dataframe['Sales_Target']

    # Determine the commissions rate and calculate commissions
    dataframe['Commission_Rate'] = dataframe['Pct_To_Target'].apply(calc_commission_rate)
    dataframe['Commissions_Amount'] = dataframe['Commission_Rate'] * dataframe['Sales']

    # We want to track sales,commission amounts and sales targets over all the simulations within the list defined previously
    stats_track.append([dataframe['Sales'].sum().round(0),
                      dataframe['Commissions_Amount'].sum().round(0),
                      dataframe['Sales_Target'].sum().round(0)])
results_df = pd.DataFrame.from_records(all_stats, columns=['Sales',
                                                           'Commissions_Amount',
                                                           'Sales_Target'])
results_df.describe().style.format('{:,}')

matplotgraph = plt.figure()
plt.plot(results_df)
plt.xlabel('Sales')
plt.ylabel('Price(by $10)')
plt.show() 
