#!/bin/bash

mkdir -p ~/.streamlit/

echo "\
[theme]
primaryColor = '#667eea'
backgroundColor = '#ffffff'
secondaryBackgroundColor = '#f0f2f6'
textColor = '#262730'
font = 'sans serif'

[client]
showErrorDetails = true
toolbarMode = 'viewer'

[server]
headless = true
port = \$PORT
runOnSave = true
maxUploadSize = 200
enableXsrfProtection = true
" > ~/.streamlit/config.toml
