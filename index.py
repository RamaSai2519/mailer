from config import prusers_collection
from generator import CodeGenerator
from emailer import EmailSender


class Compute:
    def __init__(self) -> None:
        pass

    def get_users(self) -> list:
        query = {'email': 'ktummala@gitam.in'}
        users = list(prusers_collection.find(query))
        return users

    def generate_barcode(self, user_id: str) -> bytes:
        code_gen = CodeGenerator(user_id)
        barcode_filename = code_gen.save_qr_code_as_image()
        print(barcode_filename)
        return barcode_filename

    def compute(self) -> None:
        users = self.get_users()
        for user in users:
            barcode_filename = self.generate_barcode(str(user['_id']))
            email_sender = EmailSender(barcode_filename)
            email_sender.send_email(user, user['email'])


if __name__ == '__main__':
    Compute().compute()
