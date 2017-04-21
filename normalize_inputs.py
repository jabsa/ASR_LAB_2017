 ###normalisation information
import logging
import os
import numpy
from merlin_gen_scripts.acoustic_composition import AcousticComposition
from merlin_gen_scripts.min_max_norm import MinMaxNormalisation

from merlin_gen_scripts.mean_variance_norm import MeanVarianceNorm

def prepare_file_path_list(file_id_list, file_dir, file_extension, new_dir_switch=True):
    if not os.path.exists(file_dir) and new_dir_switch:
        os.makedirs(file_dir)
    file_name_list = []
    with open(file_id_list, 'r') as fileid_list:
        for file_id in fileid_list:
            file_name = file_dir + '/' + file_id.strip() + file_extension
            file_name_list.append(file_name)
    return  file_name_list


def do_lab_normalization(main_path, n_input_dim=711, n_output_dim=199):
    print('Doing input feature normaization')
    norm_info_file = os.path.join(main_path, '/norm_info_mgc_lf0_vuv_bap_' + str(n_output_dim) + '_MVN.dat')
    data_dir=main_path + '/data'
    train_list=data_dir + '/train_list'
    val_list=data_dir + '/val_list'
    test_list=data_dir +'/test_list'
    all_list=data_dir +'/all_list'
    label_norm_file = data_dir + '/label_norm.dat'
    binary_label_dir= data_dir + '/binary_label_' + str(n_input_dim)
    normalized_label_dir=data_dir + '/normalized_feats/'
    if not os.path.exists(normalized_label_dir):
        os.makedirs(normalized_label_dir)

    binary_label_train_list   = prepare_file_path_list(train_list, binary_label_dir, '.lab')
    binary_label_all_list   = prepare_file_path_list(all_list, binary_label_dir, '.lab')
    label_norm_all_list  = prepare_file_path_list(all_list, normalized_label_dir, '.lab')

    #print(label_norm_file)
    min_max_normaliser = MinMaxNormalisation(feature_dimension = n_input_dim, min_value = 0.01, max_value = 0.99)
    ###use only training data to find min-max information, then apply on the whole dataset
    min_max_normaliser.find_min_max_values(binary_label_train_list)
    min_max_normaliser.normalise_data(binary_label_all_list, label_norm_all_list)
        ### save label normalisation information for unseen testing labels
    label_min_vector = min_max_normaliser.min_vector
    label_max_vector = min_max_normaliser.max_vector
    label_norm_info = numpy.concatenate((label_min_vector, label_max_vector), axis=0)
    label_norm_info = numpy.array(label_norm_info, 'float32')
    fid = open(label_norm_file, 'wb')
    label_norm_info.tofile(fid)
    fid.close()
    print('saved %s vectors to %s' %(label_min_vector.size, label_norm_file))



def do_acoustic_composition(main_path, n_input_dim=711, n_output_dim=199):
    print('Extracting acoustic delta features and doing normalisation')
    delta_win = [-0.5, 0.0, 0.5]
    acc_win = [1.0, -2.0, 1.0]

    data_path=main_path + '/data/acoustic_feats_'+str(n_output_dim)

    all_list=main_path +'/data/all_list'
    out_dimension_dict = { 'mgc' : 180,'lf0' : 3,'vuv' : 1,'bap' : 15}

    in_dimension_dict = { 'mgc' : 60,'lf0' : 1,'vuv' : 1,'bap' : 5}

    in_dir_dict= {'mgc': data_path + '/mgc/', 'bap': data_path + '/bap/', 'lf0':data_path +'/lf0/'}

    comp_output_dir=main_path + '/data/acoustic_feats_' + str(n_output_dim)
    ext_dict= {'mgc': '.mgc', 'bap': '.bap', 'lf0':'.lf0'}

    in_file_list_dict={}
    for feature_name in in_dir_dict.keys():
        in_file_list_dict[feature_name] = prepare_file_path_list(all_list, in_dir_dict[feature_name],ext_dict[feature_name], False)
        print(len(in_file_list_dict[feature_name]))

    out_file_list = prepare_file_path_list(all_list, comp_output_dir ,'.cmp', False)
    acoustic_worker = AcousticComposition(delta_win = delta_win, acc_win = acc_win)
    acoustic_worker.prepare_nn_data(in_file_list_dict, out_file_list, in_dimension_dict, out_dimension_dict)

def do_acoustic_normalisation(main_path, n_input_dim=711, n_output_dim=199):
    logger=logging.getLogger("label_normalization")
    logger.info('normalising acoustic (output) features using MVN')
    cmp_norm_info = None
    norm_info_file= main_path + '/data/acoustic_norm_info.dat'
    all_list=main_path +'/data/all_list'
    train_list=main_path +'/data/train_list'
    in_data_dir=main_path +'/data/acoustic_feats_' +str(n_output_dim)
    out_data_dir=main_path +'/data/normalized_feats/'
    out_dimension_dict = { 'mgc' : 180,'lf0' : 3,'vuv' : 1,'bap' : 15}
    in_dimension_dict = { 'mgc' : 60,'lf0' : 1,'vuv' : 1,'bap' : 5}

    train_norm_list = prepare_file_path_list(train_list, in_data_dir ,'.cmp', False)
    in_norm_list = prepare_file_path_list(all_list, in_data_dir ,'.cmp', False)
    out_norm_list = prepare_file_path_list(all_list, out_data_dir ,'.cmp', False)
    normaliser = MeanVarianceNorm(feature_dimension=n_output_dim)
            ###calculate mean and std vectors on the training data, and apply on the whole dataset
    global_mean_vector = normaliser.compute_mean(train_norm_list, 0, n_output_dim)
    global_std_vector = normaliser.compute_std(train_norm_list, global_mean_vector, 0, n_output_dim)
    normaliser.feature_normalisation(in_norm_list, out_norm_list)
    cmp_norm_info = numpy.concatenate((global_mean_vector, global_std_vector), axis=0)

    cmp_norm_info = numpy.array(cmp_norm_info, 'float32')
    fid = open(norm_info_file, 'wb')
    cmp_norm_info.tofile(fid)
    fid.close()
    logger.info('saved vectors to %s' %(norm_info_file))
    feature_index = 0
    var_dir = main_path + '/data/var/'
    if not os.path.exists(var_dir):
        os.makedirs(var_dir)

    var_file_dict = {}
    for feature_name in out_dimension_dict.keys():
        var_file_dict[feature_name] = os.path.join(var_dir, feature_name + '_' + str(out_dimension_dict[feature_name]))

    for feature_name in out_dimension_dict.keys():
        feature_std_vector = numpy.array(global_std_vector[:,feature_index:feature_index+out_dimension_dict[feature_name]], 'float32')
        fid = open(var_file_dict[feature_name], 'w')
        feature_std_vector.tofile(fid)
        fid.close()
        logger.info('saved %s variance vector to %s' %(feature_name, var_file_dict[feature_name]))
        # logger.debug(' value was\n%s' % feature_std_vector)
        feature_index += out_dimension_dict[feature_name]



if __name__=="__main__":
    main_path="/home/pbaljeka/festvox-keras/ss_dnn/"
    #main_path="/home/pbaljeka/check_normalization/slt"
    do_lab_normalization(main_path, n_input_dim=711, n_output_dim=199)
    do_acoustic_composition(main_path, n_input_dim=711, n_output_dim=199)
    do_acoustic_normalisation(main_path, n_input_dim=711, n_output_dim=199)

