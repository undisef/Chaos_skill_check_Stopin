import pytest
import pyautogui
import os
import subprocess
from time import sleep
from PIL import Image
from re import search
from platform import system
import pytesseract
import logging


LOGGER = logging.getLogger(__name__)

APP_PATH = "img_viewer.py"
APP_TITLE = "Simple Image Viewer"


def get_window_coordinates_by_title(title):
    os_name = system()
    LOGGER.info(f"Operating system: {os_name}")
    if os_name == "Windows":
        from pygetwindow import getWindowsWithTitle

        windows = getWindowsWithTitle(title)
        if windows:
            win = windows[0]
            return [int(win.left), int(win.top)]
        else:
            raise Exception(f"Window titled '{title}' not found on Windows.")

    elif os_name == "Darwin":
        from Quartz import (
            CGWindowListCopyWindowInfo,
            kCGWindowListOptionOnScreenOnly,
            kCGNullWindowID,
        )

        windows = CGWindowListCopyWindowInfo(
            kCGWindowListOptionOnScreenOnly, kCGNullWindowID
        )
        for window in windows:
            window_title = window.get("kCGWindowName", "")
            if title in window_title:
                bounds = window["kCGWindowBounds"]
                LOGGER.info(bounds)
                return [int(bounds["X"]), int(bounds["Y"])]
        raise Exception(f"Window titled '{title}' not found on macOS.")

    else:
        raise Exception("This function only supports Windows and macOS")


def delete_files(files_list):
    for file_path in files_list:
        if os.path.isfile(file_path):
            os.remove(file_path)
            LOGGER.info(f"{file_path} has been deleted.")
        else:
            LOGGER.info(f"{file_path} does not exist.")


def click_load_image_1_button(init_x, init_y):
    pyautogui.click(init_x + 30, init_y + 90)
    sleep(1)


def click_load_image_2_button(init_x, init_y):
    pyautogui.click(init_x + 830, init_y + 90)
    sleep(1)


def click_save_image_1_button(init_x, init_y):
    pyautogui.click(init_x + 110, init_y + 90)
    sleep(1)


def click_save_image_2_button(init_x, init_y):
    pyautogui.click(init_x + 900, init_y + 90)
    sleep(1)


def click_compare_button(init_x, init_y):
    pyautogui.click(init_x + 750, init_y + 500)
    sleep(3)


def type_filename_in_module_window_and_save(filename):
    pyautogui.write(filename)
    pyautogui.press("enter")
    sleep(2)
    pyautogui.press("enter")
    sleep(1)


def type_filename_in_module_window_and_save_in_jpg(filename):
    pyautogui.write(filename)
    os_name = system()
    LOGGER.info(f"Operating system: {os_name}")
    if os_name == "Windows":
        pyautogui.press("tab")
        sleep(1)
        pyautogui.press("down")
        sleep(1)
        pyautogui.press("down")
        sleep(1)
        pyautogui.press("enter")
        sleep(1)
        pyautogui.press("enter")
        sleep(1)
        pyautogui.press("enter")
        sleep(1)
    elif os_name == "Darwin":
        pyautogui.click(800, 375)
        sleep(1)
        pyautogui.click(800, 395)
        sleep(1)
        pyautogui.click(1000, 420)
        sleep(1)
        pyautogui.press("enter")
        sleep(1)
    else:
        raise Exception("This function only supports Windows and macOS")


def search_and_open_file_in_module_window(filename):
    pyautogui.write(filename)
    pyautogui.press("enter")
    sleep(1)


def make_screenshot_of_app_and_save_with_filename(filename):
    screenshot = pyautogui.screenshot(region=(0, 50, 1680, 900))
    screenshot.save(filename)


def parse_comparison_result_status_from_app_screenshot(filename):
    result_img = Image.open(filename)
    os_name = system()
    if os_name == "Windows":
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    text_from_image = pytesseract.image_to_string(result_img)
    LOGGER.info(text_from_image)
    lines = text_from_image[:-1].splitlines()
    img_comparison_result = None
    for i, line in enumerate(lines):
        if search(r"Result", line) and i + 1 < len(lines):
            img_comparison_result = lines[i + 1].strip()
    return img_comparison_result


class TestMethods:
    @classmethod
    def setup_class(cls):
        screen_width, screen_height = pyautogui.size()
        LOGGER.info(f"Screen resolution: {screen_width}x{screen_height}")

        test_generated_files_to_cleanup = (
            "REF_Image.png",
            "REF_Image.jpg",
            "step4_report.png",
            "step7_report.png",
        )
        delete_files(test_generated_files_to_cleanup)

        cls.img_viewer_app_process = subprocess.Popen(["python", APP_PATH])
        sleep(5)
        if cls.img_viewer_app_process.poll() is not None:
            raise Exception(f"Failed to start the application {APP_PATH}")

        app_coordinates = get_window_coordinates_by_title(APP_TITLE)
        LOGGER.info(f"App window coordinates: {app_coordinates}")
        cls.init_x = app_coordinates[0]
        cls.init_y = app_coordinates[1]

    @classmethod
    def teardown_class(cls):
        if cls.img_viewer_app_process:
            cls.img_viewer_app_process.terminate()
            cls.img_viewer_app_process.wait()

    def test_step_1(self):
        # Step 1: Run the Python app
        assert (
            self.img_viewer_app_process.poll() is None
        ), "Image viewer app is not running"

    def test_step_2(self):
        # Step 2: Import image: IMAGE_1
        click_load_image_1_button(self.init_x, self.init_y)
        search_and_open_file_in_module_window("IMAGE_1.png")
        assert "IMAGE_1.png" in os.listdir(), "Failed to import IMAGE_1.png"

    def test_step_3(self):
        # Step 3: Grab an open image and save as a reference image - REF_Image
        click_save_image_1_button(self.init_x, self.init_y)
        type_filename_in_module_window_and_save("REF_Image.png")
        assert "REF_Image.png" in os.listdir(), "Failed to save REF_Image.png"

    def test_step_4(self):
        # Step 4: Verify with image comparison that the imported image looks correctly in the Image Editor (IMAGE_1=REF_Image)

        # Step 4.1: Open REF_Image for comparison
        click_load_image_2_button(self.init_x, self.init_y)
        search_and_open_file_in_module_window("REF_Image.png")

        # Step 4.2: click compare button
        click_compare_button(self.init_x, self.init_y)

        # Step 4.3: make screenshot with report
        make_screenshot_of_app_and_save_with_filename("step4_report.png")
        img_comparison_result = parse_comparison_result_status_from_app_screenshot(
            "step4_report.png"
        )
        assert img_comparison_result == "Passed", "Comparison result is Failed"

    def test_step_5(self):
        # Step 5: Export the open Image in JPG format to a local drive
        click_save_image_2_button(self.init_x, self.init_y)
        type_filename_in_module_window_and_save_in_jpg("REF_Image.jpg")
        assert "REF_Image.jpg" in os.listdir(), "Failed to save REF_Image.png"

    def test_step_6(self):
        # Step 6: Verify that the exported image exists
        assert os.path.isfile("REF_Image.jpg"), "REF_Image.jpg does not exist."

    def test_step_7(self):
        # Step 7: Verify with image comparison whether the exported image is equal to IMAGE_2 (to be failed)

        # Step 7.1: Import image: REF_Image.jpg
        click_load_image_1_button(self.init_x, self.init_y)
        search_and_open_file_in_module_window("REF_Image.jpg")

        # Step 7.2: Import image: IMAGE_2.png
        click_load_image_2_button(self.init_x, self.init_y)
        search_and_open_file_in_module_window("IMAGE_2.png")

        # Step 7.3: click compare button
        click_compare_button(self.init_x, self.init_y)

        # Step 7.4: make screenshot with report
        make_screenshot_of_app_and_save_with_filename("step7_report.png")
        img_comparison_result = parse_comparison_result_status_from_app_screenshot(
            "step7_report.png"
        )
        assert img_comparison_result == "Passed", "Comparison result is Failed"


if __name__ == "__main__":
    pytest.main()
