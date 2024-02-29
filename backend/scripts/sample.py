import pandas as pd
import numpy as np

# Creating a sample dataset for virtual users
# Assuming a dataset with 1000 users
np.random.seed(0)
user_ids = np.arange(1, 10001)
ages_updated = np.random.randint(13, 81, size=10000)
gender = np.random.choice(['Male', 'Female'], size=10000)
health_conditions_updated = np.random.choice(['None', 'Asthma', 'Pneumonia', 'COPD', 'Cardiovascular', 'Allergy', 'Other'], size=10000)

# Adding pregnancy status
# Assuming females aged 18-45 can be pregnant
is_pregnant = np.random.choice([0, 1], size=10000)
for i in range(len(is_pregnant)):
    if gender[i] == 'Male' or ages_updated[i] < 18 or ages_updated[i] >= 45:
        is_pregnant[i] = 0  # Setting non-eligible individuals to '0'

# Creating the updated DataFrame
users_df_updated = pd.DataFrame({
    'User_ID': user_ids,
    'Age': ages_updated,
    'Gender': gender,
    'Pregnant': is_pregnant,
    'Health_Condition': health_conditions_updated
})

# Adding the air quality and mask wearing columns to the dataset

# Air quality levels
pm10_levels = ['Good', 'Moderate', 'Slightly Unhealthy', 'Unhealthy', 'Very Unhealthy']
pm2_5_levels = ['Good', 'Moderate', 'Slightly Unhealthy', 'Unhealthy', 'Very Unhealthy']

# Randomly assign air quality levels
users_df_updated['PM10_Level'] = np.random.choice(pm10_levels, size=10000)
users_df_updated['PM2_5_Level'] = np.random.choice(pm2_5_levels, size=10000)

# Function to determine mask wearing necessity based on conditions
def determine_mask_wearing(age, health_condition, pregnant, pm10_level, pm2_5_level):
    # Very High-Risk: Age >= 70 and has a bronchial condition
    if age >= 70 and health_condition in ['Asthma', 'Pneumonia', 'COPD', 'Cardiovascular']:
        if pm10_level in ['Slightly Unhealthy'] or pm2_5_level in ['Slightly Unhealthy']:
            return 'Required'
        elif pm10_level in ['Moderate']:
            return 'Recommended'
        else:
            return 'Not Necessary'
    
    # High-Risk: Age >= 70, or has a bronchial condition, or is pregnant
    elif age >= 70 or health_condition in ['Asthma', 'Pneumonia', 'COPD'] or pregnant == 1:
        if pm10_level in ['Moderate']:
            return 'Recommended'
        elif pm10_level in ['Slightly Unhealthy'] or pm2_5_level in ['Slightly Unhealthy']:
            return 'Required'
        else:
            return 'Not Necessary'

    # Normal User
    else:
        if pm10_level in ['Unhealthy', 'Very Unhealthy'] or pm2_5_level in ['Unhealthy', 'Very Unhealthy']:
            return 'Required'
        else:
            return 'Not Necessary'

# Applying the function to each row in the DataFrame
users_df_updated['Mask_Wearing'] = users_df_updated.apply(lambda x: determine_mask_wearing(x['Age'], x['Health_Condition'], x['Pregnant'], x['PM10_Level'], x['PM2_5_Level']), axis=1)

users_df_updated.to_csv('../data/vi_user.csv')

print(users_df_updated.head())
