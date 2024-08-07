# Web Scraping with Streamlit

 This project demonstrates a Streamlit application that scrapes election results from a website and displays them in an interactive user interface.

 Users can search for specific constituencies and view the names, parties, vote counts, and wards (constituencies) of winners and losers.

### Requirements

 - Python 3.x
 - streamlit (install with: pip install streamlit)
 - requests (install with: pip install requests)
 - beautifulsoup4 (install with: pip install beautifulsoup4)
 - streamlit_option_menu (install with: pip install streamlit-option-menu)

### Instructions

##### 1. Clone or download this repository:

>    git clone https://github.com/yourusername/web-scraping-streamlit.git



##### 2. Install the required libraries:
>  pip install -r requirements.txt

##### 3. Run the application:
>    streamlit run app.py

## Code Breakdown

 ### app.py

 The core Python script (app.py) utilizes the following libraries:
 - streamlit: Creates the user interface.
 - streamlit_option_menu: Enables the tabbed interface for "People Won" and "People Lost" results.
 - requests: Fetches data from the website.
 - beautifulsoup4: Parses the HTML content.

 ### Key Functions

 - state_result_name(url, constituencyname): Retrieves the option value (constituency code) based on the constituency name.
 - scrape_options(url): Scrapes the available constituency options from the provided URL.
 - construct_urls(base_url, options): Builds the individual URLs for each constituency based on the base URL and options.
 - fetch_data(urls): Fetches candidate information from each constituency URL, extracts relevant data (name, party, votes, ward), and stores it in a dictionary.
 - main(): The main function that drives the Streamlit app.

### Streamlit App Structure

 - Title: "Web Scraping with Streamlit"
 - Sidebar:
   - Input fields for base URL and constituency name.
   - "Search" button to initiate scraping.
   - Displays the constructed state URL (for reference).
 - Tabs:
   - "People Won": Displays data for winning candidates.
   - "People Lost": Displays data for losing candidates.

### Error Handling

 The code incorporates error handling to gracefully handle potential issues like:
 - Failed URL fetching.
 - Missing HTML elements during parsing.
 - Non-matching constituency names.


### Disclaimer

 This code is provided for educational purposes only. Remember to respect website terms of service and avoid scraping excessive data.

