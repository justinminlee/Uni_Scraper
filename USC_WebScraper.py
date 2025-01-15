from bs4 import BeautifulSoup
import os
import pandas as pd

# Directory containing the saved degree pages
input_dir = "usc_degree_pages"
output_file = "usc_all_degree_details.csv"

# Extract details from each degree page
def extract_degree_details(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        
        # Extract main program details
        program_name = soup.find("h1", class_="program-header--title")
        entry_threshold = soup.find("h3", text="Entry threshold")
        duration_domestic = soup.find("strong", audience="domestic")
        duration_international = soup.find("strong", audience="international")
        indicative_fees = soup.find("h3", text="Indicative fees")
        qtac_code = soup.find("h3", text="QTAC code")
        start_semester = soup.find("h3", text="Start")

        # Extract career outcomes and additional information
        career_outcomes_section = soup.find("h3", text="Career outcomes")
        career_outcomes = career_outcomes_section.find_next("ul").get_text(strip=True, separator=" | ") if career_outcomes_section else "N/A"

        # Safely extract and handle missing data
        details = {
            "Program Name": program_name.get_text(strip=True) if program_name else "N/A",
            "Entry Threshold": entry_threshold.find_next("strong", class_="key-figure").get_text(strip=True) if entry_threshold else "N/A",
            "Duration (Domestic)": duration_domestic.get_text(strip=True) if duration_domestic else "N/A",
            "Duration (International)": duration_international.get_text(strip=True) if duration_international else "N/A",
            "Indicative Fees": indicative_fees.find_next("strong", class_="key-figure").get_text(strip=True) if indicative_fees else "N/A",
            "QTAC Code": qtac_code.find_next("strong", class_="key-figure").get_text(strip=True) if qtac_code else "N/A",
            "Start Semester": start_semester.find_next("li").get_text(strip=True) if start_semester else "N/A",
            "Career Outcomes": career_outcomes,
        }
        
        # Add all additional sections dynamically
        additional_sections = soup.find_all("h3")
        for section in additional_sections:
            section_title = section.get_text(strip=True)
            section_value = section.find_next("div").get_text(strip=True) if section.find_next("div") else "N/A"
            if section_title not in details:  # Avoid overwriting existing fields
                details[section_title] = section_value

        return details

# Parse all saved degree pages
def parse_all_saved_pages():
    degree_details = []
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        if filename.endswith(".html"):
            print(f"Parsing: {file_path}")
            details = extract_degree_details(file_path)
            degree_details.append(details)
    return degree_details

# Save to CSV
degree_data = parse_all_saved_pages()
df = pd.DataFrame(degree_data)
df.to_csv(output_file, index=False)
print(f"Saved all degree details to '{output_file}'.")


# 오래 걸리는 작업이므로 시간이 오래걸림
# International vs Domestic
# Accuracy of data