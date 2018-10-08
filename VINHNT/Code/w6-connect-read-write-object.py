import rados
try:
	cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
except TypeError as e:
	print 'Argument validation error: ', e
	raise e

print "create cluster handle."
try:
	cluster.connect()
except Exception as e:
	print "connection error: ", e
	raise e
finally: 
	print "connected to the cluster"

print "\n\n I/O context and object operations"
print "======================================"

try:
	cluster_stats = cluster.get_cluster_stats()
except Exception as e:
	print "error", e
	raise e
finally: 
	print "==============cluster_status============"
	for key, value in cluster_stats.iteritems():
		print key, value

print "\n\nPool Operations"
print "====================================="

print "\nAvalable Pools"
pools = cluster.list_pools()

for pool in pools:
	print pool

#print "\nCreate 'test' pool"
#cluster.create_pool('test')

print "\nPool named 'test' exists: " + str(cluster.pool_exists('test'))
print "\nVerify 'test' pool exists"

pools = cluster.list_pools()
for pool in pools:
	print pool
print "\n==================================="
ioctx = cluster.open_ioctx('test')
print "\nWriting object 'hw' with contents 'Hello world!' to pool 'data'"
#ioctx.write_full("hw", "Hello World!")

#ioctx.write_full("name", "My name is Vinh")

#ioctx.write_full("wtf", "What the fuck")

object_iterator = ioctx.list_objects()

#ioctx.write_full("person", "Information of one person")
#ioctx.set_xattr("person", "name", "Nguyen Trong Vinh")
#ioctx.set_xattr("person", "olds", "23 years old")
#ioctx.set_xattr("person", "nation", "Vietnam")

while True :
	try: 
		rados_object = object_iterator.next()
		print "Object contents: " + rados_object.read()
	except StopIteration :
		break
print ioctx.get_xattr("person", "name")
print ioctx.get_xattr("person", "olds")
print ioctx.get_xattr("person", "nation")
