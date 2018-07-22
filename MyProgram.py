import sys
import csv

def getHealth(status):
    health = None
    if status == 'LOST':
       health = 'DEAD'    
    if status == 'FOUND':         
       health = 'ALIVE'          
    
    return health
   
#requiired where 'None' appears in output where length of row in input file is 4.
def ifEmpty(s):
    if s is None:
        return ''
    return str(s)

def composeDict(nodeType, row):

    dict1={}    
    
    if nodeType == 1:
       dict1['node'] = row['node1']
       dict1['monitor_time'] = row['monitor_time']
       dict1['generated_time'] = row['generated_time']       
       # no matter what the status is, the first node it's always alive
       dict1['health'] = 'ALIVE'  
       dict1['message'] = ifEmpty(row['node1']) + ' ' + ifEmpty(row['status']) + ' ' + ifEmpty(row['node2'])              
    else:
       dict1={}
       dict1['node'] = row['node2']
       dict1['monitor_time'] = row['monitor_time']
       dict1['generated_time'] = row['generated_time']              
       # the second node the status depends of the action performed by node1
       dict1['health'] = getHealth(row['status'])  
       dict1['message'] = ifEmpty(row['node1']) + ' ' + ifEmpty(row['status']) + ' ' + ifEmpty(row['node2'])       

    return dict1      
        
def printList(btlist):
    
    for index in range(len(btlist)):      
        
        if btlist[index]: 
           print(" %s %s %s %s" % (btlist[index]["node"], btlist[index]["health"], btlist[index]["monitor_time"], btlist[index]["message"]) )


def openfile(filename):

    #define the list that will contain the nodes 
    btlist = [{}]
         
    with open(filename) as f:

         cf = csv.DictReader(f, delimiter=' ', quoting=csv.QUOTE_NONE, fieldnames=['monitor_time','generated_time','node1','status', 'node2', 'dummy'])
         i=0
         for row in cf:
             i += 1
             # used to create an error and exit program when the input file is not in the correct form e.g length of row is 6.
             if row['dummy']:
                raise ValueError('Row has invalid data...', i, row['dummy'])           
             if row['status'] not in ('HELLO','LOST','FOUND'):
                raise ValueError('Value not in scope (HELLO, LOST, FOUND)...', i, row['status'])           

        
             # check if the node already exists in the list
             position = next((i for i,item in enumerate(btlist) if item.get("node") == row['node1']), [])
     
             if position:
                # if the node is already in the list, check if the current generated datetime is greater than the one in the list
                # if it's greatter then update the date and the status
                if btlist[position]['generated_time'] < row['generated_time']:      
                   btlist[position]['monitor_time'] = row['monitor_time']
                   btlist[position]['generated_time'] = row['generated_time']
                   # by definition the node1 is always alive
                   btlist[position]['health'] = 'ALIVE'  
                   btlist[position]['message'] = ifEmpty(row['node1']) + ' ' + ifEmpty(row['status']) + ' ' + ifEmpty(row['node2'])
#               
             else: 
      
                dict1 = composeDict(1, row)
                btlist.append(dict1)

             if row['node2']:
                # check if the node2 already exists in the list
                position = next((i for i,item in enumerate(btlist) if item.get("node") == row['node2']), [])
             
                if position:
                   # if the node is already in the list, check if the current generated datetime is greater than the one in the list
                   # if it's greater - update the date and the status

                   if btlist[position]['generated_time'] < row['generated_time']:
      
                      btlist[position]['monitor_time'] = row['monitor_time']
                      btlist[position]['generated_time'] = row['generated_time']                      
                      btlist[position]['health'] = getHealth(row['status'])
                      btlist[position]['message'] = ifEmpty(row['node1']) + ' ' + ifEmpty(row['status']) + ' ' + ifEmpty(row['node2'])                      
                   
                else: 

                   dict1 = composeDict(2, row)
                   btlist.append(dict1)
          
    printList(btlist)
    
if __name__ == '__main__':
         
  try:
    
     if len(sys.argv) < 2:
        raise ValueError('Process has invalid number of parameters...')
     
     filename = sys.argv[1]     
     
     openfile(filename) 

  except ValueError as err:
      print(err.args)
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      