# analysis page
# Importing
import streamlit as st  # Used to build the web app
import pandas as pd  # Used for data manipulation and analysis
import matplotlib.pyplot as plt  # Used for plotting graphs
import seaborn as sns  # Used for advanced visualizations
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from plots import (
    create_fig1,
    create_fig2,
    create_fig3,
    create_fig4,
    create_fig5,
    create_fig6,
    create_fig7,
    create_fig8,
    create_fig9
)
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
    df_cleaned['learning_style'] = df_cleaned['learning_style'].replace({'Kinesthetic': 'Practical'})
    df_cleaned['student_id'] = df_cleaned['student_id'].str.replace('STU', '').astype(int)
    df_cleaned['recommended_path'] = df_cleaned['recommended_path'].str.replace('→', '-')
    df_cleaned['actual_path_followed'] = df_cleaned['actual_path_followed'].str.replace('→', '-')
    df_cleaned['current_gpa'] = df_cleaned['final_assessment_score'] / 100 * 4 
    df_cleaned['Followed_AI_Path'] = (df_cleaned['actual_path_followed'] == df_cleaned['recommended_path']).map({True: 'Yes', False: 'No'})
    # /data cleaning⬅
    return df, df_cleaned
df, df_cleaned = load_and_clean_data()
# /load & clean data

# sidebar config
with st.sidebar:
    st.markdown("Data addon filters")
    learning_style = st.sidebar.multiselect(
    "Learning Style",
    df_cleaned["learning_style"].unique(),
    default = df_cleaned["learning_style"].unique()
    )

    difficulty = st.sidebar.multiselect(
        "Difficulty",
        df_cleaned["contextual_difficulty_level"].unique(),
        default = df_cleaned["contextual_difficulty_level"].unique()
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
        st.text(
"""
Our team was first formed in STP’s labs. With the guidance of our dear moderators, we learned the fundamentals of the Python programming language, various libraries,
and essential soft skills such as presentation skills, time management, team work, using Canva, LinkedIn, and much more.
Most importantly, we developed the ability to search for information independently, teach ourselves new concepts, and share knowledge with one another. This project represents our graduation project.
Using what we learned in python and more, We hope you like it and find it sophisticated enough to match STP’s level of professionalism and cleverness.
"""
        )
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
            st.subheader("Raw Data")
            st.dataframe(df.head(), use_container_width=True)
            st.link_button("Data's Kaggle link", "https://www.kaggle.com/datasets/ziya07/ai-powered-personalized-learning-dataset")
            st.download_button(
            label = "Download raw data",
            data = raw_csv_data,
            file_name="AI_Personalized_learning.csv",
            mime = 'text/csv'
            )
        with tab2:
            st.subheader("Cleaned Data")
            st.dataframe(df_cleaned.head(), use_container_width=True)
            st.download_button(
            label = "Download cleaned data",
            data = cleaned_csv_data,
            file_name="Cleaned_AI_Personalized_learning.csv",
            mime = 'text/csv'
            )
        with tab3:
            st.subheader("Filtered data")
            st.dataframe(filtered_df.head(), use_container_width=True)
            st.download_button(
            label = "Download filtered data",
            data = filtered_csv_data,
            file_name="Filtered_AI_Personalized_learning.csv",
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
col4.metric("Avg Modules Completed", round(filtered_df['completed_modules'].mean(),1))

# /general info 
# questions & answers
tab_ai, tab_behavior, tab_st_factors = st.tabs(["AI impact", "Learning behavior", "Student factors"])
with tab_ai :
    t1, t2, t3, t4  = st.tabs(["Question 1","Question 2","Question 3","Question 4"])
    with t1 :
        st.subheader(" Question 1 :How Does different frequency of ai tools usage levels vary in the final score?")
        with st.container(border = True) :
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("Answer : AI Path Analysis")
                st.pyplot(create_fig1(filtered_df))
            with col2 :
                st.space()
                st.text(
                '''
                    This graph visualizes the distribution of quiz scores between students who followed an AI-recommended learning path and those who did not.
                    The middle horizontal line shows the median score, while the box and whiskers represent the spread and total range of the results.
                '''
                       )
                st.info('Students who followed the AI-recommended path achieved a slightly higher median score and a higher upper-quartile range than those who did not.')

    with t2 :
        st.subheader(" Question 2 :Comparing bet. Students scores before and after AI personalized studying paths.")
        with st.container(border = True) :
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("Answer : Before vs After AI")
                st.pyplot(create_fig2(filtered_df))
            with col2:
                st.space()
                st.text(
                    '''
                    This graph compares student performance across two different stages: the initial quiz accuracy and the final assessment score, To see if actually following AI recommendations makes a difference.
                    The middle horizontal line is the median, the box holds the middle 50% of scores, and each dot represents an individual student's result.
                    '''
                )
                st.info('There is a noticable upward shift in performance, which means taking the recommended AI path actually boosts the performance.')
    
    with t3 :
        st.subheader(" Question 3 :Does following the AI-Recommended Path actually lead to higher Quiz Scores?")
        with st.container(border = True):
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown('Answer : Another analysis on AI vs Final score')
                st.pyplot(create_fig3(filtered_df))
            with col2:
                st.text(
                    '''
                    This bar plot compares the average final quiz scores between students who followed the AI-recommended path and those who did not.
                    The bar heights show the average score for each group, while the thin vertical lines indicate the range of variation or uncertainty in those results.
                    '''
                    )
                st.info('The graph shows that students who followed the AI recommendation achieved a slightly higher average score than those who did not.')

    with t4 :
        st.subheader(" Question 4 :Which Type of students that uses AI personalized paths and recommendations get affected the most,The low performance students or the higher performing students?")
        with st.container(border = True):
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("Answer : AI effect on different levels of performing students")
                st.pyplot(create_fig4(filtered_df))
            with col2:
                st.text(
                    """
                    This bar chart compares the performance lift between a student's previous GPA and their current GPA after following the AI-recommended path.
                    It shows the effect of AI on different levels of performer students.
                    Compare the heights of the blue and green bars to see the GPA change for each group, with the thin vertical lines showing how much the data varies.
                    """
                    )
                st.info('The AI-recommended path provides a significant performance boost for "Low Performers," while "High Performers" maintain their already high scores little difference.')

with tab_behavior :
    t5, t6, t7 = st.tabs(["Question 5","Question 6","Question 7"])
    with t5:
        st.subheader(" Question 5 :Which Learning Style completes more Difficult Modules and faster?")
        with st.container(border = True):
            col1, col2= st.columns([1,1])
            with col1:  
                st.markdown("Answer : Time taken for hard modules")
                st.pyplot(create_fig5(filtered_df, difficulty))
            with col2:
                st.text(
                    '''
                    These graphs compare how different learning styles handle difficult coursework by measuring both volume and speed.
                    Higher bars show a greater quantity or average time for each group,
                    while the thin vertical lines indicate the range of variation in the timing data.
                    '''
                )
                st.info('Kinesthetic learners complete the highest number of hard modules,even though all styles spent roughly the same time on the modules.')

    with t6 :
        if not filtered_df.empty:
            best_style = filtered_df.groupby('learning_style')['completed_modules'].mean().idxmax()
            diffs = ", ".join(filtered_df['contextual_difficulty_level'].unique())
        else:
            best_style = "N/A"
            diffs = "selected"
        st.subheader(" Question 6 :Compare between the modules taken and the contextual difficulty for students with different learning types.")
        with st.container(border = True):
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("Answer : Learning styles and different modules")
                st.pyplot(create_fig6(filtered_df))
            with col2:
                st.text(
                    '''
                    This point plot tracks the average number of modules completed across different difficulty levels for each learning style.
                    Follow the lines to see how completion rates change as difficulty increases,
                    while the vertical bars show the range of variation for each learning style.
                    '''
                    )
                st.info(f'At the {diffs} difficulty level, {best_style} learners complete more modules on average than the rest.')

    with t7 :
        st.subheader("Question 7 :Does time spend per module affects the final score? (more time better score?)")
        with st.container(border = True):
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("Answer : The relation of time per module with the final score")
                st.pyplot(create_fig7(filtered_df))
            with col2:
                st.text(
                    """
                    This graph shows if the amount of time spent on learning modules makes a difference in the student's final assessment performance.
                    Each dot shows an individual's result, and the flat red line indicates that spending more time does not lead to a higher score.
                    """
                    )
                st.info('The horizontal red line shows that spending more time does not result in a higher grade.')

with tab_st_factors :
    t8, t9 = st.tabs(["Question 8", "Question 9"])
    with t8 :
        st.subheader(" Question 8 :Compare previous average grades (GPA) with final (GPA) in the dataset.")
        with st.container(border = True):
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("Answer : Change of gpa previous vs current")
                st.pyplot(create_fig8(filtered_df))
            with col2:
                st.text(
                    """
                    This joint plot explores the correlation between a student's previous GPA and their current GPA using a scatter plot and regression line.
                    Each dot represents a student's relationship between past and current GPA,
                    while the bars on the edges show how many students fall into each specific GPA range.
                    """
                    )
                st.info('The flat regression line and scattered points indicate that there is almost no correlation between a students past GPA and their current GPA in this dataset.')

    with t9 :
        st.subheader(" Question 9 :At what Age do Distraction Events have the most negative impact on the Final Performance Label ?")
        with st.container(border = True):
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("Answer : Distractions and Age impact on scores")
                st.pyplot(create_fig9(filtered_df))
            with col2 :
                st.text(
                    '''
                    This faceted regression plot examines how the frequency of distraction events affects final assessment scores.
                    Check if the red line in each age box slopes up or down to see how distractions affect scores for that specific age group.
                    '''
                    )
                st.info('The impact of distractions is highly variable by age, showing slight positive correlations for 18 and 22-year-olds, but negative correlations for ages 20, 23, and 24.')

# /questions & answers

# final conclusion (recommendation)

st.header("Summary and recommendation")
with st.expander('View summary & recommendation') :
    with st.container(border = True):
        st.text(
"""
In conclusion, the data demonstrates that the AI-recommended learning path provided a decent academic advantage by shifting student performance into higher, more consistent scoring brackets.
While traditional metrics like 'time spent' or 'past GPA' showed little to no correlation with current success, the adherence to AI personalization emerged as a primary driver of improvement.
This impact was most transformative for lower-performing students, who saw a significant 'performance lift, effectively narrowing the achievement gap.
By optimizing the quality of study rather than just the quantity, the AI successfully neutralized external challenges like distractions and varying learning styles,
proving that personalized digital guidance is a powerful tool for elevating overall student outcomes.
At the finale, We do recommend using AI but with caution just for your academic advantage and not to rely on it.
"""
                )
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
    st.link_button('- Ziad Ashraf','https://www.linkedin.com/in/zeyad-ashraf-aboelhamd-867a38364')
    st.link_button('- Youssef Mohamed','https://www.linkedin.com/in/youssef-mohamed-5404a73b3')
    st.link_button('- Mohamed Tag','')
    st.link_button('- Ali Mostafa','https://www.linkedin.com/in/ali-eldemery-7356902a9  ')

with col3 :
    st.markdown("### :red-background[Our E-Mail:]")
    st.markdown("[syntax.squad.codeteam@gmail.com](mailto:syntax.squad.codeteam@gmail.com)")
    st.info("If You would like, support us by visiting our pages, and if you have other cool places and organizations where we can learn and have fun, Don't hesitate to contact us! Or Even, You could offer us a job ;)")

# /credits--

# /displaying
