"""
Authentication utilities for Microsoft Graph API
"""

import msal
import os
from typing import Optional, Dict, Any

class AuthManager:
    """Handles Microsoft Graph API authentication using MSAL"""

    def __init__(self):
        """Initialize the authentication manager"""
        self.client_id = os.getenv('AZURE_CLIENT_ID')
        self.client_secret = os.getenv('AZURE_CLIENT_SECRET')
        self.tenant_id = os.getenv('AZURE_TENANT_ID')

        # Microsoft Graph scopes
        self.scopes = [
            'https://graph.microsoft.com/Calendars.ReadWrite',
            'https://graph.microsoft.com/User.Read'
        ]

        self.redirect_uri = 'http://localhost:8501'  # Streamlit default

        # Create MSAL application
        self.app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=f'https://login.microsoftonline.com/{self.tenant_id}',
            client_credential=self.client_secret
        )

    def get_auth_url(self) -> str:
        """Get the authorization URL for OAuth flow"""
        auth_url = self.app.get_authorization_request_url(
            scopes=self.scopes,
            redirect_uri=self.redirect_uri
        )
        return auth_url

    def authenticate_with_code(self, auth_code: str) -> Optional[Dict[str, Any]]:
        """Authenticate using authorization code"""
        try:
            result = self.app.acquire_token_by_authorization_code(
                auth_code,
                scopes=self.scopes,
                redirect_uri=self.redirect_uri
            )

            if 'access_token' in result:
                return result
            else:
                print(f"Authentication failed: {result.get('error_description', 'Unknown error')}")
                return None

        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return None

    def authenticate_interactive(self) -> Optional[Dict[str, Any]]:
        """Interactive authentication (for testing)"""
        try:
            # This would open a browser for authentication
            # For Streamlit, we'll need to handle this differently
            accounts = self.app.get_accounts()

            if accounts:
                # Try to get token silently
                result = self.app.acquire_token_silent(self.scopes, account=accounts[0])
                if result and 'access_token' in result:
                    return result

            # If no cached token, need interactive auth
            # This is a placeholder - actual implementation would depend on deployment
            print("Interactive authentication required")
            return None

        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return None

    def refresh_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Refresh an expired access token"""
        try:
            result = self.app.acquire_token_by_refresh_token(
                refresh_token,
                scopes=self.scopes
            )

            if 'access_token' in result:
                return result
            else:
                return None

        except Exception as e:
            print(f"Token refresh error: {str(e)}")
            return None
