from mpmath.libmp.libmpf import math
from sympy import isprime, factorint, mod_inverse, randprime, sqrt
from helper import generate_prime
import gmpy2
from concurrent.futures import ThreadPoolExecutor
import random
from hashlib import sha256


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


class EllipticCurve:
    def __init__(self, p, a, b):
        self.p = p  # Prime modulus
        self.a = a
        self.b = b

    def subtract_points(self, P, Q):
        """Subtract point Q from point P on the elliptic curve."""
        # To subtract Q, add the inverse of Q
        Q_inverse = Point(Q.x, -Q.y % self.p)
        return self.add_points(P, Q_inverse)

    def add_points(self, P: Point, Q: Point):
        """Add two points P and Q on the elliptic curve."""
        if P is None:
            return Q
        if Q is None:
            return P

        # Convert points to gmpy2.mpz
        P_x = gmpy2.mpz(P.x)
        P_y = gmpy2.mpz(P.y)
        Q_x = gmpy2.mpz(Q.x)
        Q_y = gmpy2.mpz(Q.y)

        if P_x == Q_x and P_y == Q_y:
            # Use precomputed inverses if available or memoize them
            inv_2P_y = gmpy2.invert(2 * P_y, self.p)
            m = (3 * P_x**2 + self.a) * inv_2P_y % self.p
        else:
            inv_Qx_minus_Px = gmpy2.invert(Q_x - P_x, self.p)
            m = (Q_y - P_y) * inv_Qx_minus_Px % self.p

        x_r = (m**2 - P_x - Q_x) % self.p
        y_r = (m * (P_x - x_r) - P_y) % self.p

        return Point(int(x_r), int(y_r))

    def batch_add_points(self, points):
        """Batch add multiple points for better performance."""
        result = None
        for point in points:
            result = self.add_points(result, point)
        return result

    def find_points_on_curve(self, x_start, x_end):
        points = []
        for x in range(x_start, x_end):
            rhs = (
                x**3 + self.a * x + self.b
            ) % self.p  # Right-hand side of the curve equation
            # Check if rhs is a quadratic residue
            if pow(rhs, (self.p - 1) // 2, self.p) == 1:
                # rhs is a quadratic residue, so we can find y
                y = modular_square_root(rhs, self.p)
                if y == None:
                    continue
                points.append(Point(x, y))
                # Add the negative y as well since it's also a point on the curve
                break
                points.append(Point(x, self.p - y))

        return points

    def find_points_on_curve_parallel(self, points, num_threads=32):
        segment_size = self.p // num_threads
        x_segments = [
            (i * segment_size, (i + 1) * segment_size) for i in range(num_threads)
        ]

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(self.find_points_on_curve, x_start, x_end)
                for x_start, x_end in x_segments
            ]
            for future in futures:
                points.extend(future.result())
        return points

    def find(self):
        """Find parameters (a, b) such that the number of points on the elliptic curve is prime."""
        for a in range(1, self.p):
            for b in range(1, self.p):
                points = self.find_points_on_curve_parallel()
                if isprime(len(points)):
                    return (self.a, self.b), len(points)
        return None, []  # Return None if no such (a, b) is found

    def scalar_multiply(self, k, P):
        """Multiply the point by the multiplier k using the double-and-add method."""
        if P is None:
            raise ValueError("Point not set for multiplication.")

        result = Point(0, 0)  # Initialize result as the point at infinity
        addend = P  # Use the internal point for multiplication

        while k:
            if k & 1:  # If k is odd
                result = self.add_points(result, addend)  # Using '1' for a
            addend = self.add_points(addend, addend)  # Double the point
            k >>= 1  # Divide k by 2

        return result

    def self_multiply_generator_v2(self, point, n):
        """Multiply the generator point by an integer n using an efficient method."""
        print(f"First point on the curve: {point}")

        # Start with the point itself
        current_point = point
        points = [current_point]  # Initialize the list of points

        # Calculate the first few points using doubling
        for _ in range(1, n):
            current_point = self.add_points(current_point, point)  # P + P, 2P, 3P, ...
            points.append(current_point)

        print("Calculated points:")
        for i, pt in enumerate(points):
            print(f"P[{i}] = {pt}")

        return points[-1]  # Return the nth point

    # def self_multiply_generator(self, point, n):
    #     diem_sinh = point
    #     print(f"first point on the curve: {diem_sinh}")
    #     p_1 = diem_sinh  # first point
    #     print(f"p1 = {p_1}")
    #
    #     # calculate the second point
    #     p_2 = self.add_points(p_1, p_1)
    #     print(f"p2 = {p_2}")
    #
    #     # calculate further points
    #     temp = p_2
    #     for i in range(3, n + 1):
    #         temp = self.add_points(temp, p_1)
    #     return temp

    def set_point(self, point, k):
        """Set the point and multiplier for multiplication."""
        self.point = point
        self.k = k


def modular_square_root(a, p):
    # Tonelli-Shanks algorithm for finding a square root modulo p
    if pow(a, (p - 1) // 2, p) != 1:
        return None  # No square root exists if not a quadratic residue
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    # Implement the general Tonelli-Shanks here for other cases
    # (the full implementation is a bit longer)


# Thông số của đường cong elliptic


def main():

    p = 2**255 - 19
    a, b = 486662, 1  # Curve parameters
    print(f"Parameters: a = {a}, b = {b}, p = {p}")

    curve = EllipticCurve(p, a, b)
    # generator_point_x = 9
    # generator_point_y = (
    #     int(
    #         math.sqrt(
    #             generator_point_x**3 + b * generator_point_x**2 + generator_point_x
    #         )
    #     )
    # ) % p
    points = []
    curve.find_points_on_curve_parallel(points)
    # print(points)
    print(curve.scalar_multiply(10**10, points[0]))


class ECDSA(EllipticCurve):
    def __init__(self, p, a, b):
        super().__init__(p, a, b)


# def ecdsa_sig(msg, private_key):
#     z = sha256(msg)
#     while True:
#         k = random.randint(1, N - 1)
#         R = elliptic_multiply(k, G)
#         r = R[0] % N
#         if r == 0:
#             continue
#         s = (pow(k, -1, N) * (z + r * private_key)) % N
#         if s != 0:
#             break
#     return (r, s)


# def ecdsa_ver(msg, signature, public_key):
#     r, s = signature
#     if not (1 <= r < N and 1 <= s < N):
#         return False
#     z = sha256(msg)
#     w = pow(s, -1, N)
#     u1 = (z * w) % N
#     u2 = (r * w) % N
#     P = elliptic_add(elliptic_multiply(u1, G), elliptic_multiply(u2, public_key))
#     return P[0] % N == r
#
#
# # Hàm mã hóa ElGamal
# def ec_elgamal_encrypt(Pm, Q):
#     k = random.randint(1, N - 1)
#     C1 = elliptic_multiply(k, G)
#     C2 = elliptic_add(Pm, elliptic_multiply(k, Q))
#     return (C1, C2)
#
#
# def ec_elgamal_decrypt(C, d):
#     C1, C2 = C
#     Pm = elliptic_add(C2, elliptic_multiply(-d, C1))
#     return Pm


# main()
