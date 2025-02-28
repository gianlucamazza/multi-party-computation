import unittest
from security.secure_channel import SecureChannel

class TestSecureChannel(unittest.TestCase):
    def setUp(self):
        # Create two secure channels for testing
        self.channel_a = SecureChannel()
        self.channel_b = SecureChannel()
        
    def test_key_exchange(self):
        """Test that symmetric keys can be exchanged securely."""
        # Set public keys
        self.channel_a.set_partner_public_key(self.channel_b.get_public_key())
        self.channel_b.set_partner_public_key(self.channel_a.get_public_key())
        
        # Exchange keys
        encrypted_key_a = self.channel_a.exchange_symmetric_key()
        encrypted_key_b = self.channel_b.exchange_symmetric_key()
        
        # Receive keys
        self.channel_a.receive_symmetric_key(encrypted_key_b)
        self.channel_b.receive_symmetric_key(encrypted_key_a)
        
        # Verify keys are set
        self.assertIsNotNone(self.channel_a.partner_symmetric_key)
        self.assertIsNotNone(self.channel_b.partner_symmetric_key)
        
    def test_encryption_decryption(self):
        """Test that messages can be encrypted and decrypted."""
        # Test basic encryption/decryption with own key
        test_message = b"Hello, secure world!"
        encrypted = self.channel_a.encrypt(test_message)
        decrypted = self.channel_a.decrypt(encrypted)
        
        self.assertNotEqual(encrypted, test_message)  # Encryption should change the message
        self.assertEqual(decrypted, test_message)     # Decryption should restore it
        
    def test_partner_communication(self):
        """Test that partners can communicate securely."""
        # Set up secure channels
        self.channel_a.set_partner_public_key(self.channel_b.get_public_key())
        self.channel_b.set_partner_public_key(self.channel_a.get_public_key())
        
        # Exchange keys
        encrypted_key_a = self.channel_a.exchange_symmetric_key()
        encrypted_key_b = self.channel_b.exchange_symmetric_key()
        
        # Receive keys
        self.channel_a.receive_symmetric_key(encrypted_key_b)
        self.channel_b.receive_symmetric_key(encrypted_key_a)
        
        # Test partner encryption/decryption
        test_message = b"Secret message from A to B"
        
        # A encrypts a message for B
        encrypted_for_b = self.channel_a.encrypt_for_partner(test_message)
        
        # B decrypts the message from A
        decrypted_by_b = self.channel_b.decrypt(encrypted_for_b)
        
        self.assertEqual(decrypted_by_b, test_message)
        
        # Test in the other direction
        test_message_2 = b"Secret message from B to A"
        
        # B encrypts a message for A
        encrypted_for_a = self.channel_b.encrypt_for_partner(test_message_2)
        
        # A decrypts the message from B
        decrypted_by_a = self.channel_a.decrypt(encrypted_for_a)
        
        self.assertEqual(decrypted_by_a, test_message_2)
        
    def test_error_handling(self):
        """Test error handling for invalid operations."""
        # Test setting partner key is required
        channel_c = SecureChannel()
        with self.assertRaises(ValueError):
            channel_c.exchange_symmetric_key()
            
        # Test type checking for messages
        with self.assertRaises(TypeError):
            self.channel_a.encrypt("not bytes")  # Should be bytes
            
        # Test trying to use partner encryption before key exchange
        channel_d = SecureChannel()
        test_message = b"This won't work"
        with self.assertRaises(ValueError):
            channel_d.encrypt_for_partner(test_message)
            
if __name__ == '__main__':
    unittest.main()