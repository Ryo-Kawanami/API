import os
import numpy as np
import xml.etree.ElementTree as ET
from PIL import Image
from xml.etree.ElementTree import *

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


class API_auto_annotation_xml():

    # １．このコンストラクタを画像パスのループの先頭に挿入してください。
    # 1. Insert this constructor at the beginning of the image path loop.
    def __init__(self, in_img_path, out_xml_dir):
        # 予備情報の作成
        # Create preliminary information
        self.in_img_path = in_img_path
        self.out_xml_dir = out_xml_dir
        self.folder_text = in_img_path.split("/")[-2]
        self.filename_text = in_img_path.split("/")[-1]
        image = Image.open(in_img_path)
        image_np = load_image_into_numpy_array(image)
        self.img_width = image_np.shape[1]
        self.img_height = image_np.shape[0]
        self.img_depth = image_np.shape[2]

        if os.path.exists(self.out_xml_dir)==False:
            os.makedirs(self.out_xml_dir)
            
        self.obj_dict_list = []


    # ２．このメソッドをオブジェクトごとのバウンディングボックスの情報が得られる場所に挿入してください。
    # 2. Insert this method where you can get per-object bounding box information.
    def iter(self, class_name, confidence, xmin, ymin, xmax, ymax):
        obj_dict = {"class_name":class_name, "confidence":confidence, \
                    "xmin":xmin, "ymin":ymin, "xmax":xmax, "ymax":ymax}
        self.obj_dict_list.append(obj_dict)


    # ３．XMLファイルとして出力するために、このメソッドを画像パスのループの一番最後に挿入してください。
    # 3. Insert this method at the very end of the image path loop to output as a XML file.
    def make_xml(self, confidence_score_thresh):
        # xml elementの作成
        # create xml element
        annotation = Element ("annotation", {"verified":"no"})
        folder = SubElement(annotation, "folder")
        folder.text = self.folder_text
        filename = SubElement(annotation, "filename")
        filename.text = self.filename_text
        path = SubElement(annotation, "path")
        path.text = os.path.abspath(self.in_img_path)
        source = SubElement(annotation, "source")
        database = SubElement(source, "database")
        database.text = "Unknown"
        size = SubElement(annotation, "size")
        width = SubElement(size, "width")
        width.text = str(self.img_width)
        height = SubElement(size, "height")
        height.text = str(self.img_height)
        depth = SubElement(size, "depth")
        depth.text = str(self.img_depth)
        segmented = SubElement(annotation, "segmented")
        segmented.text = str(0)

        for obj_dict in self.obj_dict_list:
            here_class = obj_dict["class_name"]
            here_score = obj_dict["confidence"]
            here_xmin = obj_dict["xmin"]
            here_ymin = obj_dict["ymin"]
            here_xmax = obj_dict["xmax"]
            here_ymax = obj_dict["ymax"]

            if float(here_score) > confidence_score_thresh:
                obj = SubElement(annotation, "object")
                class_name = SubElement(obj, "name")
                class_name.text = here_class
                pose = SubElement(obj, "pose")
                pose.text = "Unspecified"
                truncated = SubElement(obj, "truncated")
                truncated.text = str(0)
                difficult = SubElement(obj, "difficult")
                difficult.text = str(0)
                bndbox = SubElement(obj, "bndbox")
                box_xmin = SubElement(bndbox, "xmin")
                box_xmin.text = str(here_xmin)
                box_ymin = SubElement(bndbox, "ymin")
                box_ymin.text = str(here_ymin)
                box_xmax = SubElement(bndbox, "xmax")
                box_xmax.text = str(here_xmax)
                box_ymax = SubElement(bndbox, "ymax")
                box_ymax.text = str(here_ymax)

        dump (annotation)
        tree = ET.ElementTree(annotation)

        out_xml_file_path = os.path.join(self.out_xml_dir, self.in_img_path.split("/")[-1][:-4] + ".xml")
        tree.write(out_xml_file_path, encoding="UTF-8")