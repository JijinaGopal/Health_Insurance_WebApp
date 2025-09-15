# import the streamlit library
import streamlit as st

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

import warnings
warnings.filterwarnings("ignore")


@st.cache_data

@st.cache_data
def load_csv():
    df = pd.read_csv(r"C:\Users\Administrator\Desktop\Internship\Insurance_Operations\Health Insurance Claims\Streamlit_App\health_insurance_dataset.csv")
    return df

df = load_csv()

df["ClaimDate"] = pd.to_datetime(df["ClaimDate"], errors="coerce")


# credentials dictionary
USER_CREDENTIALS = {
    "admin": "admin123",
    "user": "user123"
}

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False


def login():
    st.header("🔐 Welcome to your Insurance Dashboard")

    username = st.text_input("Username",key="login_username_input")
    password = st.text_input("Password", type="password", key="login_password_input")
    login_button = st.button("Login", key="login_button_input")


    if login_button:
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["authenticated"] = True
            st.success(f"Welcome, {username}!")
            st.rerun()
    
        else:
            st.error("Invalid username or password")


def main_app():


    st.sidebar.title("🧭 Navigation")
    selection = st.sidebar.radio("Go to Section",["Home Page","Key Metrics","Analysis"])


    if selection == "Home Page":
        st.markdown(""" 
### 🛡️ Industry Context:
In the health insurance sector, claims represent a major cost driver, requiring swift and accurate evaluation to reduce fraud, ensure fair reimbursements, and manage customer risk. Traditional manual and rule-based approaches are often inefficient and reactive. By leveraging historical claims data—including demographics, provider details, diagnoses, and claim amounts—insurers can adopt a proactive strategy to identify patterns, automate risk assessments, and optimize cost allocation.
                    
### 🎯 Objectives
- Monitor key performance metrics
- Enhance operational efficiency and financial sustainability
- Analyzing patterns in claim submissions, identifying cost-driving factors etc:      
       """)
        



    if selection == "Key Metrics":
        st.header("📊 Performance at a Glance")
        

        # Extract Year for filtering
        df["Year"] = df["ClaimDate"].dt.year

        # Extract Month for filtering
        df["month"] = df["ClaimDate"].dt.month_name()
        month_order = ["January", "February", "March", "April", "May", "June","July", "August", "September", "October", "November", "December"]
        df["month"] = pd.Categorical(df["month"],categories=month_order,ordered=True)




        # Filter options
        Year= df["Year"].dropna().sort_values().unique()
        Month =df["month"].dropna().sort_values().unique()
        Claim_Status=df["ClaimStatus"].dropna().unique()
        Claim_Type=df["ClaimType"].dropna().unique()
        Patient_Gender=df["PatientGender"].dropna().unique()
        Provider_Speciality=df["ProviderSpecialty"].dropna().unique()
        Patient_Employment_Status=df["PatientEmploymentStatus"].dropna().unique()
        Marital_Status=df["PatientMaritalStatus"].dropna().unique()
        Provider_Location=df["ProviderLocation"].dropna().unique()


        st.sidebar.title("🔍 Filters")
        selected_years = st.sidebar.multiselect("Year", Year)

        selected_months = st.sidebar.multiselect("Month", Month)
        
        selected_status = st.sidebar.multiselect("Claim Status", Claim_Status)

        selected_types = st.sidebar.multiselect("Claim Type", Claim_Type)
        
        selected_gender = st.sidebar.multiselect("Patient Gender", Patient_Gender)

        selected_employmentstatus = st.sidebar.multiselect("Patient Employment Status",Patient_Employment_Status)

        selected_maritalstatus = st.sidebar.multiselect("Marital Status",Marital_Status)
        
        selected_providerspeciality=st.sidebar.multiselect("Provider Speciality",Provider_Speciality)

        selected_providerlocation = st.sidebar.multiselect("Provider Location",Provider_Location)



        # Apply filters
        final_df = df.copy()
        if selected_years:
            final_df = final_df[final_df["year"].isin(selected_years)]
        if selected_months:
            final_df = final_df[final_df["month"].isin(selected_months)]
        if selected_status:
            final_df = final_df[final_df["product_name"].isin(selected_status)]
        if  selected_types:
            final_df = final_df[final_df["utm_source"].isin( selected_types)]
        if selected_gender:
            final_df = final_df[final_df["utm_campaign"].isin(selected_gender)]
        if selected_employmentstatus:
            final_df = final_df[final_df["device_type"].isin(selected_employmentstatus)]
        if selected_maritalstatus:
            final_df = final_df[final_df["device_type"].isin(selected_maritalstatus)]
        if selected_providerspeciality:
            final_df = final_df[final_df["device_type"].isin(selected_providerspeciality)]
        if selected_providerlocation:
            final_df = final_df[final_df["device_type"].isin(selected_providerlocation)]



        st.subheader("📌 Key Metrics")
        # ✅ KPI Calculations

        Total_Claims=final_df['ClaimID'].count()
        Total_Claims_Amount=final_df['ClaimAmount'].sum()/1000000
        Average_Claim_Amount=final_df['ClaimAmount'].mean()
        Total_Providers=final_df['ProviderID'].count()
        Average_Patient_Age=df['PatientAge'].mean()
        Claim_Approval_Rate=df[df['ClaimStatus']=='approved'].count()/final_df['ClaimID'].count()*100
        Claim_Denial_Rate=df[df['ClaimStatus']=='Denied'].count()/final_df['ClaimID'].count()*100
        Claim_Pending_Rate=df[df['ClaimStatus']=='Pending'].count()/final_df['ClaimID'].count()*100
        Income_vs_ClaimAmout_Correlation=df['PatientIncome'].corr(df['ClaimAmount'])


        col1, col2, col3 = st.columns(3)
        
        col1.metric("🎯 Total Claims", Total_Claims)
        col2.metric("💰 Total Claim Amount",f"${Total_Claims_Amount:,.2f} M")
        col3.metric("💰 Average Claim Amount",f"${Average_Claim_Amount:,.2f}")


    



    if st.button("Logout"):
        st.session_state["authenticated"] = False

# Run app
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
else:
    main_app()