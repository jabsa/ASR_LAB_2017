import numpy as np
import sys
import os
import binary_io
io_funcs = binary_io.BinaryIOCollection()
#need to make this better.. read in a file with phonelist etc. This is only for testing.

def get_items(infile):
    with open(infile, 'r') as f:
        itemlist=f.read().strip().split('___')
        itemlist.pop(-1)
        itemlist.insert(0,"0")
    return itemlist

def one_hot(number, max_size):
    """ Returns the one hot vector of a number, given the max"""
    b = np.zeros(max_size,dtype=float)
    b[number]=1.0
    return b

def make_binary(outdir, infile, phonefile):
    """Makes binary vectors"""
    PHONELIST=get_items(phonefile)
    VC=['+','-'] #VC, VRND, CVOX
    PRESENTLIST=['0', '+','-'] #VC, VRND, CVOX
    CPLACE=['0', 'a','b','d','g','l','p','v']
    VLNG=['0','a','d','l','s']
    CTYPE=['0','a','f','l','n','r','s']
    STRENGTHLIST=['0', 1, 2, 3]#VFRONT, VHEIGHT

   #Phone, vc, vheight, vfront, vlng, vrnd, ctype, cplace, cvox
    features=[PHONELIST,
            VC,
            STRENGTHLIST,
            STRENGTHLIST,
            VLNG,
            PRESENTLIST,
            CTYPE,
	    CPLACE,
            PRESENTLIST]
    
    final_list=[]
    final_mat=[]
    filename=infile.strip().split('/')[-1]
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    outfile= outdir + '/' + filename
    with open(infile, 'r') as f:
        for line in f:
            feat_list=line.strip().split()
            for feat, list_name in enumerate(features):
                print "DEBUG: ", list_name, feat_list[feat],
                final_list.extend(get_element(feat_list[feat], list_name))
            final_mat.append(final_list)
            print(len(final_list))
            final_list=[]
        io_funcs.array_to_binary_file(final_mat, outfile)
    
    #print '\n'.join([ str(element) for element in final_list ])

def get_element(item, find_list):
    """Returns the item index in a list"""
    #print(find_list[0]==item)
    print(np.where(np.asarray(find_list) == item)[0][0])
    return list(one_hot(np.where(np.asarray(find_list)==item)[0][0], len(find_list)))

def read_binary_file(filename, feature_dimension):
    load_mat=io_funcs.load_binary_file(filename, feature_dimension)
    return load_mat

if __name__=="__main__":
    infile=sys.argv[1]
    outdir=sys.argv[2]
    phonelist=sys.argv[3]
    make_binary(outdir,infile, phonelist)
    outfile=outdir +'/' + infile.strip().split('/')[-1]
#    binary_mat = read_binary_file(outfile,711)
#    print binary_mat


