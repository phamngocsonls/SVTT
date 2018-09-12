/*
 * Copyright (c) 2009-2017 Nicira, Inc.
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

#ifndef OFPROTO_OFPROTO_PROVIDER_H
#define OFPROTO_OFPROTO_PROVIDER_H 1

/* Definitions for use within ofproto.
 *
 *
 * Thread-safety
 * =============
 *
 * Lots of ofproto data structures are only accessed from a single thread.
 * Those data structures are generally not thread-safe.
 *
 * The ofproto-dpif ofproto implementation accesses the flow table from
 * multiple threads, including modifying the flow table from multiple threads
 * via the "learn" action, so the flow table and various structures that index
 * it have been made thread-safe.  Refer to comments on individual data
 * structures for details.
 */

#include "cfm.h"
#include "classifier.h"
#include "guarded-list.h"
#include "heap.h"
#include "hindex.h"
#include "object-collection.h"
#include "ofproto/ofproto.h"
#include "openvswitch/list.h"
#include "openvswitch/ofp-actions.h"
#include "openvswitch/ofp-errors.h"
#include "openvswitch/ofp-flow.h"
#include "openvswitch/ofp-group.h"
#include "openvswitch/ofp-meter.h"
#include "openvswitch/ofp-port.h"
#include "openvswitch/ofp-switch.h"
#include "openvswitch/ofp-table.h"
#include "ovs-atomic.h"
#include "ovs-rcu.h"
#include "ovs-thread.h"
#include "openvswitch/shash.h"
#include "simap.h"
#include "timeval.h"
#include "tun-metadata.h"
#include "versions.h"
#include "vl-mff-map.h"

struct match;
struct ofputil_flow_mod;
struct ofputil_packet_in_private;
struct bfd_cfg;
struct meter;
struct ofoperation;
struct ofproto_packet_out;
struct smap;

extern struct ovs_mutex ofproto_mutex;

/* An OpenFlow switch. */
struct ofproto {
    const struct ofproto_class *ofproto_class;
    char *type;                 /* Datapath type. */
    char *name;                 /* Datapath name. */

    /* Settings. */
    uint64_t fallback_dpid;     /* Datapath ID if no better choice found. */
    uint64_t datapath_id;       /* Datapath ID. */

    /* Datapath. */
    struct hmap ports;          /* Contains "struct ofport"s. */
    struct shash port_by_name;
    struct simap ofp_requests;  /* OpenFlow port number requests. */
    struct hmap ofport_usage;   /* Map ofport to last used time. */

    /* Flow tables. */
    struct oftable *tables;

    /* Rules indexed on their cookie values, in all flow tables. */

    /* List of expirable flows, in all flow tables. */

    /* OpenFlow connections. */

    /* Groups. */
    struct cmap groups;               /* Contains "struct ofgroup"s. */

     /* Tunnel TLV mapping table. */
};

void ofproto_init_tables(struct ofproto *, int n_tables);
void ofproto_init_max_ports(struct ofproto *, uint16_t max_ports);

struct ofproto *ofproto_lookup(const char *name);
struct ofport *ofproto_get_port(const struct ofproto *, ofp_port_t ofp_port);

/* An OpenFlow port within a "struct ofproto".
 *
 * The port's name is netdev_get_name(port->netdev).
 *
 * With few exceptions, ofproto implementations may look at these fields but
 * should not modify them. */
struct ofport {
    struct hmap_node hmap_node; /* In struct ofproto's "ports" hmap. */
    struct ofproto *ofproto;    /* The ofproto that contains this port. */
    struct netdev *netdev;
    struct ofputil_phy_port pp;
    ofp_port_t ofp_port;        /* OpenFlow port number. */
    uint64_t change_seq;
    long long int created;      /* Time created, in msec. */
    int mtu;
};

void ofproto_port_set_state(struct ofport *, enum ofputil_port_state);

/* OpenFlow table flags:
 *
 *   - "Hidden" tables are not included in OpenFlow operations that operate on
 *     "all tables".  For example, a request for flow stats on all tables will
 *     omit flows in hidden tables, table stats requests will omit the table
 *     entirely, and the switch features reply will not count the hidden table.
 *
 *     However, operations that specifically name the particular table still
 *     operate on it.  For example, flow_mods and flow stats requests on a
 *     hidden table work.
 *
 *     To avoid gaps in table IDs (which have unclear validity in OpenFlow),
 *     hidden tables must be the highest-numbered tables that a provider
 *     implements.
 *
 *   - "Read-only" tables can't be changed through OpenFlow operations.  (At
 *     the moment all flow table operations go effectively through OpenFlow, so
 *     this means that read-only tables can't be changed at all after the
 *     read-only flag is set.)
 *
 * The generic ofproto layer never sets these flags.  An ofproto provider can
 * set them if it is appropriate.
 */
enum oftable_flags {
    OFTABLE_HIDDEN = 1 << 0,   /* Hide from most OpenFlow operations. */
    OFTABLE_READONLY = 1 << 1  /* Don't allow OpenFlow controller to change
                                  this table. */
};

/* A flow table within a "struct ofproto".
 *
 *
 * Thread-safety
 * =============
 *
 * Adding or removing rules requires holding ofproto_mutex.
 *
 * Rules in 'cls' are RCU protected.  For extended access to a rule, try
 * incrementing its ref_count with ofproto_rule_try_ref(), or
 * ofproto_rule_ref(), if the rule is still known to be in 'cls'.  A rule
 * will be freed using ovsrcu_postpone() once its 'ref_count' reaches zero.
 *
 * Modifying a rule requires the rule's own mutex.
 *
 * Freeing a rule requires ofproto_mutex.  After removing the rule from the
 * classifier, release a ref_count from the rule ('cls''s reference to the
 * rule).
 *
 * Refer to the thread-safety notes on struct rule for more information.*/
struct oftable {
    enum oftable_flags flags;
    struct classifier cls;      /* Contains "struct rule"s. */
    char *name;                 /* Table name exposed via OpenFlow, or NULL. */

    /* Maximum number of flows or UINT_MAX if there is no limit besides any
     * limit imposed by resource limitations. */
    unsigned int max_flows;
    /* Current number of flows, not counting temporary duplicates nor deferred
     * deletions. */
    unsigned int n_flows;

    /* These members determine the handling of an attempt to add a flow that
     * would cause the table to have more than 'max_flows' flows.
     *
     * If 'eviction_fields' is NULL, overflows will be rejected with an error.
     *
     * If 'eviction_fields' is nonnull (regardless of whether n_eviction_fields
     * is nonzero), an overflow will cause a flow to be removed.  The flow to
     * be removed is chosen to give fairness among groups distinguished by
     * different values for the subfields within 'groups'. */
    struct mf_subfield *eviction_fields;
    size_t n_eviction_fields;

    /* Eviction groups.
     *
     * When a flow is added that would cause the table to have more than
     * 'max_flows' flows, and 'eviction_fields' is nonnull, these groups are
     * used to decide which rule to evict: the rule is chosen from the eviction
     * group that contains the greatest number of rules.*/
    uint32_t eviction_group_id_basis;
    struct hmap eviction_groups_by_id;
    struct heap eviction_groups_by_size;

    /* Flow table miss handling configuration. */
    ATOMIC(enum ofputil_table_miss) miss_config;

    /* Eviction is enabled if either the client (vswitchd) enables it or an
     * OpenFlow controller enables it; thus, a nonzero value indicates that
     * eviction is enabled.  */
#define EVICTION_CLIENT  (1 << 0)  /* Set to 1 if client enables eviction. */
#define EVICTION_OPENFLOW (1 << 1) /* Set to 1 if OpenFlow enables eviction. */
    unsigned int eviction;

    /* If zero, vacancy events are disabled.  If nonzero, this is the type of
       vacancy event that is enabled: either OFPTR_VACANCY_DOWN or
       OFPTR_VACANCY_UP.  Only one type of vacancy event can be enabled at a
       time. */
    enum ofp14_table_reason vacancy_event;

    /* Non-zero values for vacancy_up and vacancy_down indicates that vacancy
     * is enabled by table-mod, else these values are set to zero when
     * vacancy is disabled */
    uint8_t vacancy_down; /* Vacancy threshold when space decreases (%). */
    uint8_t vacancy_up;   /* Vacancy threshold when space increases (%). */

    atomic_ulong n_matched;
    atomic_ulong n_missed;
};

/* Assigns TABLE to each oftable, in turn, in OFPROTO.
 *
 * All parameters are evaluated multiple times. */
#define OFPROTO_FOR_EACH_TABLE(TABLE, OFPROTO)              \
    for ((TABLE) = (OFPROTO)->tables;                       \
         (TABLE) < &(OFPROTO)->tables[(OFPROTO)->n_tables]; \
         (TABLE)++)

/* An OpenFlow flow within a "struct ofproto".
 *
 * With few exceptions, ofproto implementations may look at these fields but
 * should not modify them.
 *
 *
 * Thread-safety
 * =============
 *
 * Except near the beginning or ending of its lifespan, rule 'rule' belongs to
 * the classifier rule->ofproto->tables[rule->table_id].cls.  The text below
 * calls this classifier 'cls'.
 *
 * Motivation
 * ----------
 *
 * The thread safety rules described here for "struct rule" are motivated by
 * two goals:
 *
 *    - Prevent threads that read members of "struct rule" from reading bad
 *      data due to changes by some thread concurrently modifying those
 *      members.
 *
 *    - Prevent two threads making changes to members of a given "struct rule"
 *      from interfering with each other.
 *
 *
 * Rules
 * -----
 *
 * A rule 'rule' may be accessed without a risk of being freed by a thread
 * until the thread quiesces (i.e., rules are RCU protected and destructed
 * using ovsrcu_postpone()).  Code that needs to hold onto a rule for a
 * while should increment 'rule->ref_count' either with ofproto_rule_ref()
 * (if 'ofproto_mutex' is held), or with ofproto_rule_try_ref() (when some
 * other thread might remove the rule from 'cls').  ofproto_rule_try_ref()
 * will fail if the rule has already been scheduled for destruction.
 *
 * 'rule->ref_count' protects 'rule' from being freed.  It doesn't protect the
 * rule from being deleted from 'cls' (that's 'ofproto_mutex') and it doesn't
 * protect members of 'rule' from modification (that's 'rule->mutex').
 *
 * 'rule->mutex' protects the members of 'rule' from modification.  It doesn't
 * protect the rule from being deleted from 'cls' (that's 'ofproto_mutex') and
 * it doesn't prevent the rule from being freed (that's 'rule->ref_count').
 *
 * Regarding thread safety, the members of a rule fall into the following
 * categories:
 *
 *    - Immutable.  These members are marked 'const'.
 *
 *    - Members that may be safely read or written only by code holding
 *      ofproto_mutex.  These are marked OVS_GUARDED_BY(ofproto_mutex).
 *
 *    - Members that may be safely read only by code holding ofproto_mutex or
 *      'rule->mutex', and safely written only by coding holding ofproto_mutex
 *      AND 'rule->mutex'.  These are marked OVS_GUARDED.
 */
enum OVS_PACKED_ENUM rule_state {
    RULE_INITIALIZED, /* Rule has been initialized, but not inserted to the
                       * ofproto data structures.  Versioning makes sure the
                       * rule is not visible to lookups by other threads, even
                       * if the rule is added to a classifier. */
    RULE_INSERTED,    /* Rule has been inserted to ofproto data structures and
                       * may be visible to lookups by other threads. */
    RULE_REMOVED,     /* Rule has been removed from ofproto data structures,
                       * and may still be visible to lookups by other threads
                       * until they quiesce, after which the rule will be
                       * removed from the classifier as well. */
};

struct rule {
    /* Where this rule resides in an OpenFlow switch.
     * These are immutable once the rule is constructed, hence 'const'. */
    struct ofproto *const ofproto; /* The ofproto that contains this rule. */
    const struct cls_rule cr;      /* In owning ofproto's classifier. */
    const uint8_t table_id;        /* Index in ofproto's 'tables' array. */

    /* Number of references.
     * The classifier owns one reference.
     * Any thread trying to keep a rule from being freed should hold its own
     * reference. */

    /* A "flow cookie" is the OpenFlow name for a 64-bit value associated with
     * a flow. */

    /* Removal reason for sending flow removed message.
     * Used only if 'flags' has OFPUTIL_FF_SEND_FLOW_REM set and if the
     * value is not OVS_OFPRR_NONE. */

    /* OpenFlow actions.  See struct rule_actions for more thread-safety
     * notes. */

    /* In owning meter's 'rules' list.  An empty list if there is no meter. */

    /* Flow monitors (e.g. for NXST_FLOW_MONITOR, related to struct ofmonitor).
     *
     * 'add_seqno' is the sequence number when this rule was created.
     * 'modify_seqno' is the sequence number when this rule was last modified.
     * See 'monitor_seqno' in connmgr.c for more information. */

    /* Optimisation for flow expiry.  In ofproto's 'expirable' list if this
     * rule is expirable, otherwise empty. */
};

void ofproto_rule_ref(struct rule *);
bool ofproto_rule_try_ref(struct rule *);
void ofproto_rule_unref(struct rule *);

static inline const struct rule_actions * rule_get_actions(const struct rule *);
static inline bool rule_is_table_miss(const struct rule *);
static inline bool rule_is_hidden(const struct rule *);

/* A set of actions within a "struct rule".
 *
 *
 * Thread-safety
 * =============
 *
 * A struct rule_actions may be accessed without a risk of being freed by
 * code that holds 'rule->mutex' (where 'rule' is the rule for which
 * 'rule->actions == actions') or during the RCU active period.
 *
 * All members are immutable: they do not change during the rule's
 * lifetime. */
struct rule_actions {
    /* Flags.
     *
     * 'has_meter' is true if 'ofpacts' contains an OFPACT_METER action.
     *
     * 'has_learn_with_delete' is true if 'ofpacts' contains an OFPACT_LEARN
     * action whose flags include NX_LEARN_F_DELETE_LEARNED. */
    bool has_meter;
    bool has_learn_with_delete;
    bool has_groups;

    /* Actions. */
    uint32_t ofpacts_len;         /* Size of 'ofpacts', in bytes. */
    struct ofpact ofpacts[];      /* Sequence of "struct ofpacts". */
};
BUILD_ASSERT_DECL(offsetof(struct rule_actions, ofpacts) % OFPACT_ALIGNTO == 0);

const struct rule_actions *rule_actions_create(const struct ofpact *, size_t);
void rule_actions_destroy(const struct rule_actions *);
bool ofproto_rule_has_out_port(const struct rule *, ofp_port_t port)
    OVS_REQUIRES(ofproto_mutex);

#define DECL_OFPROTO_COLLECTION(TYPE, NAME)                             \
    DECL_OBJECT_COLLECTION(TYPE, NAME)                                  \
static inline void NAME##_collection_ref(struct NAME##_collection *coll)   \
{                                                                       \
    for (size_t i = 0; i < coll->collection.n; i++) {                   \
        ofproto_##NAME##_ref((TYPE)coll->collection.objs[i]);           \
    }                                                                   \
}                                                                       \
                                                                        \
static inline void NAME##_collection_unref(struct NAME##_collection *coll) \
{                                                                       \
    for (size_t i = 0; i < coll->collection.n; i++) {                   \
        ofproto_##NAME##_unref((TYPE)coll->collection.objs[i]);         \
    }                                                                   \
}

DECL_OFPROTO_COLLECTION (struct rule *, rule)

#define RULE_COLLECTION_FOR_EACH(RULE, RULES)                           \
    for (size_t i__ = 0;                                                \
         i__ < rule_collection_n(RULES)                                 \
             ? (RULE = rule_collection_rules(RULES)[i__]) != NULL : false; \
         i__++)

/* Pairwise iteration through two rule collections that must be of the same
 * size. */
#define RULE_COLLECTIONS_FOR_EACH(RULE1, RULE2, RULES1, RULES2)        \
    for (size_t i__ = 0;                                               \
         i__ < rule_collection_n(RULES1)                               \
             ? ((RULE1 = rule_collection_rules(RULES1)[i__]),          \
                (RULE2 = rule_collection_rules(RULES2)[i__]) != NULL)  \
             : false;                                                  \
         i__++)

/* Limits the number of flows allowed in the datapath. Only affects the
 * ofproto-dpif implementation. */
extern unsigned ofproto_flow_limit;

/* Maximum idle time (in ms) for flows to be cached in the datapath.
 * Revalidators may expire flows more quickly than the configured value based
 * on system load and other factors. This variable is subject to change. */
extern unsigned ofproto_max_idle;

/* Number of upcall handler and revalidator threads. Only affects the
 * ofproto-dpif implementation. */
extern size_t n_handlers, n_revalidators;

static inline struct rule *rule_from_cls_rule(const struct cls_rule *);

void ofproto_rule_expire(struct rule *rule, uint8_t reason)
    OVS_REQUIRES(ofproto_mutex);
void ofproto_rule_delete(struct ofproto *, struct rule *)
    OVS_EXCLUDED(ofproto_mutex);
void ofproto_rule_reduce_timeouts__(struct rule *rule, uint16_t idle_timeout,
                                    uint16_t hard_timeout)
    OVS_REQUIRES(ofproto_mutex) OVS_EXCLUDED(rule->mutex);
void ofproto_rule_reduce_timeouts(struct rule *rule, uint16_t idle_timeout,
                                  uint16_t hard_timeout)
    OVS_EXCLUDED(ofproto_mutex);

/* A group within a "struct ofproto", RCU-protected. */
struct ofgroup {
    /* Group versioning. */
    struct versions versions;

    /* Number of references.
     *
     * This is needed to keep track of references to the group in the xlate
     * module.
     *
     * If the main thread removes the group from an ofproto, we need to
     * guarantee that the group remains accessible to users of
     * xlate_group_actions and the xlate_cache, as the xlate_cache will not be
     * cleaned up until the corresponding datapath flows are revalidated. */

    /* No lock is needed to protect the fields below since they are not
     * modified after construction. */
};

struct ofgroup *ofproto_group_lookup(const struct ofproto *ofproto,
                                     uint32_t group_id, ovs_version_t version,
                                     bool take_ref);

void ofproto_group_ref(struct ofgroup *);
bool ofproto_group_try_ref(struct ofgroup *);
void ofproto_group_unref(struct ofgroup *);

void ofproto_group_delete_all(struct ofproto *)
    OVS_EXCLUDED(ofproto_mutex);

DECL_OFPROTO_COLLECTION (struct ofgroup *, group)

#define GROUP_COLLECTION_FOR_EACH(GROUP, GROUPS)                        \
    for (size_t i__ = 0;                                                \
         i__ < group_collection_n(GROUPS)                               \
             ? (GROUP = group_collection_groups(GROUPS)[i__]) != NULL: false; \
         i__++)

/* Pairwise iteration through two group collections that must be of the same
 * size. */
#define GROUP_COLLECTIONS_FOR_EACH(GROUP1, GROUP2, GROUPS1, GROUPS2)    \
    for (size_t i__ = 0;                                                \
         i__ < group_collection_n(GROUPS1)                              \
             ? ((GROUP1 = group_collection_groups(GROUPS1)[i__]),       \
                (GROUP2 = group_collection_groups(GROUPS2)[i__]) != NULL) \
             : false;                                                   \
         i__++)

/* ofproto class structure, to be defined by each ofproto implementation.
 *
 *
 * Data Structures
 * ===============
 *
 * These functions work primarily with four different kinds of data
 * structures:
 *
 *   - "struct ofproto", which represents an OpenFlow switch.
 *
 *   - "struct ofport", which represents a port within an ofproto.
 *
 *   - "struct rule", which represents an OpenFlow flow within an ofproto.
 *
 *   - "struct ofgroup", which represents an OpenFlow 1.1+ group within an
 *     ofproto.
 *
 * Each of these data structures contains all of the implementation-independent
 * generic state for the respective concept, called the "base" state.  None of
 * them contains any extra space for ofproto implementations to use.  Instead,
 * each implementation is expected to declare its own data structure that
 * contains an instance of the generic data structure plus additional
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
 *            "alloc"       "construct"       "destruct"       "dealloc"
 *            ------------  ----------------  ---------------  --------------
 *   ofproto  ->alloc       ->construct       ->destruct       ->dealloc
 *   ofport   ->port_alloc  ->port_construct  ->port_destruct  ->port_dealloc
 *   rule     ->rule_alloc  ->rule_construct  ->rule_destruct  ->rule_dealloc
 *   group    ->group_alloc ->group_construct ->group_destruct ->group_dealloc
 *
 * "ofproto", "ofport", and "group" have this exact life cycle.  The "rule"
 * data structure also follow this life cycle with some additional elaborations
 * described under "Rule Life Cycle" below.
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
 * Conventions
 * ===========
 *
 * Most of these functions return 0 if they are successful or a positive error
 * code on failure.  Depending on the function, valid error codes are either
 * errno values or OFPERR_* OpenFlow error codes.
 *
 * Most of these functions are expected to execute synchronously, that is, to
 * block as necessary to obtain a result.  Thus, these functions may return
 * EAGAIN (or EWOULDBLOCK or EINPROGRESS) only where the function descriptions
 * explicitly say those errors are a possibility.  We may relax this
 * requirement in the future if and when we encounter performance problems. */

struct ofproto_class {
    /* Initializes provider.  The caller may pass in 'iface_hints',
     * which contains an shash of "struct iface_hint" elements indexed
     * by the interface's name.  The provider may use these hints to
     * describe the startup configuration in order to reinitialize its
     * state.  The caller owns the provided data, so a provider must
     * make copies of anything required.  An ofproto provider must
     * remove any existing state that is not described by the hint, and
     * may choose to remove it all. */

};

extern const struct ofproto_class ofproto_dpif_class;

int ofproto_class_register(const struct ofproto_class *);
int ofproto_class_unregister(const struct ofproto_class *);

/* Criteria that flow_mod and other operations use for selecting rules on
 * which to operate. */
struct rule_criteria {
    /* An OpenFlow table or 255 for all tables. */
    uint8_t table_id;

    /* OpenFlow matching criteria.  Interpreted different in "loose" way by
     * collect_rules_loose() and "strict" way by collect_rules_strict(), as
     * defined in the OpenFlow spec. */
    struct cls_rule cr;
    ovs_version_t version;

    /* Matching criteria for the OpenFlow cookie.  Consider a bit B in a rule's
     * cookie and the corresponding bits C in 'cookie' and M in 'cookie_mask'.
     * The rule will not be selected if M is 1 and B != C.  */
    ovs_be64 cookie;
    ovs_be64 cookie_mask;

    /* Selection based on actions within a rule:
     *
     * If out_port != OFPP_ANY, selects only rules that output to out_port.
     * If out_group != OFPG_ALL, select only rules that output to out_group. */
    ofp_port_t out_port;
    uint32_t out_group;

    /* If true, collects only rules that are modifiable. */
    bool include_hidden;
    bool include_readonly;
};

/* flow_mod with execution context. */
struct ofproto_flow_mod {
    /* Allocated by 'init' phase, may be freed after 'start' phase, as these
     * are not needed for 'revert' nor 'finish'.
     *
     * This structure owns a reference to 'temp_rule' (if it is nonnull) that
     * must be eventually be released with ofproto_rule_unref().  */
    struct rule *temp_rule;
    struct rule_criteria criteria;
    struct cls_conjunction *conjs;
    size_t n_conjs;

    /* Replicate needed fields from ofputil_flow_mod to not need it after the
     * flow has been created. */
    uint16_t command;
    bool modify_cookie;
    /* Fields derived from ofputil_flow_mod. */
    bool modify_may_add_flow;
    bool modify_keep_counts;
    enum nx_flow_update_event event;

    /* These are only used during commit execution.
     * ofproto_flow_mod_uninit() does NOT clean these up. */
    ovs_version_t version;              /* Version in which changes take
                                         * effect. */
    bool learn_adds_rule;               /* Learn execution adds a rule. */
    struct rule_collection old_rules;   /* Affected rules. */
    struct rule_collection new_rules;   /* Replacement rules. */
};

void ofproto_flow_mod_uninit(struct ofproto_flow_mod *);

/* port_mod with execution context. */
struct ofproto_port_mod {
    struct ofputil_port_mod pm;
    struct ofport *port;                /* Affected port. */
};

/* flow_mod with execution context. */
struct ofproto_group_mod {
    struct ofputil_group_mod gm;

    ovs_version_t version;              /* Version in which changes take
                                         * effect. */
    struct ofgroup *new_group;          /* New group. */
    struct group_collection old_groups; /* Affected groups. */
};

/* packet_out with execution context. */
struct ofproto_packet_out {
    ovs_version_t version;
    struct dp_packet *packet;
    struct flow *flow;
    struct ofpact *ofpacts;
    size_t ofpacts_len;

    void *aux;   /* Provider private. */
};

void ofproto_packet_out_uninit(struct ofproto_packet_out *);

enum ofperr ofproto_flow_mod(struct ofproto *, const struct ofputil_flow_mod *)
    OVS_EXCLUDED(ofproto_mutex);
enum ofperr ofproto_flow_mod_init_for_learn(struct ofproto *,
                                            const struct ofputil_flow_mod *,
                                            struct ofproto_flow_mod *)
    OVS_EXCLUDED(ofproto_mutex);
enum ofperr ofproto_flow_mod_learn(struct ofproto_flow_mod *, bool keep_ref,
                                   unsigned limit, bool *below_limit)
    OVS_EXCLUDED(ofproto_mutex);
enum ofperr ofproto_flow_mod_learn_refresh(struct ofproto_flow_mod *ofm);
enum ofperr ofproto_flow_mod_learn_start(struct ofproto_flow_mod *ofm)
    OVS_REQUIRES(ofproto_mutex);
void ofproto_flow_mod_learn_revert(struct ofproto_flow_mod *ofm)
    OVS_REQUIRES(ofproto_mutex);
void ofproto_flow_mod_learn_finish(struct ofproto_flow_mod *ofm,
                                          struct ofproto *orig_ofproto)
    OVS_REQUIRES(ofproto_mutex);
void ofproto_add_flow(struct ofproto *, const struct match *, int priority,
                      const struct ofpact *ofpacts, size_t ofpacts_len)
    OVS_EXCLUDED(ofproto_mutex);
void ofproto_delete_flow(struct ofproto *, const struct match *, int priority)
    OVS_REQUIRES(ofproto_mutex);
void ofproto_flush_flows(struct ofproto *);

enum ofperr ofproto_check_ofpacts(struct ofproto *,
                                  const struct ofpact ofpacts[],
                                  size_t ofpacts_len)
    OVS_REQUIRES(ofproto_mutex);

static inline const struct rule_actions *
rule_get_actions(const struct rule *rule)
{
    return rule->actions;
}

/* Returns true if 'rule' is an OpenFlow 1.3 "table-miss" rule, false
 * otherwise.
 *
 * ("Table-miss" rules are special because a packet_in generated through one
 * uses OFPR_NO_MATCH as its reason, whereas packet_ins generated by any other
 * rule use OFPR_ACTION.) */
static inline bool
rule_is_table_miss(const struct rule *rule)
{
    return rule->cr.priority == 0 && cls_rule_is_catchall(&rule->cr);
}

/* Returns true if 'rule' should be hidden from the controller.
 *
 * Rules with priority higher than UINT16_MAX are set up by ofproto itself
 * (e.g. by in-band control) and are intentionally hidden from the
 * controller. */
static inline bool
rule_is_hidden(const struct rule *rule)
{
    return rule->cr.priority > UINT16_MAX;
}

static inline struct rule *
rule_from_cls_rule(const struct cls_rule *cls_rule)
{
    return cls_rule ? CONTAINER_OF(cls_rule, struct rule, cr) : NULL;
}

static inline const struct tun_table *
ofproto_get_tun_tab(const struct ofproto *ofproto)
{
    return ovsrcu_get(struct tun_table *, &ofproto->metadata_tab);
}

#endif /* ofproto/ofproto-provider.h */
