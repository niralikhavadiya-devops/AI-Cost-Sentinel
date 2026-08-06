import streamlit as st
import json
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd 
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
highest_platform = max(cost_data, key=cost_data.get)
highest_cost = cost_data[highest_platform]
# Budget Health Indicator

if total_cost < 500:
    st.success("🟢 Budget Status: Healthy")

elif total_cost < 800:
    st.warning("🟡 Budget Status: Warning")

else:
    st.error("🔴 Budget Status: Critical")
    st.subheader("📈 Budget Usage")

budget_limit = 1000
usage = total_cost / budget_limit

st.progress(usage)

st.write(f"**Budget Used:** {usage * 100:.1f}% of ${budget_limit}")
st.markdown("---")
st.subheader("📌 Cost Category Summary")

high = sum(1 for v in cost_data.values() if v >= 200)
medium = sum(1 for v in cost_data.values() if 100 <= v < 200)
low = sum(1 for v in cost_data.values() if v < 100)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("🔴 High Cost", high)

with c2:
    st.metric("🟡 Medium Cost", medium)

with c3:
    st.metric("🟢 Low Cost", low)
st.markdown("---")
st.subheader("🏆 Top Spending Platform")

st.metric(
    label=highest_platform,
    value=f"${highest_cost:.2f}"
)
st.markdown("---")
st.subheader("🥇 Top 3 Most Expensive Platforms")

top3 = sorted(
    cost_data.items(),
    key=lambda x: x[1],
    reverse=True
)[:3]

for i, (platform, cost) in enumerate(top3, start=1):
    medal = ["🥇", "🥈", "🥉"][i-1]
    st.write(f"{medal} **{platform}** — ${cost:.2f}")
    # Highest & Lowest Cost Platform

highest = max(cost_data, key=cost_data.get)
lowest = min(cost_data, key=cost_data.get)

col1, col2 = st.columns(2)

with col1:
    st.success(f"🏆 Highest Cost: {highest} (${cost_data[highest]:.2f})")

with col2:
    st.info(f"💸 Lowest Cost: {lowest} (${cost_data[lowest]:.2f})")
    st.markdown("---")
st.subheader("📊 Cost Insights")

total_platforms = len(cost_data)
average_cost = total_cost / total_platforms

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total Platforms",
        total_platforms
    )

with col2:
    st.metric(
        "Average Cost",
        f"${average_cost:.2f}"
    )
    st.markdown("---")
st.subheader("🤖 AI Cost Recommendation")

if highest_cost > 300:
    st.warning(
        f"💡 {highest_platform} is the highest cost platform today (${highest_cost:.2f}). "
        "Consider reviewing usage, token consumption, or workloads to optimize costs."
    )
else:
    st.success(
        "✅ Overall platform spending looks healthy. No immediate optimization required."
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
st.markdown("---")
st.subheader("📥 Download Cost Report")

df = pd.DataFrame(
    list(cost_data.items()),
    columns=["Platform", "Cost ($)"]
)

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📄 Download CSV Report",
    data=csv,
    file_name="ai_cost_report.csv",
    mime="text/csv"
)
st.success("✅ Dashboard Status : Healthy")

st.info(
    f"📅 Last Updated: {datetime.now().strftime('%d %b %Y | %I:%M %p')}"
)

st.markdown("---")

st.subheader("ℹ️ Project Information")

st.info("""
**Project Name:** AI Cost Sentinel

**Version:** 2.0

**Developer:** Nirali Khavadiya

**Tech Stack:** Python, Streamlit, Pandas, Matplotlib

**Status:** Production Ready 🚀
""")