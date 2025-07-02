"""
Scheduling Agent POC - Streamlit Interface
Main application for testing Outlook integration with PydanticAI and Prefect
"""

import streamlit as st
import os
from datetime import datetime, timedelta
from typing import Optional
import pandas as pd

# Import our custom modules (will be created)
from agents.scheduling_agent import SchedulingAgent
from utils.auth import AuthManager
from integrations.graph_client import GraphClient

# Page configuration
st.set_page_config(
    page_title="Scheduling Agent POC",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'access_token' not in st.session_state:
        st.session_state.access_token = None
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None
    if 'calendar_events' not in st.session_state:
        st.session_state.calendar_events = []

def main():
    """Main application function"""
    initialize_session_state()

    st.title("📅 Scheduling Agent POC")
    st.markdown("*Outlook integration with PydanticAI and Prefect*")

    # Sidebar for authentication and settings
    with st.sidebar:
        st.header("🔐 Authentication")

        if not st.session_state.authenticated:
            if st.button("Login with Microsoft", type="primary"):
                # TODO: Implement authentication flow
                st.info("Authentication flow will be implemented")
                # auth_manager = AuthManager()
                # result = auth_manager.authenticate()
        else:
            st.success(f"✅ Logged in as: {st.session_state.user_info.get('name', 'User')}")
            if st.button("Logout"):
                # Clear session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

    # Main content area
    if st.session_state.authenticated:
        show_authenticated_interface()
    else:
        show_login_interface()

def show_login_interface():
    """Show interface for non-authenticated users"""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
        ### Welcome to the Scheduling Agent POC

        This application demonstrates:
        - 🤖 **PydanticAI** with Groq's Llama-3.3-70B model
        - 📅 **Microsoft Graph API** for Outlook integration
        - ⚡ **Prefect** for workflow orchestration
        - 🎯 **Streamlit** for the user interface

        **To get started:**
        1. Click "Login with Microsoft" in the sidebar
        2. Authorize the application to access your calendar
        3. Start scheduling meetings with AI assistance!
        """)

        st.info("👈 Please authenticate using the sidebar to continue")

def show_authenticated_interface():
    """Show main interface for authenticated users"""

    # Create tabs for different features
    tab1, tab2, tab3, tab4 = st.tabs([
        "📅 Calendar View",
        "🤖 AI Scheduling",
        "📊 Analytics",
        "⚙️ Settings"
    ])

    with tab1:
        show_calendar_view()

    with tab2:
        show_ai_scheduling()

    with tab3:
        show_analytics()

    with tab4:
        show_settings()

def show_calendar_view():
    """Display calendar events and basic operations"""
    st.header("📅 Your Calendar")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Date range selector
        date_range = st.date_input(
            "Select date range",
            value=(datetime.now().date(), datetime.now().date() + timedelta(days=7)),
            help="Choose the date range to view your calendar events"
        )

        # Refresh button
        if st.button("🔄 Refresh Calendar"):
            # TODO: Implement calendar refresh
            st.info("Calendar refresh will be implemented")

    with col2:
        # Quick actions
        st.subheader("Quick Actions")
        if st.button("➕ New Meeting", type="primary"):
            st.info("Quick meeting creation will be implemented")

        if st.button("🔍 Find Available Time"):
            st.info("Available time finder will be implemented")

    # Display calendar events (placeholder)
    st.subheader("Upcoming Events")

    # Sample data for now
    sample_events = pd.DataFrame({
        'Time': ['09:00 - 10:00', '14:00 - 15:30', '16:00 - 17:00'],
        'Title': ['Team Standup', 'Project Review', 'Client Call'],
        'Attendees': ['3', '5', '2'],
        'Status': ['Confirmed', 'Tentative', 'Confirmed']
    })

    st.dataframe(sample_events, use_container_width=True)

def show_ai_scheduling():
    """AI-powered scheduling interface"""
    st.header("🤖 AI-Powered Scheduling")

    st.markdown("""
    Use natural language to schedule meetings. The AI will:
    - Find available time slots
    - Suggest optimal meeting times
    - Handle conflicts automatically
    - Send invitations to attendees
    """)

    # Natural language input
    user_request = st.text_area(
        "Describe your meeting request:",
        placeholder="Schedule a 1-hour team meeting next week with John and Sarah to discuss the project roadmap",
        height=100
    )

    col1, col2 = st.columns([1, 4])

    with col1:
        if st.button("🚀 Process Request", type="primary"):
            if user_request.strip():
                with st.spinner("AI is processing your request..."):
                    # TODO: Implement AI processing
                    process_ai_request(user_request)
            else:
                st.warning("Please enter a meeting request")

    with col2:
        st.caption("Example: 'Schedule a 30-minute meeting with the marketing team tomorrow afternoon'")

def process_ai_request(request: str):
    """Process AI scheduling request"""
    # Placeholder for AI processing
    st.success("✅ Request processed successfully!")

    # Show mock results
    with st.expander("📋 AI Analysis Results", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Meeting Details Extracted:**")
            st.write("• Duration: 1 hour")
            st.write("• Attendees: John, Sarah")
            st.write("• Topic: Project roadmap discussion")
            st.write("• Timeframe: Next week")

        with col2:
            st.markdown("**Suggested Time Slots:**")
            st.write("🟢 Tuesday 2:00 PM - 3:00 PM")
            st.write("🟡 Wednesday 10:00 AM - 11:00 AM")
            st.write("🟢 Thursday 3:00 PM - 4:00 PM")

    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✅ Accept First Suggestion"):
            st.success("Meeting scheduled for Tuesday 2:00 PM!")
    with col2:
        if st.button("📝 Modify Request"):
            st.info("Modification interface will be implemented")
    with col3:
        if st.button("❌ Cancel"):
            st.info("Request cancelled")

def show_analytics():
    """Show scheduling analytics and insights"""
    st.header("📊 Scheduling Analytics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Meetings This Week", "12", "↑ 3")
    with col2:
        st.metric("Average Duration", "45 min", "↓ 5 min")
    with col3:
        st.metric("Success Rate", "94%", "↑ 2%")
    with col4:
        st.metric("AI Suggestions Used", "8", "↑ 1")

    # Placeholder charts
    st.subheader("Meeting Patterns")
    chart_data = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        'Meetings': [3, 4, 2, 5, 1]
    })
    st.bar_chart(chart_data.set_index('Day'))

def show_settings():
    """Application settings and configuration"""
    st.header("⚙️ Settings")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("AI Configuration")

        model_choice = st.selectbox(
            "AI Model",
            ["groq:llama-3.3-70b-versatile", "groq:llama3-70b-8192", "groq:mixtral-8x7b-32768"],
            help="Choose the AI model for scheduling assistance"
        )

        ai_creativity = st.slider(
            "AI Creativity Level",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            help="Higher values make AI more creative in suggestions"
        )

        st.checkbox("Enable conflict detection", value=True)
        st.checkbox("Auto-send meeting invitations", value=False)

    with col2:
        st.subheader("Calendar Preferences")

        default_duration = st.selectbox(
            "Default Meeting Duration",
            ["15 min", "30 min", "45 min", "1 hour", "2 hours"],
            index=1
        )

        work_hours_start = st.time_input("Work Day Start", value=datetime.strptime("09:00", "%H:%M").time())
        work_hours_end = st.time_input("Work Day End", value=datetime.strptime("17:00", "%H:%M").time())

        time_zone = st.selectbox(
            "Time Zone",
            ["UTC-8 (PST)", "UTC-5 (EST)", "UTC+0 (GMT)", "UTC+1 (CET)"],
            index=0
        )

    # Save settings button
    if st.button("💾 Save Settings", type="primary"):
        st.success("Settings saved successfully!")

if __name__ == "__main__":
    main()
