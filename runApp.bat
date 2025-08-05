@echo off
for /f "tokens=14 delims= " %%a in ('ipconfig ^| findstr /i "IPv4"') do set MYIP=%%a
echo Your IP address is %MYIP%
start http://%MYIP%:8501
streamlit run app.py --server.address=0.0.0.0