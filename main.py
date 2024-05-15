import sys
from evaluators.grouper import evaluate_grouper

# get input from command line: -fa or -fc or both

if len(sys.argv) < 2:
    path = ["datasets/FC_1.0", "datasets/FA_1.1"] 
    evaluate_grouper(path)
elif(len(sys.argv) == 2):
    if(sys.argv[1] == '-fa'):
        path = ["datasets/FA_1.1"]
        evaluate_grouper(path, 'ALL', 'FA')
    elif(sys.argv[1] == '-fc'):
        path = ["datasets/FC_1.0"]
        evaluate_grouper(path, 'ALL', 'FC')
    elif(sys.argv[1] == '-test'):
        path = ["datasets/FC_1.0", "datasets/FA_1.1"] 
        evaluate_grouper(path, 'TEST')
    elif(sys.argv[1] == '-train'):
        path = ["datasets/FC_1.0", "datasets/FA_1.1"] 
        evaluate_grouper(path, 'TRAIN')
    elif(sys.argv[1] == '-v'):
        path = ["datasets/FC_1.0", "datasets/FA_1.1"]
        evaluate_grouper(path, 'V')
elif(len(sys.argv) == 3):
    if(sys.argv[1] == '-fa' and sys.argv[2] == '-test'):
        path = ["datasets/FA_1.1"]
        evaluate_grouper(path, 'TEST', 'FA')
    elif(sys.argv[1] == '-fa' and sys.argv[2] == '-train'):
        path = ["datasets/FA_1.1"]
        evaluate_grouper(path, 'TRAIN', 'FA')
    elif(sys.argv[1] == '-fa' and sys.argv[2] == '-v'):
        path = ["datasets/FA_1.1"]
        evaluate_grouper(path, 'V', 'FA')
    elif(sys.argv[1] == '-fc' and sys.argv[2] == '-test'):
        path = ["datasets/FC_1.0"]
        evaluate_grouper(path, 'TEST', 'FC')
    elif(sys.argv[1] == '-fc' and sys.argv[2] == '-train'):
        path = ["datasets/FC_1.0"]
        evaluate_grouper(path, 'TRAIN', 'FC')
    elif(sys.argv[1] == '-fc' and sys.argv[2] == '-v'):
        path = ["datasets/FC_1.0"]
        evaluate_grouper(path,'V', 'FC')

    
