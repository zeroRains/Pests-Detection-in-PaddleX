import cv2

def draw_anchor(img_path,anchors,thread=0.3):
    img = cv2.imread(img_path,-1)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    for data in anchors:
        if data["score"]>=thread:
            box = data["bbox"]
            text = f"{data['category']}_%.2f"%(data["score"])
            img = cv2.rectangle(img,(int(box[0]),int(box[1])),(int(box[0]+box[2]),int(box[1]+box[3])),(0,255,0), 2)
            img = cv2.putText(img, text, (int(box[0]),int(box[1])), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 2)
    return img


