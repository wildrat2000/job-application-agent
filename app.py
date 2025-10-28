import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Page configuration
st.set_page_config(
    page_title="Samuel's Job Application Agent",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #D1FAE5;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #10B981;
    }
    .job-card {
        background-color: #F8FAFC;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
        border-left: 4px solid #3B82F6;
    }
</style>
""", unsafe_allow_html=True)

class CloudJobAgent:
    def __init__(self):
        self.samuel_profile = {
            "name": "Samuel Mbugua Wambaa",
            "email": "swambaa@gmail.com",
            "phone": "+254 721 219359",
            "skills": [
                "Network & Systems Administration (Windows, Linux)",
                "Microsoft 365 / SharePoint Online Administration", 
                "Cloud Services (AWS EC2, Office 365, Zimbra)",
                "VOIP Systems Deployment (Asterisk, Elastix)",
                "LAN/WAN Design and Network Rollout",
                "ERP Systems Implementation"
            ],
            "experience": 20
        }
    
    def search_remote_jobs(self, platforms=["remoteok"]):
        """Search jobs from multiple platforms"""
        jobs = []
        
        try:
            # Remote OK API
            if "remoteok" in platforms:
                remoteok_jobs = self.search_remoteok()
                jobs.extend(remoteok_jobs)
                
        except Exception as e:
            st.error(f"Search error: {e}")
            
        return jobs
    def search_remoteok(self):
    """Search Remote OK API"""
    try:
        url = "https://remoteok.io/api?tags=devops&tags=it"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            jobs_data = response.json()
            filtered_jobs = []
            
            for job in jobs_data[1:11]:  # First 10 jobs
                if job.get('position'):
                    # Filter for Samuel's skills
                    description = f"{job.get('position', '')} {job.get('description', '')}".lower()
                    relevant_skills = ['network', 'system', 'cloud', 'sharepoint', 'aws', 'linux', 'voip', 'administrator']
                    
                    if any(skill in description for skill in relevant_skills):
                        filtered_jobs.append({
                            'title': job.get('position', ''),
                            'company': job.get('company', ''),
                            'description': job.get('description', '')[:200] + '...',
                            'url': f"https://remoteok.io/l/{job.get('id', '')}",
                            'platform': 'Remote OK',
                            'date_found': datetime.now().strftime('%Y-%m-%d')
                        })
            
            return filtered_jobs
    except Exception as e:
        st.error(f"Remote OK search error: {e}")
        return []
    
    return []
  
    def calculate_match_score(self, job_description):
        """Calculate job match score"""
        job_desc_lower = job_description.lower()
        key_skills = ['network', 'system administrator', 'sharepoint', 'aws', 'office 365', 
                     'linux', 'windows server', 'voip', 'cloud', 'helpdesk']
        
        matches = sum(1 for skill in key_skills if skill in job_desc_lower)
        return min(100, (matches / len(key_skills)) * 100)
    
    def generate_cover_letter(self, job_title, company, job_description):
        """Generate AI-style cover letter"""
        
        match_score = self.calculate_match_score(job_description)
        
        cover_letter = f"""
Samuel Mbugua Wambaa
ICT Network Manager | Systems Administrator | ICT Consultant
+254 721 219359 | swambaa@gmail.com
LinkedIn: linkedin.com/in/samuel-wambaa-974a06373

{datetime.now().strftime('%B %d, %Y')}

Hiring Manager
{company}

Dear Hiring Manager,

I am writing to express my enthusiastic interest in the {job_title} position at {company}. With over 20 years of comprehensive ICT experience, I have developed expertise that aligns perfectly with your requirements.

Your organization's needs particularly resonate with my background in:

"""
        
        # Dynamic content based on job description
        if 'sharepoint' in job_description.lower():
            cover_letter += "• **SharePoint Online Administration**: Successfully developed global intranet portals for 78 countries and trained 80+ regional trainers\n"
        
        if 'aws' in job_description.lower() or 'cloud' in job_description.lower():
            cover_letter += "• **Cloud Infrastructure Management**: Extensive experience with AWS EC2, Office 365, and hybrid cloud environments\n"
        
        if 'network' in job_description.lower():
            cover_letter += "• **Network Architecture**: Designed and implemented robust LAN/WAN networks across multiple locations\n"
        
        if 'voip' in job_description.lower():
            cover_letter += "• **VOIP Systems**: Deployed Asterisk/Elastix VOIP solutions for enhanced communication\n"
        
        # Default strengths
        cover_letter += f"""
My recent accomplishments include:
- Leading ICT infrastructure for laboratory operations across 10 districts in Somalia
- Managing Office 365 cloud email for 200+ users
- Implementing AWS backup systems and virtual server environments

I am confident that my {self.samuel_profile['experience']}-year track record in ICT management and my passion for technological innovation would make me a valuable asset to your team.

Thank you for considering my application. I look forward to discussing how my skills can contribute to {company}'s success.

Sincerely,
Samuel Mbugua Wambaa
"""
        
        return cover_letter, match_score

def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 Samuel\'s Cloud Job Application Agent</h1>', unsafe_allow_html=True)
    
    # Initialize agent
    agent = CloudJobAgent()
    
    # Sidebar
    st.sidebar.title("Configuration")
    st.sidebar.markdown("---")
    
    # Search settings
    platforms = st.sidebar.multiselect(
        "Job Platforms",
        ["remoteok", "linkedin", "indeed", "glassdoor"],
        default=["remoteok"]
    )
    
    min_match_score = st.sidebar.slider("Minimum Match Score", 0, 100, 60)
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Job Search", "📊 Applications", "✉️ Cover Letters", "⚙️ Profile"])
    
    with tab1:
        st.subheader("Find Remote IT Jobs")
        
        if st.button("🎯 Search Jobs", type="primary"):
            with st.spinner("Searching for matching jobs..."):
                jobs = agent.search_remote_jobs(platforms)
                
                if jobs:
                    st.success(f"Found {len(jobs)} relevant jobs!")
                    
                    for i, job in enumerate(jobs):
                        match_score = agent.calculate_match_score(job['description'])
                        
                        if match_score >= min_match_score:
                            with st.container():
                                st.markdown(f"""
                                <div class="job-card">
                                    <h4>{job['title']}</h4>
                                    <p><strong>Company:</strong> {job['company']} | <strong>Platform:</strong> {job['platform']}</p>
                                    <p><strong>Match Score:</strong> {match_score:.1f}%</p>
                                    <p>{job['description']}</p>
                                    <a href="{job['url']}" target="_blank">View Job</a>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Application buttons
                                col1, col2 = st.columns([1, 1])
                                with col1:
                                    if st.button(f"Generate Cover Letter", key=f"letter_{i}"):
                                        cover_letter, _ = agent.generate_cover_letter(
                                            job['title'], job['company'], job['description']
                                        )
                                        st.session_state[f'cover_letter_{i}'] = cover_letter
                                        st.session_state[f'current_job_{i}'] = job
                                
                                with col2:
                                    if st.button("Save Job", key=f"save_{i}"):
                                        if 'saved_jobs' not in st.session_state:
                                            st.session_state.saved_jobs = []
                                        st.session_state.saved_jobs.append(job)
                                        st.success("Job saved!")
                                
                                # Show cover letter if generated
                                if f'cover_letter_{i}' in st.session_state:
                                    st.text_area("Generated Cover Letter", 
                                               st.session_state[f'cover_letter_{i}'], 
                                               height=300,
                                               key=f"textarea_{i}")
                                
                                st.markdown("---")
                else:
                    st.warning("No jobs found. Try different platforms or check your connection.")
    
    with tab2:
        st.subheader("Application Dashboard")
        
        if 'saved_jobs' in st.session_state and st.session_state.saved_jobs:
            st.metric("Saved Jobs", len(st.session_state.saved_jobs))
            
            # Create applications dataframe
            apps_data = []
            for job in st.session_state.saved_jobs:
                match_score = agent.calculate_match_score(job['description'])
                apps_data.append({
                    'Job Title': job['title'],
                    'Company': job['company'],
                    'Platform': job['platform'],
                    'Match Score': f"{match_score:.1f}%",
                    'Date Saved': job.get('date_found', 'N/A')
                })
            
            st.dataframe(pd.DataFrame(apps_data))
            
            # Export options
            if st.button("Export to CSV"):
                df = pd.DataFrame(apps_data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="samuel_job_applications.csv",
                    mime="text/csv"
                )
                
            # Clear saved jobs
            if st.button("Clear All Saved Jobs"):
                st.session_state.saved_jobs = []
                st.success("Saved jobs cleared!")
        else:
            st.info("No applications yet. Search for jobs and save them!")
    
    with tab3:
        st.subheader("Cover Letter Generator")
        
        job_title = st.text_input("Job Title", "Senior Network Administrator")
        company = st.text_input("Company Name", "Tech Solutions Inc")
        job_description = st.text_area("Job Description", "Looking for experienced network administrator with AWS and SharePoint skills...")
        
        if st.button("Generate Cover Letter"):
            cover_letter, match_score = agent.generate_cover_letter(job_title, company, job_description)
            
            st.metric("Job Match Score", f"{match_score:.1f}%")
            st.text_area("Custom Cover Letter", cover_letter, height=400)
            
            # Download option
            st.download_button(
                label="Download Cover Letter",
                data=cover_letter,
                file_name=f"cover_letter_{company}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    with tab4:
        st.subheader("Samuel's Profile")
        
        st.write("**Samuel Mbugua Wambaa**")
        st.write(f"**Experience:** {agent.samuel_profile['experience']} years")
        st.write("**Email:** swambaa@gmail.com")
        st.write("**Phone:** +254 721 219359")
        st.write("**Location:** Nairobi, Kenya")
        
        st.subheader("Key Skills")
        for skill in agent.samuel_profile['skills']:
            st.write(f"• {skill}")
        
        st.subheader("About This App")
        st.info("""
        This cloud-based job application agent helps Samuel find and apply for remote IT positions.
        Features include:
        - Automated job searching across multiple platforms
        - Intelligent job matching based on Samuel's skills
        - Custom cover letter generation
        - Application tracking dashboard
        - Cloud access from any device
        """)

if __name__ == "__main__":
    main()
