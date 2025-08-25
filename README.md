# AWS Platform CLI & GUI

A self-service command-line tool and graphical interface for developers to provision and manage AWS resources (EC2, S3, Route53) within safe, pre-defined standards.

## Features

- **Dual Interface**: Both CLI and modern GUI interface
- **EC2 Management**: Create, start, stop, terminate, and list EC2 instances
- **S3 Management**: Create, delete, upload files, and list S3 buckets  
- **Route53 Management**: Create, delete, manage DNS records, and list hosted zones
- **Resource Tagging**: Consistent tagging for all resources created by the CLI
- **Safety Constraints**: Built-in limits and confirmations for secure operations
- **Interactive GUI**: User-friendly graphical interface with real-time feedback

## Prerequisites

- Python 3.7+
- AWS Account with appropriate permissions
- AWS credentials configured

### Required AWS Permissions

Your AWS user/role needs the following permissions:
- `ec2:*` (EC2 management)
- `s3:*` (S3 bucket management)
- `route53:*` (DNS management)

## Installation

### Local Development

1. **Install Git and Python (if not already installed):**
   
   **Windows:**
   - Git: Download from [git-scm.com](https://git-scm.com/download/win) or `winget install Git.Git`
   - Python: Download from [python.org](https://www.python.org/downloads/) or `winget install Python.Python.3`
   
   **macOS:**
   ```bash
   # Using Homebrew:
   brew install git python
   
   # Or download from official sites
   ```
   
   **Linux:**
   ```bash
   # Ubuntu/Debian:
   sudo apt install git python3 python3-pip
   
   # CentOS/RHEL/Fedora:
   sudo yum install git python3 python3-pip
   # or
   sudo dnf install git python3 python3-pip
   ```

2. **Clone the repository:**
   ```bash
   git clone https://github.com/LirChen/AWS_Resource_manager_cli_and_ui.git
   cd AWS_Resource_manager_cli_and_ui
   ```

3. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   # On Linux/macOS you might need:
   sudo pip3 install -r requirements.txt
   ```

4. **For GUI support, install system dependencies:**
   
   **Windows:**
   - No additional installation needed (tkinter included with Python)
   
   **macOS:**
   ```bash
   # tkinter comes with Python on macOS, but if you have issues:
   brew install python-tk
   ```
   
   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt install python3-tk
   ```
   
   **Linux (CentOS/RHEL/Fedora):**
   ```bash
   # CentOS/RHEL:
   sudo yum install tkinter
   # or
   sudo yum install python3-tkinter
   
   # Fedora:
   sudo dnf install python3-tkinter
   ```

5. **Configure AWS credentials:** (see AWS Environment Variables Setup below)

### AWS EC2 Instance Setup

#### Amazon Linux

1. **Update system and install prerequisites:**
   ```bash
   sudo yum update -y
   sudo yum install git python3-pip -y
   ```

2. **Clone the repository:**
   ```bash
   git clone https://github.com/LirChen/AWS_Resource_manager_cli_and_ui.git
   cd AWS_Resource_manager_cli_and_ui
   ```

3. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   # If permission issues:
   sudo pip3 install -r requirements.txt
   ```

4. **Install GUI dependencies for Amazon Linux:**
   ```bash
   # Amazon Linux 2:
   sudo yum install tkinter -y
   # or try:
   sudo yum install python3-tkinter -y
   
   # If above doesn't work:
   sudo amazon-linux-extras install python3.8
   sudo yum install python38-tkinter -y
   ```

5. **Configure AWS credentials:**
   ```bash
   export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
   export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"
   export AWS_DEFAULT_REGION="us-east-1"
   ```

5. **Test the installation:**
   ```bash
   # Test CLI (works everywhere):
   python3 Manager.py --help
   
   # Note: GUI cannot run on headless servers like EC2
   # Use CLI commands instead for server environments
   ```

#### Ubuntu

1. **Update system and install prerequisites:**
   ```bash
   sudo apt update
   sudo apt install git python3-pip -y
   ```

2. **Clone the repository:**
   ```bash
   git clone https://github.com/LirChen/AWS_Resource_manager_cli_and_ui.git
   cd AWS_Resource_manager_cli_and_ui
   ```

3. **Install dependencies using Virtual Environment (Recommended for Ubuntu 22.04+):**
   ```bash
   # Install python3-venv if not already installed
   sudo apt install python3-venv python3-full
   
   # Create virtual environment
   python3 -m venv myenv
   
   # Activate the environment
   source myenv/bin/activate
   
   # Now install the packages
   pip install -r requirements.txt
   ```

   **Alternative for older Ubuntu versions:**
   ```bash
   pip3 install -r requirements.txt
   # If permission issues:
   sudo pip3 install -r requirements.txt
   ```

4. **Install GUI dependencies for Ubuntu:**
   ```bash
   sudo apt install python3-tk -y
   ```

5. **Configure AWS credentials:**
   ```bash
   export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
   export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"
   export AWS_DEFAULT_REGION="us-east-1"
   ```

6. **Test the installation:**
   ```bash
   # With virtual environment active:
   python Manager.py --help
   
   # Or if not using virtual environment:
   python3 Manager.py --help
   
   # Note: GUI cannot run on headless servers like EC2
   # Use CLI commands instead for server environments
   ```

7. **Running the project:**
   ```bash
   # Make sure virtual environment is active
   source myenv/bin/activate
   
   # Run your script
   python Manager.py --help
   python Manager_ui.py  # For GUI
   
   # When finished - deactivate virtual environment
   deactivate
   ```

## AWS Environment Variables Setup

To run this Python integration, you need to configure your AWS credentials as environment variables. This avoids hardcoding secrets inside your code.

### Linux / macOS

Open your shell configuration file (e.g., ~/.bashrc or ~/.zshrc).

Add the following lines at the bottom of the file:
```bash
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"
export AWS_DEFAULT_REGION="us-east-1"
```

Save the file and reload it:
```bash
source ~/.bashrc
```
**or**
```bash
source ~/.zshrc
```

### Windows PowerShell

Run the following commands (they will persist across sessions):
```powershell
setx AWS_ACCESS_KEY_ID "YOUR_ACCESS_KEY"
setx AWS_SECRET_ACCESS_KEY "YOUR_SECRET_KEY"
setx AWS_DEFAULT_REGION "us-east-1"
```

### Command Prompt (temporary, current session only)
```cmd
set AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
set AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
set AWS_DEFAULT_REGION=us-east-1
```

### If you are in PowerShell terminal (inside PyCharm or standalone):
```powershell
$env:AWS_ACCESS_KEY_ID = "YOUR_ACCESS_KEY"
$env:AWS_SECRET_ACCESS_KEY = "YOUR_SECRET_KEY"
$env:AWS_DEFAULT_REGION = "us-east-1"
```

Check that they are set:
```powershell
echo $env:AWS_ACCESS_KEY_ID
```

**Important Notes for EC2:**
- Use `python3` and `pip3` instead of `python` and `pip` (unless using virtual environment)
- Default users: `ec2-user` for Amazon Linux, `ubuntu` for Ubuntu
- If you get permission errors with pip, consider using virtual environment or `sudo`
- **GUI cannot run on EC2** - use CLI commands only

### Verification

You can verify that the variables are set correctly by running:

**Linux/macOS:**
```bash
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY
echo $AWS_DEFAULT_REGION
```

**Windows PowerShell:**
```powershell
echo $env:AWS_ACCESS_KEY_ID
echo $env:AWS_SECRET_ACCESS_KEY
echo $env:AWS_DEFAULT_REGION
```

## Usage

The tool provides both CLI and GUI interfaces:

**GUI Interface**: Best for local development on Windows, macOS, or Linux desktop
**CLI Interface**: Works everywhere - local machines, servers, EC2 instances

### GUI Interface (Recommended for Local Development)

**Important**: The GUI requires a graphical display and works best on local machines. It **cannot run on headless servers** like AWS EC2 instances without additional setup.

**Supported Environments:**
- ✅ Local Windows machines
- ✅ Local macOS machines  
- ✅ Local Linux with desktop environment
- ❌ AWS EC2 instances (headless servers)
- ❌ Remote servers without GUI

Launch the graphical interface:
```bash
# If using virtual environment:
python Manager_ui.py

# Otherwise:
python3 Manager_ui.py
```

**If you get "TclError: no display name and no $DISPLAY environment variable":**
- This means you're on a headless server (like EC2) without a graphical display
- Use the CLI instead: `python3 Manager.py --help`
- The CLI provides all the same functionality

The GUI provides:
- **Modern Interface**: Clean, intuitive design with real-time feedback
- **Service Tabs**: Separate tabs for EC2, S3, and Route53 management
- **Form Validation**: Built-in validation and error handling
- **Visual Feedback**: Progress indicators and confirmation dialogs
- **Resource Lists**: Visual tables showing all your resources
- **One-Click Actions**: Easy resource management with confirmation prompts

### CLI Interface (Command Line Examples)

#### EC2 Instances

**Create Instance (Enhanced with Subnet & Security Group Selection):**
```bash
# New format with subnet and security group selection
python3 Manager.py ec2 create ubuntu t3.micro subnet-1 sg-0d15f0e90387da6d4
python3 Manager.py ec2 create amazon-linux t2.small subnet-2 sg-0a8336384b6d3b85b

# Parameters explained:
# - AMI: ubuntu or amazon-linux
# - Instance Type: t3.micro or t2.small
# - Subnet: subnet-1 or subnet-2 (predefined subnets)
# - Security Group: Your security group ID in the VPC
```

**Manage Instance:**
```bash
python3 Manager.py ec2 manage start i-1234567890abcdef0
python3 Manager.py ec2 manage stop i-1234567890abcdef0
python3 Manager.py ec2 manage terminate i-1234567890abcdef0
```

**List Instances:**
```bash
python3 Manager.py ec2 list
```

#### S3 Buckets

**Create Bucket:**
```bash
python3 Manager.py s3 create private
python3 Manager.py s3 create public  # Requires confirmation
```

**Upload File:**
```bash
python3 Manager.py s3 upload /path/to/file.txt bucket-name file.txt
```

**Delete Bucket:**
```bash
python3 Manager.py s3 delete s3-bucket-lirchen-abc123
```

**List Buckets:**
```bash
python3 Manager.py s3 list
```

#### Route53 DNS

**Create Hosted Zone:**
```bash
python3 Manager.py route53 create example.com
```

**Manage DNS Records:**
```bash
# Create A record
python3 Manager.py route53 manage create Z1D633PJN98FT9 www.example.com A 192.168.1.1

# Update CNAME record
python3 Manager.py route53 manage update Z1D633PJN98FT9 api.example.com CNAME api.provider.com

# Delete record
python3 Manager.py route53 manage delete Z1D633PJN98FT9 old.example.com A 192.168.1.100
```

**Delete Hosted Zone:**
```bash
python3 Manager.py route53 delete Z1D633PJN98FT9
```

**List Hosted Zones:**
```bash
python3 Manager.py route53 list
```

## Safety Constraints

### EC2 Constraints
- **Instance Types**: Only `t3.micro` and `t2.small` allowed
- **Hard Limit**: Maximum 2 running instances at any time
- **AMI Options**: Latest Ubuntu or Amazon Linux only
- **Network**: Predefined VPC with two subnet options
- **Security**: User must specify their own security group

### S3 Constraints
- **Public Buckets**: Requires explicit confirmation
- **Bucket Naming**: Automatic unique naming with random suffix
- **Access Control**: Public buckets use bucket policies (not ACLs)

### Route53 Constraints
- **Zone Management**: Only CLI-created zones can be modified
- **Record Management**: Only records in CLI-created zones can be managed
- **Zone Deletion**: Available both via CLI and GUI with double confirmation

## GUI Features

### EC2 Management
- **Visual Instance Creation**: Easy form-based instance creation
- **Subnet Selection**: Choose between predefined subnets
- **Security Group Input**: Specify your security group ID
- **Instance Monitoring**: Real-time status updates
- **Bulk Operations**: Start, stop, or terminate multiple instances

### S3 Management
- **Bucket Creation**: Simple bucket creation with privacy options
- **File Upload**: Drag-and-drop file uploads (planned feature)
- **Bucket Policies**: Automatic policy management for public buckets
- **Storage Monitoring**: View bucket sizes and file counts

### Route53 Management
- **Zone Creation**: Intuitive hosted zone creation
- **DNS Records**: Easy record management (create, update, delete)
- **Zone Deletion**: Safe zone deletion with confirmation
- **Record Types**: Support for A, AAAA, CNAME, MX, TXT, NS, SOA records

## Tagging Convention

All resources created by this CLI are tagged with:
- `CreatedBy`: Owner identifier (configurable in code)
- `Visibility`: For S3 buckets (public/private)

**Example Tags:**
```json
{
  "CreatedBy": "lirchen",
  "Visibility": "private"
}
```

## Configuration

Edit the `OWNER` variable in `Manager.py` to set your identifier:
```python
OWNER = "your-username"
```

### Network Configuration

The tool uses predefined subnets. Update these in your code if needed:
```python
subnet_options = {
    "subnet-1": "subnet-0468e933b4fdab115",  # Your subnet ID 1
    "subnet-2": "subnet-0a8336384b6d3b85b"   # Your subnet ID 2
}
```

## Error Handling

The CLI and GUI provide clear error messages for common scenarios:
- Resource not found
- Permission denied
- Invalid resource states
- AWS service limits exceeded
- Network configuration issues
- Security group validation errors

## Cleanup Instructions

### Clean Up All Resources

**Using GUI:**
- Use the respective "List" sections in each tab
- Click delete buttons for each resource
- Follow confirmation prompts

**Using CLI:**

**EC2 Instances:**
```bash
python3 Manager.py ec2 list
# Terminate each instance manually:
python3 Manager.py ec2 manage terminate i-xxxxxxxxx
```

**S3 Buckets:**
```bash
python3 Manager.py s3 list
# Delete each bucket:
python3 Manager.py s3 delete bucket-name
```

**Route53 Zones:**
```bash
python3 Manager.py route53 list
# Delete each zone:
python3 Manager.py route53 delete zone-id
```

## Troubleshooting

### Common Issues

**"Unable to locate credentials"**
- Check that AWS environment variables are set correctly
- Verify AWS credentials are valid

**"Access Denied"**
- Ensure your AWS user has the required permissions
- Check if MFA is required for your account

**"Cannot create public bucket"**
- AWS security settings may block public access
- Bucket will be created as private for security

**"Bucket name already exists"**
- S3 bucket names must be globally unique
- The CLI uses random suffixes to avoid conflicts

**"Security group not found"**
- Verify the security group ID exists in your VPC
- Ensure the security group ID format starts with 'sg-'

**"externally-managed-environment" Error (Ubuntu 22.04+):**
- Use virtual environment as shown in Ubuntu installation section
- This is a safety feature in newer Ubuntu versions
- Alternative: Use `--break-system-packages` flag (not recommended)

**GUI Issues:**
- **"TclError: no display name and no $DISPLAY environment variable"**: You're on a headless server (like EC2). GUI cannot run - use CLI instead.
- **"ModuleNotFoundError: No module named 'tkinter'"**: Install tkinter (see Dependencies section)
- **Amazon Linux**: `sudo yum install python3-tkinter -y`
- **Ubuntu**: `sudo apt install python3-tk -y` 
- **GUI works only on local machines** with graphical displays
- **CLI works everywhere**: `python3 Manager.py --help`

### Getting Help

Use `--help` with any command:
```bash
python3 Manager.py --help
python3 Manager.py ec2 --help
python3 Manager.py s3 create --help
```

## Security Best Practices

- ✅ No secrets stored in repository
- ✅ Uses AWS roles/profiles for authentication
- ✅ Consistent resource tagging
- ✅ Built-in safety constraints
- ✅ Confirmation prompts for destructive actions
- ✅ Private-by-default for S3 buckets
- ✅ Network security with user-specified security groups
- ✅ GUI input validation and sanitization

## Dependencies

```txt
boto3>=1.26.0
botocore>=1.29.0
click>=8.0.0
tabulate>=0.9.0
customtkinter>=5.2.0
```

**Note about GUI Dependencies:**
- **Windows**: tkinter comes pre-installed with Python
- **macOS**: tkinter included, but may need `brew install python-tk` if issues occur
- **Linux**: Requires manual installation of tkinter:
  - Ubuntu/Debian: `sudo apt install python3-tk`
  - CentOS/RHEL: `sudo yum install python3-tkinter`
  - Fedora: `sudo dnf install python3-tkinter`
  - Amazon Linux: `sudo yum install tkinter` or `sudo yum install python3-tkinter`

Install all dependencies:
```bash
# With virtual environment (recommended for Ubuntu 22.04+):
pip install -r requirements.txt

# Without virtual environment:
pip3 install -r requirements.txt
```

## Screenshots

The GUI provides an intuitive interface for:
- 🚀 **EC2 Tab**: Instance creation and management
- 📦 **S3 Tab**: Bucket operations and file management  
- 🌐 **Route53 Tab**: DNS zone and record management
- 📊 **Resource Lists**: Visual tables with action buttons

---

**Note**: This tool is designed for development environments. Always review and test in non-production environments first.

## Recent Updates

### v2.0 Features
- **GUI Interface**: Modern graphical user interface
- **Enhanced EC2 Creation**: Subnet and security group selection
- **Route53 Zone Deletion**: GUI support for hosted zone deletion
- **Improved Error Handling**: Better validation and user feedback
- **Visual Resource Management**: Intuitive tables and action buttons
- **Virtual Environment Support**: Updated installation instructions for Ubuntu 22.04+ compatibility
