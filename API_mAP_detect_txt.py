import os

class API_mAP_detect_txt():

    # １．このコンストラクタを画像パスのループの先頭に挿入してください。
    # 1. Insert this constructor at the beginning of the image path loop.
    def __init__(self, in_img_path, out_txt_dir):
        self.in_img_path = in_img_path
        self.out_txt_dir = out_txt_dir
        if os.path.exists(self.out_txt_dir)==False:
            os.makedirs(self.out_txt_dir)

        self.out_txt_list = []

        print(self.in_img_path)
        print(self.out_txt_dir)
        
    
    # ２．このメソッドをclass_name, confidence, left, topなどのオブジェクトごとのバウンディングボックスの情報が得られる場所に挿入してください。
    # left, top, width, heightなどは、left=xmin, top=ymin, width=xmax-xmin, height=ymax-yminのように計算してください。
    # 2. Insert this method where you can get per-object bounding box information such as class_name, confidence, left, top.
    # For left, top, width, height, etc., calculate as left = xmin, top = ymin, width = xmax-xmin, height = ymax-ymin.
    def iter(self, class_name, confidence, left, top, width, height):
        obj_info_string = class_name + " " + confidence + " " + left + " " + top + " " + width + " " + height
        self.out_txt_list.append(obj_info_string)


    # ３．テキストファイルとして出力するために、このメソッドを画像パスのループの一番最後に挿入してください。
    # 3. Insert this method at the very end of the image path loop to output as a text file.
    def make_txt(self):
        out_txt_file_path = os.path.join(self.out_txt_dir, self.in_img_path.split("/")[-1][:-4]+".txt")

        with open(out_txt_file_path, mode="w") as f:
            f.write("\n".join(self.out_txt_list))