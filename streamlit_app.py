# INSTRUCTIONS:
# 1. Open a "Terminal" by: View --> Terminal OR just the "Terminal" through the hamburger menu
# 2. run in terminal with: streamlit run streamlit_app.py
# 3. click the "Open in Browser" link that pops up OR click on "Ports" and copy the URL
# 4. Open a Simple Browswer with View --> Command Palette --> Simple Browser: Show
# 5. use the URL from prior steps as intput into this simple browser




import streamlit as st
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

st.title("Facebook Social Network Analysis")
st.write("IS445 - Interactive Network Visualization")

# Read the Facebook network dataset
@st.cache_data
def load_data():
    graph = nx.read_edgelist(
        "facebook_combined.txt",
        nodetype=int
    )
    return graph

G = load_data()

# Basic network statistics
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()

st.header("Dataset Overview")

st.write("Number of users:", num_nodes)
st.write("Number of friendships:", num_edges)

# Calculate the degree of each user
degrees = dict(G.degree())

df = pd.DataFrame(
    list(degrees.items()),
    columns=["User", "Number of Friends"]
)

st.header("Sample Data")
st.dataframe(df.head(10))


# Visualization 1: Degree Distribution
st.header("Visualization 1: Distribution of Friends")

st.write(
    "This chart shows how the number of friends "
    "varies across users in the Facebook network."
)

# Interactive slider
max_degree = int(df["Number of Friends"].max())

degree_range = st.slider(
    "Select the range of number of friends",
    min_value=0,
    max_value=max_degree,
    value=(0, min(200, max_degree))
)

# Filter data based on slider
filtered_df = df[
    (df["Number of Friends"] >= degree_range[0]) &
    (df["Number of Friends"] <= degree_range[1])
]

# Create histogram with Altair
import altair as alt

histogram = (
    alt.Chart(filtered_df)
    .mark_bar(color="#4C78A8")
    .encode(
        x=alt.X(
            "Number of Friends:Q",
            bin=alt.Bin(maxbins=30),
            title="Number of Friends"
        ),
        y=alt.Y(
            "count():Q",
            title="Number of Users"
        ),
        tooltip=[
            alt.Tooltip("count():Q", title="Users")
        ]
    )
    .properties(height=400)
)

st.altair_chart(histogram, use_container_width=True)

st.write(
    "Number of users in selected range:",
    len(filtered_df)
)

st.subheader("Visualization 1: Analysis")

st.write("""
The first visualization shows the distribution of the number of friends
in the Facebook network. The distribution is strongly right-skewed,
meaning most users have relatively few connections, while a small
number of users have many friends. I used a histogram because it makes
it easier to compare how many users fall into different ranges of
friend counts. I chose blue bars and labeled both axes to keep the
chart simple and readable. I also added an interactive slider so users
can filter the range of friend counts and explore the distribution.
If I had more time, I would experiment with different bin sizes and
a logarithmic scale to better show users with very high numbers
of connections.
""")

# Visualization 2: Facebook Network Graph
st.header("Visualization 2: Facebook Friendship Network")

st.write(
    "This visualization shows connections between "
    "users in the Facebook network. Select a user "
    "to explore their local friendship network."
)

# Select a central user
selected_user = st.selectbox(
    "Select a user to explore",
    options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
)

# Get the selected user's friends
friends = list(G.neighbors(selected_user))

# Limit the number of friends displayed
max_friends = st.slider(
    "Maximum number of friends to display",
    min_value=5,
    max_value=100,
    value=30
)

selected_friends = sorted(friends)[:max_friends]

# Create a subgraph
nodes_to_show = [selected_user] + selected_friends
subgraph = G.subgraph(nodes_to_show)

# Calculate node positions
positions = nx.spring_layout(
    subgraph,
    seed=42
)

# Convert nodes to a dataframe
node_data = []

for node in subgraph.nodes():
    node_data.append({
        "User": node,
        "x": positions[node][0],
        "y": positions[node][1],
        "Type": "Selected User" if node == selected_user else "Friend",
        "Degree": G.degree(node)
    })

nodes_df = pd.DataFrame(node_data)

# Convert edges to a dataframe
edge_data = []

for source, target in subgraph.edges():
    edge_data.append({
        "x": positions[source][0],
        "y": positions[source][1],
        "x2": positions[target][0],
        "y2": positions[target][1]
    })

edges_df = pd.DataFrame(edge_data)

# Create edges

# Draw the network graph using Matplotlib
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 7))

fig.patch.set_facecolor("#FFFFFF")
ax.set_facecolor("#FFFFFF")

node_colors = [
    "#E45756" if node == selected_user else "#4C78A8"
    for node in subgraph.nodes()
]

nx.draw_networkx(
    subgraph,
    pos=positions,
    ax=ax,
    node_color=node_colors,
    node_size=180,
    edge_color="#AAAAAA",
    width=0.8,
    alpha=0.9,
    with_labels=True,
    font_size=8,
    font_color="black"
)

ax.set_title(
    f"Friendship Network of User {selected_user}",
    fontsize=15
)

ax.axis("off")

st.pyplot(fig)
plt.close(fig)


st.write("Selected user:", selected_user)
st.write("Total friends of selected user:", len(friends))
st.write("Nodes displayed:", subgraph.number_of_nodes())
st.write("Friendship connections displayed:", subgraph.number_of_edges())

st.subheader("Visualization 2: Analysis")

st.write("""
The second visualization shows the friendship connections between
a selected Facebook user and their friends. I used a network graph
because it helps show relationships that would be difficult to
understand in a regular table. The selected user is shown in red,
while their friends are shown in blue, and gray lines represent
connections between users. I used a spring layout to make the
network structure easier to see. The dropdown menu allows users
to select different people, and the slider controls how many
friends are displayed. If I had more time, I would improve the
layout for larger networks and add community detection to identify
different social groups.
""")
