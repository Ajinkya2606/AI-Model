import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os

# Function to open and display images based on a given prompt
def open_images(prompt):
    folder_path = r"D:\Python Projects\AI Model\Data"
    prompt = prompt.replace(" ", "_")

    # Generate the file name for the images
    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)

        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1) # Pause for 1 sec before showing the next image

        except IOError:
            print(f"Unable to open {image_path}")

# API details for the Hugging Face Stable Diffusion model
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
env_path = r'D:\Python Projects\AI Model\.env'
headers = {"Authorization": f"Bearer {get_key(env_path, 'HuggingFaceAPIKey')}"}


# Async function to send a query to the hugging face API
async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

# Async function to generate image based on the given prompt
async def generate_images(prompt: str):
    tasks = []

    # Create 4 image generation task
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4k, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    # Save image
    for i, image_bytes in enumerate(image_bytes_list):
        with open(fr"D:\Python Projects\AI Model\Data\{prompt.replace(' ', '_')}{i+1}.jpg", "wb")as f:
            f.write(image_bytes)

def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

# Main loop to monitor for image generation requests
while True:

    try:
        with open(r"D:\Python Projects\AI Model\Frontend\Files\ImageGeneration.data", "r") as f:
            Data: str = f.read()

        Prompt, Status = Data.split(",")

        if Status == "True":
            print("Generating Images ... ")
            ImaageStatus = GenerateImages(prompt=Prompt)

            # Reset 
            with open(r"D:\Python Projects\AI Model\Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")
                break
        else:
            sleep(1)
    
    except:
        pass