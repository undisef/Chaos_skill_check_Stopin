# Chaos Skill Check Project

This repository contains scripts for viewing and comparing images, as well as test cases required for skill check task.

## Table of Contents
- [Environment Setup](#environment-setup)
- [Installation of Tesseract OCR](#installation-of-tesseract-ocr)
- [Usage](#usage)
  - [Image Viewer](#image-viewer)
  - [Testing](#testing)
  
---

## Environment Setup

1. **Create a virtual environment**  

   ```bash
   python -m venv .venv
   ```

2. **Activate the virtual environment**

   On macOS/Linux: 

   ```bash
   source .venv/bin/activate
   ```

   On Windows:

   ```cmd
   .venv\Scripts\activate
   ```

3. **Install required packages**

   ```bash
   pip install -r requirements.txt
   ```


## Installation of Tesseract OCR
The script test.py uses the pytesseract library for Optical Character Recognition (OCR). \
To enable OCR capabilities, a separate installation of the Tesseract OCR Engine is required.

   - Windows:
   Download the Tesseract installer from the official GitHub repository and run the installer.
   [Tesseract OCR for Windows ](https://github.com/UB-Mannheim/tesseract/wiki)

   - macOS:
    Install Tesseract via Homebrew.

      ```bash
      brew install tesseract
      ```

## Usage

### Image Viewer

The img_viewer.py script provides a desktop application for viewing, comparing, and saving images in JPG or PNG formats.

To launch the application, run:

   ```bash
   python img_viewer.py
   ```

### Testing

The test.py script contains seven pytests for the skill check task.

To execute the tests, run:

   ```bash
   pytest test.py
   ```

As a result output, tests will generate two files step4_report.png and step7_report.png with capruted comparison report from img_viewer app.