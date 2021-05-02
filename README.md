Supervisely to COCO
=========================

Convert [supervisely](https://supervise.ly/) output to COCO keypoint data format

 - [COCO Annotation Dataset format](https://www.immersivelimit.com/tutorials/create-coco-annotations-from-scratch/#coco-dataset-format)
 - [COCO keypoint API webpage](https://cocodataset.org/#keypoints-2020)


HowToUse
------------------------
**1. Set the Class**

![class_setting](https://user-images.githubusercontent.com/66738234/116811915-c9878000-ab86-11eb-964c-8d1ea13125b2.png)

 * setting the title to **person**
 * setting shape to **keypoints**
 * drawing the keypoints templete or uploading a keypoint image
 

**2. Draw keypoints on the image**

![skeleton_drawing](https://user-images.githubusercontent.com/66738234/116812122-0b64f600-ab88-11eb-91da-6e42107672ac.png)

**3. Download annotation and meta file(.json) from supervisely**

**4. Execute the code**

     #Anconda prompt
     
     > python supervisely2coco.py meta_file_path annotation_dir_path save_dir_path
     
     * meta_file_path: ~/meta.json
     * annotation_dir_path: ~/ann
     * save_dir_path: ~/, default = ./result.json
    
 Output
 ----------------------
 
![result](https://user-images.githubusercontent.com/66738234/116812782-7ebc3700-ab8b-11eb-8872-de34acc400c1.png)

cf. On the left is **'sample_1_person.png'**, and on the right is **'smaple_2_person.png'**.

![input_images](https://user-images.githubusercontent.com/66738234/116812900-2afe1d80-ab8c-11eb-91a9-8f70ff1f4206.png)
 
 

------------------------
Souce code Referenced: https://gist.github.com/caiofcm/0b93b0084669a1287633d9ebf32f3833
