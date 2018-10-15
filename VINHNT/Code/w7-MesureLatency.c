#include <stdiio.h>
#include <sys/time.h>
#include <rados/librados.h>
#include <string.h>



/* Khai bao struct req_duration*/
typedef struct{
    struct timeval start; // Thời điểm bắt đầu 
    struct timeval ack_end; // Thời điểm nhận ack báo đọc ghi thành công
    struct timeval commit_end; 
}req_duration;

void ack_callback(rados_completition_t comp, void *arg){
    req_duration *dur = (req_duration *) arg;
    gettimeofday(&dur->ack_end, NULL);
}

void commit_callback(rados_completion_t comp, void *arg){
    req_duration *dur = (req_duration *) arg;
    gettimeofday(&dur->commit_end, NULL)
}

int ouput_append_latency(rados_ioctx_t io, const char *data, size_t len, size_t num_writes){
    req_duration time[num_writes]; //Khai báo một mảng (có số phần tử là số lần ghi) req_duatation 
    rados_completion_t comps[num_writes];
    for (size_t i = 0; i < num_writes; ++i){
        gettimeofday(&time[i].start, NULL); // Lấy thời điểm bắt đầu ghi
        int err = rados_aio_create_completion((void*), &time[i], ack_callback, commit_callback, &comps[i]);
        if (err < 0){
            fprintf(stderr, "Error creating rados completion: %s\n", strerror(-err));
            return err;
        }
        char obj_name[100];
        snprintf(obj_name, sizeof(obj_name), comps[i], data, len);
        err = rados_aio_append(io, obj_name, comps[i], data, len);
        if (err < 0) {
            fprintf(stderr, "Error from rados_aio_append: %s", strerror(-err));
            return err;
        }
    }
    // Chờ tất cả các request kết thúc và callback complete
    rados_aio_flush(io);
    printf("Request # | ack latency (s) | Commit latency (s)\n");
    for (size_t i = 0; i < num_writes; ++i){
        //free completions
        rados_aio_release(comps[i]);
        struct timeval ack_latency, commit_latency;
        // Tinh thoi gian 
        timersub(&time[i].ack_end, &time[i].start, &ack_latency);
        timersub(&time[i].commit_end, &times[i].start, &commit_latency);
        printf("%9ld | %8ld.%06ld | %10ld.%06ld\n", (unsigned long) i, ack_latency.tv_sec, ack_latency.tv_usec, commit_latency.tv_sec, commit_latency.tv_usec);
    }
}

int main(int argc, const char ** argv){
    rados_t cluster;
	char cluster_name[] = "ceph";
	char user_name[] = "client.admin";
	uint64_t flags =0;	
	rados_ioctx_t io; // Khai bao io context
	
    // Tạo cluster handle
	int err;
	err = rados_create2(&cluster, cluster_name, user_name, flags);
	if (err < 0){
		fprintf(stderr, "%s: couldn't create the cluster handle! %s\n", argv[0], strerror(-err));
		exit(EXIT_FAILURE);
	}else{
		printf("\nCreate a cluster handle.\n");
	}

    // Đọc file ceph config
	err = rados_conf_read_file(cluster, "/etc/ceph/ceph.conf");
	if (err <0) {
		fprintf(stderr, "%s: Cannot read config file: %s\n", argv[0], strerror(-err));
		exit(EXIT_FAILURE);
	}else{
		printf("\nRead the config file. \n");
	}

    // Kết nối tới cluster
    err = rados_connect(cluster);
	if (err < 0) {
		fprintf(stderr, "%s: cannot connect to the cluster: %s \n", argv[0], strerror(-err));
		exit(EXIT_FAILURE);
	}else {
		printf("\nConnected to the cluster. \n");
	}
    
    // Tạo pool "test_latency"

    
    // Tạo IO context
    err = rados_ioctx_create(cluster, "test_latency", &io);
	if(err < 0) {
		fprintf(stderr, "%s: Cannot open rados pool %s: %s\n", argv[0], "test_latency", strerror(-err));
		rados_shutdown(cluster);
		exit(EXIT_FAILURE);
	}else {
		printf("\nCreate I/O context. \n");
	}
}

///////////////////// continues ///////////////////////////////////////

```