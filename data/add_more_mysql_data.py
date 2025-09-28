#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add more sample data to MySQL database for Track-B application
"""

import mysql.connector
import json
import random
from datetime import datetime, timedelta

# MySQL配置
MYSQL_CONFIG = {
    'host': 'test.2brain.ai',
    'user': 'Track_B_2',
    'password': 'mfsd123_B_2',
    'database': 'bee_beta2'
}

def connect_to_mysql():
    """连接到MySQL数据库"""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        print("Successfully connected to MySQL database")
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def add_more_users(conn, count=50):
    """添加更多用户数据"""
    cursor = conn.cursor()
    
    industries = ['Technology', 'Finance', 'Healthcare', 'Education', 'Marketing', 
                 'Consulting', 'Real Estate', 'Manufacturing', 'Retail', 'Media']
    
    education_levels = ['High School', 'Associate', 'Bachelor', 'Master', 'PhD', 'MBA']
    
    for i in range(count):
        username = f"user_{i+11}"
        email = f"user{i+11}@example.com"
        full_name = f"User {i+11}"
        phone = f"+1-555-{1000+i:04d}"
        location = f"City {i+1}, State {i+1}"
        industry = random.choice(industries)
        experience_years = random.randint(0, 15)
        education_level = random.choice(education_levels)
        
        try:
            cursor.execute("""
                INSERT INTO user_profiles 
                (username, email, full_name, phone, location, industry, experience_years, education_level)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (username, email, full_name, phone, location, industry, experience_years, education_level))
        except mysql.connector.IntegrityError:
            continue
    
    conn.commit()
    cursor.close()
    print(f"Added {count} new users")

def add_more_jobs(conn, count=100):
    """添加更多职位数据"""
    cursor = conn.cursor()
    
    job_templates = [
        {
            'title': 'Software Engineer',
            'description': 'Develop and maintain software applications using modern technologies and best practices.',
            'requirements': 'Bachelor\'s degree in Computer Science or related field, experience with programming languages, knowledge of software development methodologies',
            'skills': ['JavaScript', 'Python', 'Java', 'React', 'Node.js', 'SQL'],
            'salary_min': 70000,
            'salary_max': 120000
        },
        {
            'title': 'Data Analyst',
            'description': 'Analyze data to provide insights and support business decisions through reporting and visualization.',
            'requirements': 'Strong analytical skills, experience with data analysis tools, knowledge of SQL and Excel',
            'skills': ['SQL', 'Excel', 'Python', 'Tableau', 'Power BI', 'Statistics'],
            'salary_min': 55000,
            'salary_max': 90000
        },
        {
            'title': 'Marketing Manager',
            'description': 'Develop and execute marketing strategies to increase brand awareness and drive customer acquisition.',
            'requirements': 'Experience in marketing, strong communication skills, knowledge of digital marketing tools',
            'skills': ['Digital Marketing', 'Google Analytics', 'Social Media', 'Content Marketing', 'SEO', 'Email Marketing'],
            'salary_min': 65000,
            'salary_max': 110000
        },
        {
            'title': 'Project Manager',
            'description': 'Lead project teams to deliver projects on time, within budget, and according to specifications.',
            'requirements': 'Project management experience, strong leadership skills, knowledge of project management methodologies',
            'skills': ['Project Management', 'Agile', 'Scrum', 'Risk Management', 'Stakeholder Management', 'JIRA'],
            'salary_min': 75000,
            'salary_max': 130000
        },
        {
            'title': 'UX/UI Designer',
            'description': 'Create user-centered designs by understanding business requirements and user feedback.',
            'requirements': 'Portfolio demonstrating design skills, experience with design tools, knowledge of user research',
            'skills': ['Figma', 'Sketch', 'Adobe Creative Suite', 'User Research', 'Prototyping', 'Design Systems'],
            'salary_min': 60000,
            'salary_max': 100000
        }
    ]
    
    companies = [
        'TechCorp Inc.', 'DataFlow Analytics', 'InnovateTech', 'DesignStudio', 'CloudFirst Solutions',
        'GrowthMarketing', 'FinancePro', 'SalesForce Solutions', 'PeopleFirst HR', 'QualityTech',
        'AITech Solutions', 'WebCraft Studios', 'ServerTech', 'BusinessInsights', 'CustomerFirst',
        'Digital Dynamics', 'Future Systems', 'Global Solutions', 'NextGen Technologies', 'Smart Solutions'
    ]
    
    locations = [
        'San Francisco, CA', 'New York, NY', 'Seattle, WA', 'Austin, TX', 'Boston, MA',
        'Los Angeles, CA', 'Chicago, IL', 'Denver, CO', 'Miami, FL', 'Phoenix, AZ',
        'Atlanta, GA', 'Dallas, TX', 'Portland, OR', 'Nashville, TN', 'Charlotte, NC'
    ]
    
    job_types = ['full-time', 'part-time', 'contract', 'internship']
    experience_levels = ['entry', 'mid', 'senior', 'executive']
    
    for i in range(count):
        template = random.choice(job_templates)
        company = random.choice(companies)
        location = random.choice(locations)
        job_type = random.choice(job_types)
        experience_level = random.choice(experience_levels)
        
        # 根据经验级别调整薪资
        salary_multiplier = {'entry': 0.7, 'mid': 1.0, 'senior': 1.3, 'executive': 1.8}
        multiplier = salary_multiplier[experience_level]
        
        salary_min = int(template['salary_min'] * multiplier)
        salary_max = int(template['salary_max'] * multiplier)
        
        # 随机调整技能
        skills = random.sample(template['skills'], random.randint(3, len(template['skills'])))
        
        cursor.execute("""
            INSERT INTO job_postings 
            (title, company, location, description, requirements, salary_min, salary_max, 
             job_type, experience_level, skills, benefits, contact_email, application_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            template['title'],
            company,
            location,
            template['description'],
            template['requirements'],
            salary_min,
            salary_max,
            job_type,
            experience_level,
            json.dumps(skills),
            'Health insurance, 401k, flexible work hours, professional development',
            f'careers@{company.lower().replace(" ", "").replace(".", "").replace(",", "")}.com',
            f'https://{company.lower().replace(" ", "").replace(".", "").replace(",", "")}.com/careers'
        ))
    
    conn.commit()
    cursor.close()
    print(f"Added {count} new job postings")

def add_more_resumes(conn, count=200):
    """添加更多简历数据"""
    cursor = conn.cursor()
    
    # 获取所有用户ID
    cursor.execute("SELECT id FROM user_profiles")
    user_ids = [row[0] for row in cursor.fetchall()]
    
    categories = ['Technology', 'Finance', 'Marketing', 'Sales', 'Design', 'Data', 'Engineering', 'Management']
    
    resume_templates = [
        {
            'title': 'Software Developer',
            'skills': ['Python', 'JavaScript', 'React', 'Node.js', 'SQL', 'Git'],
            'experience': '3+ years of software development experience',
            'education': 'Bachelor in Computer Science'
        },
        {
            'title': 'Data Analyst',
            'skills': ['SQL', 'Python', 'Excel', 'Tableau', 'Statistics', 'R'],
            'experience': '2+ years of data analysis experience',
            'education': 'Bachelor in Statistics'
        },
        {
            'title': 'Marketing Specialist',
            'skills': ['Digital Marketing', 'Google Analytics', 'Social Media', 'Content Creation', 'SEO'],
            'experience': '2+ years of marketing experience',
            'education': 'Bachelor in Marketing'
        },
        {
            'title': 'Sales Representative',
            'skills': ['B2B Sales', 'CRM', 'Negotiation', 'Client Relationship', 'Sales Strategy'],
            'experience': '3+ years of sales experience',
            'education': 'Bachelor in Business'
        },
        {
            'title': 'UX Designer',
            'skills': ['Figma', 'User Research', 'Prototyping', 'Design Systems', 'Adobe Creative Suite'],
            'experience': '2+ years of UX design experience',
            'education': 'Bachelor in Design'
        }
    ]
    
    for i in range(count):
        user_id = random.choice(user_ids)
        template = random.choice(resume_templates)
        category = random.choice(categories)
        
        # 生成简历文本
        resume_text = f"""
User {i+1}
{template['title']}
{template['experience']}

Skills: {', '.join(random.sample(template['skills'], random.randint(3, len(template['skills']))))}

Education: {template['education']}

Experience:
- Company {i+1} ({random.randint(1, 5)} years)
- Company {i+2} ({random.randint(1, 3)} years)

Projects:
- Project {i+1}: {template['title']} related project
- Project {i+2}: Data analysis and visualization

Certifications:
- {template['title']} Certification
- Professional Development Certificate
        """.strip()
        
        # 生成建议
        suggestions = [
            'Consider adding more quantifiable achievements to your resume.',
            'Highlight specific projects and their impact on business outcomes.',
            'Include more industry-specific keywords to improve ATS compatibility.',
            'Add leadership experience and team management skills.',
            'Consider obtaining relevant certifications to enhance your profile.',
            'Include metrics and KPIs to demonstrate your impact.',
            'Add more technical skills relevant to your target industry.',
            'Consider adding a summary section to highlight key strengths.'
        ]
        
        suggestion = random.choice(suggestions)
        
        # 生成职位匹配
        job_matches = [
            {
                'title': template['title'],
                'location': f"City {i+1}, State {i+1}",
                'skills': random.sample(template['skills'], random.randint(2, 4))
            }
        ]
        
        score = round(random.uniform(3.0, 4.8), 1)
        file_name = f"user_{i+1}_resume.pdf"
        file_size = random.randint(100000, 500000)
        
        cursor.execute("""
            INSERT INTO resumes 
            (user_id, resume_text, suggestion, job_matches, score, category, file_name, file_size)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id,
            resume_text,
            suggestion,
            json.dumps(job_matches),
            score,
            category,
            file_name,
            file_size
        ))
    
    conn.commit()
    cursor.close()
    print(f"Added {count} new resumes")

def add_more_applications(conn, count=300):
    """添加更多职位申请数据"""
    cursor = conn.cursor()
    
    # 获取所有用户ID、职位ID和简历ID
    cursor.execute("SELECT id FROM user_profiles")
    user_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id FROM job_postings")
    job_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id FROM resumes")
    resume_ids = [row[0] for row in cursor.fetchall()]
    
    statuses = ['pending', 'reviewed', 'interviewed', 'offered', 'rejected']
    
    notes_templates = [
        'Application received, under review',
        'Strong background, scheduled for interview',
        'Technical skills match requirements',
        'Experience level below requirements',
        'Perfect fit for the role',
        'Moving to next round of interviews',
        'Application submitted successfully',
        'Good cultural fit, considering for role',
        'Skills gap identified',
        'Excellent communication skills'
    ]
    
    for i in range(count):
        user_id = random.choice(user_ids)
        job_id = random.choice(job_ids)
        resume_id = random.choice(resume_ids)
        status = random.choice(statuses)
        notes = random.choice(notes_templates)
        
        cursor.execute("""
            INSERT INTO job_applications 
            (user_id, job_id, resume_id, status, notes)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, job_id, resume_id, status, notes))
    
    conn.commit()
    cursor.close()
    print(f"Added {count} new job applications")

def add_more_analyses(conn, count=150):
    """添加更多简历分析数据"""
    cursor = conn.cursor()
    
    # 获取所有用户ID和简历ID
    cursor.execute("SELECT id FROM user_profiles")
    user_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id FROM resumes")
    resume_ids = [row[0] for row in cursor.fetchall()]
    
    analysis_types = ['skills_gap', 'market_fit', 'improvement_suggestions', 'salary_analysis', 'career_path']
    
    for i in range(count):
        user_id = random.choice(user_ids)
        resume_id = random.choice(resume_ids)
        analysis_type = random.choice(analysis_types)
        
        # 根据分析类型生成不同的结果
        if analysis_type == 'skills_gap':
            analysis_result = {
                'missing_skills': random.sample(['Python', 'JavaScript', 'AWS', 'Docker', 'Kubernetes', 'React', 'Node.js'], random.randint(1, 3)),
                'recommended_courses': random.sample(['Python Fundamentals', 'AWS Cloud Practitioner', 'Docker Basics', 'React Development'], random.randint(1, 2)),
                'skill_match_percentage': random.randint(60, 95)
            }
        elif analysis_type == 'market_fit':
            analysis_result = {
                'market_demand': random.choice(['High', 'Medium', 'Very High', 'Low']),
                'salary_range': f"${random.randint(50, 150)}k-${random.randint(80, 200)}k",
                'growth_potential': random.choice(['Strong', 'Excellent', 'Good', 'Limited']),
                'recommended_roles': random.sample(['Software Engineer', 'Data Analyst', 'Product Manager', 'UX Designer'], random.randint(1, 3))
            }
        elif analysis_type == 'improvement_suggestions':
            analysis_result = {
                'strengths': random.sample(['Strong technical background', 'Good communication skills', 'Relevant experience', 'Educational background'], random.randint(2, 4)),
                'weaknesses': random.sample(['Limited leadership experience', 'Need more quantifiable achievements', 'Skills gap in emerging technologies'], random.randint(1, 2)),
                'recommendations': random.sample(['Add more metrics', 'Include leadership examples', 'Obtain relevant certifications', 'Highlight project impact'], random.randint(2, 3))
            }
        elif analysis_type == 'salary_analysis':
            analysis_result = {
                'current_market_rate': f"${random.randint(60, 120)}k",
                'experience_multiplier': round(random.uniform(0.8, 1.5), 2),
                'location_adjustment': round(random.uniform(0.9, 1.3), 2),
                'recommended_salary_range': f"${random.randint(70, 140)}k-${random.randint(90, 180)}k"
            }
        else:  # career_path
            analysis_result = {
                'current_level': random.choice(['Entry', 'Mid', 'Senior']),
                'next_steps': random.sample(['Obtain certification', 'Take leadership role', 'Learn new technology', 'Network in industry'], random.randint(2, 3)),
                'timeline': f"{random.randint(1, 3)} years",
                'potential_roles': random.sample(['Senior Developer', 'Team Lead', 'Architect', 'Manager'], random.randint(1, 2))
            }
        
        cursor.execute("""
            INSERT INTO user_resume_analyses 
            (user_id, resume_id, analysis_type, analysis_result)
            VALUES (%s, %s, %s, %s)
        """, (user_id, resume_id, analysis_type, json.dumps(analysis_result)))
    
    conn.commit()
    cursor.close()
    print(f"Added {count} new resume analyses")

def main():
    """主函数"""
    print("Starting to add more sample data to MySQL database...")
    
    conn = connect_to_mysql()
    if not conn:
        return
    
    try:
        # 添加更多数据
        add_more_users(conn, 50)
        add_more_jobs(conn, 100)
        add_more_resumes(conn, 200)
        add_more_applications(conn, 300)
        add_more_analyses(conn, 150)
        
        # 显示最终统计
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM user_profiles")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM job_postings")
        job_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM resumes")
        resume_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM job_applications")
        application_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM user_resume_analyses")
        analysis_count = cursor.fetchone()[0]
        
        cursor.close()
        
        print("\n" + "="*50)
        print("FINAL DATABASE STATISTICS:")
        print("="*50)
        print(f"Total Users: {user_count}")
        print(f"Total Job Postings: {job_count}")
        print(f"Total Resumes: {resume_count}")
        print(f"Total Job Applications: {application_count}")
        print(f"Total Resume Analyses: {analysis_count}")
        print("="*50)
        print("Sample data addition completed successfully!")
        
    except Exception as e:
        print(f"Error adding sample data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main() 