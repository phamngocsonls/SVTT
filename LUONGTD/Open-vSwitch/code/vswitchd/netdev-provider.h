/*
 * Copyright (c) 2009, 2010, 2011, 2012, 2013, 2014, 2016 Nicira, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at:
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef NETDEV_PROVIDER_H
#define NETDEV_PROVIDER_H 1

/* Generic interface to network devices. */

#include "connectivity.h"
#include "netdev.h"
#include "openvswitch/list.h"
#include "ovs-numa.h"
#include "packets.h"
#include "seq.h"
#include "openvswitch/shash.h"
#include "smap.h"

#ifdef  __cplusplus
extern "C" {
#endif

struct netdev_tnl_build_header_params;
#define NETDEV_NUMA_UNSPEC OVS_NUMA_UNSPEC

/* A network device (e.g. an Ethernet device).
 *
 * Network device implementations may read these members but should not modify
 * them. */
struct netdev {
    /* The following do not change during the lifetime of a struct netdev. */
    char *name;                         /* Name of network device. */
    const struct netdev_class *netdev_class; /* Functions to control
                                                this device. */

    /* If this is 'true' the user did not specify a netdev_class when
     * opening this device, and therefore got assigned to the "system" class */
    bool auto_classified;

    /* If this is 'true', the user explicitly specified an MTU for this
     * netdev.  Otherwise, Open vSwitch is allowed to override it. */
    bool mtu_user_config;

    int ref_cnt;                        /* Times this devices was opened. */

    /* A sequence number which indicates changes in one of 'netdev''s
     * properties.   It must be nonzero so that users have a value which
     * they may use as a reset when tracking 'netdev'.
     *
     * Minimally, the sequence number is required to change whenever
     * 'netdev''s flags, features, ethernet address, or carrier changes. */
    uint64_t change_seq;

    /* A netdev provider might be unable to change some of the device's
     * parameter (n_rxq, mtu) when the device is in use.  In this case
     * the provider can notify the upper layer by calling
     * netdev_request_reconfigure().  The upper layer will react by stopping
     * the operations on the device and calling netdev_reconfigure() to allow
     * the configuration changes.  'last_reconfigure_seq' remembers the value
     * of 'reconfigure_seq' when the last reconfiguration happened. */
    struct seq *reconfigure_seq;
    uint64_t last_reconfigure_seq;

    /* The core netdev code initializes these at netdev construction and only
     * provide read-only access to its client.  Netdev implementations may
     * modify them. */
    int n_txq;
    int n_rxq;
    struct shash_node *node;            /* Pointer to element in global map. */
    struct ovs_list saved_flags_list; /* Contains "struct netdev_saved_flags". */
};

static inline void
netdev_change_seq_changed(const struct netdev *netdev_)
{
    struct netdev *netdev = CONST_CAST(struct netdev *, netdev_);
    seq_change(connectivity_seq_get());
    netdev->change_seq++;
    if (!netdev->change_seq) {
        netdev->change_seq++;
    }
}

static inline void
netdev_request_reconfigure(struct netdev *netdev)
{
    seq_change(netdev->reconfigure_seq);
}

const char *netdev_get_type(const struct netdev *);
const struct netdev_class *netdev_get_class(const struct netdev *);
const char *netdev_get_name(const struct netdev *);
struct netdev *netdev_from_name(const char *name);
void netdev_get_devices(const struct netdev_class *,
                        struct shash *device_list);
struct netdev **netdev_get_vports(size_t *size);

/* A data structure for capturing packets received by a network device.
 *
 * Network device implementations may read these members but should not modify
 * them.
 *
 * None of these members change during the lifetime of a struct netdev_rxq. */
struct netdev_rxq {
    struct netdev *netdev;      /* Owns a reference to the netdev. */
    int queue_id;
};

struct netdev *netdev_rxq_get_netdev(const struct netdev_rxq *);


struct netdev_flow_dump {
    struct netdev *netdev;
    odp_port_t port;
    bool terse;
    struct nl_dump *nl_dump;
};

/* Network device class structure, to be defined by each implementation of a
 * network device.
 *
 * These functions return 0 if successful or a positive errno value on failure,
 * except where otherwise noted.
 *
 *
 * Data Structures
 * ===============
 *
 * These functions work primarily with two different kinds of data structures:
 *
 *   - "struct netdev", which represents a network device.
 *
 *   - "struct netdev_rxq", which represents a handle for capturing packets
 *     received on a network device
 *
 * Each of these data structures contains all of the implementation-independent
 * generic state for the respective concept, called the "base" state.  None of
 * them contains any extra space for implementations to use.  Instead, each
 * implementation is expected to declare its own data structure that contains
 * an instance of the generic data structure plus additional
 * implementation-specific members, called the "derived" state.  The
 * implementation can use casts or (preferably) the CONTAINER_OF macro to
 * obtain access to derived state given only a pointer to the embedded generic
 * data structure.
 *
 *
 * Life Cycle
 * ==========
 *
 * Four stylized functions accompany each of these data structures:
 *
 *            "alloc"          "construct"        "destruct"       "dealloc"
 *            ------------   ----------------  ---------------  --------------
 * netdev      ->alloc        ->construct        ->destruct        ->dealloc
 * netdev_rxq  ->rxq_alloc    ->rxq_construct    ->rxq_destruct    ->rxq_dealloc
 *
 * Any instance of a given data structure goes through the following life
 * cycle:
 *
 *   1. The client calls the "alloc" function to obtain raw memory.  If "alloc"
 *      fails, skip all the other steps.
 *
 *   2. The client initializes all of the data structure's base state.  If this
 *      fails, skip to step 7.
 *
 *   3. The client calls the "construct" function.  The implementation
 *      initializes derived state.  It may refer to the already-initialized
 *      base state.  If "construct" fails, skip to step 6.
 *
 *   4. The data structure is now initialized and in use.
 *
 *   5. When the data structure is no longer needed, the client calls the
 *      "destruct" function.  The implementation uninitializes derived state.
 *      The base state has not been uninitialized yet, so the implementation
 *      may still refer to it.
 *
 *   6. The client uninitializes all of the data structure's base state.
 *
 *   7. The client calls the "dealloc" to free the raw memory.  The
 *      implementation must not refer to base or derived state in the data
 *      structure, because it has already been uninitialized.
 *
 * If netdev support multi-queue IO then netdev->construct should set initialize
 * netdev->n_rxq to number of queues.
 *
 * Each "alloc" function allocates and returns a new instance of the respective
 * data structure.  The "alloc" function is not given any information about the
 * use of the new data structure, so it cannot perform much initialization.
 * Its purpose is just to ensure that the new data structure has enough room
 * for base and derived state.  It may return a null pointer if memory is not
 * available, in which case none of the other functions is called.
 *
 * Each "construct" function initializes derived state in its respective data
 * structure.  When "construct" is called, all of the base state has already
 * been initialized, so the "construct" function may refer to it.  The
 * "construct" function is allowed to fail, in which case the client calls the
 * "dealloc" function (but not the "destruct" function).
 *
 * Each "destruct" function uninitializes and frees derived state in its
 * respective data structure.  When "destruct" is called, the base state has
 * not yet been uninitialized, so the "destruct" function may refer to it.  The
 * "destruct" function is not allowed to fail.
 *
 * Each "dealloc" function frees raw memory that was allocated by the
 * "alloc" function.  The memory's base and derived members might not have ever
 * been initialized (but if "construct" returned successfully, then it has been
 * "destruct"ed already).  The "dealloc" function is not allowed to fail.
 *
 *
 * Device Change Notification
 * ==========================
 *
 * Minimally, implementations are required to report changes to netdev flags,
 * features, ethernet address or carrier through connectivity_seq. Changes to
 * other properties are allowed to cause notification through this interface,
 * although implementations should try to avoid this. connectivity_seq_get()
 * can be used to acquire a reference to the struct seq. The interface is
 * described in detail in seq.h. */
struct netdev_class {
    /* Type of netdevs in this class, e.g. "system", "tap", "gre", etc.
     *
     * One of the providers should supply a "system" type, since this is
     * the type assumed if no type is specified when opening a netdev.
     * The "system" type corresponds to an existing network device on
     * the system. */

/* ## ------------------- ## */
/* ## Top-Level Functions ## */
/* ## ------------------- ## */

    /* Called when the netdev provider is registered, typically at program
     * startup.  Returning an error from this function will prevent any network
     * device in this class from being opened.
     *
     * This function may be set to null if a network device class needs no
     * initialization at registration time. */
    int (*init)(void);
    ...
};

int netdev_register_provider(const struct netdev_class *);
int netdev_unregister_provider(const char *type);

#if defined(__FreeBSD__) || defined(__NetBSD__)
extern const struct netdev_class netdev_bsd_class;
#elif defined(_WIN32)
extern const struct netdev_class netdev_windows_class;
#else
extern const struct netdev_class netdev_linux_class;
#endif
extern const struct netdev_class netdev_internal_class;
extern const struct netdev_class netdev_tap_class;

#ifdef  __cplusplus
}
#endif

#endif /* netdev.h */
