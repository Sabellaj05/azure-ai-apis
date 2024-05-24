"""
OCR test 
"""

import os
import cv2
import gradio as gr
from gradio import Interface, Image, Textbox # wasn't working 
from dotenv import load_dotenv
from utils import unique_name
from vision_functions import VisionFunctions


def load_envs():
    load_dotenv()
    try:
        ENDPOINT = os.getenv("VISION_ENDPOINT")
        KEY = os.getenv("VISION_KEY")
        return ENDPOINT, KEY

    except KeyError:
        raise ValueError("Missing VISION_ENDPOINT and VISION_KEY environment variables")

def init_vision_client():
    ENDPOINT, KEY = load_envs()
    vision_client = VisionFunctions(ENDPOINT, KEY)
    return vision_client

def extract_boxes(result):
    bounding_boxes = []
    blocks = result['readResult']['blocks']
    for block in blocks:
        for line in block['lines']:
            line_polygon = [(p['x'], p['y']) for p in line['boundingPolygon']]
            bounding_boxes.append((line_polygon, (0, 0, 255)))  # lines: orange
            for word in line['words']:
                word_polygon = [(p['x'], p['y']) for p in word['boundingPolygon']]
                bounding_boxes.append((word_polygon, (255, 0, 0)))  # words: blue 
    return bounding_boxes   

def draw_boxes(image, bounding_boxes, line_width=2):
    image = cv2.imread(image)
    for polygon, color in bounding_boxes: 
        points = [(int(x), int(y)) for x, y in polygon] 
        for i in range(len(points)):
            start_point = points[i]
            end_point = points[(i + 1) % len(points)]
            cv2.line(image, start_point, end_point, color, line_width)
    return image

def process_image(image):
    # init
    vision_client = init_vision_client()

    _path = os.path.join(os.getcwd(), "temp_images")
    if not os.path.exists(_path):
        os.makedirs(_path)
    # Save the uploaded image to a temporary file
    u_name = unique_name("temp_image.jpg")
    temp_image_path = os.path.join(_path, u_name)
    cv2.imwrite(temp_image_path, image)

    result_from_path = vision_client.ocr_path(temp_image_path)

    if result_from_path:
        bounding_boxes = extract_boxes(result_from_path)
        final_image = draw_boxes(temp_image_path, bounding_boxes)
        
        # Convert final_image to RGB for displaying with Gradio
        final_image_rgb = cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB)

        return final_image_rgb, result_from_path

    return None, None

def display_results(image):
    processed_image, result = process_image(image)
    
    if result:
        text_output = "Image analysis results:\n\nRead:\n"
        for line in result['readResult']['blocks'][0]['lines']:
            text_output += f"Line: '{line['text']}'\n"
            ## to cluttered
            #for word in line['words']:
            #    text_output += f"\tWord: '{word['text']}', Confidence {word['confidence']:.4f}\n"
        text_output += f"\nImage height: {result['metadata']['height']}\n"
        text_output += f"Image width: {result['metadata']['width']}\n"
        text_output += f"Model version: {result['modelVersion']}\n"
        return processed_image, text_output

    return None, "Error processing the image"

def llm_format():
    """
    Estaria bueno combinar con algo de NLP con el texto extraido
    """
    pass

gredio = Interface(
    fn=display_results,
    inputs=Image(label="Upload an Image"),
    outputs=[Image(label="Processed Image"), Textbox(label="OCR Results")],
    title="Azure Vision OCR",
    description="Upload an image to perform OCR and display the bounding boxes around the text."
)

if __name__ == "__main__":
    #gredio.launch(share=True) # for sharing the link
    gredio.launch()
