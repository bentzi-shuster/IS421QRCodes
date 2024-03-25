import sys
import qrcode
from dotenv import load_dotenv
import logging.config
from pathlib import Path
import os
import argparse
from datetime import datetime
import validators

load_dotenv()

QR_DIRECTORY = os.getenv('QR_CODE_DIR', 'qr_codes')
FILL_COLOR = os.getenv('FILL_COLOR', 'black')
BACK_COLOR = os.getenv('BACK_COLOR', 'white')


class QRCodeGenerator:
    def __init__(self, url, path, fill_color='red', back_color='white'):
        self.url = url
        self.path = path
        self.fill_color = fill_color
        self.back_color = back_color

    def validate_url(self):
        if validators.url(self.url):
            return True
        else:
            logging.error(f"Invalid URL provided: {self.url}")
            return False

    def generate(self):
        if not self.validate_url():
            return

        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(self.url)
            qr.make(fit=True)
            img = qr.make_image(fill_color=self.fill_color,
                                back_color=self.back_color)

            with self.path.open('wb') as qr_file:
                img.save(qr_file)
            logging.info(f"saved QR code to {self.path}")

        except Exception as e:
            logging.error(
                f"An error occurred while generating the QR code: {e}")


class DirectoryCreator:
    def __init__(self, path):
        self.path = path

    def create(self):
        try:
            self.path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logging.error(f"Failed to create directory: {e}")
            exit(1)


class Logger:
    @staticmethod
    def setup_logging():
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
            ]
        )


def main():
    parser = argparse.ArgumentParser(description='Generate a QR code.')
    parser.add_argument('--url', help='The URL to encode in the QR code',
                        default='https://github.com/kaw393939')
    args = parser.parse_args()

    Logger.setup_logging()

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    qr_filename = f"QRCode_{timestamp}.png"

    qr_code_full_path = Path.cwd() / QR_DIRECTORY / qr_filename

    DirectoryCreator(Path.cwd() / QR_DIRECTORY).create()

    QRCodeGenerator(args.url, qr_code_full_path,
                    FILL_COLOR, BACK_COLOR).generate()


if __name__ == "__main__":
    main()
