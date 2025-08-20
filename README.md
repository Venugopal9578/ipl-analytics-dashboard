# 🏆 The Ultimate IPL Analytics Dashboard

An interactive data analysis dashboard for the Indian Premier League (IPL) from 2008-2020. This application allows users to explore player statistics, team head-to-head records, and venue-specific insights.

**[➡️ View the Live Demo Here](https://ipl-analytics-dashboard-udnap.streamlit.app/)**


---

## ✨ Features

This dashboard is divided into three main sections for comprehensive analysis:

* **Player Performance Analysis:**
    * Select any batsman from the dropdown menu.
    * View key performance metrics like Total Runs, Strike Rate, Batting Average, and number of Dismissals.
    * Visualize the player's run-scoring trends season by season with a dynamic bar chart.

* **Team vs. Team Head-to-Head:**
    * Select two different teams to compare their historical performance.
    * Instantly see the total matches played and the number of wins for each team.
    * View a summary table of the last 5 encounters between the selected teams.

* **Venue Insights:**
    * Choose any stadium from the dropdown list.
    * See the total number of matches hosted at that venue.
    * Analyze the impact of the coin toss with a pie chart showing the percentage of teams that choose to bat or field.
    * Discover the percentage of matches won by the team that wins the toss at that specific venue.

---

## 🛠️ Technologies Used

* **Language:** Python
* **Libraries:**
    * **Streamlit:** For creating the interactive web application.
    * **Pandas:** For data manipulation and cleaning.
    * **Matplotlib & Seaborn:** For data visualization and plotting.

---

## 🚀 How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Venugopal9578/ipl-analytics-dashboard.git](https://github.com/Venugopal9578/ipl-analytics-dashboard.git)
    ```
2.  **Navigate into the project directory:**
    ```bash
    cd ipl-analytics-dashboard
    ```
3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
