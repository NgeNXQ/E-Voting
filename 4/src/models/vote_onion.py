import rsa

class VoteOnion:

    def __init__(self, candidate_id: int, initial_buffer_noise: bytes) -> 'VoteOnion':
        self._signature = None
        self._layers_count: int = 1
        self._layers_with_noise: list[int] = list()
        self._buffer_noise_size_bytes = len(initial_buffer_noise)
        self._buffer: bytes = candidate_id.to_bytes() + initial_buffer_noise

    def get_buffer(self) -> bytes:
        return self._buffer

    def get_layers_count(self) -> int:
        return self._layers_count

    def get_signature(self) -> bytes:
        return self._signature

    def set_signature(self, value: bytes) -> None:
        self._signature = value

    def pop_layer(self, rsa_private_key: rsa.PrivateKey) -> bytes:
        if rsa_private_key is None:
            raise ValueError("rsa_private_key cannot be None")

        self._layers_count -= 1
        self._buffer = rsa.decrypt(self._buffer, rsa_private_key)

        if self._layers_count in self._layers_with_noise:
            self._layers_with_noise.remove(self._layers_count)
            self._buffer = self._buffer[:-self._buffer_noise_size_bytes]

        return self._buffer

    def push_layer(self, rsa_public_key: rsa.PublicKey, buffer_payload: bytes = None) -> None:
        if rsa_public_key is None:
            raise ValueError("rsa_public_key cannot be None")

        if buffer_payload is not None:
            self._buffer += buffer_payload
            self._layers_with_noise.append(self._layers_count)

        self._layers_count += 1
        self._buffer = rsa.encrypt(self._buffer, rsa_public_key)

    def remove_initial_noise(self) -> None:
        self._buffer = self._buffer[:-self._buffer_noise_size_bytes]