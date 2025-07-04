"""
Scheduling Agent using PydanticAI with Groq
"""
from pydantic_ai import Agent
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class MeetingRequest(BaseModel):
    """Model for meeting requests"""
    title: str
    duration_minutes: int
    attendees: List[str]
    preferred_time: Optional[str] = None
    description: Optional[str] = None

class TimeSlot(BaseModel):
    """Model for available time slots"""
    start_time: datetime
    end_time: datetime
    confidence: float  # 0.0 to 1.0

class SchedulingResult(BaseModel):
    """Model for scheduling results"""
    success: bool
    suggested_slots: List[TimeSlot]
    meeting_details: MeetingRequest
    conflicts: List[str] = []

class SchedulingAgent:
    """AI-powered scheduling agent using PydanticAI"""

    def __init__(self):
        """Initialize the scheduling agent"""
        self.agent = Agent(
            'groq:llama-3.3-70b-versatile',
            output_type=SchedulingResult,
            system_prompt="""You are an intelligent scheduling assistant.
            Your job is to help users schedule meetings by:
            1. Extracting meeting details from natural language requests
            2. Analyzing calendar availability for the EXACT date/time requested
            3. Carefully checking for conflicts with existing calendar events
            4. Only suggesting time slots that are actually available (no overlaps)
            5. If no slots are available on the requested date, mark success=False and list specific conflicts

            IMPORTANT RULES FOR CONFLICT DETECTION:
            - A meeting conflicts ONLY if it overlaps with existing events
            - Example: If existing event is 09:00-09:30, then 10:00-11:00 is FREE (no overlap)
            - Example: If existing event is 14:00-15:30, then 15:00-16:00 CONFLICTS (overlaps)
            - Check exact times carefully - adjacent events don't conflict
            - If user requests "tomorrow", use the next day's calendar data
            - If user requests "today", use today's calendar data
            - Be precise about availability - don't suggest alternative dates unless specifically asked
            - Mark success=False only if there's a REAL conflict (time overlap)
            - List specific conflicts with exact times when conflicts exist

            Always be helpful, professional, and efficient in your responses."""
        )

    async def process_request(self, user_request: str, calendar_data: Optional[Dict[str, Any]] = None) -> SchedulingResult:
        """Process a natural language scheduling request"""
        try:
            # Prepare context for the AI
            context = f"""
            User request: {user_request}
            Calendar data: {calendar_data or 'No calendar data provided'}

            Please analyze this request and provide scheduling recommendations.
            """

            result = await self.agent.run(context)
            return result.output
        except Exception as e:
            # Return error result
            return SchedulingResult(
                success=False,
                suggested_slots=[],
                meeting_details=MeetingRequest(
                    title="Error parsing request",
                    duration_minutes=30,
                    attendees=[]
                ),
                conflicts=[f"Error processing request: {str(e)}"]
            )

    def process_request_sync(self, user_request: str, calendar_data: Optional[Dict[str, Any]] = None) -> SchedulingResult:
        """Synchronous version of process_request"""
        try:
            context = f"""
            User request: {user_request}
            Calendar data: {calendar_data or 'No calendar data provided'}

            Please analyze this request and provide scheduling recommendations.
            """

            result = self.agent.run_sync(context)
            return result.output
        except Exception as e:
            return SchedulingResult(
                success=False,
                suggested_slots=[],
                meeting_details=MeetingRequest(
                    title="Error parsing request",
                    duration_minutes=30,
                    attendees=[]
                ),
                conflicts=[f"Error processing request: {str(e)}"]
            )
