#!/usr/bin/env python3

import tkinter as tk
import cv2
import glob
import numpy as np
from PIL import Image, ImageTk
import random
import threading
from typing import List
import pickle as pk
import sys

class CalibUI:

    def __init__(
        self, 
        size : float,
        chess_board_size : List[int] = [8, 6],
        dir_name : str = './tmp_calib_dir/',
    ):
        '''
        Initialize the CalibUI class.

        Input:
            size: ground truth size of square on chess board, in mm
            chess_board_size: size of square intersections
            dir_name: name of the directionary to store saved images
        '''
        assert isinstance(size, float), \
            '[ERROR] input size is invalid'
        assert len(chess_board_size) == 2, \
            '[ERROR] input chess_board_size is invalid'
        assert isinstance(dir_name, str), \
            '[ERROR] input dir_name is invalid'
        self._size = size
        self._board_size = chess_board_size
        self._dir_name = dir_name
        self._cap = cv2.VideoCapture(-1)
        self._cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        self._img_rgb : np.ndarray()
        self._stop_event = None
        self._window = None
    
    def start_UI(self):
        self._window = tk.Tk()
        self._window.geometry('800x800+10+20')
        img_button = tk.Button(
            self._window,
            text = 'Save Image',
            fg = 'blue',
        )
        img_button.pack(side = 'bottom')
        img_button.bind('<Button-1>', self._save_img)

        calib_button = tk.Button(
            self._window,
            text = 'Calibrate Camera',
            fg = 'red',
        )
        calib_button.pack(side = 'bottom')
        calib_button.bind('<Button-1>', self._calibrate_camera)

        self._stop_event = threading.Event()
        self.thread = threading.Thread(target = self._show_img, args = ())
        self.thread.start()
        
        self._window.wm_title('Camera Calibration')
        self._window.wm_protocol('WM_DELETE_WINDOW', self._on_close)
        self._window.mainloop()
    
    def _save_img(self, event):
        num = str(random.randint(0, 100000))
        img_name = self._dir_name + num + '.png'
        cv2.imwrite(img_name, self._img_rgb)
        print (f'[INFO] image saved in "{img_name}"')

    def _show_img(self):
        try:
            while not self._stop_event.is_set():
                ret, frame = self._cap.read()
                self._img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_tk = self._mat_to_tk_image()

                img_label = tk.Label(image = img_tk)
                img_label.image = img_tk
                img_label.place(x = 0, y = 0)
        except:
            print ('[INFO] sliently pass exception')
    
    def _on_close(self):
        self._stop_event.set()
        self._cap.release()
        self._window.quit()
        print ('[INFO] shutdown camera calibration gui')
    
    def _mat_to_tk_image(self):
        img_pil = Image.fromarray(self._img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)
        return img_tk
    
    def _calibrate_camera(self, event):
        self._stop_event.set()
        img_fnames = glob.glob(self._dir_name + '/*.png')
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        objp = np.zeros((1, self._board_size[0] * self._board_size[1], 3), np.float32)
        objp[0,:,:2] = np.mgrid[
            0 : self._board_size[0], 
            0 : self._board_size[1],
        ].T.reshape(-1, 2)
        objp = objp * self._size

        obj_points, img_points = [], []

        for fname in img_fnames:
            curr_img = cv2.imread(fname)
            img_gray = cv2.cvtColor(curr_img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(
                img_gray, 
                self._board_size, 
                cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE
            )
            if ret:
                obj_points.append(objp)
                corners_2d = cv2.cornerSubPix(img_gray, corners, (11, 11), (-1, -1), criteria)
                img_points.append(corners_2d)
        
        if len(obj_points) == 0: 
            print ('[INFO] no valid image for calibration found')
            print ('[INFO] calibration failed, please restart')
            return
        
        ret, \
        camera_matrix, \
        dist_coeffs, \
        rvecs, \
        tvecs = cv2.calibrateCamera(
            objectPoints = obj_points,
            imagePoints = img_points,
            imageSize = img_gray.shape[: : -1],
            cameraMatrix = None,
            distCoeffs = None,
        )

        calib_dict = {}
        calib_dict['camera_matrix'] = camera_matrix
        calib_dict['dist_coeffs']   = dist_coeffs
        calib_dict['rvecs'] = rvecs
        calib_dict['tvecs'] = tvecs

        with open('cam_calb_result.pickle', 'wb') as f:
            pk.dump(calib_dict, f)

if __name__ == '__main__':
    square_size = float(sys.argv[1])
    calib_ui = CalibUI(size = square_size)
    calib_ui.start_UI()

        





