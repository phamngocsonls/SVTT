#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <rados/librados.h>

int main (int argc, const char **argv)
{
	rados_t cluster;
	char cluster_name[] = "ceph";
	char user_name[] = "client.admin";
	uint64_t flags =0;	
	rados_ioctx_t io; // Khai bao io context
	
	int err;
	err = rados_create2(&cluster, cluster_name, user_name, flags);
	if (err < 0){
		fprintf(stderr, "%s: couldn't create the cluster handle! %s\n", argv[0], strerror(-err));
		exit(EXIT_FAILURE);
	}else{
		printf("\nCreate a cluster handle.\n");
	}

	err = rados_conf_read_file(cluster, "/etc/ceph/ceph.conf");
	if (err <0) {
		fprintf(stderr, "%s: Cannot read config file: %s\n", argv[0], strerror(-err));
		exit(EXIT_FAILURE);
	}else{
		printf("\nRead the config file. \n");
	}
	err = rados_conf_parse_argv(cluster, argc, argv);
	if (err < 0) {
		fprintf(stderr, "%s: Cannot parse command line arguments: %s\n", argv[0], strerror(-err));
		exit(EXIT_FAILURE);
	}else {
		printf("\nRead the command line argument. \n");
	}

	err = rados_connect(cluster);
	if (err < 0) {
		fprintf(stderr, "%s: cannot connect to the cluster: %s \n", argv[0], strerror(-err));
		exit(EXIT_FAILURE);
	}else {
		printf("\nConnected to the cluster. \n");
	}

	err = rados_ioctx_create(cluster, "test", &io);
	if(err < 0) {
		fprintf(stderr, "%s: Cannot open rados pool %s: %s\n", argv[0], "test", strerror(-err));
		rados_shutdown(cluster);
		exit(EXIT_FAILURE);
	}else {
		printf("\nCreate I/O context. \n");
	}

	err = rados_write(io, "string", "Mot vi du don gian", 18, 0);
	if (err < 0) {
		fprintf(stderr, "%s: Cannot write object \"string\" to pool \"test\". %s: %s\n", argv[0], strerror(-err));
		rados_ioctx_destroy(io);
		rados_shutdown(cluster);
		exit(1);
	}else {
		printf("\n Wrote successfuly.\n");
	}

	char xattr[] = "5 words";
	err = rados_setxattr(io, "string", "num_words", xattr, 8);
	if (err < 0) {
		fprintf(stderr, "%s: cannot write xattr to pool test %s: %s\n", argv[0], strerror(-err));
		rados_ioctx_destroy(io);
		rados_shutdown(cluster);
		exit(1);
	}else {
		printf("\n DONE xattr\n");
	}
	
	//  READ DATA FROM THE CLUSTER 
	rados_completion_t comp;
	err = rados_aio_create_completion(NULL, NULL, NULL, &comp);
	if (err < 0) {
		fprintf(stderr, "%s: Could not create aio completion: %s\n", argv[0], strerror(-err));
		rados_ioctx_destroy(io);
		rados_shutdown(cluster);
	}else {
		printf("\nCreated AIO completion. \n");
	}

	char read_res[100];
	err = rados_aio_read(io, "string", comp, read_res, 18, 0);
	if (err < 0) {
		fprintf(stderr, "%s: Cannot read. %s %s\n", argv[0], strerror(-err));
		rados_ioctx_destroy(io);
		rados_shutdown(cluster);
		exit(1);
	}else {
		printf("\n Read object \"string\" done. the contents are: \n %s \n", read_res);
	}
	rados_aio_release(comp);
}

