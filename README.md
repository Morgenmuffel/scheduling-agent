# Microsoft Graph API - Outlook integration

1. **Azure Sign In/ Subscribe**     - Go to [Azure Portal](https://portal.azure.com/)

  ✅ If you sign in using your personal account, you might see AADSTS50020 error. That error occurs because your personal Microsoft account (e.g. Outlook or Live) is not connected to any Azure AD tenant—you’re signed into the default Microsoft Services tenant, which no longer functions like a tenant where you can register apps. You need to:

  ### Create a new Azure tenant using your personal account
    1.	Go to Azure free account: https://azure.microsoft.com/free
    2.	Sign in with your personal Microsoft account.
    3.	Follow the “Start free” flow. This will create:
    •	A new Azure subscription
    •	A new Microsoft Entra (Azure AD) tenant, where you’re Global Admin  ￼ ￼ ￼

  After that, you can switch between your Microsoft Services default tenant (which is read-only) and your new tenant (where you can register apps and invite users).

  ### Join Microsoft Developer Program
  https://developer.microsoft.com/en-us/microsoft-365/dev-program

2. **Azure App Registration**
   - Follow this [guide]
   https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app
   - Sign in to the  **Microsoft Entra admin center**
   - Go to Identity > Applications > App registrations and select New registration
   - Save the following':
     - **Client ID**
     - **Tenant ID**
     - **Client Secret** (under "Certificates & secrets")

3. **Add API Permissions**  
   - In the App Registration → **API Permissions**
   - Add permission: `Calendars.ReadWrite` under Microsoft Graph (Delegated or Application as needed)
   - Click "Grant admin consent"

4. **Install Required Python Packages**
   ```bash
   pip install msal requests
   ```
