import re
import spacy
import PyPDF2
import docx2txt
import json

class ResumeParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.text = self.extract_text()
        self.nlp = spacy.load("en_core_web_sm")

    def extract_text(self):
        """
        Extract text from PDF or DOCX file.
        """
        if self.filepath.endswith('.pdf'):
            return self.extract_from_pdf()
        elif self.filepath.endswith('.docx'):
            return self.extract_from_docx()
        else:
            raise ValueError("Unsupported file format. Only PDF and DOCX are supported.")
    
    def extract_from_pdf(self):
        text = ""
        with open(self.filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text

    def extract_from_docx(self):
        return docx2txt.process(self.filepath)
    
    def extract_name(self):
        """
        Extract name using spaCy's named entity recognition (NER).
        """
        doc = self.nlp(self.text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return None
    
    def extract_email(self):
        """
        Extract email addresses using regex.
        """
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, self.text)
        return emails[0] if emails else None
    
    def extract_phone(self):
        """
        Extract phone numbers using regex.
        """
        phone_pattern = r'\(?\b[0-9]{3}[-.)\s]?[0-9]{3}[-.\s]?[0-9]{4}\b'
        phones = re.findall(phone_pattern, self.text)
        return phones[0] if phones else None
    
    def extract_address(self):
        """
        Extract potential address information.
        """
        address_keywords = ["Street", "St.", "Avenue", "Ave.", "Road", "Rd.", "Boulevard", "Blvd.", "Lane", "Ln.", "Drive", "Dr."]
        lines = self.text.split("\n")
        for line in lines:
            if any(keyword in line for keyword in address_keywords):
                return line.strip()
        return None

    def extract_skills(self, skills_list):
        """
        Extract skills based on a predefined list of skills.
        """
        found_skills = []
        for skill in skills_list:
            if re.search(r'\b' + re.escape(skill) + r'\b', self.text, re.IGNORECASE):
                found_skills.append(skill)
        return found_skills
    
    def extract_education(self):
        """
        Extract education information by searching for common degree keywords.
        """
        degrees = ['Bachelor', 'Master', 'PhD', 'B.Sc', 'M.Sc', 'B.A', 'M.A', 'MBA', 'B.Tech', 'M.Tech', 'High School']
        education_info = []
        for degree in degrees:
            if degree in self.text:
                education_info.append(degree)
        return education_info

    def extract_experience(self):
        """
        Extract experience information by detecting patterns like job titles and durations.
        """
        experience_pattern = r'(?i)(\b\d{1,2}\s+years\b|\b\d{1,2}\+?\s+years\b|\b\d{4}\b[-–]\b\d{4}\b)'
        experience_matches = re.findall(experience_pattern, self.text)
        return experience_matches if experience_matches else "Not specified"
    
    def parse(self, skills_list):
        """
        Parse the resume for structured information.
        """
        return {
            "Name": self.extract_name(),
            "Email": self.extract_email(),
            "Phone": self.extract_phone(),
            "Address": self.extract_address(),
            "Skills": self.extract_skills(skills_list),
            "Education": self.extract_education(),
            "Experience": self.extract_experience(),
        }

    def save_to_json(self, data, output_path="parsed_resume.json"):
        """
        Save parsed data to a JSON file.
        """
        with open(output_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Parsed data saved to {output_path}")

if __name__ == "__main__":
    filepath = "path/to/your/resume/file"  # Replace with the path to the resume
    skills_list = ["Python", "Java", "Machine Learning", "Data Science", "SQL", "Git"]
    
    parser = ResumeParser(filepath)
    parsed_data = parser.parse(skills_list)

    # Print parsed data
    print("Parsed Resume Data:")
    for key, value in parsed_data.items():
        print(f"{key}: {value}")

    # Save parsed data to JSON
    parser.save_to_json(parsed_data, output_path="parsed_resume.json")