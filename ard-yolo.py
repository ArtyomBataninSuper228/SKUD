# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import argparse
from threading import Thread
from types import NoneType
from PTZ import *
import cv2.dnn
import numpy as np

from ultralytics.utils import ASSETS, yaml_load
from ultralytics.utils.checks import check_yaml

CLASSES = yaml_load(check_yaml("coco8.yaml"))["names"]
colors = np.random.uniform(0, 255, size=(len(CLASSES), 3))
ax = 0
ay = 0
original_image = None
ptz = PTZ(port = "/dev/cu.usbserial-110")

def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    """
    Draw bounding boxes on the input image based on the provided arguments.

    Args:
        img (np.ndarray): The input image to draw the bounding box on.
        class_id (int): Class ID of the detected object.
        confidence (float): Confidence score of the detected object.
        x (int): X-coordinate of the top-left corner of the bounding box.
        y (int): Y-coordinate of the top-left corner of the bounding box.
        x_plus_w (int): X-coordinate of the bottom-right corner of the bounding box.
        y_plus_h (int): Y-coordinate of the bottom-right corner of the bounding box.
    """
    label = f"{CLASSES[class_id]} ({confidence:.2f})"
    color = colors[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def main(onnx_model,):
    global ax, ay, videcamera_capture
    """
    Load ONNX model, perform inference, draw bounding boxes, and display the output image.

    Args:
        onnx_model (str): Path to the ONNX model.
        input_image (str): Path to the input image.

    Returns:
        (List[Dict]): List of dictionaries containing detection information such as class_id, class_name, confidence,
        box coordinates, and scale factor.
    """
    # Load the ONNX model
    #cv2.dnn.readNetFromDarknet('C:\\Users\ArtyMax\PycharmProjects\Yolo\runs\detect\train2\weights\best.pt')
    #model: cv2.dnn.Net=cv2.dnn.readNet('C:\\Users\\ArtyMax\\PycharmProjects\\Yolo\\runs\detect\\train2\weights\\best.pt')
    model: cv2.dnn.Net = cv2.dnn.readNetFromONNX(onnx_model)


    while 1:
        #original_image: np.ndarray = cv2.imread(input_image)
        [height, width, _] = original_image.shape

        # Prepare a square image for inference
        length = max((height, width))
        image = np.zeros((length, length, 3), np.uint8)
        image[0:height, 0:width] = original_image

        # Calculate scale factor
        scale = length / 640

        # Preprocess the image and prepare blob for model
        blob = cv2.dnn.blobFromImage(image, scalefactor=1 / 255, size=(640, 640), swapRB=True)
        model.setInput(blob)

        # Perform inference
        outputs = model.forward()

        # Prepare output array
        outputs = np.array([cv2.transpose(outputs[0])])
        rows = outputs.shape[1]

        boxes = []
        scores = []
        class_ids = []
        max_s = 0
        # Iterate through output to collect bounding boxes, confidence scores, and class IDs
        for i in range(rows):
            classes_scores = outputs[0][i][4:]
            (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(classes_scores)
            if maxScore >= 0.4:
                if outputs[0][i][2]*outputs[0][i][3] > max_s:
                    max_s = outputs[0][i][2]*outputs[0][i][3]
                    ax = (outputs[0][i][0] - 320)*scale*0.0386
                    ay = (outputs[0][i][1] - 320*9/16)*scale*0.0386
                box = [
                    outputs[0][i][0] - (0.5 * outputs[0][i][2]),  # x center - width/2 = left x
                    outputs[0][i][1] - (0.5 * outputs[0][i][3]),  # y center - height/2 = top y
                    outputs[0][i][2],  # width
                    outputs[0][i][3],  # height
                ]
                boxes.append(box)
                scores.append(maxScore)
                class_ids.append(maxClassIndex)

        # Apply NMS (Non-maximum suppression)
        result_boxes = cv2.dnn.NMSBoxes(boxes, scores, 0.25, 0.45, 0.5)

        detections = []

        # Iterate through NMS results to draw bounding boxes and labels
        for i in range(len(result_boxes)):
            index = result_boxes[i]
            box = boxes[index]
            detection = {
                "class_id": class_ids[index],
                "class_name": CLASSES[class_ids[index]],
                "confidence": scores[index],
                "box": box,
                "scale": scale,
            }
            detections.append(detection)
            draw_bounding_box(
                original_image,
                class_ids[index],
                scores[index],
                round(box[0] * scale),
                round(box[1] * scale),
                round((box[0] + box[2]) * scale),
                round((box[1] + box[3]) * scale),
            )

        # Display the image with bounding boxes\
        #original_image=cv2.resize(original_image, (1920, 1080))
        #print(type(original_image))
        cv2.imshow("image", original_image)
        cv2.waitKey(1)
        #print(ax, ay)
        ptz.ax = ax
        ptz.ay = ay
        ptz.update()
        ax = 0
        ay = 0
    # Read the input image
    cv2.destroyAllWindows()




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="/Users/artembatanin/PycharmProjects/messenger/yolo11n.onnx", help="Input your ONNX model.")
    parser.add_argument("--img", default="rtsp://admin:Test_Test@192.168.1.63/:8080/stream1", help="Path to input image.")
    args = parser.parse_args()
    videcamera_capture = cv2.VideoCapture(args.img)

    def func():
        global original_image
        while videcamera_capture.isOpened():
            ret, image = videcamera_capture.read()
            if not ret:
                print("not ret")
                continue
            original_image = cv2.resize(image, (1920, 1080))


    th = Thread(target=func)
    th.start()
    while type(original_image) == NoneType:
        pass
    main(args.model)