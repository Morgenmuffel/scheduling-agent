
# Outlook integration with Microsoft Graph API

### 1. Azure Sign In/Subscribe

Go to [Azure Portal](https://portal.azure.com/)

  ✅ If you sign in using your personal account, you might see AADSTS50020 error. That error occurs because your personal Microsoft account (e.g. Outlook or Live) is not connected to any Azure AD tenant—you’re signed into the default Microsoft Services tenant, which no longer functions like a tenant where you can register apps. You need to:

  ### Create a new Azure tenant using your personal account
  - Go to [Azure free account](https://azure.microsoft.com/free)
  - Sign in with your personal Microsoft account.
  - Follow the “Start free” flow. This will create:
    - A new Azure subscription
    - A new Microsoft Entra (Azure AD) tenant, where you’re Global Admin
    - Fun fact: in case you don't agree to receiving email/ sharing your details with partners, you might be found not eligible to the free trial

After that, you can switch between your Microsoft Services default tenant (which is read-only) and your new tenant (where you can register apps and invite users).

### 2. Join Microsoft Developer Program

Visit: https://developer.microsoft.com/en-us/microsoft-365/dev-program

### 3. Azure App Registration- Follow this [guide](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)
- Sign in to the **Microsoft Entra admin center**
- Go to **Identity > Applications > App registrations** and select **New registration**
- Save the following:
  - **Client ID**
  - **Tenant ID**
  - **Client Secret** (under "Certificates & secrets")

### 4. Add API Permissions- In the App Registration → **API Permissions**
- Add permission: `Calendars.ReadWrite` under Microsoft Graph (Delegated or Application as needed)
- Click "Grant admin consent"

### 5. Install Required Python Packages

```bash
pip install -r requirements.txt
```

## Additional Resources

- [Microsoft Graph Python Tutorial](https://learn.microsoft.com/en-us/graph/tutorials/python?context=outlook%2Fcontext&tabs=aad)


# Get a Groq API Key
1. Go to [Groq Console](https://console.groq.com/home)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
