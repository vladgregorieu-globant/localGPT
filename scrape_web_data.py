import requests
from bs4 import BeautifulSoup
import os

def download_pdf(url, output_folder):
    try:
        # Fetch the webpage content
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the webpage content with BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Find all links to PDF files
            pdf_links = [a["href"] for a in soup.find_all("a", href=True) if a["href"].endswith(".pdf")]

            # Create the output folder if it doesn't exist
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Download and save each PDF file
            for pdf_link in pdf_links:
                pdf_url = pdf_link if pdf_link.startswith("http") else url + pdf_link
                pdf_filename = os.path.join(output_folder, pdf_url.split("/")[-1])

                with open(pdf_filename, "wb") as pdf_file:
                    pdf_response = requests.get(pdf_url)
                    pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_filename}")

        else:
            print(f"Failed to retrieve {url}: Status code {response.status_code}")

    except Exception as e:
        print(f"Error downloading from {url}: {str(e)}")

if __name__ == "__main__":
    # Set the URL of the webpage containing PDF links
    start_url = "https://www.irs.gov/irb"
    
    # Set the output folder where PDF files will be saved
    output_folder = "SOURCE_DOCUMENTS"

    # Start downloading PDF files
    download_pdf(start_url, output_folder)
