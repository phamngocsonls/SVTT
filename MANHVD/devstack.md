# DevStack
- Install Linux
- Add Stack User 
```
$ sudo useradd -s /bin/bash -d /opt/stack -m stack
```
  - Change privileges
```
$ echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack
$ sudo su -stack
```
- Download DevStack
```
$ git clone https://git.openstack.org/openstack-dev/devstack
$ cd devstack
```
- Create a local.conf
```
[[local|localrc]]
GIT_BASE=${GIT_BASE:-https://git.openstack.org}
ADMIN_PASSWORD=1111
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD

disable_service n-net c-api c-sch c-vol
disable_service tempest
```
- Start the install
```
./stack.sh
```
