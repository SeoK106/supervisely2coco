"""
   **************************************
    Author : SeoK106
    ------------------------------------
    Original Author: Caio Marcellos          
         Email: caiocuritiba@gmail.com
   **************************************
    
    # Converting from suvervisely output to COCO data format
    
    Example of Usage in commandline:
    > python supervisely2coco.py  meta_file_path(~/meta.json)  annotation_directory_path(~/ann)  save_directory_path(~/,default = ./result.json)
     
"""

import os
import numpy as np
import json
from datetime import datetime
import argparse
import sys


def convert_supervisely_to_coco(meta_path, ann_dir, save_dir='./'):
    
    ann_fnames, ann_jsons = get_all_ann_files(ann_dir)
    meta_category,meta_keypoints,meta_skeleton,node_names = get_info_from_meta(meta_path)
  
    # Generate "categories" part
    catg_repr = [{
            "supercategory":category,
            "id": idx,
            "name": category,
            "keypoints":meta_keypoints[idx-1],
            "skeleton":meta_skeleton[idx-1]
    } for idx,category in enumerate(meta_category,1)]

    ann_name = []
    for name in ann_fnames:
        ann_name.append(name.split(".")[0])


    # Generate "images" and "annotations" part 
    out_cnv_imgs = [
        divide_and_generate_annots(seq, ann_fnames[seq], ann_jsons[seq], meta_category, ann_dir, node_names)
        for seq in range(len(ann_fnames))
    ]

    images_repr = [out[0] for out in out_cnv_imgs]
    images_repr.sort(key=lambda x: x['id'])
    
    ann_repr = [x for out in out_cnv_imgs for x in out[1]]
    ann_repr.sort(key=lambda x: x['image_id'])

    
    # Generate COCO format
    coco_fmt = {
        "info": {
            "description" : "Convert supersively to COCO format",
            "version": " ", # set the version
            "year": datetime.now().strftime('%Y'),
            "contributor": " ", # set the name of contributor
            "date_created": datetime.now().strftime("%Y/%m/%d")
        },
        "licenses": [
            {
                "id": , # set the license id
                "name": " "  # set the license name
            }
        ],
        "images": images_repr,
        "annotations": ann_repr,
        "categories": catg_repr
    }

    # Save the result json file in sava_path
    if save_dir:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        path = save_dir +"result.json"
        with open(path, 'w') as f:
            json.dump(coco_fmt, f, cls=NpEncoder)
    else:
        print("No directory path to save result.json")


    return coco_fmt


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer): 
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


def divide_and_generate_annots(idimg, fname_img, json_suprv, categories, imgs_base_dir, node_names, start_annot_id=10000):
    # Generate image_part
    # omitted elements: coco_url, date_captured, flickr_url
    image_annot = {
            "license": , # set the id of license ex)"licenses": 1
            "file_name": fname_img,
            "height": json_suprv['size']['height'],
            "width": json_suprv['size']['width'],
            "id": int(idimg)
            }

    # Generate annotation_part
    objects = []
    for obj in json_suprv['objects']:
        if obj:
            object_list = []
            nodes = obj["nodes"]
            for name in node_names:
                coord = []
                for pos in nodes[name]['loc']:
                    coord.append(round(pos))
                object_list.append(coord)
        objects.append(object_list)

    # When keypoints exist
    ann = []
    for indx,obj in enumerate(objects,1):
        coords = np.array(obj)

        # Calculate bbox element
        bbox = [
                np.min(coords,axis=0)[0],
                np.min(coords,axis=0)[1],
                np.max(coords,axis=0)[0] - np.min(coords,axis=0)[0],
                np.max(coords,axis=0)[1] - np.min(coords,axis=0)[1],
            ]

        flatten_objects = coords.flatten().tolist()
        for i in range(len(obj)):
            flatten_objects.insert(3*i+2,2)

        # Matching category_id 
        # The category in the COCO data format is "person"
        catg_id = 0
        for idx,catg in enumerate(categories,1):
            if catg == "person":
                catg_id = idx
        if catg_id == 0:
            catg_id = None

        ann.append(
            {
                "segmentation": [],
                "num_keypoints": len(obj),
                "area": bbox[2]*bbox[3],
                "iscrowd": 1 if len(objects)>1 else 0,
                "keypoints": flatten_objects,
                "image_id": int(idimg),
                "bbox": bbox,
                "category_id": catg_id,
                "id": indx*10000 + int(idimg)
            }
        )

    # When keypoints don't exist
    if not objects:
        ann.append(
            {
                "image_id": int(idimg),
                "id": start_annot_id + int(idimg)
            }
        )

    return image_annot, ann


def get_all_ann_files(ann_dir):
    file_list = os.listdir(ann_dir)
    all_ann_files = [file for file in file_list if file.endswith(".json")]
    all_fname_img = [fname.split('.')[0] for fname in all_ann_files]  
    all_json_ann = []
    
    for json_path in all_ann_files:
        with open(os.path.join(ann_dir,json_path)) as fs:
            json_suprv = json.load(fs)
        all_json_ann += [json_suprv]
        
    return all_fname_img, all_json_ann


def get_info_from_meta(meta_json_path):
    with open(meta_json_path) as mf:
        json_meta = json.load(mf)

    meta_category = [clss['title'] for clss in json_meta['classes']]
    
    meta_keypoints = []
    meta_skeleton = []
    node_names = []

    sub_jsons = json_meta['classes']
    for sub in sub_jsons:
        sub_nodes = []
        sub_edges = []
        if 'geometry_config' in sub:
            sub_json = sub['geometry_config']
            for node in sub_json['nodes']:
                temp = []
                node_names.append(node)
                for node in sub_json['nodes'][node]['label']:
                    temp.append(node)
                sub_nodes.append(''.join(temp))
  
            for sub_class in sub_json['edges']:
                temp = []
                temp2 = []
                for node in sub_class['label']:
                    temp.append(node)
                temp = ''.join(temp)
                temp = temp.split(',')
                for num in temp:
                    if num.isdigit():
                        temp2.append(int(num))
                sub_edges.append(temp2)
                
        meta_keypoints.append(sub_nodes)
        meta_skeleton.append(sub_edges)
    
    return meta_category,meta_keypoints,meta_skeleton,node_names


def main():
    parser = argparse.ArgumentParser(description="""
    Supervisely2Coco:
    Converting from suvervisely output to COCO data format
    Example of Usage in commandline:
        > python supervisely2coco.py  meta_file_path('~/meta.json')  annotation_directory_path('~/ann')  save_path(~/)
    """)
    parser.add_argument(
        "-v",
        "--version",
        help="display version information",
        action="version",
        version="Supervisely2Coco {}, Python {}".format('0.0.1', sys.version),
    )
    parser.add_argument("meta_file_path", type=str, help="Meta.json file path(~/meta.json)")
    parser.add_argument("ann_dir", type=str, help="Annotations directory path (usually downloaded in '~/ann' )")
    parser.add_argument("save_dir", type=str, help="Path to save converted JSON file(~/)") 
    args = parser.parse_args()

    meta_file_path = args.meta_file_path
    ann_dir = args.ann_dir
    save_dir = args.save_dir
    
    coco_fmt = convert_supervisely_to_coco(meta_file_path, ann_dir, save_dir)
    print('\n**Successful conversion!**')


if __name__ == "__main__":
    main()
