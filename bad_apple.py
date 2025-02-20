import sys
import cv2
from pprint import pprint

from	tcp_bridge	import TCPBridge

img_name_base = "assets/badapple/16x16/img_"

def rescale_frame(frame_input):
    dim = (16, 16)
    return cv2.resize(frame_input, dim, interpolation=cv2.INTER_AREA)

def	frame2grayscale(frame):
	frame_data = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	return cv2.threshold(frame_data, 127, 255, cv2.THRESH_BINARY)[1]

def get_filename(fileid):
	return f"{img_name_base}{fileid:04}.png"

def	rescale_bad_apple():
	video = cv2.VideoCapture("assets/badapple/badapple.mp4")

	fps_in = video.get(cv2.CAP_PROP_FPS)
	fps_out = 8

	count_in = 0
	count_out = 0
	success = 1

	while True:
		success = video.grab()
		if not success:
			break

		out_due = int(count_in / fps_in * fps_out)
		if out_due > count_out:
			success, frame = video.retrieve()
			if not success:
				break
			frame = rescale_frame(frame)
			frame = frame2grayscale(frame)
			cv2.imwrite(f"{get_filename(count_out)}", frame)
			count_out += 1
			print(f"{count_in}:{count_out} done")
		count_in += 1

def frame2bitmap(frame):
	data = []
	count = 0
	for line in img:
		for pixel in line:
			if pixel[0] == 0x00:
				data.append(0)
			else:
				data.append(1)
	return data


def print_bitmap(frame):
	for k, v in enumerate(frame):
		print(v, end="")
		if not ((k + 1) % 16):
			print()

def bitmap2array(frame):
	frame = frame2bitmap(frame)
	data = []

	data_tmp = 0
	count = 0
	for pixel in frame:
		if pixel == 1:
			data_tmp += 1
		count += 1
		if count == 8:
			data.append(data_tmp)
			count = 0
			data_tmp = 0
		data_tmp <<= 1
	return data

def print_array(frame):
	for k, v in enumerate(frame):
		print(bin(v).removeprefix("0b").rjust(8, "0"), end="")
		if not ((k + 1) % 2):
			print()

if __name__ == "__main__":
	# rescale_bad_apple()

	tcp_bridge = TCPBridge("", 4444)

	# img = cv2.imread(get_filename(1733))
	# img = cv2.imread(get_filename(579))
	# img = cv2.imread(get_filename(61))
	# data = bitmap2array(img)
	# print_array(data)

	data = []
	base = 10
	nb_frame = 32

	for i in range(base, base + nb_frame + 1):
		img = cv2.imread(get_filename(i))
		array = bitmap2array(img)
		data.extend(array)
		print_array(array)
		print()


	tcp_bridge.accept_connection()
	tcp_bridge.send_program(data, start=0x1000)
	tcp_bridge.close()
