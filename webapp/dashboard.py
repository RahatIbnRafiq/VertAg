import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import auth
import constants



def generate_mini_trend(shelf_id, df):
    shelf_trend = df[df["shelf_id"] == shelf_id].sort_values("date").tail(7)
    fig, ax = plt.subplots(figsize=(5, 0.4))
    sns.lineplot(data=shelf_trend, x="date", y="health_percentage", ax=ax, marker="o", color="blue", linewidth=1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.grid(False)
    st.pyplot(fig)

@st.cache_data
def load_health_data():
    df = pd.read_csv(constants.DATA_PATH)

    df["health_percentage"] = pd.to_numeric(df["health_percentage"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"])
    df["shelf_id"] = df["shelf_id"].astype(str)
    return df


def overall_health(df):
    overall_health = df.groupby("date")["health_percentage"].mean().iloc[-1]
    st.metric(label=constants.FARM_HEALTH_TITLE, value=f"{overall_health:.2f} %")
    

def health_trend_plot_shelves(df):
    st.subheader(constants.HEALTH_TREND_TITLE)
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



def health_shelves_table(df):
    st.subheader(constants.SHELF_OVERVIEW_TITLE)

    # Get the most recent health data for each shelf
    latest_date = df["date"].max()
    latest_shelf_data = df[df["date"] == latest_date][["shelf_id", "health_percentage"]]



    import streamlit.components.v1 as components

    st.markdown(constants.HOVER_TABLE_STYLE, unsafe_allow_html=True)

    # Create an interactive table where rows are clickable
    for _, row in latest_shelf_data.iterrows():
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button(f"📋 Shelf {row['shelf_id']}", key=f"shelf_{row['shelf_id']}"):
                st.session_state["selected_shelf"] = row["shelf_id"]
                st.switch_page("shelf_detail.py")
        col2.metric(constants.HEALTH_METRIC_LABEL, f"{row['health_percentage']:.1f}")
        with col3:
            generate_mini_trend(row["shelf_id"], df)



def greet_dashboard():
    st.title(constants.APP_TITLE)
    st.write(constants.WELCOME_MESSAGE.format(username=st.session_state['username']))
    
    

def show_dashboard():
    auth.require_authentication()

    greet_dashboard()

    df = load_health_data()

    overall_health(df)

    health_trend_plot_shelves(df)
    
    health_shelves_table(df)
    
    
    
    
    