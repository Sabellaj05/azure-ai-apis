"""
Lo ideal seria usar cli arguments para elegir que funcion usar, *Pendiente*
"""

import os
import time
import uuid
import cv2
from utils import show_image, unique_name
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from vision_functions import VisionFunctions

# para que no se quejen los ifs
global result_from_path
global result_from_url

result_from_path = None
result_from_url = None

def main() -> None:
    load_dotenv()
    try:
        ENDPOINT = os.getenv("VISION_ENDPOINT")
        KEY = os.getenv("VISION_KEY")
    except KeyError:
        print("Missing VISION_ENDPOINT and VISION_KEY environment variables")

    vision_client = VisionFunctions(ENDPOINT, KEY)
    image_path = "sample.jpg"
    url_path = None

    # Change functions accordingly 
    result_from_path = vision_client.ocr_path(image_path)
    #result_from_url = vision_client.ocr_url()

    # create "data" directory if not present
    current = os.getcwd()
    data_dir = os.path.join(current, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    def extract_boxes(result):
        bounding_boxes = []
        blocks = result['readResult']['blocks']
        for block in blocks:
            for line in block['lines']:
                # line bounding polygon
                line_polygon = [(p['x'], p['y']) for p in line['boundingPolygon']]
                bounding_boxes.append((line_polygon, (0, 255, 0)))  # lines: green 
                for word in line['words']:
                    # word bounding polygon
                    word_polygon = [(p['x'], p['y']) for p in word['boundingPolygon']]
                    bounding_boxes.append((word_polygon, (255, 0, 0)))  # words: blue 
        return bounding_boxes   
    
    def draw_boxes(image, bounding_boxes, line_width=2):
        # load image
        image = cv2.imread(image)
        # apply boxes
        for polygon, color in bounding_boxes: 
            points = [(int(x), int(y)) for x, y in polygon] 
            for i in range(len(points)):
                start_point = points[i]
                end_point = points[(i + 1) % len(points)]
                cv2.line(image, start_point, end_point, color, line_width)
        return image
    

    if result_from_path:
        print("Image analysis results :")
        print(" Read:")

        if result_from_path.read is not None:
            for line in result_from_path.read.blocks[0].lines:
                print(f"\tLine: '{line.text}")
                for word in line.words:
                    print(f"\t\tWord: '{word.text}', Confidence {word.confidence:.4f}")
        print()

        print(f" Image height: {result_from_path.metadata.height}")
        print(f" Image width: {result_from_path.metadata.width}\n")
        print(f" Model version: {result_from_path.model_version}")

        bounding_boxes = extract_boxes(result_from_path)
        final_image = draw_boxes(image_path, bounding_boxes)
        # cv2.imshow("Final image", final_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        show_image(final_image)



    if result_from_url:
        print("Image analysis results:")
        print(" Read:")

        if result_from_url.read is not None:
            for line in result_from_url.read.blocks[0].lines:
                print(f"\tLine: '{line.text}'")
                for word in line.words:
                    print(f"\t\tWord: '{word.text}', Confidence {word.confidence:.4f}")

        print(f" Image height: {result_from_url.metadata.height}")
        print(f" Image width: {result_from_url.metadata.width}")
        print(f" Model version: {result_from_url.model_version}")

        bounding_boxes = extract_boxes(result_from_url)
        final_image = draw_boxes(image_path, bounding_boxes)
        # bruh
        # cv2.imshow("Final image", final_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        
        show_image(final_image)

    # save image
    output_path = os.path.join(data_dir, unique_name())
    cv2.imwrite(output_path, final_image)



if __name__ == "__main__":
    main()




