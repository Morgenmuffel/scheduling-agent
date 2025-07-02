"""
Prefect workflows for calendar operations
"""

from prefect import task, flow
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio

from integrations.graph_client import GraphClient
from agents.scheduling_agent import SchedulingAgent

@task
def authenticate_user(client_id: str, client_secret: str, tenant_id: str) -> Optional[str]:
    """Authenticate user and return access token"""
    # This would integrate with the auth manager
    # For now, return placeholder
    return "placeholder_token"

@task
def fetch_calendar_events(access_token: str, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
    """Fetch calendar events from Microsoft Graph"""
    try:
        client = GraphClient(access_token)
        events = client.get_calendar_events(start_date, end_date)
        return events
    except Exception as e:
        print(f"Error fetching calendar events: {str(e)}")
        return []

@task
def find_available_slots(access_token: str, attendee_emails: List[str],
                        duration_minutes: int) -> List[Dict[str, Any]]:
    """Find available time slots for meeting"""
    try:
        client = GraphClient(access_token)
        slots = client.find_meeting_times(attendee_emails, duration_minutes)
        return slots
    except Exception as e:
        print(f"Error finding available slots: {str(e)}")
        return []

@task
def process_ai_scheduling_request(user_request: str, calendar_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process scheduling request using AI"""
    try:
        agent = SchedulingAgent()
        result = agent.process_request_sync(user_request, calendar_data)

        # Convert Pydantic model to dict for Prefect serialization
        return {
            'success': result.success,
            'suggested_slots': [slot.model_dump() for slot in result.suggested_slots],
            'meeting_details': result.meeting_details.model_dump(),
            'conflicts': result.conflicts
        }
    except Exception as e:
        print(f"Error processing AI request: {str(e)}")
        return {
            'success': False,
            'suggested_slots': [],
            'meeting_details': {},
            'conflicts': [f"AI processing error: {str(e)}"]
        }

@task
def create_calendar_meeting(access_token: str, meeting_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create a new calendar meeting"""
    try:
        client = GraphClient(access_token)
        result = client.create_meeting(meeting_data)
        return result
    except Exception as e:
        print(f"Error creating meeting: {str(e)}")
        return None

@flow(name="Smart Scheduling Flow")
def smart_scheduling_flow(
    user_request: str,
    access_token: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> Dict[str, Any]:
    """
    Complete smart scheduling workflow
    1. Fetch current calendar data
    2. Process AI request
    3. Find available slots
    4. Return scheduling recommendations
    """

    # Set default date range if not provided
    if not start_date:
        start_date = datetime.now()
    if not end_date:
        end_date = start_date + timedelta(days=7)

    # Fetch current calendar events
    calendar_events = fetch_calendar_events(access_token, start_date, end_date)

    # Prepare calendar data for AI
    calendar_context = {
        'events': calendar_events,
        'date_range': {
            'start': start_date.isoformat(),
            'end': end_date.isoformat()
        }
    }

    # Process with AI
    ai_result = process_ai_scheduling_request(user_request, calendar_context)

    return {
        'ai_analysis': ai_result,
        'calendar_events': calendar_events,
        'processing_time': datetime.now().isoformat()
    }

@flow(name="Create Meeting Flow")
def create_meeting_flow(
    access_token: str,
    meeting_details: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Workflow to create a new meeting
    """

    # Create the meeting
    meeting_result = create_calendar_meeting(access_token, meeting_details)

    if meeting_result:
        return {
            'success': True,
            'meeting_id': meeting_result.get('id'),
            'meeting_url': meeting_result.get('webLink'),
            'created_at': datetime.now().isoformat()
        }
    else:
        return {
            'success': False,
            'error': 'Failed to create meeting',
            'created_at': datetime.now().isoformat()
        }

@flow(name="Find Available Times Flow")
def find_available_times_flow(
    access_token: str,
    attendee_emails: List[str],
    duration_minutes: int,
    preferred_times: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Workflow to find available meeting times
    """

    # Find available slots
    available_slots = find_available_slots(access_token, attendee_emails, duration_minutes)

    # Process and rank the slots (could be enhanced with AI)
    processed_slots = []
    for slot in available_slots:
        processed_slots.append({
            'start_time': slot.get('meetingTimeSlot', {}).get('start', {}),
            'end_time': slot.get('meetingTimeSlot', {}).get('end', {}),
            'confidence': slot.get('confidence', 0.0),
            'attendee_availability': slot.get('attendeeAvailability', [])
        })

    return {
        'available_slots': processed_slots,
        'total_slots_found': len(processed_slots),
        'search_completed_at': datetime.now().isoformat()
    }
