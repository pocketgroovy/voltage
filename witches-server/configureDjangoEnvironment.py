#!/usr/bin/env python

import os
import sys
import argparse
from shutil import copyfile

from ConfigParser import RawConfigParser

DEFAULT_ENV = 'dev'
CFG_FILENAME = 'settings.cfg'
CFG_TEMPLATE = os.path.join(os.path.dirname(__file__), 'templates/{0}'.format(CFG_FILENAME))
CFG_DESTINATION = os.path.join(os.path.dirname(__file__), 'Voltage/Voltage/configs')


SECTION_MAP = {
	'dev': 'Dev',
	'staging': 'Staging',
	'production': 'Prod',
	'admin': 'Admin',
	'local': 'Local',
}


def configure_server_environment(env, cfg_path):
	print ("configuring server environment: " + env)

	config = RawConfigParser()

	if(valid_file(cfg_path)):
		config.read(cfg_path)
		# print config.sections()

		config.set('Env', 'environment', SECTION_MAP[env])
		save_config(config, cfg_path)

	else:
		raise Exception("File does not exist at path: {0}".format(cfg_path))

	

def save_config(config, cfg_path):
	with open(cfg_path, 'wb') as configfile:
		config.write(configfile)
		print ("saved configuration: " + cfg_path)

def valid_file(path):
    return os.path.isfile(path) 

def copy_config_template(template, destination, filename):
	if(not valid_dir(destination)):
		os.makedirs(destination)

	if(valid_file(template)):
		cfg_path = '{0}/{1}'.format(destination, filename)
		copyfile(template, cfg_path)							# will overwrite if exists

		return cfg_path

	else:

		raise Exception("Template does not exist at path: {0}".format(template))

def valid_dir(path):
	return os.path.isdir(path)

def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('--env', default=DEFAULT_ENV, choices=['dev', 'staging', 'production', 'admin', 'local'])

	return parser.parse_args()

def main(argv):
	args = get_arguments()
	cfg_path = copy_config_template(CFG_TEMPLATE, CFG_DESTINATION, CFG_FILENAME)	
	configure_server_environment(args.env, cfg_path)

if __name__ == '__main__':
	main(sys.argv)





