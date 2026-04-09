# analysis page
# Importing
import streamlit as st  # Used to build the web app
import pandas as pd  # Used for data manipulation and analysis
import matplotlib.pyplot as plt  # Used for plotting graphs
import seaborn as sns  # Used for advanced visualizations
import sys
from pathlib import Path
# /Importing

# page configuration

st.set_page_config(
    page_title="AI personalized learning", 
    layout="wide",
    initial_sidebar_state="expanded"
    )

# /page configuration
# load & clean data
@st.cache_data
def load_and_clean_data() :
    # load data 
    df = pd.read_csv("AI_Personalized_Learning.csv")
    # data cleaning
    df_cleaned = df.copy()
    df_cleaned = df_cleaned.drop(columns=["gender"])
    df_cleaned['education_level'] = df_cleaned['education_level'].replace({'PG': 'Postgraduate', 'UG': 'Undergraduate'})
    df_cleaned['student_id'] = df_cleaned['student_id'].str.replace('STU', '').astype(int)
    df_cleaned['recommended_path'] = df_cleaned['recommended_path'].str.replace('→', '-', regex=False)
    df_cleaned['actual_path_followed'] = df_cleaned['actual_path_followed'].str.replace('→', '-', regex=False)
    df_cleaned['current_gpa'] = df_cleaned['final_assessment_score'] / 100 * 4
    df_cleaned['Followed_AI_Path'] = (df_cleaned['actual_path_followed'] == df_cleaned['recommended_path']).map({True: 'Yes', False: 'No'})
    # /data cleaning⬅
    return df, df_cleaned
df, df_cleaned = load_and_clean_data()

# visualization /plots
# Q1 : How Does different frequency of ai tools usage levels vary in the final score?
def create_fig1(filtered_df):
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    sns.boxplot(
        data=filtered_df, 
        x='Followed_AI_Path', 
        y='final_assessment_score', 
        palette='Purples', 
        ax=ax1
    )
    ax1.set_title('Quiz Scores: AI-Recommended Path vs. Manual Path', fontsize=14)
    ax1.set_xlabel('Followed AI-Recommended Path?', fontsize=12)
    ax1.set_ylabel('Quiz Score', fontsize=12)
    return fig1
# /Q1

# Q2 : Comparing bet. Students scores before and after AI personalized studying paths.
def create_fig2(filtered_df):
    df_melted = filtered_df.melt(id_vars=['student_id'],
                value_vars=['quiz_accuracy', 'final_assessment_score'],
                var_name='Phase',
                value_name='Score')
    sns.set_theme(style="whitegrid")
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.boxplot(
        data=df_melted,
        x='Phase', 
        y='Score', 
        palette='muted', 
        showfliers=False, 
        ax=ax2
    )
    sns.swarmplot(
        data=df_melted, 
        x='Phase', 
        y='Score', 
        color=".25", 
        alpha=0.6, 
        ax=ax2
    )
    ax2.set_title('Student Performance: Before vs. After AI Personalized Path')
    ax2.set_ylabel('Final Score (%)')
    ax2.set_xlabel('Study Phase')
    return fig2
# /Q2

# Q3 : What was the effect of taking the recommended path or not on the final score?
def create_fig3(filtered_df):
    sns.set_theme(style="whitegrid")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.violinplot(
        data=filtered_df, 
        x='actual_path_followed', 
        y='final_assessment_score', 
        palette="Set2", 
        split=True, 
        ax=ax3 
    )
    sns.swarmplot(
        data=filtered_df, 
        x='actual_path_followed', 
        y='final_assessment_score', 
        color="black", 
        alpha=0.3, 
        ax=ax3 
    )
    ax3.set_title('Effect of AI Path Adherence on Final Score', fontsize=14)
    ax3.set_xlabel('Followed AI Recommended Path?', fontsize=12)
    ax3.set_ylabel('Final Score (%)', fontsize=12)
    ax3.set_xticks([0, 1])
    ax3.set_xticklabels(['No (Deviated)', 'Yes (Followed)'])
    return fig3
# /Q3

# Q4 : Does following the AI-Recommended Path actually lead to higher Quiz Scores?
def create_fig4(filtered_df):
    fig4, ax4 = plt.subplots(figsize=(8, 6))
    sns.barplot(
        data=filtered_df, 
        x='Followed_AI_Path', 
        y='final_assessment_score', 
        ax=ax4
    )
    ax4.set_title('Impact of Following AI-Recommended Path on Quiz Scores')
    ax4.set_xlabel('Followed AI Recommendation?')
    ax4.set_ylabel('Final Quiz Score')
    return fig4
# /Q4

# Q5 : Which Learning Style completes more Difficult Modules and faster?
def create_fig5(filtered_df, difficulty):
    modules_difficulty = filtered_df[filtered_df['contextual_difficulty_level'].isin(difficulty)]
    fig5, ax5 = plt.subplots(1, 2, figsize=(16, 6))

    sns.countplot(
        data=modules_difficulty, 
        x='learning_style', 
        palette='viridis', 
        ax=ax5[0]
    )
    ax5[0].set_title('Quantity: Hard Modules Completed per Style')
    sns.barplot(
        data=modules_difficulty, 
        x='learning_style', 
        y='avg_time_per_module', 
        palette='magma', 
        ax=ax5[1]
    )
    ax5[1].set_title('Speed: Average Time on Hard Modules')
    plt.tight_layout()
    return fig5
# /Q5

# Q6 : Compare between the modules taken and the contextual difficulty for students with different learning types.
def create_fig6(filtered_df):
    difficulty_order = ['Easy', 'Medium', 'Hard']
    selected_dificulties = [diff for diff in difficulty_order if diff in filtered_df['contextual_difficulty_level'].unique()]
    filtered_df['contextual_difficulty_level'] = pd.Categorical(filtered_df['contextual_difficulty_level'],
                                            categories=selected_dificulties,
                                            ordered=True)   
    non_nan_filtered_df = filtered_df.copy().dropna()
    non_nan_filtered_df['contextual_difficulty_level'] = non_nan_filtered_df['contextual_difficulty_level'].cat.remove_unused_categories()

    sns.set_theme(style="whitegrid")
    fig6, ax6 =plt.subplots(figsize=(10, 6))
    sns.pointplot(
        data=non_nan_filtered_df, 
        x='contextual_difficulty_level', 
        y='completed_modules',
        hue='learning_style', 
        markers=["o", "s", "D", "x"],
        linestyles=["-", "--", "-.", ":"], 
        capsize=.1, 
        ax=ax6
    )
    ax6.set_title('Module Completion Trends by Difficulty & Learning Style', fontsize=14)
    ax6.set_xlabel('Module Difficulty Level', fontsize=12)
    ax6.set_ylabel('Avg. Number of Modules Completed', fontsize=12)
    ax6.legend(title='Learning Style', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    return fig6
# /Q6

# Q7 : Compare previous average grades (GPA) with final (GPA) in the dataset.
def create_fig7(filtered_df):
    grid7 = sns.jointplot(
                data=filtered_df, 
                x='previous_gpa',
                y='current_gpa',
                kind='reg',
                color='purple'
    )
    grid7.fig.suptitle('Relationship: Past GPA vs. Current GPA', y=1.02)
    return grid7.fig
# /Q7

# Q8 : Does time spend per module affects the final score? (more time better score?)
def create_fig8(filtered_df):
    fig8, ax8 = plt.subplots()
    sns.regplot(
        data=filtered_df,
        x='avg_time_per_module',
        y='final_assessment_score',
        scatter_kws={'alpha':0.5},
        line_kws={'color':'red'}
    )
    ax8.set_title('Relationship Between Time Spent and Final Score')
    ax8.set_xlabel('Time Spent Per Module')
    ax8.set_ylabel('Final Score')
    return fig8
# /Q8

# Q9 : At what Age do Distraction Events have the most negative impact on the Final Performance Label ?
def create_fig9(filtered_df):
    sns.set_theme(style="whitegrid")
    grid9 = sns.lmplot(
                data=filtered_df,
                x='distraction_events',
                y='final_assessment_score',
                col='age',
                col_wrap=4,
                height=4,
                aspect=1,
                line_kws={'color': 'red'},
                scatter_kws={'alpha': 0.4}
    )
    grid9.set_axis_labels("Number of Distractions", "Final Score (%)")
    grid9.set_titles("Age Group: {col_name}")
    grid9.fig.subplots_adjust(top=0.9)
    grid9.fig.suptitle('Impact of Distractions on Performance by Age', fontsize=16)
    return grid9.fig
# /Q9

# Q10 : Which Type of students that uses AI personalized paths and recommendations get affected the most,
#  The low performance students or the higher performing students? 
# (compare previous GPA with the final score when the recommended path is the actual path).
def create_fig10(filtered_df):
    filtered_df['GPA_Group'] = pd.cut(filtered_df['previous_gpa'],
                            bins=[0, 2.5, 4.0],
                            labels=['Low Performers', 'High Performers'])
    df_path_followers = filtered_df[filtered_df['actual_path_followed'] == filtered_df['recommended_path']].copy()
    df_path_followers_melted = df_path_followers.melt(id_vars=['GPA_Group'],
                                    value_vars=['previous_gpa', 'current_gpa'],
                                    var_name='Metric',
                                    value_name='Performance')
    fig10, ax10 = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=df_path_followers_melted, 
        x='GPA_Group', 
        y='Performance', 
        hue='Metric', 
        palette='viridis', 
        ax=ax10
    )
    ax10.set_title('AI Path Impact: Performance Lift by Student Type', fontsize=14)
    ax10.set_ylabel('Score / Percentage (%)')
    ax10.set_xlabel('Student Performance Category')
    ax10.legend(title='Stage', labels=['Previous GPA (Scaled)', 'Current GPA'])
    return fig10
# /Q10
# /visualization /plots

# /load & clean data

# sidebar config
with st.sidebar:

    st.markdown("Data addon filters")
    learning_style = st.sidebar.multiselect(
    "Learning Style",
    df_cleaned["learning_style"].unique(),
    default=df_cleaned["learning_style"].unique()
    )
   
    difficulty = st.sidebar.multiselect(
        "Difficulty",
        df_cleaned["contextual_difficulty_level"].unique(),
        default=df_cleaned["contextual_difficulty_level"].unique()
    )

    #⬅ part of data cleaning
    @st.cache_data
    def apply_filters(df_cleaned, learning_style, difficulty):
        filtered_df = df_cleaned[
            (df_cleaned["learning_style"].isin(learning_style)) &
            (df_cleaned["contextual_difficulty_level"].isin(difficulty))
        ].copy()
        return filtered_df
    filtered_df = apply_filters(df_cleaned, learning_style, difficulty)
    # /part of data cleaning

#/sidebar config

# UI config
# Welcoming
st.title('Welcome to our data analyzing project!')
col1, col2 = st.columns([1,0.7])
with col1 :
    st.subheader('Made by Syntax Squad')
    with st.container(border = True):
        st.subheader('About Us')
        st.text("Our team was first formed in STP’s labs. With the guidance of our dear moderators, we learned the fundamentals of the Python programming language, various libraries, and essential soft skills such as presentation skills, time management, team work, using Canva, LinkedIn, and much more. Most importantly, we developed the ability to search for information independently, teach ourselves new concepts, and share knowledge with one another. This project represents our graduation project. Using what we learned in python and more, We hope you like it and find it sophisticated enough to match STP’s level of professionalism and cleverness.")
with col2 :
    st.image('syntax squad logo.jpeg', use_container_width=True)

st.divider()
# /welcoming

# making csv files for download
raw_csv_data = df.to_csv(index=False).encode('utf-8')
cleaned_csv_data = df_cleaned.to_csv(index=False).encode('utf-8')
filtered_csv_data = filtered_df.to_csv(index=False).encode('utf-8')
# /making csv files for download

st.title("AI Learning Dashboard")
with st.container(border = True):
    show_data = st.toggle("show data source")
    if show_data :
        tab1, tab2, tab3 = st.tabs(["Raw Data", "Cleaned Data", "Filtered data"])
        with tab1:
            st.subheader("Raw Data Preview")
            st.dataframe(df.head(), use_container_width=True)
            st.link_button("Data's Kaggle link", "https://www.kaggle.com/datasets/ziya07/ai-powered-personalized-learning-dataset")
            st.download_button(
            label = "Download raw data",
            data = raw_csv_data,
            file_name="AI_Personalized_learning.csv",
            mime = 'text/csv'
            )
        with tab2:
            st.subheader("Cleaned Dataset")
            st.dataframe(df_cleaned.head(), use_container_width=True)
            st.download_button(
            label = "Download cleaned data",
            data = cleaned_csv_data,
            file_name="AI_Personalized_learning.csv",
            mime = 'text/csv'
            )
        with tab3:
            st.subheader("Filtered data")
            st.dataframe(filtered_df.head(), use_container_width=True)
            st.download_button(
            label = "Download filtered data",
            data = filtered_csv_data,
            file_name="AI_Personalized_learning.csv",
            mime = 'text/csv'
            )
st.divider()

# /UI config

# displaying 
# general info

col1, col2, col3, col4 = st.columns(4)
col1.metric("Number of students", len(filtered_df))
col2.metric("Avg Score", round(filtered_df["final_assessment_score"].mean(), 2))
col3.metric("AI Followers (%)", round((filtered_df["Followed_AI_Path"] == "Yes").mean()*100, 1))
col4.metric("Avg Modules Completed", f"{filtered_df['completed_modules'].mean():.1f}")

# /general info 
# questions & answers
tab_ai, tab_behavior, tab_st_factors = st.tabs(["AI impact", "Learning behavior", "Student factors"])
with tab_ai :
    t1, t2, t3, t4 ,t10 = st.tabs(["Question 1","Question 2","Question 3","Question 4","Question 5"])
    with t1 :
        st.subheader(" Question 1 :How Does different frequency of ai tools usage levels vary in the final score?")
        with st.container(border = True) :
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("Answer : AI Path Analysis")
                st.pyplot(create_fig1(filtered_df))
            with col2 :
                st.space()
                st.text('This graph compares the distribution of quiz scores between students who followed an AI-recommended learning path and those who chose a manual path.It aims to visualize if adhering to AI suggestions leads to better overall academic performance.')
                st.info('Students who followed the AI-recommended path achieved a higher median score and a higher upper-quartile range than those who did not.')

    with t2 :
        st.subheader(" Question 2 :Comparing bet. Students scores before and after AI personalized studying paths.")
        with st.container(border = True) :
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("Answer : Before vs After AI")
                st.pyplot(create_fig2(filtered_df))
            with col2:
                st.space()
                st.text('This graph compares student performance across two different stages: the initial quiz accuracy and the final assessment score. It is designed to measure the growth or improvement in scores after students engage with an AI personalized learning path.')
                st.info('There is a clear upward shift in performance, with the final assessment showing a higher median score and a much higher concentration of students scoring above 80%.')
    
    with t3 :
        st.subheader(" Question 3 :What was the effect of taking the recommended path or not on the final score?")
        with st.container(border = True) :
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("Answer : A Different approach on AI vs Final score")
                st.pyplot(create_fig3(filtered_df))
            with col2:
                st.space()
                st.text('This graph uses a violin plot combined with a swarm plot to show the density and distribution of final scores based on AI path adherence. It aims to reveal whether students who followed the recommended path achieved more consistent, high-level results compared to those who deviated.')
                st.info('Students who followed the AI path show a tighter concentration of scores in the 80-100/%/ range, indicating more predictable and higher academic success.')

    with t4 :
        st.subheader(" Question 4 :Does following the AI-Recommended Path actually lead to higher Quiz Scores?")
        with st.container(border = True):
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown('Answer : Another analysis on AI vs Final score')
                st.pyplot(create_fig4(filtered_df))
            with col2:
                st.text('This bar plot compares the average final quiz scores between students who followed the AI-recommended path and those who did not. It is used to quickly identify if there is a noticeable difference in the mean performance of the two groups.')
                st.info('The graph shows that students who followed the AI recommendation achieved a slightly higher average score than those who did not.')

    with t10 :
        st.subheader(" Question 5 :Which Type of students that uses AI personalized paths and recommendations get affected the most,The low performance students or the higher performing students?")
        with st.container(border = True):
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("Answer : AI effect on different levels of performing students")
                st.pyplot(create_fig10(filtered_df))
            with col2:
                st.text("This bar chart compares the performance lift between a student's previous GPA and their current GPA after following the AI-recommended path. It highlights how the AI intervention affects 'Low Performers' versus 'High Performers' differently.")
                st.info('The AI-recommended path provides a significant performance boost for "Low Performers," while "High Performers" maintain their already high standard with a much smaller marginal gain.')

with tab_behavior :
    t5, t6, t8 = st.tabs(["Question 6","Question 7","Question 8"])
    with t5:
        st.subheader(" Question 6 :Which Learning Style completes more Difficult Modules and faster?")
        with st.container(border = True):
            col1, col2= st.columns([1,1])
            with col1:  
                st.markdown("Answer : Time taken for hard modules")
                st.pyplot(create_fig5(filtered_df, difficulty))
            with col2:
                st.text('These graphs compare how different learning styles handle difficult coursework by measuring both volume and speed. They show the total number of "Hard" modules finished alongside the average time taken to complete each one.')
                st.info('Kinesthetic learners complete the highest number of hard modules, even though all learning styles spend roughly the same amount of time to finish them.')

    with t6 :
        if not filtered_df.empty:
            best_style = filtered_df.groupby('learning_style')['completed_modules'].mean().idxmax()
            diffs = ", ".join(filtered_df['contextual_difficulty_level'].unique())
        else:
            best_style = "N/A"
            diffs = "selected"
        st.subheader(" Question 7 :Compare between the modules taken and the contextual difficulty for students with different learning types.")
        with st.container(border = True):
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("Answer : Learning styles and different modules")
                st.pyplot(create_fig6(filtered_df))
            with col2:
                st.text('This point plot tracks the average number of modules completed across different difficulty levels for each learning style. It is designed to show how student engagement and productivity fluctuate as the course material becomes more challenging.')
                st.info(f'At the {diffs} difficulty level, {best_style} learners complete more modules on average than the rest, despite a wider variation in their performance.')

    with t8 :
        st.subheader("Question 8 :Does time spend per module affects the final score? (more time better score?)")
        with st.container(border = True):
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("Answer : The relation of time per module with the final score")
                st.pyplot(create_fig8(filtered_df))
            with col2:
                st.text("This graph investigates if the amount of time spent on learning modules influences the student's final assessment performance. It visualizes whether a higher 'time investment' leads to a corresponding increase in academic achievement.")
                st.info('The horizontal red line shows that there is no correlation between time spent and the final score, meaning spending more time does not result in a higher grade.')

with tab_st_factors :
    t7, t9 = st.tabs(["Question 9", "Question 10"])
    with t7 :
        st.subheader(" Question 9 :Compare previous average grades (GPA) with final (GPA) in the dataset.")
        with st.container(border = True):
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("Answer : Change of gpa previous vs current")
                st.pyplot(create_fig7(filtered_df))
            with col2:
                st.text("This joint plot explores the correlation between a student's previous GPA and their current GPA using a scatter plot and regression line. It aims to determine if past academic performance is a strong predictor of current success in the program.")
                st.info('The flat regression line and scattered points indicate that there is almost no correlation between a students past GPA and their current GPA in this dataset.')

    with t9 :
        st.subheader(" Question 10 :At what Age do Distraction Events have the most negative impact on the Final Performance Label ?")
        with st.container(border = True):
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("Answer : Distractions and Age impact on scores")
                st.pyplot(create_fig9(filtered_df))
            with col2 :
                st.text('This faceted regression plot examines how the frequency of distraction events affects final assessment scores, broken down by individual age groups. It aims to identify if certain ages are more resilient or more vulnerable to the negative impact of interruptions on their performance.')
                st.info('The impact of distractions is highly variable by age, showing slight positive correlations for 18 and 22-year-olds, but negative correlations for ages 20, 23, and 24.')

# /questions & answers

# final conclusion (recommendation)

st.header("Summary and recommendation")
with st.expander('View summary & recommendation') :
    with st.container(border = True):
        st.text("In conclusion, the data demonstrates that the AI-recommended learning path provided a clear academic advantage by shifting student performance into higher, more consistent scoring brackets. While traditional metrics like 'time spent' or 'past GPA' showed little to no correlation with current success, the adherence to AI personalization emerged as a primary driver of improvement. This impact was most transformative for lower-performing students, who saw a significant 'performance lift, effectively narrowing the achievement gap. By optimizing the quality of study rather than just the quantity, the AI successfully neutralized external challenges like distractions and varying learning styles, proving that personalized digital guidance is a powerful tool for elevating overall student outcomes.")
st.divider()

# /final conclusion

# Credits---

st.header("Credits & Contact info. links")
st.subheader("Syntax Squad Team:")
col1, col2, col3 = st.columns([1,1,2], border = True)
with col1 :
    st.markdown("### :violet-background[Tools we used:]")
    st.page_link("https://python.org", label=':blue[- python.org]')
    st.page_link("https://streamlit.io", label=':red[- streamlit.io]')
    st.page_link("https://pandas.pydata.org", label=':violet[- pandas.pydata.org]')
    st.page_link("https://matplotlib.org", label=':green[- matplotlip.org]')
    st.page_link("https://seaborn.pydata.org", label=':orange[- seaborn.pydata.org]')
    st.page_link("https://code.visualstudio.com", label=':blue[- code.visualstudio.com]')
    st.page_link("https://colab.research.google.com", label=':yellow[- colab.research.google.com]')

with col2 :
    st.markdown("### :blue-background[:blue[On LinkedIn:]]")
    st.link_button('- Eissa Amr','https://www.linkedin.com/in/eissa-amr-abdelsalam')
    st.link_button('- Bilal Ahmed','https://www.linkedin.com/in/bilal-ahmed-0271a338a')
    st.link_button('- Ziad Ashraf','https://www.linkedin.com/in/zeyad-aboelhamd-867a38364')
    st.link_button('- Youssef Mohamed','https://www.linkedin.com/in/youssef-mohamed-5404a73b3')
    st.link_button('- Mohamed Tag','')
    st.link_button('- Ali Mostafa','https://www.linkedin.com/in/ali-eldemery-7356902a9  ')

with col3 :
    st.markdown("### :red-background[Our E-Mail:]")
    #st.page_link("HERE", label='syntax.squad.codeteam@gmail.com')
    st.info("If You would like, support us by visiting our pages, and if you have other cool places and organizations where we can learn and have fun, Don't hesitate to contact us! Or Even, You could offer us a job ;)")

# /credits--

# /displaying