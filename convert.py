import os
import glob
import numpy as np
import json
from tqdm import tqdm
import argparse

def json2txt(case, path):
    with open(path, 'r') as f:
        label = json.load(f)
    
    objects = label['annotation']['objects']

    # json2txt
    anno_all = []
    for i in objects:
        anno_list = []
        i = i['object']
        
        # type
        subclass = i['subclass']
        # class
        subclass = subclass.lower()
        subclass = subclass.replace(' ', '')
        
        if case in ['36_3', '36_4']:
            if subclass in ['motorcycle', 'bicycle', 'twowheeler', 'pedestrian', 'trafficlight']:
                subclass = None
        
        if subclass != None:
            # location
            anno_list.append(str(i['location']['x3d']))
            anno_list.append(str(i['location']['y3d']))
            anno_list.append(str(i['location']['z3d']))
            
            # dimensions(lwh)
            anno_list.append(str(i['dimension']['length']))
            anno_list.append(str(i['dimension']['width']))
            anno_list.append(str(i['dimension']['height']))
            
            # rotation_y
            anno_list.append(str(i['yaw']))
            anno_list.append(subclass)
            
            anno_all.append(' '.join(anno_list))
            anno_all.append('\n')

            # save txt
            save_path = path.replace('.json', '.txt').replace('/json/', '/labels/')
            with open(save_path, 'w') as file:
                for i in anno_all:
                    file.write(i)    

def pcd2npy(path):
    with open(path, 'r') as f:
        pcd = f.readlines()
    
    pcd = [i.replace('\n', '') for i in pcd]
    
    index = pcd.index("DATA ascii")
    pcd = pcd[index + 1:]

    arr_list = []
    for val in pcd:
        temp = val.split(' ')[:4]
        
        arr_list.append(np.array(temp, dtype='float32'))
        
    save_path = path.replace('.pcd', '.npy').replace('/pcd/', '/points/')
    np.save(save_path, np.array(arr_list))


def main():
    parser = argparse.ArgumentParser(description='Convert .pcd to .npy & .json to .txt')
    parser.add_argument(
        '--path',
        help='.path.'
    )
    
    args = parser.parse_args()
    
    case = args.path.split('/')[-2]
    json_path = args.path + 'json/'
    
    json_file_list = glob.glob(os.path.join(json_path, '*.json'))
    
    print('Start Convert json to txt')
    for json_path in tqdm(json_file_list):
        json2txt(case, json_path)
        
    label_path = args.path + 'labels/'
    label_file_list = glob.glob(os.path.join(label_path, '*.txt'))
    
    pcd_file_list = [i.replace('.txt', '.pcd').replace('/labels/', '/pcd/') for i in label_file_list]
    
    print('Start Convert pcd to npy')
    for pcd_path in tqdm(pcd_file_list):
        pcd2npy(pcd_path)
        
    print('Finish Converting')
    
if __name__ == '__main__':
    main()