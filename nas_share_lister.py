#!/usr/bin/env python3
"""
NAS Share Lister - Interactive CLI tool to discover and export NFS and SMB shares
"""

import os
import sys
import csv
import subprocess
import socket
from datetime import datetime
from pathlib import Path
import getpass
import ipaddress

try:
    from smb.SMBConnection import SMBConnection
except ImportError:
    print("SMB libraries not found. Please install requirements: pip install pysmb")
    sys.exit(1)


class NASShareLister:
    def __init__(self):
        self.nas_ip = None
        self.username = None
        self.password = None
        self.destination = None
        self.output_folder = None
        
    def get_user_input(self):
        """Collect user input for NAS connection and output settings"""
        print("=== NAS Share Lister ===\n")
        
        # Get NAS IP
        while True:
            self.nas_ip = input("Enter NAS IP address: ").strip()
            if self.validate_ip(self.nas_ip):
                break
            print("Invalid IP address. Please try again.")
        
        # Get credentials
        self.username = input("Enter username: ").strip()
        self.password = getpass.getpass("Enter password: ")
        
        # Get destination folder
        default_dest = os.path.expanduser("~/Desktop")
        dest_input = input(f"Enter destination folder (default: {default_dest}): ").strip()
        self.destination = dest_input if dest_input else default_dest
        
        # Create timestamped output folder
        timestamp = datetime.now().strftime("%d%m%y__%H%M")
        folder_name = f"{timestamp}_NAS_shares-export"
        self.output_folder = os.path.join(self.destination, folder_name)
        
        print(f"\nOutput will be saved to: {self.output_folder}")
        
    def validate_ip(self, ip):
        """Validate IP address format"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    def test_connection(self):
        """Test basic connectivity to the NAS"""
        print(f"\nTesting connection to {self.nas_ip}...")
        
        # Test basic connectivity
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        try:
            # Test SMB port (445)
            result = sock.connect_ex((self.nas_ip, 445))
            if result == 0:
                print("✓ SMB port (445) is accessible")
                return True
            else:
                print("✗ SMB port (445) is not accessible")
                return False
        except Exception as e:
            print(f"✗ Connection test failed: {e}")
            return False
        finally:
            sock.close()
    
    def discover_smb_shares(self):
        """Discover SMB shares on the NAS"""
        print("\nDiscovering SMB shares...")
        smb_shares = []
        
        try:
            # Create SMB connection
            conn = SMBConnection(self.username, self.password, "client", "server", use_ntlm_v2=True)
            
            if conn.connect(self.nas_ip, 445):
                print("✓ SMB connection established")
                
                # List shares
                shares = conn.listShares()
                
                for share in shares:
                    if not share.isSpecial and not share.isTemporary:
                        share_info = {
                            'share_name': share.name,
                            'share_path': f"\\\\{self.nas_ip}\\{share.name}",
                            'share_type': self.get_share_type(share),
                            'comments': share.comments or '',
                            'is_hidden': share.name.endswith('$')
                        }
                        smb_shares.append(share_info)
                        print(f"  Found: {share.name}")
                
                conn.close()
                
            else:
                print("✗ Failed to establish SMB connection")
                
        except Exception as e:
            print(f"✗ SMB discovery failed: {e}")
            
        return smb_shares
    
    def get_share_type(self, share):
        """Determine share type from SMB share object"""
        if hasattr(share, 'type'):
            # Map share type numbers to readable names
            type_map = {
                0: "Disk",
                1: "Print Queue", 
                2: "Device",
                3: "IPC"
            }
            return type_map.get(share.type, f"Type {share.type}")
        return "Disk"  # Default to disk share
    
    def discover_nfs_shares(self):
        """Discover NFS shares using showmount command"""
        print("\nDiscovering NFS shares...")
        nfs_shares = []
        
        try:
            # Use showmount command to list NFS exports
            result = subprocess.run(
                ['showmount', '-e', self.nas_ip],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("✓ NFS exports retrieved")
                lines = result.stdout.strip().split('\n')
                
                # Skip header line if present
                if lines and 'Export list' in lines[0]:
                    lines = lines[1:]
                
                for line in lines:
                    if line.strip():
                        parts = line.strip().split()
                        if parts:
                            export_path = parts[0]
                            clients = ' '.join(parts[1:]) if len(parts) > 1 else 'everyone'
                            
                            share_info = {
                                'share_name': os.path.basename(export_path) or export_path,
                                'share_path': export_path,
                                'share_type': 'NFS Export',
                                'allowed_clients': clients,
                                'full_path': f"{self.nas_ip}:{export_path}"
                            }
                            nfs_shares.append(share_info)
                            print(f"  Found: {export_path}")
            else:
                print(f"✗ showmount failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("✗ NFS discovery timed out")
        except FileNotFoundError:
            print("✗ showmount command not found. Install nfs-common package.")
        except Exception as e:
            print(f"✗ NFS discovery failed: {e}")
            
        return nfs_shares
    
    def create_output_folder(self):
        """Create the output folder"""
        try:
            os.makedirs(self.output_folder, exist_ok=True)
            print(f"\n✓ Created output folder: {self.output_folder}")
            return True
        except Exception as e:
            print(f"✗ Failed to create output folder: {e}")
            return False
    
    def save_smb_shares(self, smb_shares):
        """Save SMB shares to CSV file"""
        csv_file = os.path.join(self.output_folder, "smb-shares.csv")
        
        try:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                if smb_shares:
                    fieldnames = ['share_name', 'share_path', 'share_type', 'comments', 'is_hidden']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(smb_shares)
                else:
                    # Write empty file with headers
                    writer = csv.writer(f)
                    writer.writerow(['share_name', 'share_path', 'share_type', 'comments', 'is_hidden'])
                    
            print(f"✓ SMB shares saved to: smb-shares.csv ({len(smb_shares)} shares)")
            return True
            
        except Exception as e:
            print(f"✗ Failed to save SMB shares: {e}")
            return False
    
    def save_nfs_shares(self, nfs_shares):
        """Save NFS shares to CSV file"""
        csv_file = os.path.join(self.output_folder, "nfs-shares.csv")
        
        try:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                if nfs_shares:
                    fieldnames = ['share_name', 'share_path', 'share_type', 'allowed_clients', 'full_path']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(nfs_shares)
                else:
                    # Write empty file with headers
                    writer = csv.writer(f)
                    writer.writerow(['share_name', 'share_path', 'share_type', 'allowed_clients', 'full_path'])
                    
            print(f"✓ NFS shares saved to: nfs-shares.csv ({len(nfs_shares)} shares)")
            return True
            
        except Exception as e:
            print(f"✗ Failed to save NFS shares: {e}")
            return False
    
    def open_file_manager(self):
        """Open file manager to the output folder"""
        try:
            if sys.platform.startswith('linux'):
                subprocess.run(['xdg-open', self.output_folder])
            elif sys.platform == 'darwin':
                subprocess.run(['open', self.output_folder])
            elif sys.platform == 'win32':
                subprocess.run(['explorer', self.output_folder])
            else:
                print(f"Please manually open: {self.output_folder}")
        except Exception as e:
            print(f"Could not open file manager: {e}")
            print(f"Please manually open: {self.output_folder}")
    
    def run(self):
        """Main execution flow"""
        try:
            # Get user input
            self.get_user_input()
            
            # Test connection
            if not self.test_connection():
                print("\n✗ Cannot connect to NAS. Please check IP address and network connectivity.")
                return False
            
            # Create output folder
            if not self.create_output_folder():
                return False
            
            # Discover shares
            smb_shares = self.discover_smb_shares()
            nfs_shares = self.discover_nfs_shares()
            
            # Save results
            smb_success = self.save_smb_shares(smb_shares)
            nfs_success = self.save_nfs_shares(nfs_shares)
            
            if smb_success and nfs_success:
                print(f"\n🎉 SUCCESS! Share discovery completed.")
                print(f"📁 Results saved to: {self.output_folder}")
                print(f"📊 Found {len(smb_shares)} SMB shares and {len(nfs_shares)} NFS shares")
                
                # Ask user what to do next
                print("\nWhat would you like to do next?")
                print("  [Enter] - Open file manager to results folder")
                print("  [q] - Quit")
                
                choice = input("\nChoice: ").strip().lower()
                
                if choice != 'q':
                    self.open_file_manager()
                
                return True
            else:
                print("\n⚠️  Some operations failed. Check the output folder for partial results.")
                return False
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Operation cancelled by user.")
            return False
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
            return False


def main():
    """Entry point"""
    lister = NASShareLister()
    success = lister.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
