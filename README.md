MPT研究报告

相关概念

·区块链
区块链是随着比特币等数字加密货币的日益普及而逐渐兴起的一种全新的去中心化基础架构与分布式计算范式， 已经引起政府部门、金融机构、科技企业和资本市场的高度重视与广泛关注。 区块链技术具有去中心化、时序数据、集体维护、可编程和安全可信等特点, 特别适合构建可编程的货币系统、金融系统乃至宏观社会系统。 
·哈希（散列）
哈希（hash），一般翻译做“散列”，就是把任意长度的输入（又叫做预映射， pre-image），通过散列算法，变换成固定长度的输出，该输出就是散列值。这种转换是一种压缩映射，也就是，散列值的空间通常远小于输入的空间，不同的输入可能会散列成相同的输出，所以不可能从散列值来唯一的确定输入值。简单的说就是一种将任意长度的消息压缩到某一固定长度的消息摘要的函数。

·梅克尔树
梅克尔树是区块链的重要数据结构， 其作用是快速归纳和校验区块数据的存在性和完整性。一般意义上来讲，它是哈希大量聚集数据“块”的一种方式，它依赖于将这些数据“块”分裂成较小单位的数据块，每一个bucket块仅包含几个数据“块”，然后取每个bucket单位数据块再次进行哈希，重复同样的过程，直至剩余的哈希总数仅变为1。

基本概念
Merkle Tree是一种数据结构，用来验证计算机之间存储和传输数据的一致性，如果不使用这一数据结构，一致性的验证需要消耗大量的存储和网络资源，如比对计算机之间的所有数据；使用Merkle Tree，只需要比对merkle root（根节点）就可以达到相同的效果。整个过程，简单的描述如下：
·将数据通过哈希之后放置在叶子节点之中；
·将相邻两个数据的哈希值组合在一起，得出一个新的哈希值；
·依次类推，直到只有一个节点也就是根节点；
·在验证另外的计算机拥有和本机相同的数据时，只需验证其提供的根节点和自己的根节点一致即可。
Merke Tree使用了加密哈希算法来快速验证数据一致性，常用的加密哈希算法有SHA-256，SHA-3，Blake2等，它们可以做到：
·相同的输入有相同的输出；
·对任意数据可以实现快速计算；
·从哈希值无法推断出原信息；
·不会碰撞（即不同输入对应相同输出）；
·输入即使只有很小的改变，输出也会有极大不同。

构成方式
梅克尔树通常包含区块体的底层 (交易) 数据库， 区块头的根哈希值 (即Merkle根) 以及所有沿底层区块数据到根哈希的分支。梅克尔树运算过程一般是将区块体的数据进行分组哈希， 并将生成的新哈希值插入到梅克尔树中，如此递归直到只剩最后一个根哈希值并记为区块头的 Merkle根。 最常见的梅克尔树是比特币采用的二叉梅克尔树,，其每个哈希节点总是包含两个相邻的数据块或其哈希值  。其特点如下：
1、梅克尔树是一种树，大多数是二叉树，也可以多叉树，无论是几叉树，它都具有树结构的所有特点；
2、Merkle Tree的叶子节点的value是数据集合的单元数据或者单元数据HASH。
3、非叶子节点的value是根据它下面所有的叶子节点值，然后按照Hash算法计算而得出的。

相关参数及操作
（附实现代码）
Insert Key Value
参数列表：
·当前节点n
·节点与待插入的key的共同前缀prefix
·待插入的key
·待插入的value
·返回值列表
·是否是脏数据
·新节点引用
·错误消息
操作步骤：
·如果待插入的key的长度为0，那么意味着在当前节点上更新待插入的value；
·判断当前节点n的类型
shortNode（压缩节点）
·计算当前节点n的key与待插入的key的相同前缀下标+1（返回的是不一致的第一个下标）
·如果相同前缀下标与当前节点n的key长度一致，也就意味着待插入的key与当前节点n的key完全匹配，就是更新当前节点n的value。递归调用当前方法，参数为当前节点n的value，prefix+之前计算的相同前缀，待插入的key剩下的部分，以及value。完成后将返回的节点作为当前节点的value返回
·如果不一致，也就意味着有了分支。新建fullNode，分别对 当前节点n的key 和 待插入的key 的不一致下标开始递归调用插入后续key及value，返回值为fullNode的两个分支。节点n插入的是n的value，另一分支为待插入的value。递归完成后，当前调用返回shortNode，key为相同前缀，value为新建的fullNode。还有一种情况，如果最开始节点key就不匹配，直接就返回fullNode，因为没有共同前缀key
fullNode（分支节点）
因为是分支节点，那么每个child的key只有一位，那么只要将value插入跟待插入的key的第一位相同的child位置就可以了。
hashNode
哈希节点先去数据库中load相关节点的数据，之后再递归调用
其他
直接将key，value包装成shortNode返回
Delete Key
参数列表：
·当前节点n
·节点与待删除的key的共同prefix
·待删除的key
·返回值列表
·是否脏数据
·新节点引用
·错误信息

shortNode
·寻找节点n的key与待删除的key的共同前缀下标+1
·如果下标小于节点n的key的长度，表示key没匹配上，直接返回
·如果下标等于节点n的key的长度，表示该节点n正是需要被删除的节点，删除操作就是返回的新节点引用为nil，当前节点n在内存中就成了野节点，被mpt树排除在外了
·剩下的情况，表示待删除的key存在当前节点n的子树，递归调用删除方法，返回后，这里再判断一次返回的新节点child的类型：
·shortNode：父节点n与子节点child都是一种节点类型，直接合并key，value为child的value。
·其他：也是返回shortNode，其key为当前节点n的key，value是递归调用返回的child
fullNode
和插入类似，将待删除的key的首位与该节点对应的child带入递归调用，返回后更新对应child的value
删除之后需要检查分叉节点的所有child是否有多于2个非nil的child，如果少于2个，就可以合并child
hashNode：先从数据库load数据，在递归调用
valueNode：直接删除当前节点
Update Key Value
更新其实是Insert与Delete的整合

Get Key Value
参数列表：
·当前节点n
·待查找的key
·已经过滤的子key在key中的pos
·返回值列表
·查找的value
·新节点的引用
·是否从数据库中load数据
·错误信息

valueNode：直接返回节点n的value
shortNode
如果剩余的key（查找的key的长度-pos）的长度小于节点n的key的长度或者两个key的前缀不匹配，表示在树种没有找到对应的key，直接返回
到这里了表示待查找的key与该节点n的key是匹配的，那么只需要将节点n的value和剩余的待查找的子key带入递归
fullNode：同样套路，找到对应key的child递归调用
hashNode：先载入数据，在递归调用

应用
·数字签名
最初Merkle Tree目的是高效的处理Lamport one-time signatures。 每一个Lamport key只能被用来签名一个消息，但是与Merkle tree结合可以来签名多条Merkle。这种方法成为了一种高效的数字签名框架，即Merkle Signature Scheme。
在P2P网络中，Merkle Tree用来确保从其他节点接受的数据块没有损坏且没有被替换，甚至检查其他节点不会欺骗或者发布虚假的块。 [5]
·Trusted Computing
可信计算是可信计算组为分布式计算环境中参与节点的计算平台提供端点可信性而提出的。可信计算技术在计算平台的硬件层引入可信平台模块(Trusted Platform，TPM)，实际上为计算平台提供了基于硬件的可信根(Root of trust，RoT)。从可信根出发，使用信任链传递机制，可信计算技术可对本地平台的硬件及软件实施逐层的完整性度量，并将度量结果可靠地保存再TPM的平台配置寄存器(Platform configuration register，PCR)中，此后远程计算平台可通过远程验证机制(Remote Attestation)比对本地PCR中度量结果，从而验证本地计算平台的可信性。可信计算技术让分布式应用的参与节点摆脱了对中心服务器的依赖，而直接通过用户机器上的TPM芯片来建立信任，使得创建扩展性更好、可靠性更高、可用性更强的安全分布式应用成为可能。可信计算技术的核心机制是远程验证(remote attestation),分布式应用的参与结点正是通过远程验证机制来建立互信,从而保障应用的安全。 
·IPFS
IPFS(InterPlanetary File System)是很多NB的互联网技术的综合体，如DHT( Distributed HashTable，分布式哈希表)，Git版本控制系统，Bittorrent等。它创建了一个P2P的集群，这个集群允许IPFS对象的交换。全部的IPFS对象形成了一个被称作Merkle DAG的加密认证数据结构。
·比特币
梅克尔树最早的应用是比特币，它是由中本聪在2009年描述并创建的。Bitcoin的Blockchain利用Merkle proofs来存储每个区块的交易。

优点
相比于哈希表，使用前缀树来进行查询拥有共同前缀key的数据时十分高效，例如在字典中查找前缀为pre的单词，对于哈希表来说，需要遍历整个表，时间效率为O(n)；然而对于前缀树来说，只需要在树中找到前缀为pre的节点，且遍历以这个节点为根节点的子树即可。
但是对于最差的情况（前缀为空串），时间效率为O(n)，仍然需要遍历整棵树，此时效率与哈希表相同。
相比于哈希表，在前缀树不会存在哈希冲突的问题。
高效的字符串查找：前缀树可以非常高效地进行字符串的查找，尤其适用于前缀匹配或者模式匹配的场景。相较于哈希表等其他数据结构，前缀树不需要进行哈希计算，因此查找速度更快。
内存利用率高：前缀树可以共享相同前缀的节点，因此在存储具有公共前缀的字符串时，只需要存储一份前缀信息，大大节省了内存空间。
便于字符串排序：前缀树具有天然的排序性质，可以方便地对字符串进行排序操作，这在某些应用中十分重要。

缺点
直接查找效率低下：前缀树的查找效率是O(m)，m为所查找节点的key长度，而哈希表的查找效率为O(1)。且一次查找会有m次IO开销，相比于直接查找，无论是速率、还是对磁盘的压力都比较大。
可能会造成空间浪费：当存在一个节点，其key值内容很长（如一串很长的字符串），当树中没有与他相同前缀的分支时，为了存储该节点，需要创建许多非叶子节点来构建根节点到该节点间的路径，造成了存储空间的浪费。
空间消耗较大：前缀树在存储大量字符串时，可能会占用较多的内存空间。特别是当字符串长度相差很大时，树的深度会增加，导致内存消耗更大
构建和维护成本较高：构建和维护前缀树需要一定的时间和计算资源。每插入或删除一个字符串，都需要进行节点的分裂或合并操作，这可能会导致树的形状变动较频繁。
不适用于通用键-值存储：前缀树主要用于字符串匹配和查找，对于通用的键值对存储，需要在树的节点中额外维护值的信息，可能会增加实现的复杂性。
