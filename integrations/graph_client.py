"""
Microsoft Graph API client for calendar operations
"""

import requests
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

class GraphClient:
    """Client for Microsoft Graph API calendar operations"""

    def __init__(self, access_token: str):
        """Initialize the Graph client with access token"""
        self.access_token = access_token
        self.base_url = 'https://graph.microsoft.com/v1.0'
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """Get current user information"""
        try:
            response = requests.get(
                f'{self.base_url}/me',
                headers=self.headers
            )

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to get user info: {response.status_code}")
                return None

        except Exception as e:
            print(f"Error getting user info: {str(e)}")
            return None

    def get_calendar_events(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get calendar events within date range"""
        try:
            # Format dates for Graph API
            start_str = start_date.isoformat() + 'Z'
            end_str = end_date.isoformat() + 'Z'

            url = f'{self.base_url}/me/calendar/events'
            params = {
                '$filter': f"start/dateTime ge '{start_str}' and end/dateTime le '{end_str}'",
                '$select': 'subject,start,end,attendees,location,body',
                '$orderby': 'start/dateTime'
            }

            response = requests.get(url, headers=self.headers, params=params)

            if response.status_code == 200:
                return response.json().get('value', [])
            else:
                print(f"Failed to get calendar events: {response.status_code}")
                return []

        except Exception as e:
            print(f"Error getting calendar events: {str(e)}")
            return []

    def create_meeting(self, meeting_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new calendar meeting"""
        try:
            url = f'{self.base_url}/me/calendar/events'

            response = requests.post(
                url,
                headers=self.headers,
                json=meeting_data
            )

            if response.status_code == 201:
                return response.json()
            else:
                print(f"Failed to create meeting: {response.status_code}")
                print(f"Response: {response.text}")
                return None

        except Exception as e:
            print(f"Error creating meeting: {str(e)}")
            return None

    def get_free_busy(self, emails: List[str], start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """Get free/busy information for attendees"""
        try:
            url = f'{self.base_url}/me/calendar/getSchedule'

            data = {
                'schedules': emails,
                'startTime': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'UTC'
                },
                'endTime': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'UTC'
                },
                'availabilityViewInterval': 15
            }

            response = requests.post(url, headers=self.headers, json=data)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to get free/busy: {response.status_code}")
                return {}

        except Exception as e:
            print(f"Error getting free/busy: {str(e)}")
            return {}

    def find_meeting_times(self, attendees: List[str], duration_minutes: int,
                          max_candidates: int = 20) -> List[Dict[str, Any]]:
        """Find available meeting times using Graph API"""
        try:
            url = f'{self.base_url}/me/calendar/getSchedule'

            # Get next 7 days for searching
            start_time = datetime.now()
            end_time = start_time + timedelta(days=7)

            attendee_list = [{'emailAddress': {'address': email}} for email in attendees]

            data = {
                'attendees': attendee_list,
                'timeConstraint': {
                    'timeslots': [{
                        'start': {
                            'dateTime': start_time.isoformat(),
                            'timeZone': 'UTC'
                        },
                        'end': {
                            'dateTime': end_time.isoformat(),
                            'timeZone': 'UTC'
                        }
                    }]
                },
                'meetingDuration': f'PT{duration_minutes}M',
                'maxCandidates': max_candidates
            }

            response = requests.post(url, headers=self.headers, json=data)

            if response.status_code == 200:
                return response.json().get('meetingTimeSuggestions', [])
            else:
                print(f"Failed to find meeting times: {response.status_code}")
                return []

        except Exception as e:
            print(f"Error finding meeting times: {str(e)}")
            return []
