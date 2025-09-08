import requests
import os
from urllib.parse import urlparse
from hashlib import md5

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    # Get multiple URLs from user (comma-separated)
    urls = input("Please enter one or more image URLs (separated by commas): ").split(",")
    urls = [u.strip() for u in urls if u.strip()]  # Clean up input
    
    if not urls:
        print("✗ No URLs provided. Exiting.")
        return

    # Create directory if it doesn't exist
    os.makedirs("Fetched_Images", exist_ok=True)

    downloaded_hashes = set()  # Track duplicates
    
    for url in urls:
        try:
            # Fetch the image with a timeout
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise exception for bad status codes
            
            # Check for important headers before saving
            content_type = response.headers.get("Content-Type", "")
            if not content_type.startswith("image/"):
                print(f"✗ Skipping {url} (Not an image: {content_type})")
                continue
            
            # Generate a hash of the content to detect duplicates
            file_hash = md5(response.content).hexdigest()
            if file_hash in downloaded_hashes:
                print(f"✗ Skipping {url} (Duplicate image detected)")
                continue
            downloaded_hashes.add(file_hash)
            
            # Extract filename from URL or generate one
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                filename = f"downloaded_image_{len(downloaded_hashes)}.jpg"
            
            # Save the image
            filepath = os.path.join("Fetched_Images", filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ Successfully fetched: {filename}")
            print(f"✓ Image saved to {filepath}\n")
        
        except requests.exceptions.Timeout:
            print(f"✗ Timeout: Could not fetch {url}")
        except requests.exceptions.HTTPError as http_err:
            print(f"✗ HTTP error for {url}: {http_err}")
        except requests.exceptions.ConnectionError:
            print(f"✗ Connection error: Could not reach {url}")
        except Exception as e:
            print(f"✗ Unexpected error for {url}: {e}")
    
    print("Connection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
