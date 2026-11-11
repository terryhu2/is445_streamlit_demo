# INSTRUCTIONS:
# 1. Open a "Terminal" by: View --> Terminal OR just the "Terminal" through the hamburger menu
# 2. run in terminal with: streamlit run streamlit_app.py
# 3. click the "Open in Browser" link that pops up OR click on "Ports" and copy the URL
# 4. Open a Simple Browswer with View --> Command Palette --> Simple Browser: Show
# 5. use the URL from prior steps as intput into this simple browser




import streamlit as st
import networkx as nx
import pandas as pd

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
