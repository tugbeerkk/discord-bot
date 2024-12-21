from imageai.Detection import ObjectDetection

def detect_objects(resimm):
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath("yolov3.pt")
    detector.loadModel()
    
    output_image_path = "output_image.jpg"
    detections = detector.detectObjectsFromImage(input_image=resimm,output_image_path=output_image_path,minimum_percentage_probability=50)

    filtered_detections = []
    target_classes = ["car", "cyclists", "buses", "trucks", "trains"]

    for detected_object in detections:
        if detected_object["name"] in target_classes:
            filtered_detections.append({
                "name": detected_object["name"],
                "probability": detected_object["percentage_probability"]
            })

    return filtered_detections , output_image_path
