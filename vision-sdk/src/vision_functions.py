from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from validate import is_endpoint_valid, is_key_valid

class VisionFunctions:
    """
    init params:
        vision resource key
        vision endpoint
    func params:
        ocr_path: path to image
        ocr_url: url to image
    """
    def __init__(self, endpoint, key) -> None:
        if is_endpoint_valid(endpoint) and is_key_valid(key):
            self.client = ImageAnalysisClient(
                endpoint=endpoint, credential=AzureKeyCredential(key)
            )
        else:
            raise ValueError("Invalid endpoint or key")

    def ocr_path(self, img_path):
        client = self.client

        with open(img_path, "rb") as file:
            image = file.read()
        
        result = client.analyze(
            image,
            visual_features=[VisualFeatures.READ]
        )

        return result
    
    def ocr_url(self, img_url):
        client = self.client
        
        result = client.analyze_from_url(
            image_url=img_url,
            visual_features=[VisualFeatures.READ]
        )

        return result
    


    











