import cv2
import subprocess
import numpy as np

import config as cfg
from .Box import Box
from .Matrix import Matrix


class Detector:
    def __init__(self):
        self.img = self.take_screenshot()
        
    def take_screenshot(self):
        try:
            screenshot = subprocess.run(
                [cfg.adb_path, "exec-out", "screencap", "-p"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            self.img = np.frombuffer(screenshot.stdout, dtype=np.uint8)
            self.img = cv2.imdecode(self.img, cv2.IMREAD_COLOR)
            return self.img

        except FileNotFoundError:
            raise RuntimeError("ADB not found. Wrong path")

        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Error while running ADB: {e.stderr.decode().strip()}"
            )

    def get_shapes(self):
        digest = []

        template = cv2.imread(cfg.template_path, cv2.IMREAD_COLOR)
        if template is None:
            raise RuntimeError("Template not found. Wrong path")
        template_bw = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        templ_height, templ_width = template_bw.shape

        for idx, region in enumerate(cfg.shapes_regions):
            x, y, w, h = region
            img_temp = self.img[y : y + h, x : x + w]
            img_bw = cv2.cvtColor(img_temp, cv2.COLOR_BGR2GRAY)

            result = cv2.matchTemplate(img_bw, 
                                       template_bw, cv2.TM_CCOEFF_NORMED)
            xs, ys = np.where(result >= 0.85)

            coords = list(zip(xs, ys))
            final_coords = []

            for y_coord, x_coord in coords:
                x_center = x_coord + templ_width // 2
                y_center = y_coord + templ_height // 2

                if not any(
                    abs(x_center - cx) <= 10 and abs(y_center - cy) <= 10
                    for cx, cy in final_coords
                ):
                    final_coords.append((x_center, y_center))

            if final_coords:
                base_x, base_y = final_coords[0]
                normalized = [
                    (round((x_c - base_x) / cfg.dist), 
                     round(-(y_c - base_y) / cfg.dist))
                    for x_c, y_c in final_coords
                ]
            else:
                normalized = []

            digest.append(normalized)

        return tuple(tuple(sublist) for sublist in digest)

    
    def get_matrix(self):
        positions = []

        for x in range(8):
            for y in range(8):
                x_temp = 120 + 120 * x
                y_temp = 640 + 120 * y
                pixel_value = self.img[(y_temp, x_temp)][0]
                color_threshold = cfg.BGR_empty_box[0]

                if (pixel_value < color_threshold - 2 
                    or pixel_value > color_threshold + 2):
                    positions.append((x, abs(y - 7)))

        matrix = Matrix([[0] * 8 for _ in range(8)])

        for x, y in positions:
            Box(matrix, x, y).set_status(1)

        return matrix.matrix
