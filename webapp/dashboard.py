import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import auth 

data_path = "/Users/rahatibnrafiq/startups/vertical farming ai/VertAg/webapp/data/health_data.csv"

def show_dashboard():
    auth.require_authentication()

    st.title("Farm Monitoring Dashboard")
    st.write(f"Welcome, {st.session_state['username']}!")

    @st.cache_data
    def load_health_data():
        df = pd.read_csv(data_path)

        df["health_percentage"] = pd.to_numeric(df["health_percentage"], errors="coerce")
        df["date"] = pd.to_datetime(df["date"])
        df["shelf_id"] = df["shelf_id"].astype(str)
        return df

    df = load_health_data()

    overall_health = df.groupby("date")["health_percentage"].mean().iloc[-1]

    st.metric(label="Overall Farm Health", value=f"{overall_health:.2f} %")

    st.subheader("Farm Health Trend Over Time")
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot using seaborn
    sns.lineplot(
        data=df, 
        x="date", 
        y="health_percentage", 
        hue="shelf_id",  
        marker="o", 
        ax=ax
    )

    # Improve the aesthetics of the plot
    ax.set_title("Health Trend for Each Shelf", fontsize=14)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Health Percentage", fontsize=12)
    ax.legend(title="Shelf ID")
    ax.grid(True)

    # Show the plot in Streamlit
    st.pyplot(fig)
