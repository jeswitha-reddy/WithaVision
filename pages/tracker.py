import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide")
st.title("📊 Learning Analytics Dashboard")

if "tracker" not in st.session_state:
    st.warning("No tracking data yet.")
else:
    tracker = st.session_state.tracker

    topics = list(tracker["topics"].keys())
    values = list(tracker["topics"].values())

    col1, col2, col3 = st.columns(3)

    total_attempts = sum(values)
    unique_topics = len(topics)
    strongest = topics[np.argmax(values)] if topics else "None"

    col1.metric("Total Attempts", total_attempts)
    col2.metric("Topics Practiced", unique_topics)
    col3.metric("Most Practiced Topic", strongest)

    st.markdown("---")

    st.subheader("Practice Frequency")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=topics,
        y=values,
        text=values,
        textposition="auto"
    ))

    fig.update_layout(
        xaxis_title="Topics",
        yaxis_title="Attempts"
    )

    st.plotly_chart(fig, width="stretch")

    st.subheader("Mastery Level")

    for topic in topics:
        usage = tracker["topics"][topic]

        if usage <= 2:
            status = "🟡 Beginner"
            progress = 30
        elif usage <= 5:
            status = "🟠 Intermediate"
            progress = 70
        else:
            status = "🟢 Strong"
            progress = 100

        st.write(f"### {topic}")
        st.progress(progress)
        st.write(status)
        st.markdown("---")

    if st.button("Reset Tracker"):
        st.session_state.tracker = {"topics": {}}
        st.success("Tracker Reset Successfully")
