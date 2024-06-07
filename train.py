from classifier.template_matching import use as template_matching
from classifier.linear_svm import use as linear_svm
from rejector.hellinger_plus_correlation import is_valid_shape as hellinger_plus_correlation
import argparse 

CLASSIFIERS = {
    'template_matching' : template_matching,
    'linear_svm' : linear_svm
}

REJECTORS = {
    'hellinger_plus_correlation' : hellinger_plus_correlation
}



parser = argparse.ArgumentParser(description='Petrinet recognizer 0.1.')

parser.add_argument('--classifier', dest='classifier', type=str, nargs='?', action='store', default='linear_svm',
                    help='select a classifier you would like to train: linear_svm')
parser.add_argument('--rejector', dest='rejector', type=str, nargs='?', action='store', default='hellinger_plus_correlation',
                    help='select a rejector you would like to train: hellinger_plus_correlation')


args = parser.parse_args()

if args.classifier:
    if args.classifier not in CLASSIFIERS:
        print('Invalid classifier. Exiting...')
        exit()
    else:
        classifier = CLASSIFIERS[args.classifier]
        classifier.train()

if args.rejector:
    if args.rejector not in REJECTORS:
        print('Invalid rejector. Exiting...')
        exit()
    else:
        rejector = REJECTORS[args.rejector]
        rejector.train()