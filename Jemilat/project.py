import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st  


# Load your dataset
df = pd.read_csv("Jemilat.csv")


st.set_page_config(layout="wide")
st.title("Incident Analysis Dashboard")



#- 1 Is there a correlation between the type of incident and the number of deaths?

st.subheader("Is there a correlation between the type of incident and the number of deaths?")
# Get top 10 states by frequency
state_counts = df["State"].value_counts().nlargest(10)

# Create figure and axis
fig, ax = plt.subplots(figsize=(6,6))
ax.pie(state_counts, labels=state_counts.index, autopct='%1.1f%%')
ax.set_title("Top 10 States Distribution")

# Pass the figure to Streamlit
st.pyplot(fig)
st.markdown(f"""
The pie chart shows that the top 10 states account for the majority of recorded incidents,
             with a few states dominating the distribution.
             This suggests that certain regions experience disproportionately higher frequencies of incidents compared to others.
""")


#2  Which states report the highest number of deaths across incidents?

st.subheader("Which states report the highest number of deaths across incidents?")
fig1 = sns.catplot(x="State", kind="count", data=df, height=8, aspect=2, palette="Set2")
fig1.set_axis_labels("State", "Number of Incidents", fontsize=14)
fig1.set_xticklabels(rotation=45, fontsize=12)
fig1.set_yticklabels(fontsize=12)
fig1.fig.suptitle("Incidents by State", fontsize=18)
st.pyplot(fig1.fig)
st.markdown(f"""The chart shows that some states report far more incidents than others,
             with a few clearly standing out. This highlights that the distribution of deaths is uneven across states,
             suggesting certain regions are more heavily impacted)
""")


#3 Which states have the highest total number of deaths?

st.subheader("Which states have the highest total number of deaths?")
# Count incidents per state
state_counts = df["State"].value_counts().reset_index()
state_counts.columns = ["State", "Incident Count"]

# Select top 10 states
top_state_counts = state_counts.nlargest(10, "Incident Count")

# Plot
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=top_state_counts.sort_values("Incident Count", ascending=True),  # sort for readability
    x="Incident Count",
    y="State",
    palette="Set3",
    ax=ax2
)
ax2.set_title("Top 10 States by Incident Frequency")
ax2.set_xlabel("Number of Incidents")
ax2.set_ylabel("State")

st.pyplot(fig2)   # ✅ Use st.pyplot instead of plt.show()
st.markdown(f"""The bar chart highlights that a few states report significantly more incidents than others,
             making them stand out as the most impacted. The boxplot shows that certain incident types tend 
            to last much longer, indicating that duration varies widely depending on the nature of the event.
""")

# 4 Are certain incident types associated with longer durations?

st.subheader("Are certain incident types associated with longer durations?")
# Ensure datetime conversion
df['Start date'] = pd.to_datetime(df['Start date'])
df['End date'] = pd.to_datetime(df['End date'])

# Calculate duration in days
df['Duration'] = (df['End date'] - df['Start date']).dt.days

# Compute average duration per incident type
incident_duration = df.groupby("Incident", as_index=False)["Duration"].mean()

# Select top 10 incident types with longest average duration
top_incidents = incident_duration.nlargest(10, "Duration")["Incident"]

# Filter dataset to only those top incidents
df_top = df[df["Incident"].isin(top_incidents)]

# Boxplot of duration by incident type (top 10)
fig, ax = plt.subplots(figsize=(12,6))
sns.boxplot(x="Incident", y="Duration", data=df_top, palette="Set2", ax=ax)
ax.set_title("Top 10 Incident Types by Duration")
ax.set_xlabel("Incident Type")
ax.set_ylabel("Duration (days)")
plt.xticks(rotation=45)

st.pyplot(fig)
st.markdown(f""" The boxplot highlights the top 10 incident types with the longest average durations.
            It shows that some incident categories consistently last much longer than others, 
            indicating that duration is strongly influenced by the type of incident
 """)


# 5 Do certain states experience higher deaths relative to incident frequency?

st.subheader("Do certain states experience higher deaths relative to incident frequency?")
# Aggregate deaths and incident counts per state
state_stats = df.groupby("State").agg(
    IncidentCount=("Identifier","count"),
    TotalDeaths=("Number of deaths","sum")
).reset_index()

# Scatter plot: Incident frequency vs deaths
fig2, ax2 = plt.subplots(figsize=(8,6))
sns.scatterplot(data=state_stats, x="IncidentCount", y="TotalDeaths", ax=ax2)
ax2.set_title("Deaths vs Incident Frequency per State")
ax2.set_xlabel("Incident Frequency")
ax2.set_ylabel("Total Deaths")
st.pyplot(fig2)

st.markdown(f"""The scatter plot shows that states with more incidents generally report higher total deaths,
             suggesting a positive relationship between frequency and fatalities.
             However, some states stand out as outliers,
             experiencing disproportionately high deaths compared to their incident counts
""")


# 6 What is the trend of incidents over time (based on start date)?

st.subheader("What is the trend of incidents over time (based on start date)?")
# Ensure datetime conversion
df['Start date'] = pd.to_datetime(df['Start date'])
df['End date'] = pd.to_datetime(df['End date'])

# Create Year column from Start date
df['Year'] = df['Start date'].dt.year

# Aggregate total deaths per year
yearly_deaths = df.groupby("Year")["Number of deaths"].sum().reset_index()

# Line chart: Deaths over time
fig, ax = plt.subplots(figsize=(10,6))
sns.lineplot(
    data=yearly_deaths,
    x="Year",
    y="Number of deaths",
    marker="o",
    ax=ax
)
ax.set_title("Total Deaths Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Deaths")

st.pyplot(fig)

# --- Summary section ---
total_deaths = yearly_deaths["Number of deaths"].sum()
peak_year = yearly_deaths.loc[yearly_deaths["Number of deaths"].idxmax(), "Year"]
peak_value = yearly_deaths["Number of deaths"].max()

st.markdown(f"""
### 📊 Summary
- **Total deaths across all years:** {total_deaths}
- **Year with highest deaths:** {peak_year} ({peak_value} deaths)
- **Trend insight:** The line chart shows how fatalities vary year by year, highlighting spikes and declines.
""")


# 7. How do deaths vary across states?
fig3, ax3 = plt.subplots(figsize=(14,6))
sns.violinplot(
    data=df,
    x="State",
    y="Number of deaths",
    palette="Set1",
    ax=ax3
)
ax3.set_title("Distribution of Deaths by State")
ax3.set_xlabel("State")
ax3.set_ylabel("Number of Deaths")
plt.xticks(rotation=90)
st.pyplot(fig3)

# --- Simple Summary ---
total_deaths = df["Number of deaths"].sum()
avg_deaths = df["Number of deaths"].mean()
max_state = df.groupby("State")["Number of deaths"].sum().idxmax()
max_value = df.groupby("State")["Number of deaths"].sum().max()

st.markdown(f"""
### 📊 Summary
- **Total deaths recorded:** {total_deaths}
- **Average deaths per incident:** {avg_deaths:.1f}
- **State with highest total deaths:** {max_state} ({max_value} deaths)
""")







# Sidebar filters
st.sidebar.header("Filters")

# Dropdown for State
state_filter = st.sidebar.selectbox(
    "Select State",
    options=df["State"].unique()
)

# Dropdown for Incident
incident_filter = st.sidebar.selectbox(
    "Select Incident",
    options=df["Incident"].unique()
)

# Apply filters
filtered_df = df[
    (df["State"] == state_filter) &
    (df["Incident"] == incident_filter)
]

# Display results
st.write("### Filtered Data")
st.dataframe(filtered_df)