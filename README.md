# NAS Share Lister

[![AI Developed](https://img.shields.io/badge/AI%20Developed-Cascade-blue?style=flat-square&logo=robot)](dev-prompt.md)

An interactive CLI tool to discover and export NFS and SMB shares from Network Attached Storage (NAS) devices.

> 🤖 **AI Development**: This project was developed using AI assistance. View the [development prompt](dev-prompt.md) to see the original requirements and specifications.

## Features

- 🔍 **Automatic Discovery**: Discovers both NFS and SMB shares from any NAS device
- 📊 **CSV Export**: Exports share information to timestamped CSV files
- 🔐 **Secure Authentication**: Handles username/password authentication for SMB shares
- 📁 **Organized Output**: Creates timestamped folders with detailed share information
- 🖥️ **Cross-Platform**: Works on Linux, macOS, and Windows
- 🚀 **Easy Setup**: Simple installation and setup process

## Requirements

- Python 3.6+
- Linux: `nfs-common` package for NFS discovery
- Network access to the target NAS device

## Quick Start

### Linux (Recommended)

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd NFS-SMB-Share-Lister
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Run the tool**:
   ```bash
   ./run.sh
   ```

### Manual Installation

1. **Install system dependencies**:
   ```bash
   # Ubuntu/Debian
   sudo apt install nfs-common python3-pip python3-venv
   
   # CentOS/RHEL
   sudo yum install nfs-utils python3-pip python3-venv
   
   # macOS
   brew install python3
   ```

2. **Setup Python environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python3 nas_share_lister.py
   ```

## Usage

When you run the tool, it will interactively prompt you for:

1. **NAS IP Address**: The LAN IP of your NAS device
2. **Credentials**: Username and password for accessing shares
3. **Output Destination**: Where to save the results (default: ~/Desktop)

The tool will then:
- Test connectivity to the NAS
- Discover all available NFS and SMB shares
- Create a timestamped folder (format: `DDMMYY__HHMM_NAS_shares-export`)
- Generate two CSV files with detailed share information
- Optionally open the results folder in your file manager

## Output Format

### SMB Shares (`smb-shares.csv`)
- **share_name**: Name of the SMB share
- **share_path**: Full UNC path to the share
- **share_type**: Type of share (Disk, Print Queue, etc.)
- **comments**: Share description/comments
- **is_hidden**: Whether the share is hidden (ends with $)

### NFS Shares (`nfs-shares.csv`)
- **share_name**: Name of the NFS export
- **share_path**: Export path on the server
- **share_type**: Always "NFS Export"
- **allowed_clients**: Clients allowed to mount this export
- **full_path**: Complete mount path (server:path)

## Example Output

```
=== NAS Share Lister ===

Enter NAS IP address: 192.168.1.100
Enter username: admin
Enter password: [hidden]
Enter destination folder (default: /home/user/Desktop): 

Output will be saved to: /home/user/Desktop/200724__1430_NAS_shares-export

Testing connection to 192.168.1.100...
✓ SMB port (445) is accessible

Discovering SMB shares...
✓ SMB connection established
  Found: public
  Found: media
  Found: backups

Discovering NFS shares...
✓ NFS exports retrieved
  Found: /volume1/public
  Found: /volume1/media

✓ Created output folder: /home/user/Desktop/200724__1430_NAS_shares-export
✓ SMB shares saved to: smb-shares.csv (3 shares)
✓ NFS shares saved to: nfs-shares.csv (2 shares)

🎉 SUCCESS! Share discovery completed.
📁 Results saved to: /home/user/Desktop/200724__1430_NAS_shares-export
📊 Found 3 SMB shares and 2 NFS shares

What would you like to do next?
  [Enter] - Open file manager to results folder
  [q] - Quit
```

## Troubleshooting

### Common Issues

**"showmount command not found"**
- Install NFS utilities: `sudo apt install nfs-common`

**"SMB connection failed"**
- Check if SMB/CIFS is enabled on your NAS
- Verify credentials are correct
- Ensure port 445 is not blocked by firewall

**"Connection test failed"**
- Verify the NAS IP address is correct
- Check network connectivity: `ping <nas-ip>`
- Ensure the NAS is powered on and accessible

### Supported NAS Devices

This tool should work with most NAS devices that support standard SMB and NFS protocols, including:
- Synology DiskStation
- QNAP NAS
- FreeNAS/TrueNAS
- Netgear ReadyNAS
- Western Digital My Cloud
- Generic Linux-based NAS systems

## Dependencies

- `pysmb`: SMB/CIFS protocol support
- `smbprotocol`: Modern SMB protocol implementation
- `python-libnfs`: NFS client library (optional)
- `paramiko`: SSH support for advanced features

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is open source. See LICENSE file for details.
