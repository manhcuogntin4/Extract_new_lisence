import os
import cv2
import xml.etree.ElementTree as ET

#DATA_DIR = '/home/cuong-nguyen/2017/Projets/Permis/Extract-Permis-/Code_sources/Faster_RCNN/axa_permis_dataset/data' # to be customized
DATA_DIR = '/home/cuong-nguyen/2017/Projets/New_driver_lisence_project/CodeSources/Faster_RCNN/Faster_RCNN/axa_nouveau_permis_dataset/data' # to be customized
this_dir = os.path.dirname(__file__)

def check(obj_name):
    return  obj_name == 'nom' or obj_name == 'prenom' \
        or obj_name == 'date_naissance' or obj_name == 'date_permis' \
        or obj_name == 'date_valide' or obj_name == 'type_permis' \
        or obj_name == 'mrz'


def parse_rec(filename):
    """ Parse a PASCAL VOC xml file """
    tree = ET.parse(filename)
    objects = []
    for obj in tree.findall('object'):
        if not check(obj.find('name').text):
            continue
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(bbox.find('xmin').text) - 1,
                              int(bbox.find('ymin').text) - 1,
                              int(bbox.find('xmax').text) - 1,
                              int(bbox.find('ymax').text) - 1]
        objects.append(obj_struct)

    return objects


if __name__ == '__main__':
    annopath = os.path.join(
            DATA_DIR,
            'Annotations',
            '{:s}.xml')
    imagesetfile = os.path.join(DATA_DIR, 'ImageSets', 'train.txt')
    with open(imagesetfile, 'r') as f:
        lines = f.readlines()
    imagenames = [x.strip() for x in lines]
    cnt_nom, cnt_prenom, cnt_naissance, cnt_permis, cnt_valide, cnt_type, cnt_mrz= 0, 0, 0, 0, 0, 0, 0
    for i, imagename in enumerate(imagenames):
        image_file = os.path.join(DATA_DIR, 'Images', imagename + '.png')
        img = cv2.imread(image_file)
        cnt = {}
        for obj in parse_rec(annopath.format(imagename)):
            obj_name = obj['name']
            pts = obj['bbox']
            if obj_name not in cnt:
                cnt[obj_name] = 0
            else:
                cnt[obj_name] += 1
            training_img_name = imagename + '_' + obj_name + str(cnt[obj_name]) + '.png'
            # DEST_DIR = 'lieu' if obj_name == 'lieu' else 'nom'
            DEST_DIR = obj_name
            if not os.path.exists(DEST_DIR):
                os.makedirs(DEST_DIR)
            training_img_path = os.path.join(this_dir, DEST_DIR, training_img_name)
            #cv2.imwrite(training_img_path, img[pts[1]:pts[3], pts[0]:pts[2]])
            if obj_name == 'nom':
                cnt_nom += 1
            if obj_name == 'prenom':
                cnt_prenom += 1
            if obj_name == 'date_naissance':
                cnt_naissance += 1
            if obj_name == 'date_permis':
                cnt_permis += 1
            if obj_name == 'date_valide':
                cnt_valide += 1
            if obj_name == 'type_permis':
                cnt_type += 1
            if obj_name == 'mrz':
                cnt_mrz += 1
        print cnt_nom, cnt_prenom, cnt_naissance, cnt_permis, cnt_valide, cnt_type, cnt_mrz
        if cnt_nom != cnt_prenom or cnt_prenom != cnt_naissance or cnt_naissance != cnt_permis or cnt_permis !=cnt_valide or cnt_valide !=cnt_type \
        or cnt_type !=cnt_mrz:
    		print imagename
            	break
 

