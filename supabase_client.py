# supabase_client.py

from supabase import create_client, Client

SUPABASE_URL = "https://pxtsbqztqynrlmyhwzbo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB4dHNicXp0cXlucmxteWh3emJvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTMxODczMzksImV4cCI6MjA2ODc2MzMzOX0.jOz6NUsOiRBmWy6Qi2hNC-CI9wozqn6Vuvuc2WdTZZY"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
