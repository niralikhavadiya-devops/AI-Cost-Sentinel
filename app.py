import streamlit as st
import json
import matplotlib.pyplot as plt
from datetime import datetime
# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Cost Sentinel",
    page_icon="💰",
    layout="wide"
)

# -----------------------------
# Load Cost Data
# -----------------------------
with open("cost_data.json", "r") as file:
    cost_data = json.load(file)

# -----------------------------
# Dashboard Title
# -----------------------------
st.title("💰 AI Cost Sentinel")
st.write("Welcome to the AI Multi-Platform Cost Monitoring Dashboard")

st.markdown("---")

# -----------------------------
# Today's Summary
# -----------------------------
st.subheader("📊 Today's Cost Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Today's Cost", "$826.72")

with col2:
    st.metric("Yesterday", "$885.80")

with col3:
    st.metric("Difference", "-$59.08")

st.markdown("---")

# -----------------------------
# Total Cost
# -----------------------------
total_cost = sum(cost_data.values())
# Platform Budgets
budgets = {
    "OpenAI_DEV": 150,
    "OpenAI_PROD": 300,
    "OpenAI_INC": 200,
    "Gemini": 100,
    "Anthropic": 100,
    "Apify": 50,
    "AWS": 100
}

st.subheader("💰 Total Cost")

st.metric(
    "Total Platform Spend",
    f"${total_cost:.2f}"
)

st.markdown("---")

# -----------------------------
# Platform Search
# -----------------------------
st.subheader("🖥️ Platform Cost Details")
st.markdown("---")
st.subheader("🚨 Budget Monitoring")

for platform, cost in cost_data.items():
    budget = budgets.get(platform, 100)

    if cost > budget:
        st.error(
            f"🔴 {platform} exceeded budget! "
            f"(Budget: ${budget} | Current: ${cost:.2f})"
        )
    else:
        st.success(
            f"🟢 {platform} is within budget. "
            f"(Budget: ${budget} | Current: ${cost:.2f})"
        )

st.markdown("---")
search = st.text_input("🔍 Search Platform")

filtered_data = {
    platform: cost
    for platform, cost in cost_data.items()
    if search.lower() in platform.lower()
}

# -----------------------------
# Platform Cards
# -----------------------------
for platform, cost in filtered_data.items():

    col1, col2 = st.columns([3,1])

    with col1:
        st.markdown(f"### {platform}")

    with col2:
        st.metric("Cost", f"${cost:.2f}")

    st.divider()

# -----------------------------
# Pie Chart
# -----------------------------
st.markdown("---")

st.subheader("📊 Cost Distribution")

fig, ax = plt.subplots(figsize=(6,6))

ax.pie(
    cost_data.values(),
    labels=cost_data.keys(),
    autopct="%1.1f%%",
    startangle=90
)

ax.axis("equal")

st.pyplot(fig)

# -----------------------------
# Dashboard Status
# -----------------------------
st.markdown("---")
st.markdown("---")
st.subheader("📈 7-Day Cost Trend")

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
daily_cost = [760, 790, 810, 840, 825, 850, 826]

fig2, ax2 = plt.subplots(figsize=(8,4))

ax2.plot(days, daily_cost, marker="o")

ax2.set_xlabel("Day")
ax2.set_ylabel("Cost ($)")
ax2.set_title("Weekly Cost Trend")

st.pyplot(fig2)
st.success("✅ Dashboard Status : Healthy")

st.info("📅 Last Updated : Today")

st.caption("AI Cost Sentinel v1.0")