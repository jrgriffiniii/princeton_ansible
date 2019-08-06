#!/usr/bin/env python

import glob
import os
import subprocess
from pathlib import Path
import sys
import pdb

role_paths = []
for molecule_path_value in glob.glob('./roles/pulibrary.*/molecule'):
    molecule_path = Path(molecule_path_value)
    role_path = Path(*molecule_path.parts[:-1])
    role_paths.append(str(role_path))

echo_args = ['echo']
echo_args.extend(role_paths)
roles_pipe = subprocess.Popen(echo_args, stdout=subprocess.PIPE)

circleci_split_args = ['circleci', 'tests', 'split']
completed_process = subprocess.run(circleci_split_args, capture_output=True, stdin=roles_pipe.stdout)
roles_pipe.stdout.close()
test_files = str(completed_process.stdout)

# Trying to split the tests

test_results = []
for role in test_files.split(' '):
    print(f'Executing the tests for {role}')
    os.system(f'cd ~/princeton_ansible/{role}')
    test_process = subprocess.run(['molecule', 'test'], capture_output=True, stdout=subprocess.STDOUT, stderr=subprocess.STDERR)
    test_results.append(test_process.returncode)

error_statuses = test_results.filter(lambda status: status != 0, test_results)
if len(error_statuses) > 0:
    sys.exit(1)
