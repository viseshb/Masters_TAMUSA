import pandas as pd
import random

def generate_full_real_jobs_excel(n=10000, output_path="synthetic_real_jobs.xlsx"):
    titles = ["Data Scientist", "Software Engineer", "Product Manager", "DevOps Engineer", "Security Analyst"]
    descriptions = [
        "Develop scalable applications and collaborate with cross-functional teams.",
        "Analyze large datasets to derive actionable insights.",
        "Manage product roadmaps and oversee feature rollouts.",
        "Maintain cloud infrastructure and automate CI/CD pipelines.",
        "Ensure system security and compliance with global standards."
    ]
    requirements = [
        "Python, SQL, Machine Learning",
        "JavaScript, React, Node.js",
        "Agile, Scrum, stakeholder communication",
        "Docker, Kubernetes, AWS",
        "Firewall configuration, incident response, risk analysis"
    ]
    company_prefixes = ["Acme", "BetaSoft", "Nova", "Alpha", "TechWave", "InfoX", "CloudCore", "LearnX"]
    domains = ["cloud solutions", "AI tools", "data analytics", "cybersecurity software", "e-learning platforms"]
    regions = ["US", "Europe", "Asia", "Canada", "Australia"]

    locations = ["USA", "Germany", "Canada", "UK", "India"]
    salary_ranges = ["$80k-$100k", "$100k-$130k", "$60k-$90k", "$120k-$150k"]
    employment_types = ["Full-time", "Contract", "Internship", "Temporary"]
    industries = ["Technology", "Healthcare", "Finance", "Retail", "Education"]
    benefits = ["Health Insurance", "Remote Work", "401k", "Flexible Hours", "Free Meals"]

    rows = []
    for _ in range(n):
        row = {
            "title": random.choice(titles),
            "description": random.choice(descriptions),
            "requirements": random.choice(requirements),
            "company_profile": f"{random.choice(company_prefixes)} provides {random.choice(domains)} across {random.choice(regions)}.",
            "location": random.choice(locations),
            "salary_range": random.choice(salary_ranges),
            "employment_type": random.choice(employment_types),
            "industry": random.choice(industries),
            "benefits": random.choice(benefits),
            "fraudulent": 0
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_excel(output_path, index=False)
    print(f"✅ Generated {n} real job entries to: {output_path}")

# Run the generator
generate_full_real_jobs_excel(n=10000)
