import requests
from urllib3.exceptions import InsecureRequestWarning
import os
import csv
import cv2

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_video(url, video_name):
    # time.sleep(1)

    try:
        print('Download ', video_name, ' from ', url, ' ...')
        response = requests.get(url, verify=False)
        open('Video.mp4', "wb").write(response.content)
        print('... done')
        return True
    except requests.exceptions.RequestException as e:
        print(e)

    return False


def main():
    image_dir = r'.\keyframes'
    if not os.path.exists(image_dir):
        os.mkdir(image_dir)

    with open('keyframe_metadata.csv') as csv_file:
        keyframe_data_list = csv.reader(csv_file, delimiter=',')

        cap = None
        prev_video_name = None
        for keyframe_data in keyframe_data_list:
            if prev_video_name is not None:
                video_name = keyframe_data[0]
                frame = int(keyframe_data[2])
                image_file = os.path.join(image_dir, video_name + '_' + str(frame) + '.jpg')

                if not os.path.exists(image_file):
                    if video_name != prev_video_name:
                        url = keyframe_data[1]
                        if get_video(url, video_name):
                            cap = cv2.VideoCapture('Video.mp4')
                            prev_video_name = video_name
                            print('Extract keyframes:')
                        else:
                            break
                    cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
                    is_read, image = cap.read()
                    if is_read and image is not None:
                        print("frame number: ", frame)
                        cv2.imwrite(image_file, image)
            else:
                prev_video_name = ""


if __name__ == '__main__':
    main()
