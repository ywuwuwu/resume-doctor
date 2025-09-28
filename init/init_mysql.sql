-- MySQL init script

-- 创建数据库
CREATE DATABASE IF NOT EXISTS bee_beta2;
USE bee_beta2;

-- 删除已存在的表（如果存在）
DROP TABLE IF EXISTS user_resume_analyses;
DROP TABLE IF EXISTS job_applications;
DROP TABLE IF EXISTS user_profiles;
DROP TABLE IF EXISTS job_postings;
DROP TABLE IF EXISTS resumes;

-- 创建用户档案表
CREATE TABLE user_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    phone VARCHAR(20),
    location VARCHAR(200),
    industry VARCHAR(100),
    experience_years INT DEFAULT 0,
    education_level VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 创建简历表
CREATE TABLE resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    resume_text LONGTEXT NOT NULL,
    suggestion TEXT,
    job_matches JSON,
    score DECIMAL(3,2),
    category VARCHAR(100),
    file_name VARCHAR(255),
    file_size INT,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_profiles(id) ON DELETE SET NULL
);

-- 创建职位表
CREATE TABLE job_postings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(200) NOT NULL,
    location VARCHAR(200) NOT NULL,
    description TEXT,
    requirements TEXT,
    salary_min DECIMAL(10,2),
    salary_max DECIMAL(10,2),
    salary_currency VARCHAR(10) DEFAULT 'USD',
    job_type VARCHAR(50), -- full-time, part-time, contract, internship
    experience_level VARCHAR(50), -- entry, mid, senior, executive
    skills JSON,
    benefits TEXT,
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiry_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    contact_email VARCHAR(255),
    application_url VARCHAR(500)
);

-- 创建职位申请表
CREATE TABLE job_applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    job_id INT NOT NULL,
    resume_id INT NOT NULL,
    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending', -- pending, reviewed, interviewed, offered, rejected
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES user_profiles(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES job_postings(id) ON DELETE CASCADE,
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE
);

-- 创建简历分析历史表
CREATE TABLE user_resume_analyses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    resume_id INT,
    analysis_type VARCHAR(50), -- skills_gap, market_fit, improvement_suggestions
    analysis_result JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_profiles(id) ON DELETE SET NULL,
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE
);

-- 插入示例用户数据
INSERT INTO user_profiles (username, email, full_name, phone, location, industry, experience_years, education_level) VALUES
('john_doe', 'john.doe@email.com', 'John Doe', '+1-555-0101', 'San Francisco, CA', 'Technology', 5, 'Bachelor'),
('jane_smith', 'jane.smith@email.com', 'Jane Smith', '+1-555-0102', 'New York, NY', 'Finance', 3, 'Master'),
('mike_wilson', 'mike.wilson@email.com', 'Mike Wilson', '+1-555-0103', 'Austin, TX', 'Healthcare', 7, 'PhD'),
('sarah_jones', 'sarah.jones@email.com', 'Sarah Jones', '+1-555-0104', 'Seattle, WA', 'E-commerce', 2, 'Bachelor'),
('david_brown', 'david.brown@email.com', 'David Brown', '+1-555-0105', 'Boston, MA', 'Education', 4, 'Master'),
('lisa_wang', 'lisa.wang@email.com', 'Lisa Wang', '+1-555-0106', 'Los Angeles, CA', 'Marketing', 6, 'Bachelor'),
('robert_lee', 'robert.lee@email.com', 'Robert Lee', '+1-555-0107', 'Chicago, IL', 'Consulting', 8, 'MBA'),
('emily_chen', 'emily.chen@email.com', 'Emily Chen', '+1-555-0108', 'Denver, CO', 'Real Estate', 3, 'Bachelor'),
('alex_garcia', 'alex.garcia@email.com', 'Alex Garcia', '+1-555-0109', 'Miami, FL', 'Hospitality', 5, 'Associate'),
('maria_rodriguez', 'maria.rodriguez@email.com', 'Maria Rodriguez', '+1-555-0110', 'Phoenix, AZ', 'Manufacturing', 4, 'Bachelor');

-- 插入示例职位数据
INSERT INTO job_postings (title, company, location, description, requirements, salary_min, salary_max, job_type, experience_level, skills, benefits, contact_email, application_url) VALUES
('Senior Software Engineer', 'TechCorp Inc.', 'San Francisco, CA', 'We are looking for a Senior Software Engineer to join our growing team. You will be responsible for developing and maintaining high-quality software solutions.', '5+ years of experience in software development, proficiency in Python, Java, or JavaScript, experience with cloud platforms (AWS, GCP, Azure)', 120000.00, 180000.00, 'full-time', 'senior', '["Python", "Java", "JavaScript", "AWS", "Docker", "Kubernetes"]', 'Health insurance, 401k matching, flexible work hours, remote work options', 'careers@techcorp.com', 'https://techcorp.com/careers/senior-engineer'),
('Data Scientist', 'DataFlow Analytics', 'New York, NY', 'Join our data science team to build machine learning models and analyze large datasets to drive business decisions.', 'Master\'s degree in Statistics, Computer Science, or related field, experience with Python, R, SQL, and machine learning frameworks', 90000.00, 140000.00, 'full-time', 'mid', '["Python", "R", "SQL", "TensorFlow", "PyTorch", "Pandas", "NumPy"]', 'Competitive salary, health benefits, professional development budget', 'jobs@dataflow.com', 'https://dataflow.com/jobs/data-scientist'),
('Product Manager', 'InnovateTech', 'Seattle, WA', 'Lead product development initiatives and work closely with engineering and design teams to deliver exceptional user experiences.', '3+ years of product management experience, strong analytical skills, experience with agile methodologies', 100000.00, 160000.00, 'full-time', 'mid', '["Product Management", "Agile", "SQL", "Analytics", "User Research", "Prototyping"]', 'Stock options, health insurance, unlimited PTO', 'talent@innovatetech.com', 'https://innovatetech.com/careers/product-manager'),
('UX Designer', 'DesignStudio', 'Austin, TX', 'Create beautiful and intuitive user interfaces for web and mobile applications. Work with cross-functional teams to deliver exceptional user experiences.', 'Portfolio demonstrating UX/UI skills, proficiency in Figma, Sketch, or Adobe Creative Suite, experience with user research', 80000.00, 130000.00, 'full-time', 'mid', '["Figma", "Sketch", "Adobe Creative Suite", "User Research", "Prototyping", "Design Systems"]', 'Flexible work schedule, creative environment, professional tools provided', 'design@designstudio.com', 'https://designstudio.com/jobs/ux-designer'),
('DevOps Engineer', 'CloudFirst Solutions', 'Boston, MA', 'Build and maintain our cloud infrastructure, implement CI/CD pipelines, and ensure high availability of our services.', 'Experience with AWS, Azure, or GCP, knowledge of Docker, Kubernetes, and infrastructure as code', 95000.00, 150000.00, 'full-time', 'mid', '["AWS", "Docker", "Kubernetes", "Terraform", "Jenkins", "Linux", "Bash"]', 'Remote work options, health benefits, continuous learning opportunities', 'devops@cloudfirst.com', 'https://cloudfirst.com/careers/devops'),
('Marketing Specialist', 'GrowthMarketing', 'Los Angeles, CA', 'Develop and execute marketing campaigns across multiple channels to drive brand awareness and customer acquisition.', '2+ years of marketing experience, knowledge of digital marketing tools, strong communication skills', 60000.00, 90000.00, 'full-time', 'entry', '["Digital Marketing", "Google Analytics", "Social Media", "Content Creation", "Email Marketing"]', 'Performance bonuses, health insurance, flexible work hours', 'marketing@growthmarketing.com', 'https://growthmarketing.com/careers/marketing-specialist'),
('Financial Analyst', 'FinancePro', 'Chicago, IL', 'Analyze financial data, prepare reports, and provide insights to support business decisions and strategic planning.', 'Bachelor\'s degree in Finance, Accounting, or related field, proficiency in Excel and financial modeling', 65000.00, 95000.00, 'full-time', 'entry', '["Excel", "Financial Modeling", "SQL", "Power BI", "Accounting", "Valuation"]', '401k matching, health benefits, professional certification support', 'finance@financepro.com', 'https://financepro.com/careers/financial-analyst'),
('Sales Representative', 'SalesForce Solutions', 'Denver, CO', 'Build relationships with potential clients, understand their needs, and present solutions that drive value for their business.', 'Strong communication skills, experience in B2B sales, ability to meet and exceed sales targets', 50000.00, 80000.00, 'full-time', 'entry', '["B2B Sales", "CRM", "Negotiation", "Presentation Skills", "Customer Relationship"]', 'Commission structure, health benefits, car allowance', 'sales@salesforce.com', 'https://salesforce.com/careers/sales-rep'),
('Human Resources Manager', 'PeopleFirst HR', 'Miami, FL', 'Manage HR operations, develop policies, and support employee development and engagement initiatives.', '5+ years of HR experience, knowledge of employment laws, strong interpersonal skills', 70000.00, 110000.00, 'full-time', 'mid', '["HR Management", "Employment Law", "Recruitment", "Employee Relations", "HRIS"]', 'Health benefits, professional development, flexible work schedule', 'hr@peoplefirst.com', 'https://peoplefirst.com/careers/hr-manager'),
('Quality Assurance Engineer', 'QualityTech', 'Phoenix, AZ', 'Design and execute test plans, identify and report bugs, and ensure software quality across our product suite.', 'Experience with testing methodologies, knowledge of automation tools, attention to detail', 70000.00, 110000.00, 'full-time', 'mid', '["Manual Testing", "Automation Testing", "Selenium", "JIRA", "Test Planning", "Bug Tracking"]', 'Health insurance, 401k, professional development budget', 'qa@qualitytech.com', 'https://qualitytech.com/careers/qa-engineer'),
('Machine Learning Engineer', 'AITech Solutions', 'San Francisco, CA', 'Develop and deploy machine learning models, work with large datasets, and collaborate with data scientists and engineers.', 'Experience with ML frameworks, knowledge of Python, experience with cloud platforms', 110000.00, 170000.00, 'full-time', 'senior', '["Python", "TensorFlow", "PyTorch", "AWS", "Docker", "MLOps", "SQL"]', 'Stock options, health benefits, remote work options', 'ml@aitech.com', 'https://aitech.com/careers/ml-engineer'),
('Frontend Developer', 'WebCraft Studios', 'New York, NY', 'Build responsive and interactive web applications using modern JavaScript frameworks and best practices.', 'Proficiency in JavaScript, React, Vue, or Angular, experience with CSS and responsive design', 80000.00, 130000.00, 'full-time', 'mid', '["JavaScript", "React", "Vue", "Angular", "CSS", "HTML", "TypeScript"]', 'Flexible work hours, health benefits, professional tools', 'frontend@webcraft.com', 'https://webcraft.com/careers/frontend'),
('Backend Developer', 'ServerTech', 'Seattle, WA', 'Develop scalable backend services and APIs, work with databases, and ensure system reliability and performance.', 'Experience with Node.js, Python, or Java, knowledge of databases and API design', 85000.00, 140000.00, 'full-time', 'mid', '["Node.js", "Python", "Java", "PostgreSQL", "MongoDB", "Redis", "REST APIs"]', 'Health insurance, 401k, remote work options', 'backend@servertech.com', 'https://servertech.com/careers/backend'),
('Business Analyst', 'BusinessInsights', 'Austin, TX', 'Analyze business processes, gather requirements, and translate business needs into technical specifications.', 'Strong analytical skills, experience with requirements gathering, knowledge of business processes', 70000.00, 110000.00, 'full-time', 'mid', '["Business Analysis", "Requirements Gathering", "SQL", "Excel", "Process Modeling", "Stakeholder Management"]', 'Health benefits, professional development, flexible work schedule', 'ba@businessinsights.com', 'https://businessinsights.com/careers/business-analyst'),
('Customer Success Manager', 'CustomerFirst', 'Boston, MA', 'Build relationships with customers, ensure their success with our products, and drive customer satisfaction and retention.', 'Strong communication skills, experience in customer success or account management', 65000.00, 100000.00, 'full-time', 'mid', '["Customer Success", "Account Management", "CRM", "Customer Support", "Product Knowledge"]', 'Health insurance, performance bonuses, professional development', 'success@customerfirst.com', 'https://customerfirst.com/careers/customer-success');

-- 插入示例简历数据
INSERT INTO resumes (user_id, resume_text, suggestion, job_matches, score, category, file_name, file_size) VALUES
(1, 'John Doe\nSoftware Engineer\n5+ years of experience in full-stack development\nSkills: Python, JavaScript, React, Node.js, AWS\nEducation: Bachelor in Computer Science\nExperience: Senior Developer at TechCorp (3 years), Junior Developer at StartupXYZ (2 years)', 'Strong technical background with good experience. Consider adding more leadership experience and specific project achievements. Highlight quantifiable results from previous roles.', '[{"title": "Senior Software Engineer", "location": "San Francisco, CA", "skills": ["Python", "JavaScript", "AWS"]}, {"title": "Full Stack Developer", "location": "New York, NY", "skills": ["React", "Node.js", "Python"]}]', 4.2, 'Technology', 'john_doe_resume.pdf', 245760),
(2, 'Jane Smith\nFinancial Analyst\n3+ years of experience in financial modeling and analysis\nSkills: Excel, SQL, Power BI, Financial Modeling\nEducation: Master in Finance\nExperience: Financial Analyst at FinanceCorp (2 years), Intern at BankXYZ (1 year)', 'Good educational background and relevant experience. Consider adding more quantitative achievements and industry-specific certifications. Include specific financial metrics you\'ve improved.', '[{"title": "Financial Analyst", "location": "New York, NY", "skills": ["Excel", "Financial Modeling", "SQL"]}, {"title": "Investment Analyst", "location": "Chicago, IL", "skills": ["Power BI", "Financial Analysis"]}]', 3.8, 'Finance', 'jane_smith_resume.pdf', 198432),
(3, 'Mike Wilson\nData Scientist\n7+ years of experience in machine learning and statistical analysis\nSkills: Python, R, TensorFlow, PyTorch, SQL, AWS\nEducation: PhD in Statistics\nExperience: Senior Data Scientist at DataCorp (4 years), Research Scientist at University (3 years)', 'Excellent academic background and strong technical skills. Consider highlighting specific ML models you\'ve developed and their business impact. Add more industry-specific achievements.', '[{"title": "Data Scientist", "location": "New York, NY", "skills": ["Python", "R", "TensorFlow", "PyTorch"]}, {"title": "Machine Learning Engineer", "location": "San Francisco, CA", "skills": ["Python", "AWS", "ML"]}]', 4.5, 'Technology', 'mike_wilson_resume.pdf', 312456),
(4, 'Sarah Jones\nMarketing Specialist\n2+ years of experience in digital marketing\nSkills: Google Analytics, Social Media Marketing, Content Creation, Email Marketing\nEducation: Bachelor in Marketing\nExperience: Marketing Coordinator at GrowthCorp (2 years)', 'Good foundation in digital marketing. Consider adding more campaign results and ROI metrics. Include specific social media campaigns you\'ve managed and their performance.', '[{"title": "Marketing Specialist", "location": "Los Angeles, CA", "skills": ["Digital Marketing", "Google Analytics", "Social Media"]}, {"title": "Digital Marketing Coordinator", "location": "Austin, TX", "skills": ["Content Creation", "Email Marketing"]}]', 3.2, 'Marketing', 'sarah_jones_resume.pdf', 156789),
(5, 'David Brown\nProduct Manager\n4+ years of experience in product management\nSkills: Product Strategy, Agile, User Research, Analytics, SQL\nEducation: Master in Business Administration\nExperience: Product Manager at TechStartup (3 years), Associate PM at BigCorp (1 year)', 'Strong product management background. Consider adding more specific product launches and their success metrics. Highlight user research methodologies you\'ve used.', '[{"title": "Product Manager", "location": "Seattle, WA", "skills": ["Product Management", "Agile", "Analytics"]}, {"title": "Senior Product Manager", "location": "San Francisco, CA", "skills": ["User Research", "Product Strategy"]}]', 4.0, 'Technology', 'david_brown_resume.pdf', 223456);

-- 插入示例职位申请数据
INSERT INTO job_applications (user_id, job_id, resume_id, status, notes) VALUES
(1, 1, 1, 'reviewed', 'Strong technical background, scheduled for technical interview'),
(2, 7, 2, 'pending', 'Application received, under review'),
(3, 2, 3, 'interviewed', 'Excellent technical skills, considering for next round'),
(4, 6, 4, 'rejected', 'Experience level below requirements'),
(5, 3, 5, 'offered', 'Perfect fit for the role, offer extended'),
(1, 11, 1, 'pending', 'Application submitted'),
(2, 7, 2, 'reviewed', 'Good financial background, moving to interview stage'),
(3, 11, 3, 'interviewed', 'Strong ML background, technical interview completed'),
(4, 6, 4, 'pending', 'Application under review'),
(5, 3, 5, 'offered', 'Offer accepted, starting next month');

-- 插入示例简历分析数据
INSERT INTO user_resume_analyses (user_id, resume_id, analysis_type, analysis_result) VALUES
(1, 1, 'skills_gap', '{"missing_skills": ["Kubernetes", "Docker"], "recommended_courses": ["Docker Fundamentals", "Kubernetes Basics"], "skill_match_percentage": 85}'),
(2, 2, 'market_fit', '{"market_demand": "High", "salary_range": "$65k-$95k", "growth_potential": "Strong", "recommended_roles": ["Financial Analyst", "Investment Analyst"]}'),
(3, 3, 'improvement_suggestions', '{"strengths": ["Strong technical background", "PhD qualification"], "weaknesses": ["Limited industry experience", "Need more business impact examples"], "recommendations": ["Add quantifiable achievements", "Include business impact metrics"]}'),
(4, 4, 'skills_gap', '{"missing_skills": ["Marketing Automation", "SEO"], "recommended_courses": ["HubSpot Marketing", "SEO Fundamentals"], "skill_match_percentage": 70}'),
(5, 5, 'market_fit', '{"market_demand": "Very High", "salary_range": "$100k-$160k", "growth_potential": "Excellent", "recommended_roles": ["Product Manager", "Senior Product Manager"]}');

-- 创建索引以提高查询性能
CREATE INDEX idx_resumes_user_id ON resumes(user_id);
CREATE INDEX idx_resumes_category ON resumes(category);
CREATE INDEX idx_job_applications_user_id ON job_applications(user_id);
CREATE INDEX idx_job_applications_job_id ON job_applications(job_id);
CREATE INDEX idx_job_applications_status ON job_applications(status);
CREATE INDEX idx_job_postings_location ON job_postings(location);
CREATE INDEX idx_job_postings_job_type ON job_postings(job_type);
CREATE INDEX idx_job_postings_experience_level ON job_postings(experience_level);

-- 显示表结构和数据统计
