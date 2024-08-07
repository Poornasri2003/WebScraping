import streamlit as st
from streamlit_option_menu import option_menu
import requests
from bs4 import BeautifulSoup

# Function to retrieve option value based on constituency name
def state_result_name(url, constituencyname):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        select_element = soup.find('select')
        if select_element:
            options = select_element.find_all('option')
            for option in options:
                value = option.get('value')
                text = option.text.strip()
                if text == constituencyname:
                    return value  # Return the value if constituency name matches
            st.error("Constituency name not found in options.")
            return None
        else:
            st.error("No <select> element found in the HTML.")
            return None
    else:
        st.error(f"Failed to fetch URL: {url}")
        return None

def scrape_options(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        select_element = soup.find('select', class_='custom-select')
        if select_element:
            options = select_element.find_all('option')
            option_values = []
            
            for option in options:
                value = option.get('value')
                text = option.text.strip()
                option_values.append((value, text))
            
            return option_values
        else:
            st.error("No <select class='custom-select'> found in the HTML.")
            return []
    else:
        st.error(f"Failed to fetch URL: {url}")
        return []

def construct_urls(base_url, options):
    urls = []
    for value, text in options:
        url = f"{base_url}{value}.htm"
        urls.append((value, text, url))
    
    return urls

def fetch_data(urls):
    results = {'people_won': [], 'people_not_won': []}
    
    for value, text, url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all candidates' info
            candidates = soup.find_all('div', class_='cand-info')
            for candidate in candidates:
                status_div = candidate.find('div', class_='status')
                if status_div:
                    status = status_div.find('div').text.strip().lower()  # 'won' or 'lost'
                    votes = status_div.find_all('div')[1].text.strip().split()[0]  # extract votes number
                    
                    name = candidate.find('h5').text.strip()
                    party = candidate.find('h6').text.strip()
                    
                    # Store data in the format needed
                    candidate_info = {
                        'name': name,
                        'party': party,
                        'votes': votes,
                        'ward': text  # Using the 'ward' as the constituency name
                    }
                    
                    if status == 'won':
                        results['people_won'].append(candidate_info)
                    elif status == 'lost':
                        results['people_not_won'].append(candidate_info)
        else:
            print("ERrpor")
      
    return results

# Streamlit app
def main():
    st.title("Web Scraping with Streamlit")
    st.sidebar.title("Constituency Search")
    
    base_url = st.sidebar.text_input("Enter the base URL of the website:")
    constituency_name = st.sidebar.text_input("Enter the constituency name:")

    if 'data' not in st.session_state:
        st.session_state['data'] = {'people_won': [], 'people_not_won': []}

    if st.sidebar.button("Search"):
        if base_url and constituency_name:
            result = state_result_name(base_url, constituency_name)
            if result:
                state_url = f"https://results.eci.gov.in/PcResultGenJune2024/partywiseresult-{result}.htm"
                st.sidebar.write(state_url)
                candidate_url = "https://results.eci.gov.in/PcResultGenJune2024/candidateswise-"
                options = scrape_options(state_url)
                urls = construct_urls(candidate_url, options)
                st.session_state['data'] = fetch_data(urls)
            else:
                st.session_state['data'] = {'people_won': [], 'people_not_won': []}
        else:
            st.session_state['data'] = {'people_won': [], 'people_not_won': []}

    selected_tab = option_menu(
        menu_title=None,
        options=["People Won", "People Lost"],
        icons=['trophy', 'thumbs-down'],
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {"font-size": "18px", "text-align": "center", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
    )

    data = st.session_state['data']

    if selected_tab == "People Won":
        st.subheader("People who won:")
        if data['people_won']:
            for person in data['people_won']:
                st.write(f"- Name: {person['name']}, Party: {person['party']}, Votes: {person['votes']}, Ward: {person['ward']}")
        else:
            st.write("No winners found.")
    elif selected_tab == "People Lost":
        st.subheader("People who did not win:")
        if data['people_not_won']:
            for person in data['people_not_won']:
                st.write(f"- Name: {person['name']}, Party: {person['party']}, Votes: {person['votes']}, Ward: {person['ward']}")
        else:
            st.write("No losers found.")

if __name__ == '__main__':
    main()
