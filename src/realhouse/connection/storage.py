"""
Secure credential storage for dubai_real_estate connections.

This module handles secure storage and retrieval of connection credentials
in the user's filesystem with proper encryption and access controls.
"""

import json
import os
import stat
from pathlib import Path
from typing import Dict, List, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import getpass

from .types import AnyCredentials, ConnectionType, create_credentials


class CredentialStorage:
    """Secure storage manager for connection credentials.

    Stores encrypted credentials in user's home directory with proper
    file permissions and encryption.
    """

    def __init__(self, storage_dir: Optional[Path] = None):
        """Initialize credential storage.

        Args:
            storage_dir: Directory to store credentials. If None, uses
                        ~/.dubai_real_estate/connections/

        Example:
            >>> storage = CredentialStorage()
            >>> # Credentials stored in ~/.dubai_real_estate/connections/
        """
        if storage_dir is None:
            storage_dir = Path.home() / ".dubai_real_estate" / "connections"

        self.storage_dir = Path(storage_dir)
        self.credentials_file = self.storage_dir / "credentials.enc"
        self.key_file = self.storage_dir / ".key"
        self.auto_connection_file = self.storage_dir / "auto_connection"

        # Create storage directory with secure permissions
        self._ensure_storage_directory()

        # Initialize encryption key
        self._encryption_key = self._get_or_create_key()

    def _ensure_storage_directory(self) -> None:
        """Create storage directory with secure permissions."""
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Set directory permissions to be readable/writable only by owner
        os.chmod(self.storage_dir, stat.S_IRWXU)  # 700

    def _get_or_create_key(self) -> bytes:
        """Get or create encryption key for credentials.

        Returns:
            Encryption key bytes
        """
        if self.key_file.exists():
            return self._load_key()
        else:
            return self._create_key()

    def _create_key(self) -> bytes:
        """Create new encryption key.

        Returns:
            New encryption key bytes
        """
        # Use a simple key derivation for now
        # In production, you might want to use a master password
        password = f"dubai_real_estate-{getpass.getuser()}".encode()
        salt = os.urandom(16)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))

        # Store salt and key
        key_data = {"salt": base64.b64encode(salt).decode(), "key": key.decode()}

        self.key_file.write_text(json.dumps(key_data))
        os.chmod(self.key_file, stat.S_IRUSR | stat.S_IWUSR)  # 600

        return key

    def _load_key(self) -> bytes:
        """Load existing encryption key.

        Returns:
            Existing encryption key bytes
        """
        key_data = json.loads(self.key_file.read_text())
        return key_data["key"].encode()

    def _encrypt_data(self, data: str) -> str:
        """Encrypt data using stored key.

        Args:
            data: Data to encrypt

        Returns:
            Encrypted data as base64 string
        """
        f = Fernet(self._encryption_key)
        encrypted = f.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()

    def _decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt data using stored key.

        Args:
            encrypted_data: Encrypted data as base64 string

        Returns:
            Decrypted data string
        """
        f = Fernet(self._encryption_key)
        encrypted_bytes = base64.b64decode(encrypted_data.encode())
        return f.decrypt(encrypted_bytes).decode()

    def save_credentials(self, credentials: AnyCredentials) -> None:
        """Save credentials to secure storage.

        Args:
            credentials: Credentials object to save

        Example:
            >>> from dubai_real_estate.connection.types import ClientCredentials
            >>> creds = ClientCredentials(
            ...     name="prod",
            ...     host="localhost",
            ...     username="user",
            ...     password="secret"
            ... )
            >>> storage.save_credentials(creds)
        """
        # Load existing credentials
        all_credentials = self._load_all_credentials()

        # Convert credentials to dict
        creds_dict = self._credentials_to_dict(credentials)

        # Update credentials
        all_credentials[credentials.name] = creds_dict

        # Save encrypted credentials
        encrypted_data = self._encrypt_data(json.dumps(all_credentials))
        self.credentials_file.write_text(encrypted_data)
        os.chmod(self.credentials_file, stat.S_IRUSR | stat.S_IWUSR)  # 600

        # Update auto connection if needed
        if credentials.is_auto:
            self._set_auto_connection(credentials.name)

    def load_credentials(self, name: str) -> Optional[AnyCredentials]:
        """Load credentials by name.

        Args:
            name: Name of the connection

        Returns:
            Credentials object or None if not found

        Example:
            >>> creds = storage.load_credentials("prod")
            >>> if creds:
            ...     print(f"Host: {creds.host}")
        """
        all_credentials = self._load_all_credentials()

        if name not in all_credentials:
            return None

        creds_dict = all_credentials[name]
        return self._dict_to_credentials(creds_dict)

    def list_connections(self) -> List[str]:
        """List all available connection names.

        Returns:
            List of connection names

        Example:
            >>> connections = storage.list_connections()
            >>> print("Available connections:", connections)
        """
        all_credentials = self._load_all_credentials()
        return list(all_credentials.keys())

    def delete_credentials(self, name: str) -> bool:
        """Delete credentials by name.

        Args:
            name: Name of the connection to delete

        Returns:
            True if deleted, False if not found

        Example:
            >>> success = storage.delete_credentials("old_connection")
            >>> print(f"Deleted: {success}")
        """
        all_credentials = self._load_all_credentials()

        if name not in all_credentials:
            return False

        del all_credentials[name]

        # Save updated credentials
        encrypted_data = self._encrypt_data(json.dumps(all_credentials))
        self.credentials_file.write_text(encrypted_data)

        # Clear auto connection if this was it
        if self.get_auto_connection() == name:
            self._clear_auto_connection()

        return True

    def get_auto_connection(self) -> Optional[str]:
        """Get the name of the auto connection.

        Returns:
            Name of auto connection or None

        Example:
            >>> auto_conn = storage.get_auto_connection()
            >>> if auto_conn:
            ...     print(f"Auto connection: {auto_conn}")
        """
        if not self.auto_connection_file.exists():
            return None

        return self.auto_connection_file.read_text().strip()

    def set_auto_connection(self, name: str) -> bool:
        """Set a connection as the auto connection.

        Args:
            name: Name of the connection to set as auto

        Returns:
            True if successful, False if connection doesn't exist

        Example:
            >>> success = storage.set_auto_connection("prod")
            >>> print(f"Set auto connection: {success}")
        """
        # Check if connection exists
        if not self.load_credentials(name):
            return False

        return self._set_auto_connection(name)

    def _set_auto_connection(self, name: str) -> bool:
        """Internal method to set auto connection."""
        self.auto_connection_file.write_text(name)
        os.chmod(self.auto_connection_file, stat.S_IRUSR | stat.S_IWUSR)  # 600
        return True

    def _clear_auto_connection(self) -> None:
        """Clear the auto connection setting."""
        if self.auto_connection_file.exists():
            self.auto_connection_file.unlink()

    def _load_all_credentials(self) -> Dict[str, Dict]:
        """Load all credentials from storage.

        Returns:
            Dictionary of all credentials
        """
        if not self.credentials_file.exists():
            return {}

        try:
            encrypted_data = self.credentials_file.read_text()
            decrypted_data = self._decrypt_data(encrypted_data)
            return json.loads(decrypted_data)
        except Exception:
            # If decryption fails, return empty dict
            return {}

    def _credentials_to_dict(self, credentials: AnyCredentials) -> Dict:
        """Convert credentials object to dictionary.

        Args:
            credentials: Credentials object

        Returns:
            Dictionary representation
        """
        result = {
            "name": credentials.name,
            "connection_type": credentials.connection_type.value,
            "description": credentials.description,
            "is_auto": credentials.is_auto,
        }

        if credentials.connection_type == ConnectionType.CHDB:
            result.update({"database_path": credentials.database_path})
        elif credentials.connection_type == ConnectionType.CLIENT:
            result.update(
                {
                    "host": credentials.host,
                    "port": credentials.port,
                    "username": credentials.username,
                    "password": credentials.password,
                    "database": credentials.database,
                    "secure": credentials.secure,
                    "interface": credentials.interface,
                    "compress": credentials.compress,
                    "connect_timeout": credentials.connect_timeout,
                    "send_receive_timeout": credentials.send_receive_timeout,
                    "session_id": credentials.session_id,
                }
            )

        return result

    def _dict_to_credentials(self, data: Dict) -> AnyCredentials:
        """Convert dictionary to credentials object.

        Args:
            data: Dictionary representation

        Returns:
            Credentials object
        """
        connection_type = data["connection_type"]

        # Remove common fields from data for **kwargs
        creds_data = data.copy()
        creds_data.pop("connection_type")

        return create_credentials(connection_type=connection_type, **creds_data)


# Global storage instance
_storage = None


def get_storage() -> CredentialStorage:
    """Get global credential storage instance.

    Returns:
        Global CredentialStorage instance

    Example:
        >>> storage = get_storage()
        >>> connections = storage.list_connections()
    """
    global _storage
    if _storage is None:
        _storage = CredentialStorage()
    return _storage
