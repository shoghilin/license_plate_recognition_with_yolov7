# setup yolov7
conda activate ANPR

if test -f "yolov7"; then
    echo "YOLOv7 installed"
else
    git clone https://github.com/WongKinYiu/yolov7.git
fi

cd yolov7
if test -f "Dataset"; then
    echo "Dataset builded"
else
    echo "Build dataset"
    echo "train: Dataset/train/images" > data/alpr.yaml
    echo "val:   Dataset/train/images" >> data/alpr.yaml

    echo "nc : 1" >> data/alpr.yaml
    echo "names: ['license']" >> data/alpr.yaml

    cat data/alpr.yaml

    # Prepare dataset - split train, validation set.
    mkdir -p Dataset/train/labels

    # create training set
    mkdir -p Dataset/train
    cp -rf ../car-plate-detection/images Dataset/train

    # create validation set
    mkdir -p Dataset/val
    cp -rf ../car-plate-detection/images/Cars1*.png Dataset/val

    # create validation labels
    python ../prepare_dataset.py
    mkdir -p Dataset/val/labels
    cp -rf Dataset/train/labels/Cars1*.txt Dataset/val/labels
fi

#--- YOLOv7 Training ---#
# finetune p5 models
wget https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7_training.pt
python train.py --workers 8 --device 0 --batch-size 8 --data data/alpr.yaml --img 640 640 --cfg cfg/training/yolov7.yaml --weights 'yolov7_training.pt' --name yolov7-license --hyp data/hyp.scratch.custom.yaml

# detect
# python detect.py --weights yolov7_training.pt --conf 0.25 --img-size 640 --source inference/images/license.png