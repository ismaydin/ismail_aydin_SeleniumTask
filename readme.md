Insider Careers Page Automation

This is a Selenium-based test automation project built to verify the functionality and elements on the Insider Careers page.

####Features####

- Opens the Insider homepage and navigates to the Careers page

- Verifies key sections: Locations, Teams, and Life at Insider

- Filters available jobs by:

- Location: Istanbul, Turkiye

- Department: Quality Assurance

- Counts the number of filtered jobs

- Finds and clicks on a specific job titled:

- Software QA Tester / Intercontinental Support - Insider Testinium Tech Hub (Fresh Graduate - Remote)

####Technologies Used####

- Python 3

- Selenium WebDriver

- PyTest

- WebDriver Manager (optional, see below)

####Project Structure

insider_assessment/
│
├── src/
│   ├── pages/
│   │   ├── base_page.py
│   │   └── careers_page.py
│   └── tests/
│       └── test_careers_page.py
│
├── .gitignore
├── requirements.txt
└── README.md


####Install dependencies####

pip install -r requirements.txt


####Run the Tests####

C:\the_folder_where_placed\src> pytest -s tests/test_careers_page.py

Ensure Chrome is installed. The script uses chromedriver implicitly.

####Notes####

Page interactions include waits to ensure stability during animations/load.

####Author####

İsmail Aydın

