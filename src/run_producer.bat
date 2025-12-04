@echo off
REM Wrapper script to run uav_producer.py from project root
cd /d "%~dp0.."
python src\uav_producer.py %*
