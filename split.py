import os
import glob
import tqdm
import shutil
from sklearn.model_selection import train_test_split
import argparse

def main():
    parser = argparse.ArgumentParser(description='Convert .pcd to .npy & .json to .txt')
    parser.add_argument(
        '--path',
        help='.path.'
    )
    
    args = parser.parse_args()
    
    case = args.path.split('/')[-2]

    label_dir = args.path + 'labels/'

    file_list = [file[:-4] for file in os.listdir(label_dir) if file.endswith('.txt')]

    train, temp = train_test_split(file_list, test_size=0.2, random_state=42)
    val, test = train_test_split(temp, test_size=0.5, random_state=42)

    print('Start Data Split')
    print(f'train : {len(train)}, val : {len(val)}, test : {len(test)}')

    # save ImageSets

    with open(args.path + 'ImageSets/train.txt', 'w+') as file:
        file.write('\n'.join(train))

    with open(args.path + 'ImageSets/val.txt', 'w+') as file:
        file.write('\n'.join(val))

    with open(args.path + 'ImageSets/test.txt', 'w+') as file:
        file.write('\n'.join(test))
    
    print('Finish Data Split')

if __name__ == '__main__':
    main()