# "I hereby certify that this program is solely the result of my own work and  
# is in compliance with the Academic Integrity policy of the course syllabus  
# and the academic integrity policy of the CS department.”

import time
import random
import BitHash 
import pytest

# in order to run the pytests correctly, it is necessary to install the 
# RandomWordGenerator library:
# inside the Terminal insert: pip3 install Random-Word-Generator OR pip install Random-Word-Generator

from RandomWordGenerator import RandomWord


class CuckooHash(object):
    
    # This CuckooHash class will have 3 attributes:
    #
    # - Two hash arrays (lists) that will store the KeyData pairs.
    #   Each list will be size long. Size is a parameter and it is chosen in 
    #   the client code. If the client does not insert the parameter, or a 0 is
    #   inserted, then the size is automatically 1. 
    #
    # - numKeys will keep track of the number of KeyData pairs that have been inserted 
    def __init__(self, size = "start"):
        
        #if the size is 0 or has not been inserted, set it equal to 1
        if size == "start" or size == 0:
            size = 1
            
        #first hash table of length size 
        self.__hashArray1 = [None] * size
        
        #second hash table of length size 
        self.__hashArray2 = [None] * size
        
        #initially 0 keyData pairs are contained in the CuckooHash 
        self.__numKeys = 0
        
    # return current number of KeyData pairs in the CuckooHash     
    def __len__(self): return self.__numKeys
    
    # private method that will be used by: 
    #
    # - __growAndReHash: private method used by __reInsert to grow the CuckooHash
    #                    and "shuffle" the keyData pairs contained
    # - insert: method that will be invoked by the client to insert a keyData pair in the C.H.
    #
    # parameters: the two lists in which the KeyD ata pair will be inserted,
    #             the key and the data for the KeyData pair 
    #
    # if successful: returns the CH's tables as a tuple (containing the new keyData pair)
    # otherwise: returns False and the keyData pair left out of the CH
    def __insert(self, array1, array2, k, d):
        #creating a tuple that will contain the key and the data 
        keyData = (k, d)
        
        # when the key data pair will successfully be inserted into the C.H.
        # done will become True and the while loop will stop 
        done = False 
        
        # threshold 
        # if it takes more than 1 second (of evictions) to insert the keyData pair into the C.H.
        # then stop the while loop 
        max_time = 1
        
        start_time = time.time()  # remember when we started the insertion 
        
        # while there's a key that still hasn't been inserted / rehashed and inserted
        # and the threshold has not been crossed (there is not an "infinite loop" going on)         
        while not done and (time.time() - start_time) < max_time :
            
            # FIND THE FIRST TABLE'S NEST THAT COULD CONTAIN THE KEYDATA PAIR: 
            
            # first hash function
            # invoke BitHash with the 0 seed 
            hash1 = BitHash.BitHash(keyData[0], 0)
            
            # find nest1
            nest1 = hash1 % len(array1)
                
            # if the nest is empty
            if array1[nest1] == None: 
                
                # insert the keyData pair in the nest 
                array1[nest1] = keyData 
                
                # interrupt the while loop
                done = True         
        
                 
            # otherwise (if the nest already contains something else)
            # evict what is already contanined in nest1
            else:
                # keep track of what keyData pair is already contained in the nest 
                temp = array1[nest1]
                
                # insert the new keyData pair in the nest
                array1[nest1] = keyData 
                
                # evict temp (what needs to be moved because the new KeyData pair 
                # has been inserted) to the II hash table
                keyData = temp 
                
                # move it to the second hash table using the II hash funct.
                # FIND THE SECOND TABLE'S NEST THAT WILL CONTAIN THE EVICTED 
                # KEYDATA PAIR  
                # invoke BitHash with the 0 seed 
                seed2 = BitHash.BitHash(keyData[0], 0) 
                
                # second hash function 
                # invoke BitHash with the previous hash seed 
                hash2 = BitHash.BitHash(keyData[0], seed2)
                
                # find  nest2  
                nest2 = hash2 % len(array2) 
                
                
                # if nest2 is empty
                if array2[nest2] == None: 
                    
                    # insert the keyData pair in the nest 
                    array2[nest2] = keyData 
                    
                    # interrupt the while loop
                    done = True                 
                
                # otherwise (if the nest already contains something else)
                # evict what is already contanined in nest2
                else:
                    #keep track of what keyData pair is already contained in the nest2 
                    temp = array2[nest2] 
                    
                    # insert the new keyData pair in the nest2
                    array2[nest2] = keyData 
                    
                    # evict temp (what needs to be moved because the new KeyData pair 
                    # has been inserted) to the I hash table 
                    keyData = temp    
         
        # out of the while loop:
        # if done == True, the insertion was succesfull, return the two tables 
        if done: return array1, array2
        
        # otherwise the threshold was crossed, return false and the keyData pair 
        # that stayed out of the C.H. 
        return False, keyData
    
    # private method that will be used by: 
    #
    # - __reInsert: private method used to grow the CuckooHash tables and "shuffle" 
    #               the keyData pairs that are contained in the CH (tried max. 10 times)
    #
    # no parameters   
    # if successful it returns a tuple containing the grown and rehashed CH tables 
    # otherwise: returns False 
    def __growAndReHash(self):
        
        #reset the BitHash function
        BitHash.ResetBitHash()

        #create 2 new empty lists which are twice as long as the current hashTabs
        newList1 = [None] * (len(self.__hashArray1) * 2) 
        newList2 = [None] * (len(self.__hashArray2) * 2) 
        # insert the lists into a tuple
        newLists = newList1, newList2
        
        # initially stop is False
        # if the insertion of a keyData pair is not succesfull = 
        # = (__insert returns False because of too many evictions)
        # stop will become true 
        stop = False 
        
        # initially done is False, when the "re insertion" of all keyData pairs
        # is completed, done becomes True
        done = False 
        
        # while the "re insertion" of all keyDatas is not completed and 
        # each keyData pair is being inserted succesfully (__insert returns the hash tables) = 
        # + the threshold has not been crossed 
        while not done and not stop:
            
            # for each bucket position/nest in the old hashArray1
            for i in range(len(self.__hashArray1)):   
                # get the keyData pair 
                keyData = self.__hashArray1[i]
                
                # if it's not None 
                if keyData != None:
                    # insert it in the new Cuckoo Hash 
                    newLists = self.__insert(newList1, newList2, keyData[0], keyData[1])
                    
                    # if the insertion was not succesfull (__insert returned False)
                    if newLists[0] == False: 
                        # stop the while loop 
                        stop = True 
                        
            #for each bucket position in the old hashArray2
            for i in range(len(self.__hashArray2)):   
                # get the keyData pair 
                keyData = self.__hashArray2[i]
                
                # if it's not None 
                if keyData != None:
                    # insert it in the new Cuckoo Hash  
                    newLists = self.__insert(newList1, newList2, keyData[0], keyData[1])  
                    
                    # if the insertion was not succesfull (__insert returned False)
                    if newLists[0] == False:
                        # stop the while loop 
                        stop = True 
            
            # at this point, the for loops are completed and the insertions were
            # all succesfull, so the while loop stops 
            done = True 
            
        # out of the while loop  
        
        # if stop is True, an insertion was not succesfull
        if stop == True:
            # return False 
            return False 
        
        # otherwise the re hash, growth and re insertion was succesfull
        # return the tuple containing the new lists that form the CuckooHash 
        return newLists
    
    # private method that will be used by: 
    #
    # - insert: method that will be invoked by the client to insert a keyData pair in the C.H.
    #
    # no parameters   
    # returns True if the reInsertion of all keyData pairs into the larger C.H. was successful
    # return False if after 10 attemps the insertion is still not successful 
    def __reInsert(self, insertKey = "no"):
        
        # grow the C.H. and after resetting the hash function, re insert  
        # every keyData pair into the larger CH 
        newLists = self.__growAndReHash()
        
        # keep track of the number of attempts (trying to grow and re hash everything)
        growedNumTimes = 0 
        
        # while __growAndReHash has not succeeded and the 10 attempts threshold 
        # has not been crossed 
        while newLists == False and growedNumTimes < 10:
            # grow and re hash (check if it has succeeded - not False)
            newLists = self.__growAndReHash()
            # increment the num of attempts 
            growedNumTimes += 1
        
        # out of the while loop:
        # if the C.H. grew and all re insertions were successful
        if newLists != False:         
            
            # set the hashArray equal to the newList  
            newList1, newList2 = newLists
            self.__hashArray1 = newList1
            self.__hashArray2 = newList2
            
            # if there is a keyData pair that was left out during the inital insertion
            if insertKey != "no":
                # re insert it (into the new C.H.)
                self.insert(insertKey[0], insertKey[1])
                
            # __reInsert was successful so return True
            return True
         
        # otherwise return False (threshold crossed)        
        return False
    
    # private method that will be used by: 
    #
    # - insert: to check whether the keyData pair was already inserted in the CH 
    # - find: if a keyData pair is found in the CH, its data is returned 
    # - increment: to check whether the keyData pair was already inserted in the CH
    #
    # parameters: the key that being searched 
    #
    # if the key is found: returns the nest inside which it was found and the data 
    # else: return None, None 
    def __findNest(self, k):
        
        #FIND THE FIRST POSSIBLE NEST THAT CAN CONTAIN K (I HASH TABLE/FUNCTION)
        #first hash function
        #invoke BitHash.BitHash with the 0 seed 
        hash1 = BitHash.BitHash(k, 0)
        #find the nest
        nest1 = hash1 % len(self.__hashArray1)  
        
        #get what is contained in nest1
        keyData = self.__hashArray1[nest1]
        
        #if the nest contains a keyData pair (not None) and its key corresponds to k
        if keyData != None and keyData[0] == k:
            
            #return nest1 and data of the keyData pair (the key has been found)
            return nest1, keyData[1]
        
        #otherwise FIND THE SECOND/LAST POSSIBLE NEST THAT CAN CONTAIN K (II HASH TABLE/FUNCTION)
        #invoke BitHash.BitHash with the previous hash seed 
        hash2 = BitHash.BitHash(k, hash1)
        #find the nest 
        nest2 = hash2 % len(self.__hashArray2) 
        
        keyData = self.__hashArray2[nest2]
        
        #if the nest2 contains a keyData pair and its key corresponds to k
        if keyData != None and keyData[0] == k: 
            
            #return nest2 and data of the keyData pair (the key has been found)
            return nest2, keyData[1] 
        
        #otherwise, nothing has been found, so return None
        return None, None    
 
    # method that inserts key/data pair
    # uses following private methods: 
    #
    # - __findNest: to check whether the keyData pair was already inserted in the CH 
    # - __insert: to insert the keyData pair into the CH 
    # - __reInsert: in case the CH gets too full or there are too many evictions 
    #
    # parameters: the key and data being inserted into the CH 
    #
    # if the keyData pair was successfully inserted: returns True  
    # otherwise an exception is raised 
    def insert(self, k, d): 
        
        #create the keyData tuple that will be inserted in the CH 
        keyData = (k, d)
        
        # check whether the key was already inserted 
        nestFound, dataFound = self.__findNest(k) 
        
        #if the key has not been inserted yet 
        if dataFound == None:
            
            #insert the keyData pair using __insert
            insertion = self.__insert(  self.__hashArray1, self.__hashArray2, keyData[0], keyData[1]) 
            
            # if the keyData pair has been inserted successfully
            if insertion[0] != False:    
                
                #increment the total num of keys contained
                self.__numKeys += 1

                #if the hash tables are getting too full grow them and reHash everything
                if self.__numKeys >= ( len(self.__hashArray1) + len(self.__hashArray2) )* 0.5:     
                    # using __reInsert
                    reInsert = self.__reInsert()
                    
                    # the probability of the following is almost non-existent
                    # if __reInsert was not successful, raise an exception 
                    # (since it should be very very unlikely that this happens) 
                    if reInsert == False:
                        
                        #raise an exception
                        raise Exception("Insertion failed")
                    
                    # otherwise return True (insertion succeeded)
                    return True     
                return True 
            
            # if the keyData pair has not been inserted successfully (too many evictions)
            else: 
                # keep track of the keyData pair that was "left out" of the C.H. 
                keyData = insertion[1]
                
                # grow the hash tables, re hash and re insert everything into the C.H. 
                reInsert = self.__reInsert(keyData)
                
                # the probability of the following is almost non-existent
                # if __reInsert was not successful, raise an exception 
                # (since it should be very very unlikely that this happens)                 
                if reInsert == False:
                    
                    #raise an exception
                    raise Exception("Insertion failed")
                
                # otherwise return True (insertion succeeded)
                return True
          
        #if the key was already inserted in the C.H.
        else: 
            
            # if the nest already containing the key is part of the I hash table 
            # overwrite the keyData pair (the Data might have changed) in hashArray1
            if self.__hashArray1[nestFound] and self.__hashArray1[nestFound][0] == keyData[0]:
                self.__hashArray1[nestFound] = keyData
             
            # if the nest already containing the key is part of the II hash table 
            # overwrite the keyData pair (the Data might have changed) in hashArray2               
            elif self.__hashArray2[nestFound] and self.__hashArray2[nestFound][0] == keyData[0]:
                self.__hashArray2[nestFound] = keyData
              
            # the insertion was successful so it returns True   
            return True
    
    # method that searches for a key in the CH 
    # uses following private methods: 
    #
    # - __findNest: to check whether the keyData pair was found in the CH 
    #
    # parameters: the key and data being searched 
    #
    # if the key is found: the Data is returned
    # otherwise None is returned 
    def find(self, k):
        nest, data = self.__findNest(k)
        return data
        
    
    # Remove the element from the hash table(s) whose key is k
    # parameters: the key corresponding to the element that will be removed from the CH 
    def remove(self, k): 
        
        # first hash function
        # invoke BitHash.BitHash with the 0 seed 
        hash1 = BitHash.BitHash(k, 0)
        # find the first possible nest that can contain the keyData pair 
        nest1 = hash1 % len(self.__hashArray1)
        
        keyData1 = self.__hashArray1[nest1]
        
        #if nest1 contains a keyData pair and its key corresponds to k
        if keyData1 and keyData1[0] == k: 
            
            #keep track of the data
            temp = keyData1[1]
            
            #remove the KeyData pair from the nest
            self.__hashArray1[nest1] = None
            
            #decrement the num of keys in the Hash Tables
            self.__numKeys -= 1
            
            #return the data of the keyData pair (the keyData has been removed)
            return temp 
         
        #otherwise use the second hash function     
        #second hash function 
        #invoke BitHash with the previous hash seed 
        hash2 = BitHash.BitHash(k, hash1)
        # find the second possible nest that can contain the keyData pair 
        nest2 = hash2 % len(self.__hashArray2)       
        
        keyData2 = self.__hashArray2[nest2]        
        
        #if nest2 contains a keyData pair and its key corresponds to k
        if keyData2 and keyData2[0] == k:
            
            #keep track of the data
            temp = keyData2[1]
            
            #remove the KeyData pair from the nest
            self.__hashArray2[nest2] = None
            
            #decrement the num of keys in the Hash Tables
            self.__numKeys -= 1
            
            #return the data of the keyData pair (the keyData has been removed)
            return temp             
        
        #otherwise, the key was not found and therefore not removed, so return None
        return None 
            
        
    # MUTATOR: method that increments the Data of a keyData pair found in the CH by 1
    # or, if it is not found, it inserts the keyData pair with Data = 1
    def increment(self, k):
        
        # check whether the key is found in the CH (already inserted) 
        nestFound, dataFound = self.__findNest(k)
        keyData = k, dataFound
        
        # if it is not found, insert a keyData pair in the CH with key = k and data = 1
        if nestFound == None:
            self.insert(k, 1)
            
        #otherwise increment the data of the keyData pair by 1
        else: 
            
            # if it is part of the first hash table 
            if self.__hashArray1[nestFound] and self.__hashArray1[nestFound][0] == keyData[0]:
                # increment the data by 1
                keyData = k, dataFound + 1
                self.__hashArray1[nestFound] = keyData
                
            # otherwise it is part of the second hash table 
            elif self.__hashArray2[nestFound] and self.__hashArray2[nestFound][0] == keyData[0]:
                # increment the data by 1
                keyData = k, dataFound + 1
                self.__hashArray2[nestFound] = keyData
            
     
    # will be used in pytests and checks whether the Cuckoo Hash is an actual Cuckoo Hash
    # checks if each keyData pair inside the 2 lists is in the correct place 
    # returns True (if it's a CuckooHash) or False (if it's not)
    def isCuckoo(self):
        
        # for each element in hashArray1
        for i in range(len(self.__hashArray1)):
            
            # if the nest is not empty 
            if self.__hashArray1[i] != None:
                
                #get the key inserted in the nest
                key = self.__hashArray1[i][0]
                
                # hash it once: 
                #invoke BitHash with the 0 seed 
                hash1 = BitHash.BitHash(key, 0)
                #find nest1
                nest1 = hash1 % len(self.__hashArray1)
                
                # if the nest is not in the correct position return False 
                if i != nest1: return False
        
        # for each element in hashArray2    
        for i in range(len(self.__hashArray2)):
            
            # if the nest is not empty 
            if self.__hashArray2[i]:
                
                #get the key inserted in the nest
                key = self.__hashArray2[i][0]
                
                #hash it twice:
                seed2 = BitHash.BitHash(key, 0) 
                #invoke BitHash.BitHash with the previous hash seed 
                hash2 = BitHash.BitHash(key, seed2)
                #find nest2  
                nest2 = hash2 % len(self.__hashArray2) 
                
                # if the nest is not in the correct position return False 
                if i != nest2: return False      
        
        # at this point every element was checked and found in the correct position
        # so return True         
        return True

# fake CuckooHash class that will be used in the pytests 
class FakeCuckoo(object):
    
    # only attribute is an empty dictionary that will contain the keys and data 
    def __init__(self): self.__ch = {}
    
    # the length is the number of keys in the dictionary 
    def __len__(self): return len(self.__ch)  
    
    # method that inserts a key and data in the dict. 
    def insert(self, k, d): 
        
        self.__ch[k] = d
        # always returns True (always successful) 
        return True    
    
    # method that searches for a key in the dict. If it's found it returns the data.
    def find(self, k): 
        
        # if key is contained in the dict., return the data 
        if k in self.__ch: return self.__ch[k]    
     
    # method that removes a key from the dict. If it is removed it returns the data
        # otherwise it returns None
    def remove(self, k):
        
        # if the key is in the fake CuckooHash 
        if k in self.__ch:
            
            # get its data
            ans = self.__ch[k]
            
            # delete the key from the CuckooHash
            del self.__ch[k]
            
            # return the data 
            return ans
        
        # otherwise return None   
        
    # method that returns the keys contained in the dict. (CuckooHash)
    def keys(self): return self.__ch.keys()
    
    # method that increments the data of a key by 1, or creates a new key with data = 1
    def increment(self, k): 
        if k in self.__ch: self.__ch[k] += 1
        else: self.__ch[k] = 1
        
    

#############
## PYTESTS ##
#############
        

#TESTING THE INSERTION METHOD, FIND METHOD, LEN WHILE USING ISCUCKOO AND FAKECUCKOO
    #ON DIFFERENT SIZES OF CUCKOOHASHES 
    
#check if the class works for an EMPTY cuckooHash 
#using isCuckoo
def testIsCuckooEmptyCH_():
    
    # create a new CuckooHash  
    ch = CuckooHash() 
    
    # check isCuckoo
    isCuckoo = ch.isCuckoo()
    
    #assert that cuckooHash is a cuckoo Hash 
    assert isCuckoo == True

# check if the class works for 2 keys
# check using FakeCuckoo that all keyData pairs are inserted correctly in the CuckooHash 
def test2KeysCH_():
    
    #create a new cuckooHash  
    ch = CuckooHash(0) 
    
    # create a fake cuckooHash  
    f = FakeCuckoo()    
    
    #insert 2 key/data pairs in the cuckooHash and in the fake cuckooHash 
    for i in range(2): 
        # generate a random word as the key
        r = RandomWord()
        key = r.generate()
        
        # generate a random int as the data 
        data = random.randint(0, 100)
        
        # insert the keyData pair in both fake and real cuckooHash 
        ch.insert(key, data)
        f.insert(key, data)
        
    # check that each key inserted in the fake cuckooHash (dictionary), is also
    # found in the real cuckooHash 
    missing = 0
    
    # for each key in the fake CuckooHash 
    for k in f.keys():
        # if it is not found in the real CuckooHash, increment the missing (keys) 
        if ch.find(k) != f.find(k):
            missing += 1
         
    # assert that no keys are missing from the (real) cuckooHash    
    assert missing == 0
    
# check if the class works for a 2 keys cuckooHash using isCuckoo
def testIsCuckoo2KeysCH_():
    # create a cuckooHash  
    ch = CuckooHash(0)
    
    #insert 2 key/data pairs in the cuckooHash and in the fake cuckooHash 
    for i in range(2): 
        # generate a random word as the key
        r = RandomWord()
        key = r.generate()
        
        # generate a random int as the data 
        data = random.randint(0, 100)
        
        # insert the keyData pair in the cuckooHash 
        ch.insert(key, data)
        
    # check isCuckoo 
    isCuckoo = ch.isCuckoo()      
    
    #assert that cuckooHash is a cuckoo Hash 
    assert isCuckoo == True 
    
# check using FakeCuckoo that there is still the same number of keys in both 
#                                                     real and fake CuckooHashes     
def testLen2KeysCH_():
    #create cuckooHash table 
    ch = CuckooHash(0) 
    
    # create a fake cuckooHash  
    f = FakeCuckoo()
    
    
    #insert 2 key/data pairs in the cuckooHash and in the fake cuckooHash 
    for i in range(2): 
        # generate a random word as the key
        r = RandomWord()
        key = r.generate()
        
        # generate a random int as the data 
        data = random.randint(0, 100)
        
        # insert the keyData pair in both fake and real cuckooHash 
        ch.insert(key, data)
        f.insert(key, data)
      
    
    #assert the Len is the same in both fake and real cuckooHash
    assert  len(ch) == len(f)        

# check if the class works for a small num of keys
# check using FakeCuckoo that all keyData pairs are inserted correctly in the CuckooHash     
def testSmallNumCH_():
    
    #create a new cuckooHash  
    ch = CuckooHash(1) 
    
    # create a fake cuckooHash  
    f = FakeCuckoo()    
    
    #insert 10 key/data pairs in the cuckooHash and in the fake cuckooHash 
    for i in range(10): 
        
        # generate a random word as the key
        r = RandomWord()
        key = r.generate()
        
        # generate a random int as the data 
        data = random.randint(0, 100)
        
        # insert the keyData pair in both fake and real cuckooHash 
        ch.insert(key, data)
        f.insert(key, data)
        
    # check that each key inserted in the fake cuckooHash (dictionary), is also
    # found in the real cuckooHash 
    missing = 0
    
    # for each key in the fake CuckooHash 
    for k in f.keys():
        # if it is not found in the real CuckooHash, increment the missing (keys) 
        if ch.find(k) != f.find(k):
            missing += 1
         
    # assert that no keys are missing from the (real) cuckooHash    
    assert missing == 0    
    
# check if the class works for a small cuckooHash using isCuckoo   
def testIsCuckooSmallNumCH_():
    
    # create a cuckooHash  
    ch = CuckooHash(1)
    
    #insert 10 key/data pairs in the cuckooHash and in the fake cuckooHash 
    for i in range(10): 
        # generate a random word as the key
        r = RandomWord()
        key = r.generate()
        
        # generate a random int as the data 
        data = random.randint(0, 100)
        
        # insert the keyData pair in the cuckooHash 
        ch.insert(key, data)
        
    # check isCuckoo 
    isCuckoo = ch.isCuckoo()      
    
    #assert that cuckooHash is a cuckoo Hash 
    assert isCuckoo == True 
 
# check using FakeCuckoo that there is still the same number of keys in both 
#                                                     real and fake CuckooHashes    
def testLenSmallNumCH_():
    
    #create a cuckooHash  
    ch = CuckooHash(1) 
    
    # create a fake cuckooHash  
    f = FakeCuckoo()
    
    
    #insert 10 key/data pairs in the cuckooHash and in the Fake CuckooHash 
    for i in range(10): 
        
        # generate a random word as the key
        r = RandomWord()
        key = r.generate()
        
        # generate a random int as the data 
        data = random.randint(0, 100)
        
        # insert the keyData pair in both fake and real cuckooHash 
        ch.insert(key, data)
        f.insert(key, data)
      
    
    #assert the Len is the same in both fake and real cuckooHash
    assert  len(ch) == len(f)        
    
# check if the class works for a big num of keys
# check using FakeCuckoo that all keyData pairs are inserted correctly in the CuckooHash   
def testBigNumCH_():
    
    #create a new cuckooHash  
    ch = CuckooHash(10) 
    
    # create a fake cuckooHash  
    f = FakeCuckoo()    
    
    #insert 1000 key/data pairs in the cuckooHash and in the fake cuckooHash 
    for i in range(1000): 
        
        # generate a random word as the key
        r = RandomWord()
        key = r.generate()
        
        # generate a random int as the data 
        data = random.randint(0, 100)
        
        # insert the keyData pair in both fake and real cuckooHash 
        ch.insert(key, data)
        f.insert(key, data)
        
    # check that each key inserted in the fake cuckooHash (dictionary), is also
    # found in the real cuckooHash 
    missing = 0
    
    # for each key in the fake CuckooHash 
    for k in f.keys():
        # if it is not found in the real CuckooHash, increment the missing (keys) 
        if ch.find(k) != f.find(k):
            missing += 1
         
    # assert that no keys are missing from the (real) cuckooHash    
    assert missing == 0    
 
# check if the class works for a big cuckooHash using isCuckoo    
def testIsCuckooBigNumCH_():
    
    # create a cuckooHash  
    ch = CuckooHash(10)
    
    #insert 1000 key/data pairs in the cuckooHash and in the fake cuckooHash 
    for i in range(1000): 
        # generate a random word as the key
        r = RandomWord()
        key = r.generate()
        
        # generate a random int as the data 
        data = random.randint(0, 100)
        
        # insert the keyData pair in the cuckooHash 
        ch.insert(key, data)
        
    # check isCuckoo 
    isCuckoo = ch.isCuckoo()      
    
    #assert that cuckooHash is a cuckooHash 
    assert isCuckoo == True
 
# check using FakeCuckoo that there is still the same number of keys in both 
#                                                     real and fake CuckooHashes      
def testLenBigNumCH_():
    # create a cuckooHash  
    ch = CuckooHash(10) 
    
    # create a fake cuckooHash  
    f = FakeCuckoo()
    
    
    #insert 1000 key/data pairs in the cuckooHash and in the fake cuckooHash 
    for i in range(1000): 
        
        # generate a random word as the key
        r = RandomWord()
        key = r.generate()
        
        # generate a random int as the data 
        data = random.randint(0, 100)
        
        # insert the keyData pair in both fake and real cuckooHash 
        ch.insert(key, data)
        f.insert(key, data)
      
    
    #assert the Len is the same in both fake and real cuckooHash
    assert  len(ch) == len(f)    
    
# check if the class works for a random num of keys
# check using FakeCuckoo that all keyData pairs are inserted correctly in the CuckooHash   
def testRandomNumCH_():
    
    #create a new cuckooHash  
    ch = CuckooHash(1) 
    
    # create a fake cuckooHash  
    f = FakeCuckoo()    
    
    # generate a random num of insertions 
    rnd = random.randint(0, 5000)
    
    #insert a random num of key/data pairs in the cuckooHash and in the fake cuckooHash 
    for i in range(rnd): 
        
        # generate a random word as the key
        r = RandomWord()
        key = r.generate()
        
        # generate a random int as the data 
        data = random.randint(0, 100)
        
        # insert the keyData pair in both fake and real cuckooHash 
        ch.insert(key, data)
        f.insert(key, data)
        
    # check that each key inserted in the fake cuckooHash (dictionary), is also
    # found in the real cuckooHash 
    missing = 0
    
    # for each key in the fake CuckooHash 
    for k in f.keys():
        # if it is not found in the real CuckooHash, increment the missing (keys) 
        if ch.find(k) != f.find(k):
            missing += 1
         
    # assert that no keys are missing from the (real) cuckooHash    
    assert missing == 0  

# check if the class works for a random length cuckooHash using isCuckoo 
def testIsCuckooRandomNumCH_():
    
    # create cuckooHash  
    ch = CuckooHash(1) 
    
    # generate a random number of insertions
    rnd = random.randint(0, 5000)
  
    # insert a random num of key/data pairs in the cuckooHash and in the fake cuckooHash 
    for i in range(rnd): 
        # generate a random word as the key
        r = RandomWord()
        key = r.generate()
        
        # generate a random int as the data 
        data = random.randint(0, 100)
        
        # insert the keyData pair in the cuckooHash 
        ch.insert(key, data)
        
    # check isCuckoo 
    isCuckoo = ch.isCuckoo()      
    
    #assert that cuckooHash is a cuckooHash 
    assert isCuckoo == True    

# check using FakeCuckoo that there is still the same number of keys in both 
#                                                     real and fake CuckooHashes   
def testLenRandomNumCH_():
    
    # create a cuckooHash  
    ch = CuckooHash(1) 
    
    # create a fake cuckooHash 
    f = FakeCuckoo()
    
    # generate a random number of insertions
    rnd = random.randint(0, 5000)
    
    
    #insert a random num of random key/data pairs in the cuckooHash and in the fake cuckooHash 
    for i in range(rnd): 
        
        # generate a random word as the key
        r = RandomWord()
        key = r.generate()
        
        # generate a random int as the data 
        data = random.randint(0, 100)
        
        # insert the keyData pair in both fake and real cuckooHash 
        ch.insert(key, data)
        f.insert(key, data)
      
    
    #assert the Len is the same in both fake and real cuckooHash
    assert  len(ch) == len(f)
    
# CHECKING THE REMOVE METHOD 

# check for an empty cuckooHash 
# using find
def testRemoveEmpy1CH_():
    #create cuckooHash table 
    ch = CuckooHash() 
    
    # create fake cuckooHash table 
    f = FakeCuckoo()    
    
    #insert 10 key/data pairs in the cuckooHash and fakeCuckoo
    for i in range(10): 
        # insert Foo + i, i in fake and real cuckooHashes 
        ch.insert("Foo" + str(i), i)
        f.insert("Foo" + str(i), i)
        
    #remove all key/data pairs in the cuckooHash and fakeCuckoo
    for i in range(10): 
        # remove Foo + i, i in fake and real cuckooHashes 
        ch.remove("Foo" + str(i))
        f.remove("Foo" + str(i))    
        
    #delete a random num of random key/data pairs from the empty cuckooHash and fakeCuckoo
    rnd = random.randint(1, 999)
    for i in range(rnd):
        
        ch.remove("Foo" + str(i))
        f.remove("Foo" + str(i))
         
    # assert that they are both empty   
    assert len(ch) == len(f) == 0  
    
def testRemoveEmpy2CH_():
    #create cuckooHash table 
    ch = CuckooHash() 
        
    #delete a random num of random key/data pairs from the empty cuckooHash 
    rnd = random.randint(1, 999)
    for i in range(rnd):
        ch.remove("Foo" + str(i))
         
    # assert that it is empty 
    assert len(ch) == 0  
    
# check for a small num of keys 
# using find
def testRemoveSmallCH_():
    #create cuckooHash table 
    ch = CuckooHash(1) 
    
    # create fake cuckooHash table 
    f = FakeCuckoo()    
    
    #insert 10 key/data pairs in the cuckooHash and fakeCuckoo
    for i in range(10): 
        # insert Foo + i, i in fake and real cuckooHashes 
        ch.insert("Foo" + str(i), i)
        f.insert("Foo" + str(i), i)
        
    #delete a random num of random key/data pairs in the cuckooHash and fakeCuckoo
    rnd = random.randint(1, 9)
    for i in range(rnd):
        
        ch.remove("Foo" + str(i))
        f.remove("Foo" + str(i))
      
    # check that each key inserted/removed in the fake cuckooHash (dictionary), is also
    # found/missing in the real cuckooHash 
    missing = 0
    
    # for each key in the fake CuckooHash 
    for k in f.keys():
        # if it is not found in the real CuckooHash, increment the missing (keys) 
        if ch.find(k) != f.find(k):
            missing += 1
         
    # assert that no keys are missing from the (real) cuckooHash    
    assert missing == 0  
    
# check for a big num of keys 
# using find
def testRemoveBigCH_():
    #create a cuckooHash  
    ch = CuckooHash(1) 
    
    # create a fake cuckooHash  
    f = FakeCuckoo()    
    
    #insert 1000 key/data pairs in the cuckooHash and fakeCuckoo
    for i in range(1000): 
        # insert Foo + i, i in fake and real cuckooHashes 
        ch.insert("Foo" + str(i), i)
        f.insert("Foo" + str(i), i)
        
    #delete a random num of random key/data pairs in the cuckooHash and fakeCuckoo
    rnd = random.randint(1, 999)
    for i in range(rnd):
        
        ch.remove("Foo" + str(i))
        f.remove("Foo" + str(i))
      
    # check that each key inserted/removed in the fake cuckooHash (dictionary), is also
    # found/missing in the real cuckooHash 
    missing = 0
    
    # for each key in the fake CuckooHash 
    for k in f.keys():
        # if it is not found in the real CuckooHash, increment the missing (keys) 
        if ch.find(k) != f.find(k):
            missing += 1
         
    # assert that no keys are missing from the (real) cuckooHash    
    assert missing == 0  
    
# check remove with isCuckoo
def testRemoveIsCuckooCH_():
    #create cuckooHash table 
    ch = CuckooHash(1)    
    
    # insert a random num of key/data pairs in the cuckooHash 
    rnd = random.randint(0, 5000)    
    for i in range(rnd): 
        # insert Foo + i, i 
        ch.insert("Foo" + str(i), i)
        
    # delete a random num of random key/data pairs in the cuckooHash
    rnd = random.randint(0, 5000)
    for i in range(rnd):
        ch.remove("Foo" + str(i))
      
    isCuckoo = ch.isCuckoo()
         
    # assert that no keys are missing from the cuckooHash    
    assert isCuckoo == True
    
# check the length of the C.H. after having removed 
def testLenRemoveCH_():
    #create a cuckooHash  
    ch = CuckooHash(1) 
    
    # create a fakeCuckoo  
    f = FakeCuckoo()    
    
    #insert a random num of key/data pairs in the cuckooHash and fakeCuckoo
    rnd = random.randint(0, 5000)
    for i in range(rnd): 
        # insert Foo + i, i in fake and real cuckooHashes 
        ch.insert("Foo" + str(i), i)
        f.insert("Foo" + str(i), i)
        
    #delete a random num of random key/data pairs in the cuckooHash and fakeCuckoo
    rnd = random.randint(0, 5000)
    for i in range(rnd):
        
        ch.remove("Foo" + str(i))
        f.remove("Foo" + str(i))
         
    # assert that the fake and real CuckooHash have the same len     
    assert len(f) == len(ch)

# TEST FIND 
def testFindEmptyCH():
    #create cuckooHash table 
    ch = CuckooHash() 
    
    # create a fakeCuckoo  
    f = FakeCuckoo()     
        
    #Find a random num of random key/data pairs from the empty cuckooHash 
    rnd = random.randint(1, 999)
    
    # check that no keys are found in both CuckooHashes
    
    missing = 0
    
    for i in range(rnd):
        
        if ch.find("Foo" + str(i)) != f.find("Foo" + str(i)): 
            missing += 1
         
    # assert that no keys are missing from the (real) cuckooHash (and vice versa for the fakeCuckoo)
    assert missing == 0  
    
def testFindCH_():
    #create a cuckooHash  
    ch = CuckooHash(1) 
    
    # create a fakeCuckoo  
    f = FakeCuckoo()    
    
    # insert a random num of key/data pairs in the cuckooHash and fakeCuckoo
    rnd = random.randint(0, 5000)    
    for i in range(rnd): 
        # insert Foo + i, i in fake and real cuckooHashes 
        ch.insert("Foo" + str(i), i)
        f.insert("Foo" + str(i), i)
        
    #find a random num of random key/data pairs in the cuckooHash and fakeCuckoo
    rnd = random.randint(0, 5000)
    
    # check that each key inserted/removed in the fake cuckooHash (dictionary), is also
    # found/missing in the real cuckooHash     
    missing = 0
    
    for i in range(rnd):
        
        if ch.find("Foo" + str(i)) != f.find("Foo" + str(i)): 
            missing += 1
         
    # assert that no keys are missing from the (real) cuckooHash (and vice versa for the fakeCuckoo)
    assert missing == 0  
    
def testFindSmallCH_():
    #create a cuckooHash  
    ch = CuckooHash(1) 
    
    # create a fakeCuckoo  
    f = FakeCuckoo()    
    
    # insert a small num of key/data pairs in the cuckooHash and fakeCuckoo
    for i in range(10): 
        # insert Foo + i, i in fake and real cuckooHashes 
        ch.insert("Foo" + str(i), i)
        f.insert("Foo" + str(i), i)
        
    #find a small num of key/data pairs in the cuckooHash and fakeCuckoo
    
    # check that each key inserted/removed in the fake cuckooHash (dictionary), is also
    # found/missing in the real cuckooHash     
    missing = 0
    
    for i in range(10):
        
        if ch.find("Foo" + str(i)) != f.find("Foo" + str(i)): 
            missing += 1
         
    # assert that no keys are missing from the (real) cuckooHash (and vice versa for the fakeCuckoo)
    assert missing == 0  
    
def testFindBigCH_():
    #create a cuckooHash  
    ch = CuckooHash(1) 
    
    # create a fakeCuckoo  
    f = FakeCuckoo()    
    
    # insert a big num of key/data pairs in the cuckooHash and fakeCuckoo
    for i in range(1000): 
        # insert Foo + i, i in fake and real cuckooHashes 
        ch.insert("Foo" + str(i), i)
        f.insert("Foo" + str(i), i)
        
    #find a big num of key/data pairs in the cuckooHash and fakeCuckoo
    
    # check that each key inserted/removed in the fake cuckooHash (dictionary), is also
    # found/missing in the real cuckooHash     
    missing = 0
    
    for i in range(1000):
        
        if ch.find("Foo" + str(i)) != f.find("Foo" + str(i)): 
            missing += 1
         
    # assert that no keys are missing from the (real) cuckooHash (and vice versa for the fakeCuckoo)
    assert missing == 0  
    
# TEST INCREMENT 

def testIncrementEmptyCH():
    #create cuckooHash table 
    ch = CuckooHash() 
    
    # create a fakeCuckoo  
    f = FakeCuckoo()        
        
    #increment a random num of random key/data pairs from the empty cuckooHash and fakeCuckoo
    rnd = random.randint(1, 999)
    for i in range(rnd):
        ch.increment("Foo" + str(i))
        f.increment("Foo" + str(i))
         
    # check that each key incremented in the fake cuckooHash (dictionary), is also
    # found in the real cuckooHash 
    missing = 0
    
    # for each key in the fake CuckooHash 
    for k in f.keys():
        # if it is not found in the real CuckooHash, increment the missing (keys) 
        if ch.find(k) != f.find(k):
            missing += 1
         
    # assert that no keys are missing from the (real) cuckooHash (and vice versa for the fakeCuckoo)
    assert missing == 0  
    
    
def testIncrementSmallCH_():
    #create a cuckooHash  
    ch = CuckooHash(1) 
    
    # create a fakeCuckoo  
    f = FakeCuckoo()    
    
    # insert a small num of key/data pairs in the cuckooHash and fakeCuckoo 
    for i in range(5): 
        # insert Foo + i, i in fake and real cuckooHashes 
        ch.insert("Foo" + str(i), i)
        f.insert("Foo" + str(i), i)
        
    #increment a small num of key/data pairs in the cuckooHash and fakeCuckoo
    for i in range(5):
        
        ch.increment("Foo" + str(i))
        f.increment("Foo" + str(i))
      
    # check that each key inserted/incremented in the fake cuckooHash (dictionary), is also
    # found/missing in the real cuckooHash 
    missing = 0
    
    # for each key in the fake CuckooHash 
    for k in f.keys():
        # if it is not found in the real CuckooHash, increment the missing (keys) 
        if ch.find(k) != f.find(k):
            missing += 1
         
    # assert that no keys are missing from the (real) cuckooHash (and vice versa for the fakeCuckoo)
    assert missing == 0  
    
def testIncrementMediumCH_():
    #create a cuckooHash  
    ch = CuckooHash(1) 
    
    # create a fakeCuckoo  
    f = FakeCuckoo()    
    
    # insert a medium num of key/data pairs in the cuckooHash and fakeCuckoo 
    for i in range(500): 
        # insert Foo + i, i in fake and real cuckooHashes 
        ch.insert("Foo" + str(i), i)
        f.insert("Foo" + str(i), i)
        
    #increment a medium num of key/data pairs in the cuckooHash and fakeCuckoo
    for i in range(500):
        
        ch.increment("Foo" + str(i))
        f.increment("Foo" + str(i))
      
    # check that each key inserted/incremented in the fake cuckooHash (dictionary), is also
    # found/missing in the real cuckooHash 
    missing = 0
    
    # for each key in the fake CuckooHash 
    for k in f.keys():
        # if it is not found in the real CuckooHash, increment the missing (keys) 
        if ch.find(k) != f.find(k):
            missing += 1
         
    # assert that no keys are missing from the (real) cuckooHash (and vice versa for the fakeCuckoo)
    assert missing == 0  
    
def testIncrementBigCH_():
    #create a cuckooHash  
    ch = CuckooHash(1) 
    
    # create a fakeCuckoo  
    f = FakeCuckoo()    
    
    # insert a big num of key/data pairs in the cuckooHash and fakeCuckoo 
    for i in range(5000): 
        # insert Foo + i, i in fake and real cuckooHashes 
        ch.insert("Foo" + str(i), i)
        f.insert("Foo" + str(i), i)
        
    #increment a big num of key/data pairs in the cuckooHash and fakeCuckoo
    for i in range(3000):
        
        ch.increment("Foo" + str(i))
        f.increment("Foo" + str(i))
      
    # check that each key inserted/incremented in the fake cuckooHash (dictionary), is also
    # found/missing in the real cuckooHash 
    missing = 0
    
    # for each key in the fake CuckooHash 
    for k in f.keys():
        # if it is not found in the real CuckooHash, increment the missing (keys) 
        if ch.find(k) != f.find(k):
            missing += 1
         
    # assert that no keys are missing from the (real) cuckooHash (and vice versa for the fakeCuckoo)  
    assert missing == 0  
    
def testIncrementCH_():
    #create a cuckooHash  
    ch = CuckooHash(1) 
    
    # create a fakeCuckoo  
    f = FakeCuckoo()    
    
    # insert a big num of key/data pairs in the cuckooHash and fakeCuckoo
    for i in range(5000): 
        # insert Foo + i, i in fake and real cuckooHashes 
        ch.insert("Foo" + str(i), i)
        f.insert("Foo" + str(i), i)
        
    #increment a random num of random key/data pairs in the cuckooHash and fakeCuckoo
    rnd = random.randint(0, 5000 )
    for i in range(rnd):
        
        ch.increment("Foo" + str(i))
        f.increment("Foo" + str(i))
    
    
    # check that each key inserted/incremented in the fake cuckooHash (dictionary), is also
    # found/missing in the real cuckooHash 
    missing = 0
    
    # for each key in the fake CuckooHash 
    for k in f.keys():
        # if it is not found in the real CuckooHash, increment the missing (keys) 
        if ch.find(k) != f.find(k):
            missing += 1
         
    # assert that no keys are missing from the (real) cuckooHash (and vice versa for the fakeCuckoo)  
    assert missing == 0 
    
    


pytest.main(["-v", "-s", "CuckooHash.py"])


