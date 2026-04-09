# plots for importing (deep code)
# importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# /importing

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