import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_github_profile_image(github_url):
    try:
        parsed_url = urlparse(github_url)
        path_parts = [p for p in parsed_url.path.split('/') if p]
        
        if len(path_parts) >= 1:
            username = path_parts[0]
            profile_url = f"https://github.com/{username}"
            
            response = requests.get(profile_url)
            response.raise_for_status()  
            
            soup = BeautifulSoup(response.text, 'html.parser')
            profile_image = soup.find('img', {'alt': 'Avatar'})
            
            if profile_image and 'src' in profile_image.attrs:
                return profile_image['src']
            else:
                return "Profile image not found"
        else:
            return "Invalid GitHub URL"
            
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    print("GitHub Profile Image Extractor")
    print("-----------------------------")
    user_input = input("Enter GitHub profile or repository URL: ").strip()
    
    if not user_input.startswith(('http://', 'https://')):
        user_input = 'https://' + user_input
    
    image_link = get_github_profile_image(user_input)
    print("\nProfile Image Link:", image_link)