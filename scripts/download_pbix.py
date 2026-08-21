import os
import requests

def download_pbix_template():
    url = "https://github.com/JamesDBartlett3/ps-for-pbi/raw/main/.bin/blank.pbix"
    output_dir = "powerbi"
    output_path = os.path.join(output_dir, "Sales_Performance_Dashboard.pbix")
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Downloading blank PBIX template from: {url}")
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"Blank PBIX template successfully downloaded to: {output_path}")
        else:
            print(f"Failed to download PBIX. HTTP status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while downloading the PBIX file: {e}")

if __name__ == "__main__":
    download_pbix_template()
