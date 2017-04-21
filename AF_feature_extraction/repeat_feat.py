import sys
import numpy
 

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
	    if phone <> curr_phone : 
		phone_num +=1   
	        curr_phone = phone_lines[phone_num].strip().split()[0]
	
	#print phone, curr_phone
	with open('af_feats/' + filename + '.faf', 'a+') as wf:
	    wf.write(phone_lines[phone_num])
    return
     



if __name__=="__main__":
    filename=sys.argv[1]
    repeat_vec(filename)
