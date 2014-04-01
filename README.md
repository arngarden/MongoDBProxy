MongoDBProxy
============

MongoDBProxy is used to create a proxy around a MongoDB-connection in order to automatically handle 
AutoReconnect-exceptions.
You use MongoDBProxy in the same way you would an ordinary MongoDB-connection but don't need to worry 
about handling AutoReconnects by yourself.

Usage:

import pymongo

import mongodb_proxy

safe_conn = mongodb_proxy.MongoProxy(pymongo.MongoReplicaSetClient(replicaSet='blog_rs')

safe_conn.blogs.posts.insert(post)

**See here for more details:**
http://www.arngarden.com/2013/04/29/handling-mongodb-autoreconnect-exceptions-in-python-using-a-proxy/


**Contributors**:

Jonathan Kamens (https://github.com/jikamens)

Michael Cetrulo (https://github.com/git2samus)

Richard Frank (https://github.com/richafrank)

David Lindquist (https://github.com/dlindquist)
