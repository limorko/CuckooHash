# What
A Cuckoo Hash is a variation of the classic Hash Table data structure. The Cuckoo Hash uses multiple hash functions to keep track of where data is inserted. Each piece of information to be stored has a name, which is called a key and is connected to another piece of information called data. The data is kept in another data structure called an array ('list' in Python), which is a series of buckets that hold data, numbered from 0 and counting up. In this specific implementation of a Cuckoo Hash, the information stored in the data structure is in the form of a tuple: key and data. 

# Why
This Data Structure is very convenient because 
- Lookups are worst-case O(1) (constant time)
- Deletions are worst-case O(1)
- Insertions are amortized, expected O(1)
  
# Features 
This class contains:
- insertion method 
- deletion method
- search method
- increment method (increments the data of the corresponding keydata pair by one, or it adds a new keydata pair with 1 as the data)

The program already contains a large amount of thorough pytests that test each method in the class. 

# Inserting 
ch = CuckooHash(1)
#insert 10 key/data pairs in the cuckooHash
for i in range(10): 
    # generate a random word as the key
    r = RandomWord()
    key = r.generate()
        
    # generate a random int as the data 
    data = random.randint(0, 100)
        
    # insert the keyData pair in the cuckooHash 
    ch.insert(key, data)
    
