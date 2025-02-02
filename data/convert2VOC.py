import os
import json
import tqdm
from os import listdir, getcwd
from os.path import join

classes = ["person","bicycle","car","motorcycle","airplane","bus","train",
        "truck","boat","traffic light","fire hydrant","stop sign","parking meter",
        "bench","bird","cat","dog","horse","sheep","cow","elephant","bear","zebra",
        "giraffe","backpack","umbrella","handbag","tie","suitcase","frisbee","skis",
        "snowboard","sports ball","kite","baseball bat","baseball glove","skateboard",
        "surfboard","tennis racket","bottle","wine glass","cup","fork","knife","spoon",
        "bowl","banana","apple","sandwich","orange","broccoli","carrot","hot dog","pizza",
        "donut","cake","chair","couch","potted plant","bed","dining table","toilet","tv",
        "laptop","mouse","remote","keyboard","cell phone","microwave","oven","toaster","sink",
        "refrigerator","book","clock","vase","scissors","teddy bear","hair drier","toothbrush"]

#box form[x,y,w,h]
def convert(size,box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = box[0]*dw
    y = box[1]*dh

    xn = (box[0] + box[2]/2)*dw
    yn = (box[1] + box[3]/2)*dh

    w = box[2]*dw
    h = box[3]*dh
    return (xn,yn,w,h)

def convert_annotation():
    with open('instances_val2017.json','r') as f:
        data = json.load(f)

    open('coco/5k.txt', 'w').close() 

    for item in tqdm.tqdm(data['images']):
        image_id = item['id']
        file_name = item['file_name']
        width = item['width']
        height = item['height']
        value = filter(lambda item1: item1['image_id'] == image_id,data['annotations'])
        outfile = open('labels/val2017/%s.txt' % (file_name[:-4]), 'a+')
        write = False
        for item2 in value:
            category_id = item2['category_id']
            value1 = next(filter(lambda item3: item3['id'] == category_id,data['categories']))
            name = value1['name']
            class_id = classes.index(name)
            box = item2['bbox']
            bb = convert((width,height),box)
            outfile.write(str(class_id)+" "+" ".join([str(a) for a in bb]) + '\n')
            write = True
        outfile.close()

        if write:
            with open('coco/5k.txt', 'a') as f:
                print('data/images/val2017/%s.jpg'%(file_name[:-4]), file=f)

if __name__ == '__main__':
    convert_annotation()
