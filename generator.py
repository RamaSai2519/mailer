import boto3
import qrcode
from config import *
from io import BytesIO


class CodeGenerator:
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        self.s3_client = boto3.client(
            "s3",
            region_name=aws_region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key
        )
        self.bucket_name = 'githubmedia'

    def generate_qr_code(self, key: str) -> BytesIO:
        qr = qrcode.QRCode(
            version=1, box_size=10, border=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L
        )
        qr.add_data(key)
        qr.make(fit=True)

        qr_image = qr.make_image(
            fill_color="black", back_color="white").convert('RGBA')

        qr_image_data = qr_image.getdata()
        new_image_data = []
        for item in qr_image_data:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                new_image_data.append((255, 255, 255, 0))
            else:
                new_image_data.append(item)
        qr_image.putdata(new_image_data)

        qr_buffer = BytesIO()
        qr_image.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)
        return qr_buffer

    def save_qr_code_as_image(self) -> str:
        qr_code_img = self.generate_qr_code(self.user_id)
        filename = f"prerana_codes/{self.user_id}.png"
        file_url = self.upload_to_s3(qr_code_img, filename)

        return file_url

    def upload_to_s3(self, file_buffer: BytesIO, file_name: str) -> str:
        endpoint_url = self.s3_client.meta.endpoint_url
        file_url = f"{endpoint_url}/{self.bucket_name}/{file_name}"

        self.s3_client.upload_fileobj(
            file_buffer,
            self.bucket_name,
            file_name,
            ExtraArgs={"ACL": "public-read", "ContentType": "image/png"}
        )
        return file_url
