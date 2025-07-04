"""
Pytest configuration and fixtures
"""
import os
import pytest
from dotenv import load_dotenv

# Load all environment variables from .env
load_dotenv()

# Verify critical variables are loaded
required_vars = ['GROQ_API_KEY']
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise EnvironmentError(f"Missing environment variables: {missing_vars}")

def pytest_addoption(parser):
    """Add custom pytest options"""
    parser.addoption(
        "--verbose-agent",
        action="store_true",
        default=False,
        help="Enable verbose logging for agent interactions"
    )

@pytest.fixture
def verbose_mode(request):
    """Fixture to get verbose mode setting"""
    return request.config.getoption("--verbose-agent")

@pytest.fixture
def sample_calendar_data():
    """Sample calendar data for testing - uses tomorrow's date dynamically"""
    from datetime import datetime, timedelta

    # Get tomorrow's date (July 5, 2025 since today is July 4, 2025)
    tomorrow = datetime.now().date() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime('%Y-%m-%d')

    return {
        'events': [
            {
                'id': 'event_1',
                'subject': 'Team Standup',
                'start': {'dateTime': f'{tomorrow_str}T09:00:00.000Z'},
                'end': {'dateTime': f'{tomorrow_str}T09:30:00.000Z'},
                'attendees': [
                    {'emailAddress': {'address': 'alice@example.com', 'name': 'Alice'}},
                    {'emailAddress': {'address': 'bob@example.com', 'name': 'Bob'}}
                ],
                'location': {'displayName': 'Conference Room A'}
            },
            {
                'id': 'event_2',
                'subject': 'Project Review',
                'start': {'dateTime': f'{tomorrow_str}T14:00:00.000Z'},
                'end': {'dateTime': f'{tomorrow_str}T15:30:00.000Z'},
                'attendees': [
                    {'emailAddress': {'address': 'charlie@example.com', 'name': 'Charlie'}},
                    {'emailAddress': {'address': 'diana@example.com', 'name': 'Diana'}}
                ],
                'location': {'displayName': 'Conference Room B'}
            },
            {
                'id': 'event_3',
                'subject': 'Client Call',
                'start': {'dateTime': f'{tomorrow_str}T16:00:00.000Z'},
                'end': {'dateTime': f'{tomorrow_str}T17:00:00.000Z'},
                'attendees': [
                    {'emailAddress': {'address': 'client@external.com', 'name': 'Client'}}
                ],
                'location': {'displayName': 'Virtual'}
            }
        ],
        'date_range': {
            'start': f'{tomorrow_str}T00:00:00.000Z',
            'end': f'{tomorrow_str}T23:59:59.000Z'
        }
    }

@pytest.fixture
def empty_calendar_data():
    """Empty calendar data for testing - uses tomorrow's date dynamically"""
    from datetime import datetime, timedelta

    # Get tomorrow's date
    tomorrow = datetime.now().date() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime('%Y-%m-%d')

    return {
        'events': [],
        'date_range': {
            'start': f'{tomorrow_str}T00:00:00.000Z',
            'end': f'{tomorrow_str}T23:59:59.000Z'
        }
    }

@pytest.fixture
def busy_calendar_data():
    """Busy calendar data with many conflicts - uses today's date for conflict testing"""
    from datetime import datetime

    # Use today's date for the busy calendar test (so "today during business hours" works)
    today = datetime.now().date()
    today_str = today.strftime('%Y-%m-%d')

    return {
        'events': [
            {
                'id': f'event_{i}',
                'subject': f'Meeting {i}',
                'start': {'dateTime': f'{today_str}T{9+i:02d}:00:00.000Z'},
                'end': {'dateTime': f'{today_str}T{10+i:02d}:00:00.000Z'},
                'attendees': [
                    {'emailAddress': {'address': f'user{i}@example.com', 'name': f'User {i}'}}
                ]
            }
            for i in range(8)  # 9 AM to 5 PM busy
        ],
        'date_range': {
            'start': f'{today_str}T00:00:00.000Z',
            'end': f'{today_str}T23:59:59.000Z'
        }
    }
