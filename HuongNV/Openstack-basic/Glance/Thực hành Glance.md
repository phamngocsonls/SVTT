# Một vài tìm hiểu về thực hành Glance trên Devstack

## Mục lục

* [1. Glance command-line client](#1)
    * [1.1 List image](#11)
    * [1.2 Show information image](#12)
    * [1.3 Deactivate image](#13)
    * [1.4 Reactivate image](#14)
    * [1.5 update image](#15)
    * [1.6 upload image](#16)
    * [1.7 deleted image](#17)


<a name="1"></a>

# 1. Glance command-line client

<a name="11"></a>

## 1.1 List image

Liệt kêt tất cả các image:

```
glance image-list
```
![Imgur](https://i.imgur.com/nwY7VKa.png)

<a name="12"></a>

## 1.2 Show information image

Sử dụng:
```
glance image-show [--human-readable] [--max-column-width <integer>] <image_ID>
```
    - --human-readable: hiển thị kích thước của image
    - --max-column-width <integer>: hiển thị bảng thông số của image
![Imgur](https://i.imgur.com/JNNCoUM.png)

<a name="13"></a>

## 1.3 Deactivate image

Sử dụng:
```
glance image-deactivate <image-ID>
```
![Imgur](https://i.imgur.com/U09qOxz.png)

<a name="14"></a>

## 1.4 Reactivate image

Sử dụng:
```
glance image-reactivate <image-ID>
```
![Imgur](https://i.imgur.com/kI3yHnM.png)

<a name="15"></a>

## 1.5 Update image

Sử dụng:
```
usage: glance image-update [--architecture <ARCHITECTURE>]
                           [--protected [True|False]] [--name <NAME>]
                           [--instance-uuid <INSTANCE_UUID>]
                           [--min-disk <MIN_DISK>] [--visibility <VISIBILITY>]
                           [--kernel-id <KERNEL_ID>]
                           [--os-version <OS_VERSION>]
                           [--disk-format <DISK_FORMAT>]
                           [--os-distro <OS_DISTRO>] [--owner <OWNER>]
                           [--ramdisk-id <RAMDISK_ID>] [--min-ram <MIN_RAM>]
                           [--container-format <CONTAINER_FORMAT>]
                           [--property <key=value>] [--remove-property key]
                           <IMAGE_ID>
```
- Một vài lựa chọn trong việc update image:
    - --min-disk(): disk space(GB) để boot image
    - --visibility: Phạm vi tiếp cận image(private, public, community, shared)
    - --disk-format: định dạng image(qcow2, vhd,raw...)

- Ví dụ, update visibility image thành private:
![Imgur](https://i.imgur.com/PAq9WNx.png)

<a name="16"></a>

## 1.6 Upload image

Sử dụng:
```
glance image-upload [--file <FILE>] [--size <IMAGE_SIZE>] [--progress] <IMAGE_ID>
```

<a name="17"></a>

## 1.7 Delete image

Sử dụng:
```
glance image-delete <image-ID>
```

![Imgur](https://i.imgur.com/UgbP2ze.png)


