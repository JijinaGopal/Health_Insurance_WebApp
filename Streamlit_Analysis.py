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
        Claim_Approval_Rate=(df[df['ClaimStatus']=='Approved'].shape[0]/final_df['ClaimID'].count())*100
        Claim_Denial_Rate=(df[df['ClaimStatus']=='Denied'].shape[0]/final_df['ClaimID'].count())*100
        Claim_Pending_Rate=(df[df['ClaimStatus']=='Pending'].shape[0]/final_df['ClaimID'].count())*100
        Income_vs_ClaimAmout_Correlation=df['PatientIncome'].corr(df['ClaimAmount'])


        col1, col2, col3 = st.columns(3)
        
        col1.metric("🎯 Total Claims", Total_Claims)
        col2.metric("💰 Total Claim Amount",f"${Total_Claims_Amount:,.2f} M")
        col3.metric("💰 Average Claim Amount",f"${Average_Claim_Amount:,.2f}")


        col4, col5, col6 = st.columns(3)
        
        col4.metric("👥 Total Providers", Total_Providers)
        col5.metric("👤 Average Patient Age",f"{Average_Patient_Age:,.0f}")
        col6.metric("❌ Claim Deniel Rate",f"{Claim_Denial_Rate:,.2f}%")


        col7, col8, col9 = st.columns(3)
        
        col7.metric("✅ Claim Approved Rate", f"{Claim_Approval_Rate:,.2f}%")
        col8.metric("🔄 Claim Pending Rate",f"{Claim_Pending_Rate:,.2f}%")
        col9.metric("💹 Income vs Claim Amount Correlation",f"{Income_vs_ClaimAmout_Correlation:,.2f}")



    elif selection == "Analysis":
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


        st.markdown("### 📊 Claim Count by Status")
        Claim_status=df.groupby('ClaimStatus')['ClaimID'].count().reset_index()
        Claim_status.columns = ['Claim Status', 'Claim Count']
        st.dataframe(Claim_status)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=Claim_status,x='Claim Status',y='Claim Count',color='skyblue',ax=ax)

        for i, row in Claim_status.iterrows():
            ax.text(i,row["Claim Count"],str(int(row["Claim Count"])),ha='center',va='bottom',fontsize=9)

        ax.set_title('Claim Count by Status', fontsize=16)
        ax.set_xlabel('Claim Status', fontsize=12)
        ax.set_ylabel('Claim Count', fontsize=12)
        plt.tight_layout()
        st.pyplot(fig)



        st.markdown("---")
        st.markdown("### 🎯 Claim Count by Type")
        Claim_Type=df.groupby('ClaimType')['ClaimID'].count().reset_index()
        Claim_Type.columns = ['Claim_Type', 'Claim Count']
        st.dataframe(Claim_Type)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=Claim_Type,x='Claim_Type',y='Claim Count',color='lightgreen',ax=ax)

        for index, row in Claim_Type.iterrows():
            ax.text(index,row["Claim Count"],str(int(row["Claim Count"])),ha='center',va='bottom',fontsize=9)

        ax.set_title('Claim Count by Type', fontsize=16)
        ax.set_xlabel('Claim_Type', fontsize=12)
        ax.set_ylabel('Claim Count', fontsize=12)
        plt.tight_layout()
        st.pyplot(fig)





        st.markdown("---")
        st.markdown("### 💰 Average Claim Amount by Type")
        
        
        Claim_Type = df.groupby('ClaimType')['ClaimAmount'].mean().reset_index()
        Claim_Type.columns = ['Claim Type', 'Average Claim Amount']
        Claim_Type = Claim_Type.sort_values(by='Average Claim Amount', ascending=False)
        st.dataframe(Claim_Type)

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(Claim_Type['Claim Type'], Claim_Type['Average Claim Amount'], color='skyblue')

        
        for i, value in enumerate(Claim_Type['Average Claim Amount']):
             ax.text(i, value, f"{value:.2f}", ha='center', va='bottom', fontsize=9)

        
        ax.set_title('Average Claim Amount by Type', fontsize=14)
        ax.set_xlabel('Claim Type', fontsize=12)
        ax.set_ylabel('Average Claim Amount', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()

       
        st.pyplot(fig)




        st.markdown("---")
        st.markdown("### 📬 Claim Count by Submission Method")

        Claim_Submission_method = df.groupby('ClaimSubmissionMethod')['ClaimID'].count().reset_index()
        Claim_Submission_method.columns = ['Submission Method', 'Claim Count']
        Claim_Submission_method = Claim_Submission_method.sort_values(by='Claim Count', ascending=False)



        st.dataframe(Claim_Submission_method)

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bars = ax.bar(Claim_Submission_method['Submission Method'], Claim_Submission_method['Claim Count'], color='lightgreen')

        # Annotate each bar
        for i, value in enumerate(Claim_Submission_method['Claim Count']):
            ax.text(i, value, str(value), ha='center', va='bottom', fontsize=9)

        # Styling
        ax.set_title('Claim Count by Submission Method', fontsize=14)
        ax.set_xlabel('Submission Method', fontsize=12)
        ax.set_ylabel('Number of Claims', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Show plot in Streamlit
        st.pyplot(fig)




        st.markdown("---")
        st.markdown("### 👥 Claims by Gender")

        Gender_distribution = df.groupby('PatientGender')['ClaimID'].count().reset_index()
        Gender_distribution.columns = ['Gender', 'Claim Count']


        st.dataframe(Gender_distribution)

        # Plotting
        fig, ax = plt.subplots(figsize=(2, 2))
        ax.pie(Gender_distribution['Claim Count'],labels=Gender_distribution['Gender'],colors=['blue', 'orange'],
        autopct='%1.2f%%',startangle=90,textprops={'fontsize': 4})
        ax.set_title('Claims by Gender', fontsize=6)

        # Show plot in Streamlit
        st.pyplot(fig)



        st.markdown("---")
        st.markdown("### 🩺 Average Claim Amount by Provider Specialty")

        Avg_claimamount_providerspeciality = df.groupby('ProviderSpecialty')['ClaimAmount'].mean().reset_index()
        Avg_claimamount_providerspeciality.columns = ['Provider Specialty', 'Avg Claim Amount']
        Avg_claimamount_providerspeciality = Avg_claimamount_providerspeciality.sort_values(by='Avg Claim Amount', ascending=False)



        st.dataframe(Avg_claimamount_providerspeciality)

        # Plotting
        fig, ax = plt.subplots(figsize=(12, 8))
        bars = ax.bar(Avg_claimamount_providerspeciality['Provider Specialty'],Avg_claimamount_providerspeciality['Avg Claim Amount'],
        color='skyblue')

        # Annotate each bar
        for i, value in enumerate(Avg_claimamount_providerspeciality['Avg Claim Amount']):
            ax.text(i, value, f"{value:.2f}", ha='center', va='bottom', fontsize=9)

        # Styling
        ax.set_title('Average Claim Amount by Provider Specialty', fontsize=16)
        ax.set_xlabel('Provider Specialty', fontsize=12)
        ax.set_ylabel('Average Claim Amount', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Show plot in Streamlit
        st.pyplot(fig)



        st.markdown("---")
        st.markdown("### 🧾 Top 5 Diagnosis Codes by Average Claim Amount")
        Avg_claimamount_Diagnosiscode = (df.groupby('DiagnosisCode')['ClaimAmount'].mean()
        .reset_index(name="Avg Claim Amount").sort_values(by="Avg Claim Amount", ascending=False).head(5))

        st.dataframe(Avg_claimamount_Diagnosiscode)

        # Plotting
        fig, ax = plt.subplots(figsize=(8, 6))
        bars = ax.bar(Avg_claimamount_Diagnosiscode['DiagnosisCode'],Avg_claimamount_Diagnosiscode['Avg Claim Amount'],color='lightgreen')

        # Annotate each bar
        for i, value in enumerate(Avg_claimamount_Diagnosiscode['Avg Claim Amount']):
            ax.text(i, value, f"{value:.2f}", ha='center', va='bottom', fontsize=9)

        # Styling
        ax.set_title('Top 5 Diagnosis Codes by Average Claim Amount', fontsize=14)
        ax.set_xlabel('Diagnosis Code', fontsize=12)
        ax.set_ylabel('Average Claim Amount', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()

        
        st.pyplot(fig)






        st.markdown("---")
        st.markdown("### 🧪 Top 5 Procedure Codes by Average Claim Amount")

        Avg_claimamount_procedurecode = (df.groupby('ProcedureCode')['ClaimAmount'].mean().reset_index(name="Avg Claim Amount")
        .sort_values(by="Avg Claim Amount", ascending=False).head(5))

        st.dataframe(Avg_claimamount_procedurecode)

        # Plotting
        fig, ax = plt.subplots(figsize=(8, 6))
        bars = ax.bar(Avg_claimamount_procedurecode['ProcedureCode'],Avg_claimamount_procedurecode['Avg Claim Amount'],color='lightblue')

        # Annotate each bar
        for i, value in enumerate(Avg_claimamount_procedurecode['Avg Claim Amount']):
            ax.text(i, value, f"{value:.2f}", ha='center', va='bottom', fontsize=9)

        # Styling
        ax.set_title('Top 5 Procedure Codes by Average Claim Amount', fontsize=14)
        ax.set_xlabel('Procedure Code', fontsize=12)
        ax.set_ylabel('Average Claim Amount', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Show plot in Streamlit
        st.pyplot(fig)





        st.markdown("---")
        st.markdown("### 📤 Submission Method Efficiency")
        Submission_method_efficiency = ((df[df['ClaimStatus'] == 'Approved'].groupby('ClaimSubmissionMethod')['ClaimID'].count() /
        df.groupby('ClaimSubmissionMethod')['ClaimID'].count()) * 100).reset_index(name="Approval rate (%)")



        st.dataframe(Submission_method_efficiency)

        # Plotting
        fig, ax = plt.subplots(figsize=(8, 6))
        colors = ['orange', 'lightblue', 'lightgreen'][:len(Submission_method_efficiency)]
        bars = ax.bar(Submission_method_efficiency['ClaimSubmissionMethod'],Submission_method_efficiency['Approval rate (%)'],color=colors)

        # Annotate each bar
        for i, value in enumerate(Submission_method_efficiency['Approval rate (%)']):
            ax.text(i, value, f"{value:.2f}%", ha='center', va='bottom', fontsize=9)

        # Styling
        ax.set_title('Submission Method Efficiency', fontsize=14)
        ax.set_xlabel('Claim Submission Method', fontsize=12)
        ax.set_ylabel('Approval Rate (%)', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Show plot in Streamlit
        st.pyplot(fig)







    if st.button("Logout"):
        st.session_state["authenticated"] = False

# Run app
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
else:
    main_app()