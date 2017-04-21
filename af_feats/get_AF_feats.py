import sys
import os
#Remove duplicates from dumped af files (.af)  and repate framewise (.faf)
def remove_dup(filename):
    curr_line=None
    for line in open('af_feats/' + filename + '.daf').readlines():
	if curr_line is not None:
	   if line == curr_line:
		continue
	   else:
		with open('af_feats/' + filename + '.af', 'a+') as wf:
		    wf.write(line)
	else:
	    with open('af_feats/' + filename + '.af', 'w') as wf:
		wf.write(line)
	curr_line = line

def repeat_vec(filename):
    phone_lines=file('af_feats/' + filename + '.af').readlines()
    phone_num=0
    curr_phone=phone_lines[phone_num].strip().split()[0]
    
    for line in reversed(open('festival/coeffs/' + filename + '.feats').readlines()):
	phone=line.strip().split()[0].split('_')[0]
	print phone, curr_phone
	
        if phone <> curr_phone :
	    phone_num += 1
	    curr_phone = phone_lines[phone_num].strip().split()[0]
	#print phone, curr_phone
	with open('af_feats/' + filename + '.faf', 'a+') as wf:
	    wf.write(phone_lines[phone_num])
    return
 


if __name__ =="__main__":
    filename=sys.argv[1]
    remove_dup(filename)
    if os.path.exists('af_feats/' + filename + '.faf'): 
        os.remove('af_feats/' + filename + '.faf')
    repeat_vec(filename)
