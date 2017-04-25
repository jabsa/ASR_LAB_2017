import sys


def create_dict(filename):
    pron_dict ={}
    prev_word = None
    new_word = []
    with open(filename, 'r') as f:
	for line in f:
	    line_items = line.strip().split()
	    if line_items[0] == str(0) and line_items[1] == "pau":
		continue
	    if prev_word <> line_items[0] and prev_word is not None:
		if prev_word not in pron_dict:
		    pron_dict[prev_word] = []   		    
		    while len(new_word) > 0:
			pron_dict[prev_word].append(new_word.pop(0))
		else:
		    new_word=[]    
		new_word.append(line_items[1])
	    else:
		new_word.append(line_items[1])
	    prev_word = line_items[0]
    return pron_dict

def write_dict(writefile, pron_dict):
    with open(writefile, 'w') as wf:
	for word in pron_dict:
	   wf.write(word)
	   for phone in pron_dict[word]:
		wf.write(' ' + phone)
	   wf.write('\n')


def convert_dict(pron_dict, c_dict):
    for word in pron_dict:
	for phone_num , phone in enumerate(pron_dict[word]):
	    pron_dict[word][phone_num] = c_dict[phone]
    return pron_dict 

def make_convert_dict(map_file):
    convert_dict = {}
    with open(map_file, 'r') as mf:
	for line in mf:
	    line_items=line.strip().split()
     	    convert_dict[line_items[0]]=line_items[1]
    return convert_dict
	     
if __name__ =="__main__":
    filename=sys.argv[1]
    map_file=sys.argv[2]
    pron_dict =create_dict(filename)
    print pron_dict
    c_dict = make_convert_dict(map_file)
    #print convert_dict
    converted_dict = convert_dict(pron_dict, c_dict)
    print converted_dict
    write_dict('CVOX_dict', pron_dict)
