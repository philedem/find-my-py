import random
import time
import bluetooth
from cryptography.hazmat.primitives.asymmetric import ec

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
    private_key = ec.generate_private_key(ec.SECP224R1())
    public_key = private_key.public_key()
    return private_key, public_key

# Check if a public key is valid
def is_valid_pubkey(pub_key_compressed):
    # Implement ECC public key validation as needed
    return True  # You'll need to replace this with actual validation

# Set address from public key
def set_addr_from_key(public_key):
    # Implement address derivation from the public key
    pass

# Set payload from public key
def set_payload_from_key(public_key):
    # Implement payload derivation from the public key
    pass

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
    print("Data to send (msg_id: {}): {}".format(msg_id, data_to_send))
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
