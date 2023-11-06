import random
import time
from ecdsa import SigningKey, SECP224R1

# Set custom modem id
modem_id = 0x42424242

# Advertisement payload
adv_data = [
    0x1e,  # Length (30)
    0xff,  # Manufacturer Specific Data (type 0xff)
    0x4c, 0x00,  # Company ID (Apple)
    0x12, 0x19,  # Offline Finding type and length
    0x00,  # State
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00,  # First two bits
    0x00,  # Hint (0x00)
]

# Set random device address
rnd_addr = [0xFF, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]

# Generate a valid public key
def generate_public_key():
    sk = SigningKey.generate(curve=SECP224R1)
    vk = sk.get_verifying_key()
    return sk.to_string(), vk.to_string()

# Check if a public key is valid
def is_valid_pubkey(public_key_bytes):
    try:
        vk = VerifyingKey.from_string(public_key_bytes, curve=SECP224R1)
        return True
    except:
        return False

# Set address from public key
def set_addr_from_key(public_key):
    rnd_addr[0] = public_key[0] | 0b11000000
    rnd_addr[1] = public_key[1]
    rnd_addr[2] = public_key[2]
    rnd_addr[3] = public_key[3]
    rnd_addr[4] = public_key[4]
    rnd_addr[5] = public_key[5]

# Set payload from public key
def set_payload_from_key(public_key):
    adv_data[7:29] = public_key[6:]
    adv_data[29] = public_key[0] >> 6

# Advertisement parameters
adv_params = {
    'interval_min': 0x0640,
    'interval_max': 0x0C80,
    'type': 'ADV_NONCONN_IND',
}

# Function to reset advertising
def reset_advertising():
    # You would implement this function in Python based on your needs
    pass

# Function to send data once blocking
def send_data_once_blocking(data_to_send, msg_id):
    print("Data to send (msg_id: {}): {}".format(msg_id, data_to_send.decode('utf-8')))
    current_bit = 0

    for by_i in range(len(data_to_send)):
        for bi_i in range(8):
            if (data_to_send[by_i] >> bi_i) & 0x01:
                current_bit = 1
            else:
                current_bit = 0

            print("Sending byte {}, bit {}: {}".format(by_i, bi_i, current_bit))
            private_key, public_key = generate_public_key()

            while not is_valid_pubkey(public_key):
                private_key, public_key = generate_public_key()

            print("Generated public key: {}".format(public_key))
            set_addr_from_key(public_key)
            set_payload_from_key(public_key)
            reset_advertising()
            time.sleep(0.002)

# Main function
def main():
    current_message_id = 0

    data_to_send = b"TEST MESSAGE"

    print("Sending initial default message: {}".format(data_to_send.decode('utf-8')))

    send_data_once_blocking(data_to_send, current_message_id)

    print("Entering serial modem mode")

    #while True:
        # Implement the UART read and line processing here
        # You would read lines from the UART and send them using send_data_once_blocking

if __name__ == "__main__":
    main()
