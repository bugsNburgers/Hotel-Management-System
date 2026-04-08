# 📝 MCQ Bank — Lab 7 (MinIO & Ceph) + Lab 8 (Raft Consensus)
## 1-Mark Questions

---

**Q1.** What problem does the Raft consensus algorithm primarily solve?

- A) Load balancing across web servers
- B) Leader election and maintaining consistency in a distributed system
- C) Container resource allocation
- D) Network packet routing

> **Answer: B**

---

**Q2.** In a Raft cluster, what are the two roles that non-leader nodes take?

- A) Master and Slave
- B) Primary and Secondary
- C) Leader and Coordinator
- D) Follower and Candidate

> **Answer: D**

---

**Q3.** In a 3-node Raft cluster, what is the minimum number of nodes that must be available for the cluster to remain functional?

- A) 1
- B) 2
- C) 3
- D) 0

> **Answer: B**

---

**Q4.** What is a "quorum" in the context of Raft?

- A) The total number of nodes in a cluster
- B) The maximum number of nodes that can fail
- C) The minimum number of nodes required to make a valid decision (majority)
- D) A backup node that holds state

> **Answer: C**

---

**Q5.** In a 5-node Raft cluster, what is the quorum (majority) size?

- A) 2
- B) 3
- C) 4
- D) 5

> **Answer: B**

---

**Q6.** What happens in Raft when the current leader node fails?

- A) The cluster shuts down permanently
- B) The oldest node automatically becomes leader
- C) A new leader election is triggered among the remaining nodes
- D) All data is lost and the cluster restarts

> **Answer: C**

---

**Q7.** What Docker command is used to view live, streaming logs of a running container?

- A) `docker logs --stream <container>`
- B) `docker logs -f <container>`
- C) `docker inspect <container>`
- D) `docker attach <container>`

> **Answer: B**

---

**Q8.** Which command stops a specific running Docker container?

- A) `docker kill <container>`
- B) `docker remove <container>`
- C) `docker stop <container>`
- D) `docker pause <container>`

> **Answer: C**

---

**Q9.** In the Raft experiment, what happens when a stopped node is restarted (e.g., `docker start node1`)?

- A) It immediately becomes the new leader
- B) It rejoins the cluster as a follower
- C) It triggers another leader election
- D) It creates a new independent cluster

> **Answer: B**

---

**Q10.** What does the `-f` flag do in `docker logs -f node1`?

- A) Filters logs by error level
- B) Follows (streams) the log output in real time
- C) Saves logs to a file
- D) Forces showing all historical logs

> **Answer: B**

---

**Q11.** Which file defines the multi-container setup (nodes, networks) in the Raft lab?

- A) `node.py`
- B) `Dockerfile`
- C) `requirements.txt`
- D) `docker-compose.yml`

> **Answer: D**

---

**Q12.** What is the purpose of a Docker network in the Raft lab?

- A) To limit each container's internet access
- B) To allow the Raft nodes (containers) to communicate with each other
- C) To persist node state across restarts
- D) To expose the Raft nodes to external clients

> **Answer: B**

---

**Q13.** What does `docker compose down` do?

- A) Pauses all running containers
- B) Stops and removes all containers, networks defined in the compose file
- C) Deletes all Docker images on the system
- D) Restarts all services

> **Answer: B**

---

**Q14.** In a 5-node Raft cluster, you stop 2 nodes. The cluster:

- A) Becomes completely unavailable
- B) Stays functional because the remaining 3 nodes form a quorum
- C) Elects 2 leaders to compensate
- D) Resets all state

> **Answer: B**

---

**Q15.** What does `docker network inspect <network-name>` show?

- A) The resource usage of all containers
- B) The network configuration including connected containers, subnet, and gateway
- C) The logs of all containers on the network
- D) The Dockerfile used to build images

> **Answer: B**

---

## 2-Mark Questions

---

**Q16.** In a 5-node Raft cluster, nodes 4 and 5 are stopped. The cluster continues to work. Then node 3 is also stopped. What happens and why?

- A) Cluster continues — 2 nodes are enough for any cluster
- B) Cluster becomes unavailable — only 2 of 5 nodes remain, which is less than the quorum of 3, so no leader can be elected
- C) node1 automatically becomes leader with distributed authority
- D) The cluster splits into two independent clusters

> **Answer: B**
> *Explanation: Raft requires a majority (⌊n/2⌋ + 1) to elect a leader. For 5 nodes, quorum = 3. With only 2 nodes remaining, quorum cannot be achieved.*

---

**Q17.** Why does Raft require a majority (quorum) to elect a leader instead of any single node being allowed to declare itself leader?

- A) To reduce network bandwidth
- B) To prevent "split-brain" — where two isolated partitions each elect their own leader, causing inconsistent state
- C) To ensure the most powerful node is always leader
- D) Because Docker containers cannot communicate without majority consensus

> **Answer: B**
> *Explanation: Without quorum, a network partition could result in two leaders making conflicting decisions — called split-brain. Quorum ensures only one partition can elect a leader.*

---

**Q18.** A node was the leader and then got stopped (simulating failure). After restarting it, it becomes a follower instead of reclaiming leadership. Why?

- A) The node's data was corrupted during the stop
- B) During its absence, a new leader was elected by the remaining nodes. The restarted node rejoins as a follower and accepts the current leader's authority
- C) Docker always assigns the follower role to restarted containers
- D) Raft does not allow a previously failed node to ever become leader

> **Answer: B**

---

**Q19.** What is the significance of the Raft consensus algorithm in practical distributed systems like databases or key-value stores?

- A) It eliminates the need for replication
- B) It ensures all nodes agree on the same sequence of operations (consistency), even when some nodes fail
- C) It improves query performance by distributing reads across all nodes
- D) It removes the need for persistent storage

> **Answer: B**

---

**Q20.** In the Raft lab, why is Docker used to simulate the distributed nodes instead of separate physical machines?

- A) Docker containers are faster than VMs for computation
- B) Docker allows multiple isolated environments on a single machine with their own networking, simulating distributed nodes without needing multiple physical machines
- C) Docker is the only way to run Python applications
- D) Physical machines cannot run Raft

> **Answer: B**

---

---

# 🟪 LAB 7: MinIO & Ceph (Storage Types)

## 1-Mark Questions

---

**Q21.** What type of storage does MinIO provide?

- A) Block storage
- B) File storage
- C) Object storage
- D) In-memory storage

> **Answer: C**

---

**Q22.** What type of storage does Ceph RBD (RADOS Block Device) provide?

- A) Object storage
- B) Block storage
- C) Cold storage
- D) Distributed file storage

> **Answer: B**

---

**Q23.** Which storage type is best suited for storing unstructured data like images, videos, and documents?

- A) Block storage
- B) File storage
- C) Object storage
- D) In-memory cache

> **Answer: C**

---

**Q24.** MinIO is described as "S3-compatible." What does this mean?

- A) MinIO only runs on Amazon servers
- B) MinIO uses the same API as Amazon S3, allowing tools built for S3 to work with MinIO
- C) MinIO stores data in S3 format files on disk
- D) MinIO requires an AWS account to function

> **Answer: B**

---

**Q25.** What is a key characteristic of Object Storage compared to Block Storage?

- A) Object storage presents as a local disk drive to applications
- B) Object storage is accessed via an API and supports rich metadata per object
- C) Object storage is constrained by fixed volume sizes
- D) Object storage is faster for database read/write operations

> **Answer: B**

---

**Q26.** In the lab's e-commerce scenario, what kind of data was stored in Ceph (block storage)?

- A) Product images and videos
- B) Customer review photos
- C) Structured data like orders, users, and inventory in a database
- D) Static HTML files

> **Answer: C**

---

**Q27.** What is the purpose of object metadata in MinIO?

- A) To compress the stored object
- B) To attach descriptive key-value pairs to an object (e.g., product name, price) retrievable without downloading the file
- C) To encrypt the object before storage
- D) To define access permissions on the object

> **Answer: B**

---

**Q28.** Which HTTP method is used in the curl command to upload a product in the lab?

- A) GET
- B) PUT
- C) POST
- D) PATCH

> **Answer: C**

---

**Q29.** What does the `x-amz-meta-` prefix in MinIO metadata keys indicate?

- A) Amazon-specific authentication header
- B) Custom user-defined metadata following the S3 convention
- C) Internal MinIO system metadata
- D) Encrypted metadata fields

> **Answer: B**

---

**Q30.** What happens to MinIO object storage when the MinIO service is stopped but the webapp is still running?

- A) Both image uploads and database operations fail
- B) Database operations continue but image uploads fail because MinIO is unavailable
- C) The system automatically switches to local file storage
- D) The webapp also crashes due to dependency

> **Answer: B**

---

**Q31.** Which storage type scales horizontally by adding more storage nodes?

- A) Block storage
- B) File storage
- C) Object storage
- D) Both A and C

> **Answer: C**

---

**Q32.** In the lab, where is the SQLite database (`ecommerce.db`) physically visible?

- A) Inside the MinIO dashboard
- B) In the local host folder `my_block_data` (via block volume mount)
- C) In the Docker container's `/tmp` directory
- D) In the MinIO bucket alongside images

> **Answer: B**

---

**Q33.** What is the concept of "Separation of Concerns" demonstrated in Experiment 4 of the lab?

- A) Different teams manage different microservices
- B) Storage (data) lives independently of application logic, so data persists even when the app container goes down
- C) Each container runs a separate operating system
- D) Block and object storage use different file formats

> **Answer: B**

---

**Q34.** What command is used to interact with the SQLite database inside the webapp container?

- A) `docker inspect`
- B) `docker exec -it <container> python -c "<sqlite query>"`
- C) `docker logs <container>`
- D) `curl http://localhost:5000/db`

> **Answer: B**

---

## 2-Mark Questions

---

**Q35.** A developer uploads an image to MinIO and stores product details in a Ceph-backed SQLite database. MinIO goes down. Which operations still work and which fail?

- A) Both image access and DB queries fail
- B) DB queries still work (Ceph/block storage is unaffected); image retrieval fails (MinIO is down)
- C) Image access still works via cache; DB fails
- D) Both continue working because Docker has redundancy

> **Answer: B**
> *Explanation: Block storage (Ceph/SQLite) and object storage (MinIO) are independent services. Failure of one does not affect the other.*

---

**Q36.** Why can you see `ecommerce.db` in the local `my_block_data` folder but NOT find the uploaded image there?

- A) The image was deleted after upload
- B) Block storage mounts like a local drive (visible on host); object storage is abstracted behind an API and not stored as a plain file on the host filesystem
- C) The image is stored in a different Docker volume
- D) MinIO encrypts images so they are invisible

> **Answer: B**

---

**Q37.** What is the key advantage of attaching metadata to objects in MinIO compared to records in a block-based database?

- A) Metadata makes the object smaller
- B) Metadata (e.g., product name, price) can be read directly from the object store without querying a separate database or downloading the file
- C) Metadata enables faster writes to block storage
- D) Metadata is only used for access control

> **Answer: B**

---

**Q38.** In Experiment 3, filling up the `my_block_data` folder causes the Flask app to throw a disk error, while MinIO continues accepting images. What storage concept does this demonstrate?

- A) Object storage is faster than block storage
- B) Block storage is constrained by fixed volume size; object storage scales horizontally and is limited only by available host/cluster space
- C) Block storage does not support large files
- D) MinIO compresses data automatically

> **Answer: B**

---

**Q39.** A company stores product images in MinIO and order data in a Ceph-backed database. They want to display product price and name on the dashboard without downloading each image. What MinIO feature makes this possible?

- A) Image thumbnails
- B) Object metadata — custom key-value pairs stored alongside the object and readable without fetching the file
- C) MinIO versioning
- D) Ceph replication

> **Answer: B**

---

**Q40.** What is the conceptual difference between how Block Storage and Object Storage handle data access?

- A) Block storage uses HTTP; object storage uses TCP
- B) Block storage presents as a raw disk volume accessed at the byte/block level (like a hard drive); object storage is accessed via APIs where each object has an ID, data, and metadata
- C) Object storage is faster for sequential reads; block storage is faster for random access
- D) They are functionally identical; only the price differs

> **Answer: B**
> *Explanation: Block storage = raw disk (databases, OS use it). Object storage = API-based with metadata (cloud files, images, backups).*

---
