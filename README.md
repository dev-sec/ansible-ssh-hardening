# ssh-hardening (Ansible Role)

[![Build Status](http://img.shields.io/travis/dev-sec/ansible-ssh-hardening.svg)][1]
[![Gitter Chat](https://badges.gitter.im/Join%20Chat.svg)][2]
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-ssh--hardening-660198.svg)][3]

## Description

This role provides secure ssh-client and ssh-server configurations.

## Requirements

* Ansible

## Role Variables
| Name           | Default Value | Description                        |
| -------------- | ------------- | -----------------------------------|
|`network_ipv6_enable` | false |true if IPv6 is needed|
|`ssh_client_cbc_required` | false |true if CBC for ciphers is required. This is usually only necessary, if older M2M mechanism need to communicate with SSH, that don't have any of the configured secure ciphers enabled. CBC is a weak alternative. Anything weaker should be avoided and is thus not available.|
|`ssh_server_cbc_required` | false |true if CBC for ciphers is required. This is usually only necessary, if older M2M mechanism need to communicate with SSH, that don't have any of the configured secure ciphers enabled. CBC is a weak alternative. Anything weaker should be avoided and is thus not available.|
|`ssh_client_weak_hmac` | false |true if weaker HMAC mechanisms are required. This is usually only necessary, if older M2M mechanism need to communicate with SSH, that don't have any of the configured secure HMACs enabled.|
|`ssh_server_weak_hmac` | false |true if weaker HMAC mechanisms are required. This is usually only necessary, if older M2M mechanism need to communicate with SSH, that don't have any of the configured secure HMACs enabled.|
|`ssh_client_weak_kex` | false |true if weaker Key-Exchange (KEX) mechanisms are required. This is usually only necessary, if older M2M mechanism need to communicate with SSH, that don't have any of the configured secure KEXs enabled.|
|`ssh_server_weak_kex` | false |true if weaker Key-Exchange (KEX) mechanisms are required. This is usually only necessary, if older M2M mechanism need to communicate with SSH, that don't have any of the configured secure KEXs enabled.|
|`ssh_server_ports` | 22 |ports to which ssh-server should listen to|
|`ssh_client_ports` | 22 |ports to which ssh-client should connect to|
|`ssh_listen_to` | ['0.0.0.0'] |one or more ip addresses, to which ssh-server should listen to. Default is all adresseses, but should be configured to specific addresses for security reasons!|
|`ssh_host_key_files` | ['/etc/ssh/ssh_host_rsa_key', '/etc/ssh/ssh_host_dsa_key', '/etc/ssh/ssh_host_ecdsa_key'] |Host keys to look for when starting sshd.|
|`ssh_client_alive_interval` | 600 | specifies an interval for sending keepalive messages |
|`ssh_client_alive_count` | 3 | defines how often keep-alive messages are sent |
|`ssh_remote_hosts` | [] | one or more hosts, to which ssh-client can connect to. Default is empty, but should be configured for security reasons!|
|`ssh_allow_root_with_key` | false | false to disable root login altogether. Set to true to allow root to login via key-based mechanism.|
|`ssh_allow_tcp_forwarding` | false | false to disable TCP Forwarding. Set to true to allow TCP Forwarding.|
|`ssh_allow_agent_forwarding` | false | false to disable Agent Forwarding. Set to true to allow Agent Forwarding.|
|`ssh_use_pam` | false | false to disable pam authentication.|
|`ssh_deny_users` | '' | if specified, login is disallowed for user names that match one of the patterns.|
|`ssh_allow_users` | '' | if specified, login is allowed only for user names that match one of the patterns.|
|`ssh_deny_groups` | '' | if specified, login is disallowed for users whose primary group or supplementary group list matches one of the patterns.|
|`ssh_allow_groups` | '' | if specified, login is allowed only for users whose primary group or supplementary group list matches one of the patterns.|
|`ssh_print_motd` | false | false to disable printing of the MOTD|
|`ssh_print_last_log` | false | false to disable display of last login information|
|`sftp_enabled` | false | true to enable sftp configuration|
|`sftp_chroot_dir` | /home/%u | change default sftp chroot location|
|`ssh_client_roaming` | false | enable experimental client roaming|

## Example Playbook

    - hosts: localhost
      roles:
        - dev-sec.ssh-hardening

## Local Testing

The preferred way of locally testing the role is to use Docker. You will have to install Docker on your system. See [Get started](https://docs.docker.com/) for a Docker package suitable to for your system.

You can also use vagrant and Virtualbox or VMWare to run tests locally. You will have to install Virtualbox and Vagrant on your system. See [Vagrant Downloads](http://downloads.vagrantup.com/) for a vagrant package suitable for your system. For all our tests we use `test-kitchen`. If you are not familiar with `test-kitchen` please have a look at [their guide](http://kitchen.ci/docs/getting-started).

Next install test-kitchen:

```bash
# Install dependencies
gem install bundler
bundle install
```

### Testing with Docker
```
# fast test on one machine
bundle exec kitchen test default-ubuntu-1204

# test on all machines
bundle exec kitchen test

# for development
bundle exec kitchen create default-ubuntu-1204
bundle exec kitchen converge default-ubuntu-1204
```

### Testing with Virtualbox
```
# fast test on one machine
KITCHEN_YAML=".kitchen.vagrant.yml" bundle exec kitchen test default-ubuntu-1204

# test on all machines
KITCHEN_YAML=".kitchen.vagrant.yml" bundle exec kitchen test

# for development
KITCHEN_YAML=".kitchen.vagrant.yml" bundle exec kitchen create default-ubuntu-1204
KITCHEN_YAML=".kitchen.vagrant.yml" bundle exec kitchen converge default-ubuntu-1204
```
For more information see [test-kitchen](http://kitchen.ci/docs/getting-started)

## FAQ / Pitfalls

**I can't log into my account. I have registered the client key, but it still doesn't let me it.**

If you have exhausted all typical issues (firewall, network, key missing, wrong key, account disabled etc.), it may be that your account is locked. The quickest way to find out is to look at the password hash for your user:

    sudo grep myuser /etc/shadow

If the hash includes an `!`, your account is locked:

    myuser:!:16280:7:60:7:::

The proper way to solve this is to unlock the account (`passwd -u myuser`). If the user doesn't have a password, you should can unlock it via:

    usermod -p "*" myuser

Alternatively, if you intend to use PAM, you enabled it via `ssh_use_pam: true`. PAM will allow locked users to get in with keys.


**Why doesn't my application connect via SSH anymore?**

Always look into log files first and if possible look at the negotation between client and server that is completed when connecting.

We have seen some issues in applications (based on python and ruby) that are due to their use of an outdated crypto set. This collides with this hardening module, which reduced the list of ciphers, message authentication codes (MACs) and key exchange (KEX) algorithms to a more secure selection.

If you find this isn't enough, feel free to activate the attributes `cbc_requires` for ciphers, `weak_hmac` for MACs and `weak_kex`for KEX in the variables `ssh_client` or `ssh_server` based on where you want to support them.

**After using the role Ansibles template/copy/file module does not work anymore!**

This role deactivates SFTP. Ansible uses by default SFTP to transfer files to the remote hosts. You have to set `scp_if_ssh = True` in your ansible.cfg. This way Ansible uses SCP to copy files.

## Contributing

See [contributor guideline](CONTRIBUTING.md).

## License and Author

* Author:: Sebastian Gumprich <sebastian.gumprich@38.de>
* Author:: Christoph Hartmann <chris@lollyrock.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

[1]: http://travis-ci.org/dev-sec/ansible-ssh-hardening
[2]: https://gitter.im/dev-sec/general
[3]: https://galaxy.ansible.com/dev-sec/ssh-hardening/
