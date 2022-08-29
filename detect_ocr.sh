conda activate ANPR

cd yolov7
python detect.py --weights ./runs/train/yolov7-license/weights/best.pt --conf 0.25 --img-size 640 --source ../license --save-txt
cd ..
python OCR.py