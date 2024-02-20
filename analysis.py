# Adjusting the script to analyze top keywords and technologies per generic job title
# Importing necessary libraries for web scraping and text analysis
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

# TODO: update to add NLP to detect tech words and generic job title

# List of job URLs to scrape
job_urls = [
    "https://ai-jobs.net/job/110166-machine-learning-engineer-ai-pipeline-latm-emea-remote/",
    "https://ai-jobs.net/job/125851-data-scientist-machine-learning/",
    "https://ai-jobs.net/job/120148-machine-learning-engineer/",
    "https://ai-jobs.net/job/119603-machine-learning-engineer-ii/",
    "https://ai-jobs.net/job/119362-machine-learning-engineer-mid-level/",
    "https://ai-jobs.net/job/115583-machine-learning-engineer/",
    "https://ai-jobs.net/job/111946-machine-learning-systems-engineer-ads-ml-platform/",
    "https://ai-jobs.net/job/110166-machine-learning-engineer-ai-pipeline-latm-emea-remote/",
    "https://ai-jobs.net/job/135287-machine-learning-engineer-europe-and-uk/",
    "https://ai-jobs.net/job/131808-machine-learning-operations-engineer/",
    "https://ai-jobs.net/job/131181-machine-learning-platform-operations-engineer/",
    "https://ai-jobs.net/job/137475-ai-engineer/",
    "https://ai-jobs.net/job/136746-ai-research-scientist-generative-ai-and-multi-party-computation-mpc/",
    "https://ai-jobs.net/job/135287-machine-learning-engineer-europe-and-uk/",
    "https://ai-jobs.net/job/134255-data-scientist/",
    "https://ai-jobs.net/job/133715-ai-research-engineer/",
    "https://ai-jobs.net/job/128374-data-scientist-privacy-hub-uk/",
    "https://ai-jobs.net/job/125851-data-scientist-machine-learning/",
    "https://ai-jobs.net/job/126048-data-scientist-optimization/",
    "https://ai-jobs.net/job/126268-machine-learning-engineer-ops/",
    "https://ai-jobs.net/job/124279-data-scientist-aws-generative-ai-innovation-center-proserve-genai-open-reqs/",
    "https://ai-jobs.net/job/123566-middle-machine-learning-engineer-neurolinguistic-research/",
    "https://ai-jobs.net/job/121586-data-scientist-payment-success/",
    "https://ai-jobs.net/job/121678-engineering-manager-aiml/",
    "https://ai-jobs.net/job/118706-data-scientist-juniormid-level/",
    "https://ai-jobs.net/job/117046-data-scientist/",
    "https://ai-jobs.net/job/111183-data-scientist/",
    "https://ai-jobs.net/job/128715-machine-learning-scientist-ii/"
]

# Function to scrape and process job listings to extract keywords and technologies
def scrape_and_analyze_job_listings(job_urls):
    # Lists to hold all the keywords and technologies from all job listings
    all_keywords = []
    all_technologies = []

    # Predefined list of common technologies for filtering
    technology_terms = ['Python', 'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn', 'Pandas', 'Numpy', 'SQL', 'Hadoop', 'Spark', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Git', 'Linux', 'Java', 'C++', 'R', 'Matlab']

    # Iterate through the list of URLs and scrape content
    for url in job_urls:
        response = requests.get(url)
        if response.status_code == 200:  # Check if the response is successful
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract text content; here assuming main job description is within 'p' tags
            text_content = ' '.join([p.text for p in soup.find_all('p')])
            # Normalize the text to lower case for uniformity
            text_content = text_content.lower()
            # Extract words as potential keywords (excluding too common words and single characters)
            words = re.findall(r'\b[a-z]{2,}\b', text_content)  # Extract words with 2 or more characters
            all_keywords.extend(words)
            # Extract technologies based on predefined technology list (case insensitive)
            technologies_found = [tech for tech in technology_terms if tech.lower() in text_content]
            all_technologies.extend(technologies_found)

    # Count the occurrences of each keyword and technology
    keyword_counts = Counter(all_keywords)
    technology_counts = Counter(all_technologies)

    # Extract the top 10 keywords and technologies
    top_keywords = keyword_counts.most_common(10)
    top_technologies = technology_counts.most_common(10)

    # Return the results
    return top_keywords, top_technologies

# Note: Actual function call will be uncommented after review
# top_keywords, top_technologies = scrape_and_analyze_job_listings(job_urls)
# print("Top 10 Keywords:", top_keywords)
# print("Top 10 Technologies:", top_technologies)

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
