# Adjusting the script to analyze top keywords and technologies per generic job title

# Importing necessary libraries for web scraping and text analysis
import requests
from bs4 import BeautifulSoup
from collections import defaultdict, Counter
import re

# Function to classify job titles into generic categories based on common keywords
def classify_job_title(url):
    # Mapping specific job titles to generic ones
    title_mappings = {
        'machine learning': 'Machine Learning',
        'data scientist': 'Data Science',
        'engineering manager': 'Manager',
        'ai engineer': 'AI',
        'research scientist': 'Research',
        'operations engineer': 'Operations'
    }
    # Lowercase URL for comparison
    url_lower = url.lower()
    # Default classification if none of the keywords match
    generic_title = 'Other'
    for specific, generic in title_mappings.items():
        if specific in url_lower:
            return generic
    return generic_title

# Adjusted function to scrape, process job listings, and extract keywords and technologies per job title
def scrape_and_analyze_job_listings_by_title(job_urls):
    # Dictionary to hold keywords and technologies per generic job title
    title_keywords = defaultdict(list)
    title_technologies = defaultdict(list)

    # Predefined list of common technologies for filtering
    technology_terms = ['python', 'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'sql', 'hadoop', 'spark', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git', 'linux', 'java', 'c++', 'r', 'matlab']

    # Iterate through the list of URLs and scrape content
    for url in job_urls:
        response = requests.get(url)
        if response.status_code == 200:  # Check if the response is successful
            generic_title = classify_job_title(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract text content
            text_content = ' '.join([p.text for p in soup.find_all('p')]).lower()  # Convert to lower case
            # Extract words as potential keywords
            words = re.findall(r'\b[a-z]{2,}\b', text_content)  # Words with 2 or more characters
            title_keywords[generic_title].extend(words)
            # Extract technologies based on predefined technology list
            technologies_found = [tech for tech in technology_terms if tech in text_content]
            title_technologies[generic_title].extend(technologies_found)

    # Dictionary to hold the top 10 keywords and technologies per job title
    top_keywords_by_title = {}
    top_technologies_by_title = {}

    # Extract the top 10 keywords and technologies for each generic job title
    for title in title_keywords:
        keyword_counts = Counter(title_keywords[title])
        technology_counts = Counter(title_technologies[title])
        top_keywords_by_title[title] = keyword_counts.most_common(10)
        top_technologies_by_title[title] = technology_counts.most_common(10)

    # Return the results
    return top_keywords_by_title, top_technologies_by_title

top_keywords_by_title, top_technologies_by_title = scrape_and_analyze_job_listings_by_title(job_urls)
print("Top Keywords by Job Title:", top_keywords_by_title)
print("Top Technologies by Job Title:", top_technologies_by_title)
