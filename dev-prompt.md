# NAS Share Lister - Development Prompt

## Objective
Create an interactive CLI tool to discover and export NFS and SMB shares from Network Attached Storage (NAS) devices.

## Requirements

### User Input
1. **NAS IP Address**: User provides the LAN IP of the NAS device
2. **Authentication**: User provides username and password (stored temporarily)
3. **Output Destination**: User specifies report destination (default: `~/Desktop`)

### Core Functionality
1. **Connection**: Script connects to the specified NAS
2. **Discovery**: 
   - Identify all NFS shares
   - Identify all SMB shares
3. **Export**: Create timestamped folder in format `DDMMYY__HHMM_NAS_shares-export`
4. **Output Files**:
   - `nfs-shares.csv` - NFS share information
   - `smb-shares.csv` - SMB share information

### CSV Structure
**NFS Shares**: `share-name`, `share-path`, `share-type` (plus additional useful fields)
**SMB Shares**: Similar structure with relevant SMB share details

### User Experience
- CLI prints success message upon completion
- User options:
  - Press `q` to exit
  - Press `Enter` to open file manager to the results folder

## Implementation Notes
- Use appropriate libraries for NFS and SMB discovery
- Include proper error handling and connection testing
- Ensure cross-platform compatibility where possible
- Provide clear user feedback throughout the process