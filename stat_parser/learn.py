from os.path import exists
from glob import glob
from os import makedirs
from json import loads

from stat_parser.treebanks.normalize import gen_norm, get_words
from stat_parser.pcfg import PCFG

from stat_parser.paths import QUESTIONBANK_NORM, QUESTIONBANK_DATA
from stat_parser.paths import PENNTREEBANK_NORM, PENNTREEBANK_GLOB
from stat_parser.paths import TEMP_DIR, MODEL_TREEBANK, MODEL
from stat_parser.paths import TEST_DAT, TEST_KEY


def build_model():
    pcfg = PCFG()
    if exists(MODEL):
        pcfg.load_model(MODEL)
    
    else:
        print "Building the grammar model for the first time..."
        if not exists(TEMP_DIR):
            makedirs(TEMP_DIR)
        
        # Normalise the treebanks
        if not exists(QUESTIONBANK_NORM):
            gen_norm(QUESTIONBANK_NORM, [QUESTIONBANK_DATA])
        
        if not exists(PENNTREEBANK_NORM):
            gen_norm(PENNTREEBANK_NORM, glob(PENNTREEBANK_GLOB))
        
        # Keep a part of the treebanks for testing
        i = 0
        with open(MODEL_TREEBANK, 'w') as model, open(TEST_DAT, 'w') as dat, open(TEST_KEY, 'w') as key:
            for treebank in [QUESTIONBANK_NORM, PENNTREEBANK_NORM]:
                for tree in open(treebank):
                    i += 1
                    if (i % 730) == 0:
                        dat.write(' '.join(get_words(loads(tree)))+'\n')
                        key.write(tree)
                    else:
                        model.write(tree)
        
        # Learn PCFG
        pcfg.learn_from_treebanks([MODEL_TREEBANK])
        pcfg.save_model(MODEL)
    
    return pcfg


