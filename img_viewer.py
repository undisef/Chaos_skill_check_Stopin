import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from skimage.metrics import structural_similarity as ssim
from numpy import sum as npsum


class ImageViewerApp:
    def __init__(self, root):

        self.root = root
        self.root.title("Simple Image Viewer")

        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")

        self.image_1 = None
        self.image_2 = None
        self.img_display_1 = None
        self.img_display_2 = None
        self.canvas_1 = None
        self.canvas_2 = None
        self.image_1_compare_obj = None
        self.image_2_compare_obj = None
        self.comparison_img_diff = None

        self.comparison_widgets_list = []

        self.canvas_height = 360
        self.canvas_width = 640

        self.create_widgets()

    def create_widgets(self):
        label_1 = tk.Label(root, text="Image to compare", font=("Helvetica", 15))
        label_1.place(x=15, y=15)

        btn_load_1 = tk.Button(
            self.root,
            text="Load",
            font=("Helvetica", 15),
            bg="#FFDE59",
            command=self.load_image_1,
        )
        btn_load_1.place(x=15, y=50)

        btn_save_1 = tk.Button(
            self.root,
            text="Save",
            font=("Helvetica", 15),
            bg="#FFDE59",
            command=self.save_image_1,
        )
        btn_save_1.place(x=70, y=50)

        self.canvas_1 = tk.Canvas(
            self.root, width=self.canvas_width, height=self.canvas_height
        )
        self.canvas_1.place(x=15, y=85)

        label_2 = tk.Label(
            root, text="Image to be compared wirth", font=("Helvetica", 15)
        )
        label_2.place(x=815, y=15)

        btn_load_2 = tk.Button(
            self.root,
            text="Load",
            font=("Helvetica", 15),
            bg="#FFDE59",
            command=self.load_image_2,
        )
        btn_load_2.place(x=815, y=50)

        btn_save_2 = tk.Button(
            self.root,
            text="Save",
            font=("Helvetica", 15),
            bg="#FFDE59",
            command=self.save_image_2,
        )
        btn_save_2.place(x=870, y=50)

        self.canvas_2 = tk.Canvas(
            self.root, width=self.canvas_width, height=self.canvas_height
        )
        self.canvas_2.place(x=815, y=85)

        self.btn_compare = tk.Button(
            self.root,
            text="Compare Images",
            font=("Helvetica", 15),
            bg="#FFDE59",
            command=self.compare_images,
        )
        self.btn_compare.place(x=685, y=460)
        self.btn_compare.config(state=tk.DISABLED)

    def load_image_1(self):
        filepath = filedialog.askopenfilename(
            initialdir=".",
            title="Select An Image",
            filetypes=(
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All Files", "*.*"),
            ),
        )
        if filepath:
            self.image_1 = Image.open(filepath)
            image_1_sized = self.image_1.resize((self.canvas_width, self.canvas_height))
            self.img_display_1 = ImageTk.PhotoImage(image_1_sized)
            self.canvas_1.create_image(0, 0, anchor=tk.NW, image=self.img_display_1)

            self.image_1_compare_obj = cv2.imread(filepath)
            self.update_compare_button_state()

    def load_image_2(self):
        filepath = filedialog.askopenfilename(
            initialdir=".",
            title="Select An Image",
            filetypes=(
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All Files", "*.*"),
            ),
        )
        if filepath:
            self.image_2 = Image.open(filepath)
            image_1_sized = self.image_2.resize((self.canvas_width, self.canvas_height))
            self.img_display_2 = ImageTk.PhotoImage(image_1_sized)
            self.canvas_2.create_image(0, 0, anchor=tk.NW, image=self.img_display_2)

            self.image_2_compare_obj = cv2.imread(filepath)
            self.update_compare_button_state()

    def save_image_1(self):
        if self.image_1:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG Files", "*.png"),
                    ("JPEG Files", "*.jpg"),
                    ("All Files", "*.*"),
                ],
            )
            if filepath:
                self.image_1.save(filepath)
                messagebox.showinfo("Image Saved", "Image saved successfully!")
        else:
            messagebox.showwarning("No Image", "No image loaded to save.")

    def save_image_2(self):
        if self.image_2:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG Files", "*.png"),
                    ("JPEG Files", "*.jpg"),
                    ("All Files", "*.*"),
                ],
            )
            if filepath:
                self.image_2.save(filepath)
                messagebox.showinfo("Image Saved", "Image saved successfully!")
        else:
            messagebox.showwarning("No Image", "No image loaded to save.")

    def update_compare_button_state(self):
        if self.image_1 and self.image_2:
            self.btn_compare.config(state=tk.NORMAL)
        else:
            self.btn_compare.config(state=tk.DISABLED)

    def compare_images(self):
        if self.image_1_compare_obj.shape == self.image_2_compare_obj.shape:
            if self.comparison_widgets_list:
                for widget in self.comparison_widgets_list:
                    widget.destroy()
                self.comparison_widgets_list.clear()

            # Similarity comparison
            score, diff = ssim(
                self.image_1_compare_obj,
                self.image_2_compare_obj,
                full=True,
                gaussian_weights=True,
                channel_axis=2,
            )

            label_sim_result_title = tk.Label(
                root, text="Result:", font=("Helvetica", 15)
            )
            label_sim_result_title.place(x=15, y=495)
            self.comparison_widgets_list.append(label_sim_result_title)

            label_sim_score = tk.Label(
                root,
                text=f"Image similarity score: {round(score*100, 2)}%",
                font=("Helvetica", 15),
            )
            label_sim_score.place(x=15, y=555)
            self.comparison_widgets_list.append(label_sim_score)

            if score == 1:
                label_sim_result = tk.Label(
                    root, text="Passed", font=("Helvetica", 15), fg="green"
                )
                label_sim_result.place(x=15, y=525)
                self.comparison_widgets_list.append(label_sim_result)

            else:
                label_sim_result = tk.Label(
                    root, text="Failed", font=("Helvetica", 15), fg="red"
                )
                label_sim_result.place(x=15, y=525)
                self.comparison_widgets_list.append(label_sim_result)

                diff = (diff * 255).astype("uint8")
                diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(
                    diff_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
                )
                contours, _ = cv2.findContours(
                    thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                )
                img1_with_diff_contours = self.image_1_compare_obj.copy()
                cv2.drawContours(img1_with_diff_contours, contours, -1, (0, 0, 255), 2)

                self.display_cv2_image_with_diff(img1_with_diff_contours)

            # RGP comparison
            rgb_stats_1 = self.calculate_rgb_stats(self.image_1_compare_obj)
            rgb_stats_2 = self.calculate_rgb_stats(self.image_2_compare_obj)

            if rgb_stats_1 == rgb_stats_2:
                label_rgb_stats = tk.Label(
                    root, text="RGB data of images is similar", font=("Helvetica", 15)
                )
                label_rgb_stats.place(x=15, y=585)
                self.comparison_widgets_list.append(label_rgb_stats)
            else:
                label_rgb_stats = tk.Label(
                    root, text="RGB data of images is different", font=("Helvetica", 15)
                )
                label_rgb_stats.place(x=15, y=585)
                self.comparison_widgets_list.append(label_rgb_stats)
                table_widgets_1 = self.create_table_with_rgb_stats(
                    rgb_stats_1, "Image 1", 620
                )
                self.comparison_widgets_list.extend(table_widgets_1)
                table_widgets_2 = self.create_table_with_rgb_stats(
                    rgb_stats_2, "Image 2", 750
                )
                self.comparison_widgets_list.extend(table_widgets_2)

        else:
            messagebox.showerror(
                "Image Comparison Failed", "The dimensions of the images are not equal."
            )

    def calculate_rgb_stats(self, img_obg):
        red, green, blue = cv2.split(img_obg)

        r_sum = npsum(red)
        g_sum = npsum(green)
        b_sum = npsum(blue)

        total_pixels = img_obg.shape[0] * img_obg.shape[1]
        r_avg = round(r_sum / total_pixels, 2)
        g_avg = round(g_sum / total_pixels, 2)
        b_avg = round(b_sum / total_pixels, 2)

        total_sum = r_sum + g_sum + b_sum
        r_percentage = round((r_sum / total_sum) * 100, 2)
        g_percentage = round((g_sum / total_sum) * 100, 2)
        b_percentage = round((b_sum / total_sum) * 100, 2)

        color_stats = [
            r_sum,
            r_avg,
            r_percentage,
            g_sum,
            g_avg,
            g_percentage,
            b_sum,
            b_avg,
            b_percentage,
        ]
        return color_stats

    def create_table_with_rgb_stats(self, rgb_stats_1, title, start_y):
        table_widgets = []

        headers = [title, "Red", "Green", "Blue"]

        start_x = 30
        start_y = start_y
        x_offset = 100
        y_offset = 30

        for col, header in enumerate(headers):
            lbl = tk.Label(
                root,
                text=header,
                font=("Helvetica", 12, "bold"),
                borderwidth=2,
                relief="groove",
            )
            lbl.place(x=start_x + col * x_offset, y=start_y)
            table_widgets.append(lbl)

        stats_labels = ["Total intensity", "Average intensity", "Color Percentage"]

        for row, stat_label in enumerate(stats_labels):
            lbl_stat = tk.Label(
                root,
                text=stat_label,
                font=("Helvetica", 10),
                borderwidth=2,
                relief="groove",
            )
            lbl_stat.place(x=start_x, y=start_y + (row + 1) * y_offset)

            lbl_red = tk.Label(
                root, text=rgb_stats_1[row], borderwidth=2, relief="groove"
            )
            lbl_red.place(x=start_x + x_offset, y=start_y + (row + 1) * y_offset)
            lbl_green = tk.Label(
                root, text=rgb_stats_1[row + 3], borderwidth=2, relief="groove"
            )
            lbl_green.place(x=start_x + 2 * x_offset, y=start_y + (row + 1) * y_offset)
            lbl_blue = tk.Label(
                root, text=rgb_stats_1[row + 6], borderwidth=2, relief="groove"
            )
            lbl_blue.place(x=start_x + 3 * x_offset, y=start_y + (row + 1) * y_offset)
            table_widgets.extend([lbl_stat, lbl_red, lbl_green, lbl_blue])

        return table_widgets

    def display_cv2_image_with_diff(self, img_result):
        blue, green, red = cv2.split(img_result)
        img_array = cv2.merge((red, green, blue))
        img = Image.fromarray(img_array)
        img = img.resize((self.canvas_width, self.canvas_height))
        self.comparison_img_diff = ImageTk.PhotoImage(image=img)

        canvas_diff_result = tk.Canvas(
            self.root, width=self.canvas_width, height=self.canvas_height
        )
        canvas_diff_result.place(x=815, y=495)
        canvas_diff_result.create_image(
            0, 0, anchor=tk.NW, image=self.comparison_img_diff
        )
        self.comparison_widgets_list.append(canvas_diff_result)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewerApp(root)
    root.mainloop()
