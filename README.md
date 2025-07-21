# Private-2FA

A secure, local TOTP (Time-based One-Time Password) authenticator with GUI interface built in Python. This application allows you to manage all your 2FA codes from a single, secure desktop application.

## 🔐 Features

- **Secure Local Storage**: All secrets are stored locally in encrypted format
- **GUI Interface**: Clean, dark-themed interface with auto-refresh
- **One-Click Copy**: Click any code to copy to clipboard instantly
- **Auto-Refresh**: Codes refresh automatically every 30 seconds
- **Scrollable Interface**: Handles large numbers of accounts
- **Portable**: Can be compiled to standalone executable

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Xianzo-gamedev/Private-2FA.git
   cd Private-2FA
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment file:**
   ```bash
   cp code.env.example code.env
   ```

4. **Add your TOTP secrets to `code.env`:**
   ```
   Gmail=YOUR_SECRET_KEY_HERE
   Discord=YOUR_SECRET_KEY_HERE
   GitHub=YOUR_SECRET_KEY_HERE
   ```

5. **Run the application:**
   ```bash
   python 2FA.pyw
   ```

## 🔧 Dependencies

Create a `requirements.txt` file with these dependencies:

```
pyotp==2.8.0
pyperclip==1.8.2
python-dotenv==1.0.0
protobuf==4.25.1
```

Install using: `pip install -r requirements.txt`

## 📱 Getting TOTP Secrets

### Method 1: From Google Authenticator Export

1. **Export from Google Authenticator:**
   - Open Google Authenticator
   - Tap the three dots menu → "Transfer accounts" → "Export accounts"
   - Select accounts and generate QR code

2. **Extract secrets using the provided script:**
   - Use `google code .py` to extract secrets from the migration URL
   - Scan the QR code with any QR scanner to get the migration URL
   - Replace `YOUR_MIGRATION_URL_HERE` in the script with your actual URL
   - Run the script to get your secret keys

### Method 2: Manual Entry

When setting up 2FA on any service, they usually show a QR code and a manual entry key. Use that key directly in your `code.env` file.

## 🔒 Security Best Practices

1. **Never share your `code.env` file** - it's automatically ignored by git
2. **Keep backups** of your `code.env` file in a secure location
3. **Use strong system-level encryption** on your device
4. **Regularly update dependencies** for security patches

## 🏗️ Building Executable

To create a standalone executable using PyInstaller:

### Install PyInstaller

```bash
pip install pyinstaller
```

### Build Executable

```bash
# Basic build
pyinstaller --onefile --windowed 2FA.pyw

# Advanced build with icon and optimizations
pyinstaller --onefile --windowed --icon=icon.ico --name="Private-2FA" 2FA.pyw
```

### Build Options Explained

- `--onefile`: Creates a single executable file
- `--windowed`: Hides console window (for GUI apps)
- `--icon=icon.ico`: Sets custom icon (optional)
- `--name="Private-2FA"`: Sets executable name

### Post-Build Setup

1. **Copy required files to the dist folder:**
   ```bash
   cp code.env dist/
   ```

2. **The executable will look for `code.env` in the same directory**

3. **Distribute the folder containing:**
   - `Private-2FA.exe` (or `2FA.exe`)
   - `code.env` (with your secrets)

## 📁 File Structure

```
Private-2FA/
├── 2FA.pyw              # Main GUI application
├── google code .py      # Secret extraction utility
├── code.env             # Your TOTP secrets (not in repo)
├── code.env.example     # Template file
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## 🚨 Troubleshooting

### Common Issues

1. **"No such file or directory" error:**
   - Ensure `code.env` exists in the same directory as the script
   - Check file permissions

2. **"Invalid secret" or "Error" codes:**
   - Verify TOTP secrets are correct (no spaces, correct length)
   - Some secrets might need padding with `=` characters

3. **GUI doesn't appear:**
   - Install tkinter: `sudo apt-get install python3-tk` (Linux)
   - Use `python 2FA.pyw` instead of `pythonw`

4. **PyInstaller executable doesn't work:**
   - Ensure `code.env` is in the same folder as the executable
   - Try running from command line to see error messages

### Debug Mode

Add this line to the beginning of `2FA.pyw` for debugging:
```python
print("Debug: Starting application...")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is provided "as is" without warranty. Users are responsible for:
- Securing their TOTP secrets
- Creating appropriate backups
- Following security best practices

## 👨‍💻 Author

**Xianzo-gamedev**
- GitHub: [@Xianzo-gamedev](https://github.com/Xianzo-gamedev)
- Email: shloktiwari9044@gmail.com

---

⭐ **Don't forget to star this repository if you found it useful!**
