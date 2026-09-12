#!/usr/bin/env python3
"""
Demo Data Seeding Script
Seeds the database with demo recruiters, companies, and candidates for testing
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.user import User
from app.models.candidate import Candidate, CandidateSkill
from app.models.recruiter import Recruiter
from app.models.company import Company
from app.core.security import hash_password
from datetime import datetime

# Demo data
DEMO_CANDIDATES = [
    {
        "name": "Alice Johnson",
        "email": "alice@student.com",
        "password": "Student123!",
        "skills": ["Python", "JavaScript", "React", "PostgreSQL"],
        "bio": "Full-stack developer with 2 years of experience",
    },
    {
        "name": "Bob Smith",
        "email": "bob@student.com",
        "password": "Student123!",
        "skills": ["Java", "Spring Boot", "Docker", "Kubernetes"],
        "bio": "Backend engineer specializing in microservices",
    },
    {
        "name": "Carol White",
        "email": "carol@student.com",
        "password": "Student123!",
        "skills": ["Data Science", "Python", "TensorFlow", "SQL"],
        "bio": "Data scientist with ML expertise",
    },
    {
        "name": "David Lee",
        "email": "david@student.com",
        "password": "Student123!",
        "skills": ["Frontend", "React", "TypeScript", "CSS", "UI/UX"],
        "bio": "Frontend engineer focused on user experience",
    },
    {
        "name": "Emma Brown",
        "email": "emma@student.com",
        "password": "Student123!",
        "skills": ["DevOps", "AWS", "Terraform", "CI/CD"],
        "bio": "DevOps engineer with cloud infrastructure expertise",
    },
]

DEMO_COMPANIES = [
    {
        "name": "TechCorp Solutions",
        "description": "Leading software development company",
        "website": "https://techcorp.example.com",
        "location": "San Francisco, CA",
    },
    {
        "name": "DataViz Analytics",
        "description": "Data analytics and visualization platform",
        "website": "https://dataviz.example.com",
        "location": "New York, NY",
    },
    {
        "name": "CloudStack Systems",
        "description": "Cloud infrastructure solutions",
        "website": "https://cloudstack.example.com",
        "location": "Seattle, WA",
    },
    {
        "name": "FinTech Innovations",
        "description": "Financial technology solutions",
        "website": "https://fintech.example.com",
        "location": "Boston, MA",
    },
    {
        "name": "AI Research Labs",
        "description": "Artificial intelligence research and development",
        "website": "https://airesearch.example.com",
        "location": "Palo Alto, CA",
    },
]

DEMO_RECRUITERS = [
    {
        "name": "Sarah Martinez",
        "email": "sarah@recruiter.com",
        "password": "Recruiter123!",
        "company_name": "TechCorp Solutions",
        "title": "Senior Recruiter",
        "phone": "+1-555-0001",
    },
    {
        "name": "James Wilson",
        "email": "james@recruiter.com",
        "password": "Recruiter123!",
        "company_name": "DataViz Analytics",
        "title": "Talent Acquisition Manager",
        "phone": "+1-555-0002",
    },
    {
        "name": "Lisa Chen",
        "email": "lisa@recruiter.com",
        "password": "Recruiter123!",
        "company_name": "CloudStack Systems",
        "title": "HR Specialist",
        "phone": "+1-555-0003",
    },
    {
        "name": "Michael Johnson",
        "email": "michael@recruiter.com",
        "password": "Recruiter123!",
        "company_name": "FinTech Innovations",
        "title": "Technical Recruiter",
        "phone": "+1-555-0004",
    },
    {
        "name": "Jennifer Davis",
        "email": "jennifer@recruiter.com",
        "password": "Recruiter123!",
        "company_name": "AI Research Labs",
        "title": "Recruitment Director",
        "phone": "+1-555-0005",
    },
]


def seed_database():
    """Seed the database with demo data"""
    
    # Create engine and session
    engine = create_engine(settings.db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        print("🌱 Starting database seeding...\n")
        
        # Check if demo data already exists
        existing = session.query(User).filter_by(email="sarah@recruiter.com").first()
        if existing:
            print("⚠️  Demo data already exists! Skipping seeding.")
            print("To reseed, delete existing users first.\n")
            return
        
        # Create companies first
        print("📋 Creating companies...")
        companies = {}
        for company_data in DEMO_COMPANIES:
            company = Company(
                name=company_data["name"],
                description=company_data["description"],
                website=company_data["website"],
                location=company_data["location"],
            )
            session.add(company)
            companies[company_data["name"]] = company
        session.commit()
        print(f"✅ Created {len(companies)} companies\n")
        
        # Create candidates (students)
        print("👥 Creating candidate accounts (Students)...")
        for candidate_data in DEMO_CANDIDATES:
            user = User(
                name=candidate_data["name"],
                email=candidate_data["email"],
                password_hash=hash_password(candidate_data["password"]),
                role="CANDIDATE",
                enabled=True,
            )
            session.add(user)
            session.flush()  # Get the user ID
            
            candidate = Candidate(
                id=user.id,  # Use same ID as user (1:1 relationship)
                bio=candidate_data["bio"],
            )
            session.add(candidate)
            
            # Add skills
            for skill in candidate_data["skills"]:
                skill_obj = CandidateSkill(
                    candidate_id=user.id,
                    skill=skill
                )
                session.add(skill_obj)
        
        session.commit()
        print(f"✅ Created {len(DEMO_CANDIDATES)} candidate accounts\n")
        
        # Create recruiters
        print("💼 Creating recruiter accounts...")
        for recruiter_data in DEMO_RECRUITERS:
            company = companies[recruiter_data["company_name"]]
            
            user = User(
                name=recruiter_data["name"],
                email=recruiter_data["email"],
                password_hash=hash_password(recruiter_data["password"]),
                role="RECRUITER",
                enabled=True,
            )
            session.add(user)
            session.flush()  # Get the user ID
            
            recruiter = Recruiter(
                id=user.id,  # Use same ID as user (1:1 relationship)
                company_id=company.id,
                title=recruiter_data["title"],
                phone=recruiter_data["phone"],
            )
            session.add(recruiter)
        
        session.commit()
        print(f"✅ Created {len(DEMO_RECRUITERS)} recruiter accounts\n")
        
        print("=" * 60)
        print("🎉 DATABASE SEEDING COMPLETE!\n")
        
        print("📚 LOGIN CREDENTIALS:\n")
        
        print("👨‍💼 ADMIN ACCOUNT:")
        print("   Email:    admin@example.com")
        print("   Password: Admin123!\n")
        
        print("👥 CANDIDATE ACCOUNTS (Students):")
        for candidate in DEMO_CANDIDATES:
            print(f"   Email:    {candidate['email']}")
            print(f"   Password: {candidate['password']}")
            print(f"   Skills:   {', '.join(candidate['skills'])}\n")
        
        print("💼 RECRUITER ACCOUNTS:")
        for recruiter in DEMO_RECRUITERS:
            print(f"   Email:    {recruiter['email']}")
            print(f"   Password: {recruiter['password']}")
            print(f"   Company:  {recruiter['company_name']}")
            print(f"   Title:    {recruiter['title']}\n")
        
        print("=" * 60)
        print("\n🌐 Access at: http://localhost:5173")
        print("📖 API Docs: http://localhost:8080/docs\n")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed_database()
