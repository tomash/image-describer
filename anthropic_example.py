import os
import base64
import httpx
import anthropic

image1_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
image1_media_type = "image/jpeg"
image1_data = base64.standard_b64encode(httpx.get(image1_url).content).decode("utf-8")

image2_url = "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg"
image2_media_type = "image/jpeg"
image2_data = base64.standard_b64encode(httpx.get(image2_url).content).decode("utf-8")

# print("Image 1 data:")
# print(image1_data)

image_file = "images/14977/0994_dffd.jpeg"
image_type = "image/jpeg"
image_base64 = base64.standard_b64encode(open(image_file, "rb").read()).decode("utf-8")

#client = anthropic.Anthropic()
client = anthropic.Anthropic(
    api_key = os.environ['ANTHROPIC_API_KEY']
)

message = client.messages.create(
    # model="claude-3-5-sonnet-20241022",
    model="claude-3-haiku-20240307",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image_type,
                        "data": image_base64,
                    },
                },
                {
                    "type": "text",
                    "text": "Describe this image."
                }
            ],
        }
    ],
)

print(message)