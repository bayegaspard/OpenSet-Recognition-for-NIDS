import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
import Dataload
from torch.utils.data import DataLoader
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix,accuracy_score
from sklearn.metrics import (precision_score, recall_score,
                             f1_score,confusion_matrix,average_precision_score)
import itertools
import numpy as np
import itertools
import pandas as pd



# epoch = 20 history_final [{'val_loss': 3.6822474002838135, 'val_acc': 0.29999998211860657, 'train_loss': 11.54269027709961}, {'val_loss': 1.771144151687622, 'val_acc': 0.459090918302536, 'train_loss': 2.622060537338257}, {'val_loss': 1.49733304977417, 'val_acc': 0.47272729873657227, 'train_loss': 1.668800711631775}, {'val_loss': 1.4760304689407349, 'val_acc': 0.5136363506317139, 'train_loss': 1.4828541278839111}, {'val_loss': 1.4107227325439453, 'val_acc': 0.5590909719467163, 'train_loss': 1.355711579322815}, {'val_loss': 1.3187934160232544, 'val_acc': 0.5363636612892151, 'train_loss': 1.436032772064209}, {'val_loss': 1.171736717224121, 'val_acc': 0.550000011920929, 'train_loss': 1.3234833478927612}, {'val_loss': 1.09578275680542, 'val_acc': 0.5954546332359314, 'train_loss': 1.1878279447555542}, {'val_loss': 0.9965360164642334, 'val_acc': 0.663636326789856, 'train_loss': 1.134917140007019}, {'val_loss': 1.0754733085632324, 'val_acc': 0.6136363744735718, 'train_loss': 1.0401008129119873}, {'val_loss': 1.015233039855957, 'val_acc': 0.668181836605072, 'train_loss': 1.0170620679855347}, {'val_loss': 0.9538360834121704, 'val_acc': 0.6318181753158569, 'train_loss': 0.9501714706420898}, {'val_loss': 0.9685512185096741, 'val_acc': 0.6590909361839294, 'train_loss': 0.9937074780464172}, {'val_loss': 0.9329931139945984, 'val_acc': 0.7090909481048584, 'train_loss': 0.9353311061859131}, {'val_loss': 0.8152506351470947, 'val_acc': 0.7272727489471436, 'train_loss': 1.0522938966751099}, {'val_loss': 0.7926329970359802, 'val_acc': 0.7409090399742126, 'train_loss': 0.9276139736175537}, {'val_loss': 0.790667712688446, 'val_acc': 0.7000000476837158, 'train_loss': 0.8848629593849182}, {'val_loss': 0.7107415795326233, 'val_acc': 0.7363636493682861, 'train_loss': 0.860095202922821}, {'val_loss': 0.7106726765632629, 'val_acc': 0.75, 'train_loss': 0.810321569442749}, {'val_loss': 0.7572275400161743, 'val_acc': 0.7545454502105713, 'train_loss': 0.699836015701294}]

# num_epochs = 5
# history_final =  [{'val_loss': 3.6822474002838135, 'val_acc': 0.29999998211860657, 'train_loss': 11.54269027709961}, {'val_loss': 1.771144151687622, 'val_acc': 0.459090918302536, 'train_loss': 2.622060537338257}, {'val_loss': 1.49733304977417, 'val_acc': 0.47272729873657227, 'train_loss': 1.668800711631775}, {'val_loss': 1.4760304689407349, 'val_acc': 0.5136363506317139, 'train_loss': 1.4828541278839111}, {'val_loss': 1.4107227325439453, 'val_acc': 0.5590909719467163, 'train_loss': 1.355711579322815},{'val_loss': 1.3187934160232544, 'val_acc': 0.5363636612892151, 'train_loss': 1.436032772064209},{'val_loss': 1.171736717224121, 'val_acc': 0.550000011920929, 'train_loss': 1.3234833478927612},]
# Y_test = [[12, 11, 0, 7, 1, 4, 8, 6, 5, 5], [4, 0, 5, 10, 7, 6, 9, 0, 11, 0], [0, 12, 0, 11, 6, 5, 0, 7, 11, 8], [6, 4, 0, 9, 5, 7, 1, 10, 4, 5]]
# Y_pred = [[9, 0, 0, 8, 7, 5, 9, 0, 0, 6], [6, 0, 5, 0, 0, 0, 9, 0, 0, 0], [7, 7, 0, 12, 5, 4, 7, 7, 7, 9], [7, 0, 7, 9, 8, 7, 4, 7, 5, 7]]

def convert_to_1d(y_test,y_pred):
    y_test_final = []
    y_pred_final = []
    for i in range(len(y_test)):
        for j in range(len(y_pred[i])):
            y_test_final.append(y_test[i][j])
            y_pred_final.append(y_pred[i][j])
    return y_test_final,y_pred_final
# y_test, y_pred = convert_to_1d(Y_test,Y_pred)

def plot_losses(history):
    losses = [x['val_loss'] for x in history]
    print("losses", losses)
    plt.plot(losses, '-x')
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.legend(['losses'])
    plt.title('Loss vs. No. of epochs')
    plt.savefig("./plot_losses.png", dpi=600)
    plt.show()


def plot_accuracies(history):
    accuracies = [x['val_acc'] for x in history]
    print("accuracy", accuracies)
    plt.plot(accuracies, '-x')
    plt.xlabel('epoch')
    plt.ylabel('accuracy')
    plt.legend(['accuracy'])
    plt.title('Accuracy vs. No. of epochs')
    plt.ylim([0,1])
    plt.savefig("./plot_accuracies.png", dpi=600)
    plt.show()


def plot_all_losses(history):
    train_losses = [x.get('train_loss') for x in history]
    val_losses = [x['val_loss'] for x in history]
    plt.plot(train_losses, '-bx')
    plt.plot(val_losses, '-rx')
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.legend(['Training_loss', 'val_loss'])
    plt.title('train & val Loss vs. No. of epochs')
    plt.savefig("./plot_all_losses.png", dpi=600)
    plt.show()

# plot_all_losses(history_final)
# plot_losses(history_final)
# plot_accuracies(history_final)

def confusionMatrix(y_test,y_pred):
    return confusion_matrix(y_test, y_pred)







# def plot_confusion_matrix(y_test,y_pred):
#     cm = confusion_matrix(y_test, y_pred)
#     cm_display = ConfusionMatrixDisplay(cm).plot()
#     plt.savefig("./confusion_matrix.png", dpi=600)
#     plt.show()

# def compute_recall(y_test,y_pred):
#     return recall_score(y_test,y_pred,average='micro')
#
# def compute_precision(y_test,y_pred):
#     return precision_score(y_test,y_pred,average='micro')
#
# def compute_f1score(y_test,y_pred):
#     return f1_score(y_test,y_pred,average='micro')

import Dataload
import math

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=90)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        #cm = "{:.2f}".format(float)
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print("cm",cm.shape)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):

        #print("cm ij ",str(round(cm[i, j], 2)))
        plt.text(j, i, str(round(cm[i, j], 2)),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig("./confusion_matrix.png", dpi=600)

# Compute confusion matrix
# cnf_matrix = confusion_matrix(y_test, y_pred)
# np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
# plt.figure()

# Plot normalized confusion matri
#
# class_names = Dataload.get_class_names([0,1,4,5,6,7,8,9,10,11,12])
# plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,
#                       title='Normalized confusion matrix')
# plt.show()

def write_hist_to_file(lst,num_epochs,type=""):
    
    for l in lst:
        l["type"] = type
    if os.path.exists("Saves/history.csv"):
        hist = pd.read_csv("Saves/history.csv",index_col=0)
        hist = pd.concat((hist,pd.DataFrame.from_dict(lst)))
    else:
        hist = pd.DataFrame.from_dict(lst)
    hist.to_csv("Saves/history.csv")
    with open(f'Saves/history{type}.txt', 'a') as fp:
        #fp.write(f"history for {num_epochs} \n")
        fp.write("\n")
        for item in lst:
            # write each item on a new line
            fp.write(f"num_epochs {num_epochs} "+str(item)+"\n")
        print('Writing history Done')
def write_scores_to_file(lst,num_epochs,type=""):
    thisRun = pd.DataFrame.from_dict(lst)
    thisRun["type"] = type
    if os.path.exists("Saves/scores.csv"):
        hist = pd.read_csv("Saves/scores.csv",index_col=0)
        hist.loc[len(hist)] = thisRun.iloc[0]
    else:
        hist = thisRun
    
    hist.to_csv("Saves/scores.csv")
    with open(f'Saves/scores{type}.txt', 'a') as fp:
        fp.write("\n")
        for item in lst:
            # write each item on a new line
            fp.write(f"num_epochs {num_epochs} "+str(item).format(num_epochs)+"\n")
        print('Writing scores Done')

def write_batch_to_file(loss, num, modeltype="",batchtype=""):
    thisRun = pd.DataFrame([[loss.item(),num,modeltype,batchtype]],columns=["Loss","Batch Number","Model Type","Batch Type"])
    # thisRun["Loss"] = loss.detach()
    # thisRun["Batch Number"] = num
    # thisRun["Model Type"] = modeltype
    # thisRun["Batch Type"] = batchtype
    if os.path.exists("Saves/batch.csv"):
        hist = pd.read_csv("Saves/batch.csv",index_col=0)
        hist.loc[len(hist)] = thisRun.iloc[0]
    else:
        hist = thisRun
    
    hist.to_csv("Saves/batch.csv")


def store_values(history:list, Y_predict:list, Y_test:list, num_epochs:int, end_type:str):
    y_test, y_pred = convert_to_1d(Y_test,Y_predict)
    recall = recall_score(y_test,y_pred,average='weighted',zero_division=0)
    precision = precision_score(y_test,y_pred,average='weighted',zero_division=0)
    f1 = 2 * (precision * recall) / (precision + recall)
    # auprc = average_precision_score(y_test, y_pred, average='samples')
    score_list = [recall,precision,f1]
    write_hist_to_file(history,num_epochs,end_type)
    write_scores_to_file(score_list,num_epochs,end_type)  

#write_hist_to_file(history_final,num_epochs)
# 0
# 0,362108
# 1,115007
# 2,2543
# 3,830
# 4,241405
# 5,31843
# 6,48165
# 7,121097
# 8,80542
# 9,250000
# 10,128122
# 11,13486
# 12,11754
# 13,3341
# 14,12



# 0
# 0,10
# 1,10
# 2,10
# 3,10
# 4,10
# 5,10
# 6,10
# 7,10
# 8,10
# 9,10
# 10,10
# 11,10
# 12,10
# 13,10
# 14,10