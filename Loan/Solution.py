#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[3]:


data = pd.read_csv(r"C:\Users\vasan\OneDrive\Desktop\Python\Loan_Data.csv")


# In[4]:


data.head()


# In[6]:


data.shape


# In[84]:


def Risk_Category(row):
    if 'B' not in row['Bounce String'][-6:]:
        return "Low Risk"
    elif row['Bounce String'][-6:].count('B')==2 and 'B' not in row['Bounce String'] [-1:]:
        return "Medium Risk"
    else:
        return "High Risk"


# In[85]:


data['Risk_Category'] = data.apply(Risk_Category,axis = 1)


# In[86]:


data.head(5)


# In[87]:


data[data.Risk_Category == 'High Risk']. head(10)


# In[90]:


data['Tenure'].unique()


# In[95]:


data.drop(columns = ['risk_category'], inplace = True)


# In[96]:


data['Repaid_Count'] = data['Bounce String'].apply(lambda x: len(x))


# In[97]:


data.head(5)


# In[69]:


data['Repaid_Count'].value_counts()


# In[77]:


def Tenure_Status (row):
    if row['Repaid_Count'] <= 3:
        return "Early Tenure"
    elif row['Tenure'] - row['Repaid_Count'] <= 3:
        return "Late Tenure"
    else:
        return "Mid Tenure"


# In[78]:


data['Tenure_Status'] = data.apply(Tenure_Status , axis = 1)


# In[98]:


data.head(5)


# In[99]:


data[data.Tenure_Status == 'Late Tenure'] .head()


# In[107]:


def Ticket_Size (row):
    if row['Amount Pending'] <= 3000:
        return 'Low ticket size'
    elif row['Amount Pending'] > 3000 and row['Amount Pending'] <=5000:
        return 'Medium ticket size'
    else:
        return 'High ticket size'


# In[108]:


data['Ticket_Size'] = data.apply(Ticket_Size, axis = 1)


# In[109]:


data['Ticket_Size'] . value_counts()


# In[124]:


def Loan_Range (row):
    if row['Disbursed Amount'] <=20000:
        return 'Low EMI'
    elif row['Disbursed Amount'] >20000 and row['Disbursed Amount'] <=50000:
        return 'Medium EMI'
    else:
        return 'High EMI'
    
data['Loan_Range'] = data.apply(Loan_Range, axis = 1)

data['Loan_Range']. value_counts()


# In[137]:


def Channel (row):
    if row['Bounce String'].count('S') + row['Bounce String'].count('H') >3     or row['Bounce String'] == 'FEMI' or row['Loan_Range'] == 'Low EMI':
        return 'Whatsapp bot'
    elif row['City'] in ('Bangalore','Chennai','Mumbai','Hyderabad','Kolkata','Delhi')     and row['Interest Rate'] <=5 and row['State'] in ('Madhya Pradesh','Maharashtra')    and row['Bounce String'].count('B') + row['Bounce String'].count('L') <=2    and row['Loan_Range'] in ('Low EMI','Medium EMI'):
        return 'Voice bot'
    elif row['Bounce String'].count('B') + row['Bounce String'].count('L') >2     or 'B' in row['Bounce String'][-2:] or 'L' in row['Bounce String'][-2:] or 'BL' in row['Bounce String'][-2:]    or 'LB' in row['Bounce String'][-2:]:
        return 'Human calling (Necessary)'
    else:
        return 'Human calling (Optional)'

data['Channel'] = data.apply(Channel,axis = 1)
data.head()
data['Channel']. value_counts() 


# In[138]:


def Channel_Cost(row):
    if row['Channel'] == 'Whatsapp bot':
        return 5
    elif row['Channel'] == 'Voice bot':
        return 10
    else:
        return 50
    
data['Channel_Cost'] = data.apply(Channel_Cost, axis = 1)
data.head()


# In[152]:


data['Tenure Complete Balance'] = data['Tenure'] - data['Repaid_Count']


# In[160]:


data[data['Tenure Complete Balance'] == 1].head()


# In[143]:


import matplotlib.pyplot as plt


# In[172]:


#summary of borrowers (with graphs) based on risk

risk_summary = data['Risk_Category'].value_counts()

# Plotting
plt.figure(figsize=(8, 6))
ax = risk_summary.plot(kind='bar', color='skyblue')
plt.title('Summary of Borrowers Based on Risk')
plt.xlabel('Risk Category')
plt.ylabel('Number of Borrowers')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Annotate bars with counts
for i, count in enumerate(risk_summary):
    ax.text(i, count, str(count), ha='center', va='bottom')

plt.show()


# In[170]:


#summary of borrowers based on ticket sizes

Ticket_size_summary = data['Ticket_Size'].value_counts()

# Plotting
plt.figure(figsize=(8, 8))
plt.pie(Ticket_size_summary, labels=Ticket_size_summary.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Borrowers Based on Ticket Sizes')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()


# In[171]:


#Summary of borrowers based on tenure completion

tenure_completion_summary = data['Tenure_Status'].value_counts()

# Plotting
plt.figure(figsize=(8, 6))
ax = tenure_completion_summary.plot(kind='bar', color='skyblue')
plt.title('Summary of borrowers based on tenure completion')
plt.xlabel('Tenure Period')
plt.ylabel('Number of Borrowers')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Annotate bars with counts
for i, count in enumerate(tenure_completion_summary):
    ax.text(i, count, str(count), ha='center', va='bottom')

plt.show()


# In[168]:


# Spend recommendation for borrowers

Channel_spending = data.groupby('Channel')['Channel_Cost'].sum()

# Plotting
plt.figure(figsize=(8, 6))
ax = Channel_spending.plot(kind='bar', color='skyblue')
plt.title('Spend recommendation for borrowers')
plt.xlabel('Channel')
plt.ylabel('Total Spent')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Annotate bars with counts
for i, count in enumerate(Channel_spending):
    ax.text(i, count, str(count), ha='center', va='bottom')


# In[169]:


#Loan Range Distributed to Borrowers

Loan_Range_Summary = data['Loan_Range'].value_counts()

# Plotting
plt.figure(figsize=(8, 8))
plt.pie(Loan_Range_Summary, labels=Loan_Range_Summary.index, autopct='%1.1f%%', startangle=140)
plt.title('Loan Range Distributed to Borrowers')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()

