import time
import requests
import json
import random

# In a real environment, you would use OpenCV and a TFLite model:
# import cv2
# from tflite_runtime.interpreter import Interpreter

class RaspberryPiCameraClient:
    def __init__(self, aws_endpoint):
        self.aws_endpoint = aws_endpoint
        self.camera_active = True
        
        # Mocking the object detection model labels
        self.detectable_objects = ['Laptop', 'Wireless Mouse', 'Pasta', 'Garlic Bread', 'Diapers']
        
        print("Initializing Raspberry Pi Camera Module...")
        # self.camera = cv2.VideoCapture(0) # Standard Pi Camera initialization

    def run_object_detection(self):
        """
        Simulates the Pi capturing a frame and running a lightweight local AI 
        (like YOLOv8-Nano) to recognize objects the customer placed on the counter.
        """
        print("\n[CAMERA] Capturing frame...")
        # ret, frame = self.camera.read()
        # items = self.model.predict(frame)
        
        # Simulating random items being placed on the checkout counter
        num_items = random.randint(1, 3)
        detected_items = random.sample(self.detectable_objects, num_items)
        
        print(f"[AI VISION] Detected items on counter: {detected_items}")
        return detected_items

    def send_to_aws_cloud(self, items):
        """
        Sends the detected items to the AWS Cloud for heavy processing 
        (Market Basket Analysis, Dynamic Pricing, User Dashboard Sync).
        """
        payload = {
            "device_id": "rpi-kiosk-01",
            "timestamp": time.time(),
            "cart": items
        }
        
        try:
            print(f"[NETWORK] Transmitting data to AWS Cloud: {self.aws_endpoint}")
            # In production, use HTTPS and secure AWS API Gateway endpoints
            response = requests.post(
                f"{self.aws_endpoint}/api/cart/sync", 
                json=payload,
                timeout=5
            )
            
            if response.status_code == 200:
                cloud_data = response.json()
                if cloud_data.get('offer'):
                    print(f"\n⚡ [AWS CLOUD RESPONSE] Smart Coupon Received!")
                    print(f"👉 Push to UI: {cloud_data['offer']['message']}")
                else:
                    print("[AWS CLOUD RESPONSE] Cart Synced. No bundle available.")
            else:
                print(f"[ERROR] AWS Cloud returned status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"[NETWORK ERROR] Failed to connect to AWS: {e}")

    def start_loop(self):
        print("--- RASPBERRY PI SMART CHECKOUT ACTIVE ---")
        try:
            while self.camera_active:
                # 1. Detect objects via Camera
                items = self.run_object_detection()
                
                # 2. Send to Cloud for processing
                self.send_to_aws_cloud(items)
                
                # Wait 10 seconds before next "customer"
                time.sleep(10)
                
        except KeyboardInterrupt:
            print("\nShutting down camera...")
            # self.camera.release()

if __name__ == "__main__":
    # Point this to your EC2 Public IP
    AWS_CLOUD_URL = "http://34.230.28.56:5000" 
    
    pi_client = RaspberryPiCameraClient(aws_endpoint=AWS_CLOUD_URL)
    pi_client.start_loop()
