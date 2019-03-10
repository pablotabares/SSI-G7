#!/usr/bin/env python3
files = [
	'test.txt',
	'test2.txt'
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
