# Một vài tìm hiểu về Configuration Manila


Shared File Systems service hỗ trợ truy cập tới nhiều backends storage. Truy cập `manila.conf` để có thể định nghĩa các backend storage tùy theo mục đích sử dụng. Ví dụ như sau:

```
[DEFAULT]
enabled_share_backends=backendEMC1,backendGeneric1,backendNetApp     # định nghĩa 3 backend

[backendGeneric1]                                                    # Cấu hình backend 1
share_driver=manila.share.drivers.generic.GenericShareDriver         # Driver là Generic driver
share_backend_name=one_name_for_two_backends                         # Tên backend
service_instance_user=ubuntu_user
service_instance_password=ubuntu_user_password
service_image_name=ubuntu_image_name
path_to_private_key=/home/foouser/.ssh/id_rsa
path_to_public_key=/home/foouser/.ssh/id_rsa.pub

[backendEMC1]
share_driver=manila.share.drivers.emc.driver.EMCShareDriver
share_backend_name=backendEMC2
emc_share_backend=vnx
emc_nas_server=1.1.1.1
emc_nas_password=password
emc_nas_login=user
emc_nas_server_container=server_3
emc_nas_pool_name="Pool 2"

[backendNetApp]
share_driver = manila.share.drivers.netapp.common.NetAppDriver
driver_handles_share_servers = True
share_backend_name=backendNetApp
netapp_login=user
netapp_password=password
netapp_server_hostname=1.1.1.1
netapp_root_volume_aggregate=aggr01
``` 

