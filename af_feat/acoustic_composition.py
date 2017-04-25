 ###normalisation information
import logging
import os
import numpy
import sys
from merlin_gen_scripts.acoustic_composition import AcousticComposition

def prepare_file_path_list(file_id_list, file_dir, file_extension, new_dir_switch=True):
    if not os.path.exists(file_dir) and new_dir_switch:
        os.makedirs(file_dir)
    file_name_list = []
    with open(file_id_list, 'r') as fileid_list:
        for file_id in fileid_list:
            file_name = file_dir + '/' + file_id.strip() + file_extension
            file_name_list.append(file_name)
    return  file_name_list



def do_acoustic_composition(main_path, n_output_dim=199):
    print('Extracting acoustic delta features and composing WORLD feats as a single vector')
    delta_win = [-0.5, 0.0, 0.5]
    acc_win = [1.0, -2.0, 1.0]

    data_path=main_path + '/binary_af_feats/'

    all_list=main_path +'/etc/filelist'
    out_dimension_dict = { 'mgc' : 180,'lf0' : 3,'vuv' : 1,'bap' : 15}

    in_dimension_dict = { 'mgc' : 60,'lf0' : 1,'vuv' : 1,'bap' : 5}

    in_dir_dict= {'mgc': data_path + '/mgc/', 'bap': data_path + '/bap/', 'lf0':data_path +'/lf0/'}

    comp_output_dir=data_path
    ext_dict= {'mgc': '.mgc', 'bap': '.bap', 'lf0':'.lf0'}

    in_file_list_dict={}
    for feature_name in in_dir_dict.keys():
        in_file_list_dict[feature_name] = prepare_file_path_list(all_list, in_dir_dict[feature_name],ext_dict[feature_name], False)
        #print(len(in_file_list_dict[feature_name]))

    out_file_list = prepare_file_path_list(all_list, comp_output_dir ,'.cmp', False)
    acoustic_worker = AcousticComposition(delta_win = delta_win, acc_win = acc_win)
    acoustic_worker.prepare_nn_data(in_file_list_dict, out_file_list, in_dimension_dict, out_dimension_dict)




if __name__=="__main__":
    main_path=sys.argv[1]
    do_acoustic_composition(main_path, n_output_dim=199)

