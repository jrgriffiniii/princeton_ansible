import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_ezproxy_binary_file(host):
    file = host.file("/var/local/ezproxy/ezproxy")

    assert file.exists
    assert file.user == "ezproxy"
    assert file.group == "ezproxy"
