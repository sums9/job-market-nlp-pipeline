import requests
import pandas as pd

# A completely live, open-access tech job board API
API_URL = "https://www.arbeitnow.com/api/job-board-api"

print("Connecting to live Tech Job Board API...")
response = requests.get(API_URL)

if response.status_code == 200:
    data = response.json()
    raw_jobs = data.get('data', []) # The API stores its array inside the 'data' key
    
    print(f"Success! Fetched {len(raw_jobs)} live job postings from the server.")
    
    job_list = []
    
    for job in raw_jobs:
        title = job.get('title', '')
        # Filter to see if it's a data, analyst, or engineering role
        if any(keyword in title.lower() for keyword in ['data', 'analyst', 'engineer', 'developer']):
            job_list.append({
                "Job_Title": title,
                "Company": job.get('company_name', 'Unknown'),
                "Region": job.get('location', 'Remote'),
                "Remote": "Yes" if job.get('remote') else "No",
                "URL": job.get('url', '')
            })
            
    # Save the true data out
    df = pd.DataFrame(job_list)
    df.to_csv('real_live_jobs.csv', index=False)
    print(f"\n🎉 Genuine Portfolio Dataset Created! Saved {len(df)} real rows.")

else:
    print(f"Connection failed. Server responded with code: {response.status_code}")