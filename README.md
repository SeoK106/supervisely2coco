Supervisely to COCO
=========================

Convert [supervisely](https://supervise.ly/) output to COCO keypoint data format

 - [COCO Annotation Dataset format](https://www.immersivelimit.com/tutorials/create-coco-annotations-from-scratch/#coco-dataset-format)
 - [COCO keypoint API webpage](https://cocodataset.org/#keypoints-2020)


HowToUse
------------------------
**1. Set the Class**

<img src="https://user-images.githubusercontent.com/66738234/116811915-c9878000-ab86-11eb-964c-8d1ea13125b2.png" width="70%" title="class_setting"></img>

 * setting the title to **person**
 * setting shape to **keypoints**
 * drawing the keypoints templete or uploading a keypoint image

**2. Draw keypoints on the image**
![skeleton_drawing](https://user-images.githubusercontent.com/66738234/116812122-0b64f600-ab88-11eb-91da-6e42107672ac.png)

**3. Download annotation and meta file(.json) from supervisely**

**4. Execute the code**

    Anconda prompt
    > python supervisely2coco.py meta_file_path(~/meta.json) annotation_dir_path(~/ann) save_dir_path(~/,deault = ./result.json)


------------------------
Souce code Referenced: https://gist.github.com/caiofcm/0b93b0084669a1287633d9ebf32f3833
