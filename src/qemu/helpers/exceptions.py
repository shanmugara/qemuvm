FileNotFound = Exception("file not found")
InvalidOSType = Exception("invalid OS variant was passed")
CmdRunError = Exception("subprocess command execution failed")
BadWinMode = Exception("invalid windows install mode")
DestImageExists = Exception("destination disk image already exists")