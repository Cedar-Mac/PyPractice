import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 8)

general = pd.read_csv('./general.csv')
prenatal = pd.read_csv('./prenatal.csv')
sports = pd.read_csv('./sports.csv')

prenatal.rename(columns={'HOSPITAL': 'hospital', 'Sex': 'gender'}, inplace=True)
sports.rename(columns={'Male/female': 'gender', 'Hospital': 'hospital'}, inplace=True)

hospitals = pd.concat([general, prenatal, sports], ignore_index=True)
hospitals.drop(columns=['Unnamed: 0'], inplace=True)
hospitals.dropna(how='all', inplace=True)

hospitals['gender'] = ['m' if gender == 'man' or gender == 'male' else 'f' for gender in hospitals['gender']]
select_columns = ['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']
hospitals[select_columns] = hospitals[select_columns].fillna(0)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
ax1.hist(hospitals['age'], bins=[0, 15, 35, 55, 70, 80])
ax1.set_title('Histogram of Patient Ages')

ax2.pie(hospitals['diagnosis'].value_counts(), labels=hospitals['diagnosis'].unique())
ax2.set_title('Pie Chart of Diagnoses')

ax3.violinplot(hospitals['height'], vert=True)
ax3.set_title('Violin Plot of Patient Height')

plt.show()

print("""The answer to the 1st question: 15-35
The answer to the 2nd question: cold
The answer to the 3rd question: Because there are two different units being used""")
