import sys


def create_dict(filename):
    """Given the all.word, this returns the pronounciation dict"""
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
    """This writes the pronounciation dict"""
    with open(writefile, 'w') as wf:
	for word in pron_dict:
	   wf.write(word)
	   for phone in pron_dict[word]:
		if phone<>'666':
		    wf.write(' ' + phone)
	   wf.write('\n')

def convert_dict(pron_dict, afnumber_dict):
    """Given the pronounciation dictionary and phone to af mapping in numbers converts the pron dict"""
    for word in pron_dict:
	for phone_num , phone in enumerate(pron_dict[word]):
	    pron_dict[word][phone_num] = afnumber_dict[phone]
    return pron_dict 

def translate_dict(phone_dict, units_dict):
    """Given the units and phone to af mapping translates it to phone to af_numbers"""
    afnumber_dict ={}
    for phone in phone_dict:
	afnumber_dict[phone] = units_dict[phone_dict[phone]]
    return afnumber_dict 

def make_convert_dict(map_file):
    """Returns a dict of key:value = col1:col2"""
    convert_dict = {}
    with open(map_file, 'r') as mf:
	for line in mf:
	    line_items=line.strip().split()
	    #print line_items
     	    convert_dict[line_items[0]]=line_items[1]
    return convert_dict
	     
if __name__ =="__main__":
    filename=sys.argv[1] #all.word
    units_file=sys.argv[2] #units file
    map_file=sys.argv[3] #phone to af map file
    outfile=sys.argv[4] #final afdict name
    #Creat the pronounciation dict
    pron_dict =create_dict(filename)
    
    #Create units dict and phone dict
    units_dict = make_convert_dict(units_file)
    phone_dict = make_convert_dict(map_file)
    
    #Convert af in categories to numbers as given by units dict
    afnumber_dict = translate_dict(phone_dict, units_dict)
    
    #Convert pronounciation dict into these numbers
    converted_dict = convert_dict(pron_dict, afnumber_dict)
    #write final dict to otufile
    write_dict(outfile, pron_dict)
