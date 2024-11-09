import matplotlib.pyplot as plt
import matplotlib.patches as patches
import plotly.express as px
import pandas as pd
# Function to display schedule in a Gantt-like chart
def display_schedule(data):
    # Task names (in reverse order for visual display purposes)
    tasks = list(data.keys())[::-1]

    # Adjust the figsize to make it very wide (e.g., 24 or 30 inches wide)
    fig, ax = plt.subplots(figsize=(70, 6))  # Increase width from 16 to 30 for more detailed view

    # Loop over tasks and their respective schedules
    for i, task in enumerate(tasks):
        schedule = data[task]
        for start_time, duration in schedule:
            # Create a rectangle for each task period
            ax.add_patch(patches.Rectangle((start_time, i), duration, 0.8, edgecolor='black', facecolor='skyblue'))

    # Set task names on y-axis
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels(tasks)

    # Set labels
    ax.set_xlabel('Time')
    ax.set_ylabel('Tasks')

    # Set axis limits based on your time horizon
    max_time = max([max([start + dur for start, dur in v]) for v in data.values() if v])
    ax.set_xlim(0, max_time + 1)
    ax.set_ylim(-0.5, len(tasks) - 0.5)

    # Add grid for better visualization
    ax.grid(True)

    # Show plot
    plt.show()




def display_gantt_chart(data):
    """
    Displays a Gantt chart using Plotly based on the provided task schedule data.

    Parameters:
        data (dict): A dictionary where keys are task names and values are lists of [start_time, duration].
    """
    # Prepare the data for the Gantt chart
    tasks = []
    for task_name, schedules in data.items():
        for start_time, duration in schedules:
            tasks.append({
                'Task': task_name,
                'Start': start_time,
                'Finish': start_time + duration
            })

    # Convert to DataFrame
    df = pd.DataFrame(tasks)

    # Create the Gantt chart
    fig = px.timeline(df, x_start='Start', x_end='Finish', y='Task', title='Gantt Chart',
                      labels={'Task': 'Tasks', 'Start': 'Start Time', 'Finish': 'End Time'},
                      color='Task',
                      color_discrete_sequence=px.colors.qualitative.Plotly)

    # Ensure that the x-axis is treated as numeric
    fig.update_xaxes(type='linear')  # Treat the x-axis as linear numeric

    # Update layout for better visuals
    fig.update_layout(xaxis_title='Time', yaxis_title='Tasks', showlegend=False)

    # Show the plot
    fig.show()