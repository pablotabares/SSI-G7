#!/usr/bin/env python3

files = [
	'/root/Escritorio/test_files/test.txt',
	'/root/Escritorio/test_files/1GB.zip',
]
email_report = 'manu@manusoft.es'
project_path = '/root/Escritorio/SSI-G7/PAI1/'
log_level = 0
email_level = 3
cron_time=1 #in minutes



hashes_divider = '$<>$'
chunksize = 8192
log_levels = {
	'DEBUG': 0,
	'INFO': 1,
	'WARN': 2,
	'ERROR': 3,
	'CRITICAL': 4,
}
log_types = [
	'terminal', 'file'
]
log_file = 'log.log'
