# Import all the necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="IPL Performance Dashboard")

# --- Data Loading and Caching ---
@st.cache_data
def load_data():
    match_df = pd.read_csv('matches.csv')
    ball_df = pd.read_csv('deliveries.csv')

    # --- Data Cleaning and Preprocessing ---
    match_df['team1'] = match_df['team1'].str.replace('Delhi Daredevils', 'Delhi Capitals')
    match_df['team2'] = match_df['team2'].str.replace('Delhi Daredevils', 'Delhi Capitals')
    match_df['winner'] = match_df['winner'].str.replace('Delhi Daredevils', 'Delhi Capitals')

    match_df['team1'] = match_df['team1'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
    match_df['team2'] = match_df['team2'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
    match_df['winner'] = match_df['winner'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')

    # Merge match-level info with ball-by-ball details
    complete_df = match_df.merge(ball_df, left_on='id', right_on='match_id')

    return match_df, complete_df

# Load the data
match_data, complete_data = load_data()

# --- Sidebar Filters ---
st.sidebar.title('IPL Performance Analyzer')

analysis_type = st.sidebar.radio(
    "Select Analysis Type",
    ('Player Performance', 'Team vs. Team', 'Venue Insights')
)

# --- Main Page Content ---
st.title('🏆 The Ultimate IPL Performance Dashboard')

# --- Player Performance Analysis ---
if analysis_type == 'Player Performance':
    st.header('Player Performance Analysis')

    # Use 'batter' column (your dataset uses this)
    all_players = sorted(complete_data['batter'].unique())
    selected_player = st.selectbox('Select a Batsman', all_players)

    player_df = complete_data[complete_data['batter'] == selected_player]

    # --- Player Stats ---
    total_runs = player_df['batsman_runs'].sum()

    # some datasets have wide_runs, some don't → safe handling
    if 'wide_runs' in player_df.columns:
        total_balls_faced = player_df[player_df['wide_runs'] == 0].shape[0]
    else:
        total_balls_faced = player_df.shape[0]

    strike_rate = round((total_runs / total_balls_faced) * 100, 2) if total_balls_faced > 0 else 0
    num_dismissals = player_df[player_df['player_dismissed'] == selected_player].shape[0]
    average = round(total_runs / num_dismissals, 2) if num_dismissals > 0 else 'N/A'

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Runs", total_runs)
    with col2:
        st.metric("Strike Rate", strike_rate)
    with col3:
        st.metric("Batting Average", average)
    with col4:
        st.metric("Dismissals", num_dismissals)

    # --- Runs per Season ---
    st.subheader(f'Runs Scored by {selected_player} per Season')
    runs_per_season = player_df.groupby('season')['batsman_runs'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='season', y='batsman_runs', data=runs_per_season, ax=ax, palette='viridis')
    ax.set_title(f'Seasonal Performance of {selected_player}')
    ax.set_xlabel('Season')
    ax.set_ylabel('Total Runs')
    st.pyplot(fig)

# --- Team vs. Team Analysis ---
elif analysis_type == 'Team vs. Team':
    st.header('Team vs. Team Head-to-Head Analysis')

    all_teams = sorted(match_data['team1'].unique())

    col1, col2 = st.columns(2)
    with col1:
        team1 = st.selectbox('Select Team 1', all_teams, index=0)
    with col2:
        team2 = st.selectbox('Select Team 2', all_teams, index=1)

    if team1 and team2 and team1 != team2:
        head_to_head_df = match_data[
            ((match_data['team1'] == team1) & (match_data['team2'] == team2)) |
            ((match_data['team1'] == team2) & (match_data['team2'] == team1))
        ]

        team1_wins = head_to_head_df[head_to_head_df['winner'] == team1].shape[0]
        team2_wins = head_to_head_df[head_to_head_df['winner'] == team2].shape[0]
        total_matches = head_to_head_df.shape[0]

        st.subheader(f'Head-to-Head: {team1} vs. {team2}')
        st.metric("Total Matches Played", total_matches)

        win_data = pd.DataFrame({
            'Team': [team1, team2],
            'Wins': [team1_wins, team2_wins]
        })

        fig, ax = plt.subplots()
        sns.barplot(x='Team', y='Wins', data=win_data, ax=ax, palette='coolwarm')
        ax.set_title('Win Comparison')
        st.pyplot(fig)

        st.subheader('Last 5 Matches')
        last_5 = head_to_head_df.sort_values('date', ascending=False).head(5)
        st.dataframe(last_5[['date', 'winner', 'result', 'result_margin', 'venue']])

    elif team1 == team2:
        st.warning('Please select two different teams.')

# --- Venue Insights ---
elif analysis_type == 'Venue Insights':
    st.header('Venue Insights')

    all_venues = sorted(match_data['venue'].dropna().unique())
    selected_venue = st.selectbox('Select a Venue', all_venues)

    venue_df = match_data[match_data['venue'] == selected_venue]

    total_matches_at_venue = venue_df.shape[0]
    st.metric("Total Matches Hosted", total_matches_at_venue)

    st.subheader('Impact of Toss Decision')
    toss_decision_counts = venue_df['toss_decision'].value_counts()

    fig, ax = plt.subplots()
    ax.pie(toss_decision_counts, labels=toss_decision_counts.index, autopct='%1.1f%%',
           startangle=90, colors=['#ff9999', '#66b3ff'])
    ax.axis('equal')
    ax.set_title('Toss Decisions at this Venue')
    st.pyplot(fig)

    toss_winner_is_match_winner = venue_df[venue_df['toss_winner'] == venue_df['winner']].shape[0]
    win_percentage = round((toss_winner_is_match_winner / total_matches_at_venue) * 100, 2) if total_matches_at_venue > 0 else 0
    st.info(f"At {selected_venue}, the team that wins the toss also wins the match **{win_percentage}%** of the time.")
