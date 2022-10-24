"Implements the hashids algorithm in python"

from typing import Any, Union
import string, math, secrets, time

__all__ = [
    "PRMP_AlphaHash",
    "PRMP_PrimeHash",
    "alpha_decode",
    "alpha_encode",
    "prime_decode",
    "prime_encode",
]


class PRMP_AlphaHash:

    """Hashes and restores values using the "hashids" algorithm."""

    ALPHABET = string.ascii_letters + string.digits

    @classmethod
    def _reorder(cls, string: str, salt: str) -> str:
        """Reorders `string` according to `salt`."""
        len_salt = len(salt)

        if len_salt != 0:
            string = list(string)
            index, integer_sum = 0, 0
            for i in range(len(string) - 1, 0, -1):
                integer = ord(salt[index])
                integer_sum += integer
                j = (integer + index + integer_sum) % i
                string[i], string[j] = string[j], string[i]
                index = (index + 1) % len_salt
            string = "".join(string)

        return string

    @classmethod
    def _index_from_ratio(
        cls, dividend: Union[int, float], divisor: Union[int, float]
    ) -> int:
        """Returns the ceiled ratio of two numbers as int."""
        return int(math.ceil(float(dividend) / divisor))

    @classmethod
    def _is_uint(cls, number) -> bool:
        """Returns whether a value is an unsigned integer."""
        try:
            return number == int(number) and number >= 0
        except ValueError:
            return False

    @classmethod
    def _hash(cls, number: int, alphabet: str) -> str:
        """Hashes `number` using the given `alphabet` sequence."""
        hashed = ""
        len_alphabet = len(alphabet)
        while True:
            hashed = alphabet[number % len_alphabet] + hashed
            number //= len_alphabet
            if not number:
                return hashed

    @classmethod
    def _unhash(cls, hashed: str, alphabet: str) -> int:
        """Restores a number tuple from hashed using the given `alphabet` index."""
        number = 0
        len_alphabet = len(alphabet)
        for character in hashed:
            position = alphabet.index(character)
            number *= len_alphabet
            number += position
        return number

    def _split(self, string: str, splitters: Union[str, list, tuple]):
        """Splits a string into parts at multiple characters"""
        part = ""
        for character in string:
            if character in splitters:
                yield part
                part = ""
            else:
                part += character
        yield part

    def _ensure_length(
        self,
        encoded: str,
        min_length: int,
        alphabet: str,
        guards: str,
        values_hash: str,
    ):
        """Ensures the minimal hash length"""
        len_guards = len(guards)
        guard_index = (values_hash + ord(encoded[0])) % len_guards
        encoded = guards[guard_index] + encoded

        if len(encoded) < min_length:
            guard_index = (values_hash + ord(encoded[2])) % len_guards
            encoded += guards[guard_index]

        split_at = len(alphabet) // 2
        while len(encoded) < min_length:
            alphabet = self._reorder(alphabet, alphabet)
            encoded = alphabet[split_at:] + encoded + alphabet[:split_at]
            excess = len(encoded) - min_length
            if excess > 0:
                from_index = excess // 2
                encoded = encoded[from_index : from_index + min_length]

        return encoded

    def __init__(
        self,
        salt: str = "",
        min_length: int = 0,
        alphabet: str = ALPHABET,
        separators: str = "cfhistuCFHISTU",
        separators_ratio: float = 3.5,
        guards_ratio: float = 12,
    ) -> "PRMP_AlphaHash":
        """
        Initializes a PRMP_Hash object with salt, minimum length, and alphabet.

        :param salt: A string influencing the generated hash ids.
        :param min_length: The minimum length for generated hashes
        :param alphabet: The characters to use for the generated hash ids.
        """
        self._min_length = max(int(min_length), 0)
        self._salt = salt

        separators = "".join(x for x in separators if x in alphabet)
        alphabet = "".join(
            x
            for i, x in enumerate(alphabet)
            if alphabet.index(x) == i and x not in separators
        )

        len_alphabet, len_separators = len(alphabet), len(separators)
        if len_alphabet + len_separators < 16:
            raise ValueError("Alphabet must contain at least 16 " "unique characters.")

        separators = self._reorder(separators, salt)

        min_separators = self._index_from_ratio(len_alphabet, separators_ratio)

        number_of_missing_separators = min_separators - len_separators
        if number_of_missing_separators > 0:
            separators += alphabet[:number_of_missing_separators]
            alphabet = alphabet[number_of_missing_separators:]
            len_alphabet = len(alphabet)

        alphabet = self._reorder(alphabet, salt)
        num_guards = self._index_from_ratio(len_alphabet, guards_ratio)
        if len_alphabet < 3:
            guards = separators[:num_guards]
            separators = separators[num_guards:]
        else:
            guards = alphabet[:num_guards]
            alphabet = alphabet[num_guards:]

        self._alphabet = alphabet
        self._guards = guards
        self._separators = separators

    def encode(self, *values: list[int]) -> str:
        """Builds a hash from the passed `values`.

        :param values The values to transform into a hashid

        >>> hashids = PRMP_Hash('arbitrary salt', 16, 'abcdefghijkl0123456')
        >>> hashids.encode(1, 23, 456)
        '1d6216i30h53elk3'
        """
        if not (values and all(self._is_uint(x) for x in values)):
            return ""

        len_alphabet = len(self._alphabet)
        len_separators = len(self._separators)
        values_hash = sum(x % (i + 100) for i, x in enumerate(values))
        encoded = lottery = self._alphabet[values_hash % len(self._alphabet)]

        alphabet = self._alphabet

        for i, value in enumerate(values):
            alphabet_salt = (lottery + self._salt + alphabet)[:len_alphabet]
            alphabet = self._reorder(alphabet, alphabet_salt)
            last = self._hash(value, alphabet)
            encoded += last
            value %= ord(last[0]) + i
            encoded += self._separators[value % len_separators]

        encoded = encoded[:-1]  # cut off last separator

        if len(encoded) < self._min_length:
            len_guards = len(self._guards)
            guard_index = (values_hash + ord(encoded[0])) % len_guards
            encoded = self._guards[guard_index] + encoded

            if len(encoded) < self._min_length:
                guard_index = (values_hash + ord(encoded[2])) % len_guards
                encoded += self._guards[guard_index]

            split_at = len(alphabet) // 2
            while len(encoded) < self._min_length:
                alphabet = self._reorder(alphabet, alphabet)
                encoded = alphabet[split_at:] + encoded + alphabet[:split_at]
                excess = len(encoded) - self._min_length
                if excess > 0:
                    from_index = excess // 2
                    encoded = encoded[from_index : from_index + self._min_length]

        return encoded

    def decode(self, hashid: str) -> tuple:
        """Restore a tuple of numbers from the passed `hashid`.

        :param hashid The hashid to decode

        >>> hashids = PRMP_Hash('arbitrary salt', 16, 'abcdefghijkl0123456')
        >>> hashids.decode('1d6216i30h53elk3')
        (1, 23, 456)
        """
        if not hashid or not isinstance(hashid, str):
            return ()
        try:
            numbers = []
            parts = tuple(self._split(hashid, self._guards))
            raw_hashid = hashid
            hashid = parts[1] if 2 <= len(parts) <= 3 else parts[0]

            if not hashid:
                return

            lottery_char = hashid[0]
            hashid = hashid[1:]

            hash_parts = self._split(hashid, self._separators)
            alphabet = self._alphabet
            for part in hash_parts:
                alphabet_salt = (lottery_char + self._salt + alphabet)[: len(alphabet)]
                alphabet = self._reorder(alphabet, alphabet_salt)
                number = self._unhash(part, alphabet)
                numbers.append(number)

            return tuple(numbers) if raw_hashid == self.encode(*numbers) else ()

        except ValueError:
            return ()

    def encode_hex(self, hex_str: str) -> str:
        """Converts a hexadecimal string (e.g. a MongoDB id) to a hashid.

        :param hex_str The hexadecimal string to encodes

        >>> PRMP_Hash.encode_hex('507f1f77bcf86cd799439011')
        'y42LW46J9luq3Xq9XMly'
        """
        numbers = (
            int("1" + hex_str[i : i + 12], 16) for i in range(0, len(hex_str), 12)
        )
        try:
            return self.encode(*numbers)
        except ValueError:
            return ""

    def decode_hex(self, hashid: str) -> str:
        """Restores a hexadecimal string (e.g. a MongoDB id) from a hashid.

        :param hashid The hashid to decode

        >>> PRMP_Hash.decode_hex('y42LW46J9luq3Xq9XMly')
        '507f1f77bcf86cd799439011'
        """
        return "".join(("%x" % x)[1:] for x in self.decode(hashid))


def alpha_encode(salt: str, values: Any, **kwargs) -> str:
    if isinstance(values, (bytes, str)):
        values = [ord(v) for v in values]
        print(values)
    return PRMP_AlphaHash(salt=salt, **kwargs).encode(*values)


def alpha_decode(
    salt: str, values: Any, as_str=False, **kwargs
) -> Union[tuple[int], str]:
    values = PRMP_AlphaHash(salt=salt, **kwargs).decode(values)
    if as_str:
        values = "".join(chr(v) for v in values)
    return values


class PRMP_PrimeHash:
    MAX_64_INT = 2 ** 63 - 1
    MAX_32_INT = 2 ** 31 - 1

    def __init__(
        self, prime: int, inverse: int = None, random: int = None, bitlength: int = 64
    ) -> "PRMP_PrimeHash":

        assert bitlength in (32, 64), "bitlength can only be 32 or 64"

        self.max_int = bitlength == 32 and self.MAX_32_INT or self.MAX_64_INT
        self.prime = prime
        self.inverse = inverse or self.mod_inverse(prime, self.max_int)
        self.random = random or self.rand_n(self.max_int - 1)

    def encode(self, n: int) -> int:
        return ((int(n) * self.prime) & self.max_int) ^ self.random

    def decode(self, n: int) -> int:
        return ((int(n) ^ self.random) * self.inverse) & self.max_int

    def mod_inverse(self, n: int, p: int) -> int:
        return pow(n, -1, p + 1)

    def rand_n(self, n: int) -> int:
        return secrets.randbelow(n) + 1


def prime_encode(prime: int, values: Any, **kwargs) -> int:
    if isinstance(values, (bytes, str)):
        values = [ord(v) for v in values]

    return PRMP_PrimeHash(prime, **kwargs).encode(values)


def prime_decode(prime: int, coded: int, **kwargs) -> int:
    return PRMP_PrimeHash(prime, **kwargs).decode(coded)


if __name__ == "__main__":
    ph = PRMP_AlphaHash("arbitrary salt", 16, "abcdefghijkl0123456")
    en = ph.encode(1, 23, 456)
    de = ph.decode(en)
    print(en, de, ph._alphabet)

    print()

    prime_hash = PRMP_PrimeHash(prime=7)
    id = time.time()
    hashed_id = prime_hash.encode(id)
    unhashed_id = prime_hash.decode((hashed_id))
    print(id, hashed_id, unhashed_id)
print(chr(0))
