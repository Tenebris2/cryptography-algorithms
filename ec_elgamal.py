import random

from ecc import Point
import ecc

# choose a point


class EllipticElGamal(ecc.EllipticCurve):
    def __init__(self, p, a, b, root_point=None, secret_key=None):
        super().__init__(p, a, b)
        self.root_point = root_point or self.choose_point()
        self.secret_key = secret_key or random.randint(1, p - 1)
        self.public_key = self.self_multiply_generator(root_point, secret_key)

    def choose_point(self):
        return random.choice(self.find_points_on_curve())

    def encrypt(self, message_as_point: ecc.Point):
        """Encrypt a message with"""
        k = random.randint(1, self.p - 1)
        c_1 = self.self_multiply_generator(self.root_point, k)
        c_2 = self.add_points(
            message_as_point, self.self_multiply_generator(self.public_key, k)
        )

        return (c_1, c_2)

    def decrypt(self, c_1: Point, c_2: Point) -> Point:
        return self.subtract_points(
            c_2, self.self_multiply_generator(c_1, self.secret_key)
        )


def main():
    ecgamal = EllipticElGamal(13, 2, 2)

    point_to_encrypt = ecgamal.choose_point()

    print(point_to_encrypt)

    c_1, c_2 = ecgamal.encrypt(point_to_encrypt)

    print(c_1, c_2)

    decrypted_point = ecgamal.decrypt(c_1, c_2)

    print(decrypted_point)


main()
