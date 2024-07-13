import base64


class URLSafe:
    @staticmethod
    def add_padding(data_string: str) -> str:
        return data_string + "=" * (-len(data_string) % 4)

    @staticmethod
    def del_padding(data_string: str) -> str:
        return data_string.rstrip("=")

    def encode_data(self, data_integer: int) -> str:
        encoded_data = base64.urlsafe_b64encode(data_integer.encode("utf-8"))
        return self.del_padding(encoded_data.decode("utf-8"))

    def decode_data(self, data_string: str) -> str:
        data_padding = self.add_padding(data_string)
        encoded_data = base64.urlsafe_b64decode(data_padding)
        return encoded_data.decode("utf-8")


url_safe: URLSafe = URLSafe()
