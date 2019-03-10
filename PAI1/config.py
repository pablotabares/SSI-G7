#!/usr/bin/env python3

files = [
	'/media/mount/SSI-G7/PAI1/test.txt',
	'/media/mount/SSI-G7/PAI1/test2.txt',
]

hashes_divider = '$<>$'
chunksize = 8192

log_levels = {
	'DEBUG': 0,
	'INFO': 1,
	'WARN': 2,
	'ERROR': 3,
	'CRITICAL': 4,
}

log_level = 0

log_types = [
	'terminal', 'file'
]

log_file = 'log.log'

project_path = '/media/mount/SSI-G7/PAI1/'
#in seconds
cron_time=60
